#!/usr/bin/env python3
"""Turn-end quality gate for Claude Code and Codex Stop hooks.

Runs the linters and type checkers a project already configures on the
Python and TypeScript files changed in the working tree. Unfixable errors
block the stop and go back to the agent as the reason; a clean tree, an
unconfigured project, or a retry after a block lets the turn end.

Each checker runs from the nearest directory that configures it, so
monorepo packages use their own config. Only project-local binaries run
for TypeScript; Python checkers prefer the project venv, then PATH.

Synced by ~/.agents/sync.sh into ~/.claude/hooks and ~/.codex/hooks.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

MAX_LINES_PER_TOOL = 50
TOOL_TIMEOUT = 120

PY = (".py", ".pyi")
TS = (".ts", ".tsx", ".mts", ".cts")
JS = TS + (".js", ".jsx", ".mjs", ".cjs")


def _has_file(*names: str) -> Callable[[Path], bool]:
    return lambda d: any((d / n).is_file() for n in names)


def _has_section(filename: str, *markers: str) -> Callable[[Path], bool]:
    def check(d: Path) -> bool:
        f = d / filename
        return f.is_file() and any(m in f.read_text(errors="ignore") for m in markers)

    return check


def _any(*checks: Callable[[Path], bool]) -> Callable[[Path], bool]:
    return lambda d: any(c(d) for c in checks)


@dataclass(frozen=True)
class Checker:
    tool: str
    exts: tuple[str, ...]
    configured: Callable[[Path], bool]
    check: tuple[str, ...]
    fixes: tuple[tuple[str, ...], ...] = ()
    pass_files: bool = True
    # Project-wide checkers report on imported files too; keep only the changed ones.
    scope_output: bool = False
    node: bool = False


CHECKERS = (
    Checker(
        "ruff",
        PY,
        _any(
            _has_file("ruff.toml", ".ruff.toml"),
            _has_section("pyproject.toml", "[tool.ruff"),
        ),
        check=("check", "--quiet"),
        fixes=(("check", "--fix", "--quiet"), ("format", "--quiet")),
    ),
    Checker(
        "mypy",
        PY,
        _any(
            _has_file("mypy.ini", ".mypy.ini"),
            _has_section("pyproject.toml", "[tool.mypy"),
            _has_section("setup.cfg", "[mypy"),
        ),
        check=(),
        scope_output=True,
    ),
    Checker(
        "basedpyright",
        PY,
        _any(
            _has_file("pyrightconfig.json"),
            _has_section("pyproject.toml", "[tool.basedpyright", "[tool.pyright"),
        ),
        check=(),
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
)


def git_lines(root: Path, *args: str) -> list[str]:
    try:
        out = subprocess.run(
            ["git", *args], capture_output=True, text=True, cwd=root, timeout=10
        ).stdout
    except (subprocess.SubprocessError, OSError):
        return []
    return [line for line in out.splitlines() if line]


def changed_files(root: Path) -> list[Path]:
    """Files with uncommitted changes: staged, unstaged, and untracked."""
    names = (
        git_lines(root, "diff", "--name-only", "--diff-filter=d")
        + git_lines(root, "diff", "--cached", "--name-only", "--diff-filter=d")
        + git_lines(root, "ls-files", "--others", "--exclude-standard")
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
    return None if checker.node else shutil.which(checker.tool)


def scoped(output: str, files: list[Path], project: Path) -> str:
    """Keep lines that name a changed file, plus their indented continuation lines."""
    needles = {str(f) for f in files} | {str(f.relative_to(project)) for f in files}
    kept: list[str] = []
    keeping = False
    for line in output.splitlines():
        if any(n in line for n in needles):
            keeping = True
        elif not line[:1].isspace():
            keeping = False
        if keeping:
            kept.append(line)
    return "\n".join(kept)


def run(
    exe: str, args: tuple[str, ...], files: list[Path], project: Path
) -> tuple[int, str]:
    argv = [exe, *args, *(str(f.relative_to(project)) for f in files)]
    try:
        r = subprocess.run(
            argv, capture_output=True, text=True, cwd=project, timeout=TOOL_TIMEOUT
        )
    except subprocess.TimeoutExpired:
        return 1, f"(timed out after {TOOL_TIMEOUT}s)"
    except OSError:
        return 0, ""
    return r.returncode, (r.stdout.strip() or r.stderr.strip())


def truncate(output: str) -> str:
    lines = output.splitlines()
    if len(lines) <= MAX_LINES_PER_TOOL:
        return output
    extra = len(lines) - MAX_LINES_PER_TOOL
    return "\n".join(lines[:MAX_LINES_PER_TOOL]) + f"\n... ({extra} more lines)"


def gate(root: Path) -> list[str]:
    files = changed_files(root)
    errors: list[str] = []
    for checker in CHECKERS:
        groups: dict[Path, list[Path]] = {}
        for f in files:
            if f.suffix in checker.exts and (d := config_dir(f, root, checker)):
                groups.setdefault(d, []).append(f)
        for project, group in groups.items():
            exe = binary(project, root, checker)
            if not exe:
                continue
            targets = group if checker.pass_files else []
            for fix in checker.fixes:
                run(exe, fix, targets, project)
            code, output = run(exe, checker.check, targets, project)
            if checker.scope_output:
                output = scoped(output, group, project)
            if code != 0 and output:
                where = project.relative_to(root) if project != root else Path(".")
                errors.append(f"=== {checker.tool} ({where}) ===\n{truncate(output)}")
    return errors


def main() -> None:
    payload = json.load(sys.stdin)
    # A retry after a block ends the turn, so a stubborn error cannot loop forever.
    if payload.get("stop_hook_active"):
        return
    cwd = Path(payload.get("cwd") or ".").resolve()
    top = git_lines(cwd, "rev-parse", "--show-toplevel")
    if not top:
        return
    errors = gate(Path(top[0]))
    if errors:
        reason = (
            "Fix these errors in changed files before ending the turn:\n\n"
            + "\n\n".join(errors)
        )
        json.dump({"decision": "block", "reason": reason}, sys.stdout)


if __name__ == "__main__":
    main()
