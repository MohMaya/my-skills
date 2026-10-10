#!/usr/bin/env python3
"""Turn-end quality gate for the Claude Code Stop hook.

Runs the linters and type checkers a project already configures on the
Python, TypeScript, Go, and Rust files changed in the working tree, then
holds every changed function to a cyclomatic-complexity ratchet. Unfixable
errors block the stop and go back to the agent as the reason; a clean tree,
an unconfigured project, a timeout, or a retry after a block lets the turn
end.

Each checker runs from the nearest directory that configures it, so
monorepo packages use their own config. TypeScript tools and the Python
type checkers run only from project-local installs (node_modules, a venv),
since a global copy cannot see the project's dependencies.

Registered by ~/.agents/sync.sh as the Stop hook in Claude Code.
"""

from __future__ import annotations

import configparser
import csv
import fnmatch
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

MAX_LINES_PER_TOOL = 50
TOOL_TIMEOUT = 120
TOTAL_BUDGET = 480  # the registered hook allows 600s

PY = (".py", ".pyi")
TS = (".ts", ".tsx", ".mts", ".cts")
JS = TS + (".js", ".jsx", ".mjs", ".cjs")
GO = (".go",)
RS = (".rs",)

# A changed function may not exceed this cyclomatic complexity unless it was
# already over it at HEAD and did not get worse.
CCN_LIMIT = 10

Probe = Callable[[Path], bool]


def _has_file(*names: str) -> Probe:
    return lambda d: any((d / n).is_file() for n in names)


def _has_text(filename: str, *markers: str) -> Probe:
    def check(d: Path) -> bool:
        f = d / filename
        return f.is_file() and any(m in f.read_text(errors="ignore") for m in markers)

    return check


def _any(*checks: Probe) -> Probe:
    return lambda d: any(c(d) for c in checks)


def _pyproject_tool(d: Path, *names: str) -> dict[str, Any]:
    try:
        tools = tomllib.loads((d / "pyproject.toml").read_text()).get("tool", {})
    except (OSError, tomllib.TOMLDecodeError):
        return {}
    return next((tools[n] for n in names if isinstance(tools.get(n), dict)), {})


def _as_list(value: Any) -> list[str]:
    return (
        [value]
        if isinstance(value, str)
        else [v for v in value or [] if isinstance(v, str)]
    )


def mypy_excluded(d: Path, rel: str) -> bool:
    """mypy ignores its `exclude` regexes for files named on the command line."""
    patterns = _as_list(_pyproject_tool(d, "mypy").get("exclude"))
    for ini in ("mypy.ini", ".mypy.ini", "setup.cfg"):
        cp = configparser.ConfigParser()
        try:
            cp.read(d / ini)
        except configparser.Error:
            continue
        if cp.has_option("mypy", "exclude"):
            patterns += [
                p.strip() for p in cp.get("mypy", "exclude").splitlines() if p.strip()
            ]
    return any(re.search(p, rel) for p in patterns)


def pyright_excluded(d: Path, rel: str) -> bool:
    """Pyright ignores its `exclude` globs for files named on the command line."""
    patterns = _as_list(_pyproject_tool(d, "basedpyright", "pyright").get("exclude"))
    try:
        patterns += _as_list(
            json.loads((d / "pyrightconfig.json").read_text()).get("exclude")
        )
    except (OSError, ValueError, AttributeError):
        pass
    for p in patterns:
        p = p.rstrip("/")
        if (
            fnmatch.fnmatch(rel, p)
            or fnmatch.fnmatch(rel, p + "/*")
            or rel.startswith(p + "/")
        ):
            return True
    return False


@dataclass(frozen=True)
class Checker:
    tool: str
    exts: tuple[str, ...]
    configured: Probe
    check: tuple[str, ...]
    # (args, probe): the fix runs only when the probe accepts the project dir.
    fixes: tuple[tuple[tuple[str, ...], Probe], ...] = ()
    excluded: Callable[[Path, str], bool] = lambda d, rel: False
    pass_files: bool = True
    # Project-wide checkers report on imported files too; keep only the changed ones.
    scope_output: bool = False
    node: bool = False
    path_fallback: bool = False


_ALWAYS: Probe = lambda d: True
_RUFF_FORMATS = _any(
    _has_text("pyproject.toml", "[tool.ruff.format"),
    _has_text("ruff.toml", "[format"),
    _has_text(".ruff.toml", "[format"),
    _has_text(".pre-commit-config.yaml", "id: ruff-format"),
)

CHECKERS = (
    Checker(
        "ruff",
        PY,
        _any(
            _has_file("ruff.toml", ".ruff.toml"),
            _has_text("pyproject.toml", "[tool.ruff"),
        ),
        check=("check", "--quiet", "--force-exclude"),
        fixes=(
            (("check", "--fix", "--quiet", "--force-exclude"), _ALWAYS),
            (("format", "--quiet", "--force-exclude"), _RUFF_FORMATS),
        ),
        path_fallback=True,
    ),
    Checker(
        "mypy",
        PY,
        _any(
            _has_file("mypy.ini", ".mypy.ini"),
            _has_text("pyproject.toml", "[tool.mypy"),
            _has_text("setup.cfg", "[mypy"),
        ),
        check=(),
        excluded=mypy_excluded,
        scope_output=True,
    ),
    Checker(
        "basedpyright",
        PY,
        _any(
            _has_file("pyrightconfig.json"),
            _has_text("pyproject.toml", "[tool.basedpyright", "[tool.pyright"),
        ),
        check=(),
        excluded=pyright_excluded,
    ),
    Checker(
        "tsc",
        TS,
        _has_file("tsconfig.json"),
        check=("--noEmit", "--pretty", "false"),
        pass_files=False,
        scope_output=True,
        node=True,
    ),
    Checker(
        "eslint",
        JS,
        _has_file(
            "eslint.config.js",
            "eslint.config.mjs",
            "eslint.config.cjs",
            "eslint.config.ts",
            "eslint.config.mts",
            "eslint.config.cts",
            ".eslintrc",
            ".eslintrc.js",
            ".eslintrc.cjs",
            ".eslintrc.json",
            ".eslintrc.yml",
            ".eslintrc.yaml",
        ),
        check=(),
        node=True,
    ),
    Checker(
        "biome", JS, _has_file("biome.json", "biome.jsonc"), check=("check",), node=True
    ),
    Checker(
        "gofmt",
        GO,
        _has_file("go.mod"),
        check=("-l",),
        fixes=((("-w",), _ALWAYS),),
        path_fallback=True,
    ),
    Checker(
        "go",
        GO,
        _has_file("go.mod"),
        check=("vet", "./..."),
        pass_files=False,
        scope_output=True,
        path_fallback=True,
    ),
    Checker(
        "cargo",
        RS,
        _has_file("Cargo.toml"),
        check=("clippy", "--all-targets", "--message-format", "short", "--", "-D", "warnings"),
        fixes=((("fmt",), _ALWAYS),),
        pass_files=False,
        scope_output=True,
        path_fallback=True,
    ),
)


def git_paths(root: Path, *args: str) -> list[str]:
    try:
        out = subprocess.run(
            ["git", *args, "-z"], capture_output=True, text=True, cwd=root, timeout=10
        ).stdout
    except (subprocess.SubprocessError, OSError):
        return []
    return [p for p in out.split("\0") if p]


def repo_root(cwd: Path) -> Path | None:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=10,
        )
    except (subprocess.SubprocessError, OSError):
        return None
    return Path(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else None


def changed_files(root: Path) -> list[Path]:
    """Files with uncommitted changes: staged, unstaged, and untracked."""
    names = (
        git_paths(root, "diff", "--name-only", "--diff-filter=d")
        + git_paths(root, "diff", "--cached", "--name-only", "--diff-filter=d")
        + git_paths(root, "ls-files", "--others", "--exclude-standard")
    )
    return sorted({root / n for n in names if (root / n).is_file()})


def config_dir(file: Path, root: Path, checker: Checker) -> Path | None:
    """Nearest directory from the file up to the repo root that configures the checker."""
    for d in (file.parent, *file.parent.parents):
        if checker.configured(d):
            return d
        if d == root:
            return None
    return None


def binary(project: Path, root: Path, checker: Checker) -> str | None:
    for d in (project, *project.parents):
        candidates = (
            [d / "node_modules" / ".bin" / checker.tool]
            if checker.node
            else [d / v / "bin" / checker.tool for v in (".venv", "venv")]
        )
        for c in candidates:
            if c.is_file():
                return str(c)
        if d == root:
            break
    return shutil.which(checker.tool) if checker.path_fallback else None


def scoped(output: str, files: list[Path], project: Path) -> str:
    """Keep diagnostics that start with a changed file's path, plus their indented continuations."""
    rels = {str(f.relative_to(project)) for f in files}
    names = {str(f) for f in files} | rels | {"./" + r for r in rels}
    starts = re.compile(r"^\s*(?:%s)[:(]" % "|".join(re.escape(n) for n in names))
    kept: list[str] = []
    keeping = False
    for line in output.splitlines():
        if starts.match(line):
            keeping = True
        elif not line[:1].isspace():
            keeping = False
        if keeping:
            kept.append(line)
    return "\n".join(kept)


def run(
    exe: str, args: tuple[str, ...], files: list[Path], project: Path, deadline: float
) -> tuple[int, str] | None:
    """Return (exit code, output), or None when the tool timed out or could not start."""
    timeout = min(TOOL_TIMEOUT, deadline - time.monotonic())
    if timeout <= 1:
        return None
    argv = [exe, *args, *(str(f.relative_to(project)) for f in files)]
    try:
        r = subprocess.run(
            argv, capture_output=True, text=True, cwd=project, timeout=timeout
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    return r.returncode, (r.stdout.strip() or r.stderr.strip())


def truncate(output: str) -> str:
    lines = output.splitlines()
    if len(lines) <= MAX_LINES_PER_TOOL:
        return output
    extra = len(lines) - MAX_LINES_PER_TOOL
    return "\n".join(lines[:MAX_LINES_PER_TOOL]) + f"\n... ({extra} more lines)"


def lizard(rels: list[str], cwd: Path, deadline: float) -> dict[tuple[str, str], tuple[int, int]]:
    """Map (file, function) to (complexity, start line); empty when lizard is unavailable."""
    timeout = min(TOOL_TIMEOUT, deadline - time.monotonic())
    exe = ["lizard"] if shutil.which("lizard") else ["uvx", "--quiet", "lizard"]
    if not rels or timeout <= 1 or not shutil.which(exe[0]):
        return {}
    try:
        out = subprocess.run(
            [*exe, "--csv", *rels], capture_output=True, text=True, cwd=cwd, timeout=timeout
        ).stdout
    except (subprocess.SubprocessError, OSError):
        return {}
    found: dict[tuple[str, str], tuple[int, int]] = {}
    for row in csv.reader(out.splitlines()):
        if len(row) >= 10 and row[1].isdigit():
            key = (row[6], row[7])
            found[key] = max(found.get(key, (0, 0)), (int(row[1]), int(row[9])))
    return found


def head_complexity(root: Path, rels: list[str], deadline: float) -> dict[tuple[str, str], tuple[int, int]]:
    """Complexity of the same files as committed at HEAD; new files are absent."""
    with tempfile.TemporaryDirectory() as tmp:
        tracked = []
        for rel in rels:
            r = subprocess.run(
                ["git", "show", f"HEAD:{rel}"], capture_output=True, cwd=root, timeout=10
            )
            if r.returncode == 0:
                (Path(tmp) / rel).parent.mkdir(parents=True, exist_ok=True)
                (Path(tmp) / rel).write_bytes(r.stdout)
                tracked.append(rel)
        return lizard(tracked, Path(tmp), deadline)


def complexity(root: Path, files: list[Path], deadline: float) -> str | None:
    """Changed functions over CCN_LIMIT that are new or more complex than at HEAD."""
    rels = [str(f.relative_to(root)) for f in files if f.suffix in PY + JS + GO + RS]
    over = {k: v for k, v in lizard(rels, root, deadline).items() if v[0] > CCN_LIMIT}
    before = head_complexity(root, rels, deadline) if over else {}
    worse = [
        f"{file}:{line} {name} has complexity {ccn} (limit {CCN_LIMIT}, was {before.get((file, name), (0,))[0] or 'new'})"
        for (file, name), (ccn, line) in sorted(over.items())
        if ccn > before.get((file, name), (0, 0))[0]
    ]
    if not worse:
        return None
    return (
        "=== complexity ===\nSplit these functions or move their branches into data, "
        "types, or one shared guard:\n" + truncate("\n".join(worse))
    )


def checker_groups(checker: Checker, files: list[Path], root: Path) -> dict[Path, list[Path]]:
    """Changed files the checker covers, grouped by the directory that configures it."""
    groups: dict[Path, list[Path]] = {}
    for f in files:
        if f.suffix not in checker.exts or not (d := config_dir(f, root, checker)):
            continue
        if not checker.excluded(d, f.relative_to(d).as_posix()):
            groups.setdefault(d, []).append(f)
    return groups


def check_project(
    checker: Checker, project: Path, group: list[Path], root: Path, deadline: float
) -> str | None:
    """Apply the checker's fixes, then return its remaining errors, if any."""
    exe = binary(project, root, checker)
    if not exe:
        return None
    targets = group if checker.pass_files else []
    for args, applies in checker.fixes:
        if applies(project):
            run(exe, args, targets, project, deadline)
    result = run(exe, checker.check, targets, project, deadline)
    if result is None:
        return None  # a timeout gives the agent nothing to fix
    code, output = result
    if checker.scope_output:
        output = scoped(output, group, project)
    if code == 0 or not output:
        return None
    where = project.relative_to(root) if project != root else Path(".")
    return f"=== {checker.tool} ({where}) ===\n{truncate(output)}"


def gate(root: Path, deadline: float) -> list[str]:
    files = changed_files(root)
    found = [
        check_project(checker, project, group, root, deadline)
        for checker in CHECKERS
        for project, group in checker_groups(checker, files, root).items()
    ]
    found.append(complexity(root, files, deadline))
    return [f for f in found if f]


def stop_root(payload: dict[str, Any]) -> Path | None:
    """The repository to check, or None when this stop should pass unchecked.

    A retry after a block passes so a stubborn error cannot loop forever:
    Claude Code flags it with stop_hook_active, Cursor with loop_count. Cursor
    runs this from ~/.claude with an empty cwd and names the project in
    workspace_roots.
    """
    if payload.get("stop_hook_active") or payload.get("loop_count"):
        return None
    roots = payload.get("workspace_roots")
    root = roots[0] if isinstance(roots, list) and roots and isinstance(roots[0], str) else ""
    return repo_root(Path(payload.get("cwd") or root or ".").resolve())


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return
    root = stop_root(payload) if isinstance(payload, dict) else None
    errors = gate(root, time.monotonic() + TOTAL_BUDGET) if root else []
    if not errors:
        return
    reason = "Fix these errors in changed files before ending the turn:\n\n" + "\n\n".join(errors)
    json.dump({"decision": "block", "reason": reason}, sys.stdout)


if __name__ == "__main__":
    main()
