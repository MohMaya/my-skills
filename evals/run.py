#!/usr/bin/env python3
"""Replay real commits as tasks and grade a harness on them.

Each task in tasks.json is a past commit from Shiv's repos; a squash-merged PR's
commit names the PR ref to fetch (`fetch`), since a clone holds only main. The harness starts
at the commit's parent with a ticket-style prompt; afterwards the commit's own
tests are restored over the work and the task's check decides pass or fail.
The `oracle` harness applies the human commit, which proves a task is gradable
and gives the human diff size to compare against; `none` changes nothing, which
proves the hidden tests fail without a fix.

    python3 evals/run.py <claude|codex|oracle|none> [task-id ...]

Results append to evals/results.jsonl. Re-run after every model or kernel
change and compare pass rate, diff size, and new complexity violations.
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
AGENT_TIMEOUT = 1800

spec = importlib.util.spec_from_file_location("gate", HERE.parent / "hooks" / "stop-gate.py")
assert spec and spec.loader
gate = importlib.util.module_from_spec(spec)
sys.modules["gate"] = gate
spec.loader.exec_module(gate)

CODEX_APP_BIN = Path("/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex")


def codex_cli() -> str:
    found = shutil.which("codex") or (str(CODEX_APP_BIN) if CODEX_APP_BIN.is_file() else None)
    if not found:
        raise SystemExit(f"Codex not found: install the ChatGPT app ({CODEX_APP_BIN}) or put codex on PATH")
    return found


HARNESSES = {
    "claude": lambda work, prompt: ["claude", "-p", prompt, "--output-format", "json",
                                    "--permission-mode", "bypassPermissions"],
    "codex": lambda work, prompt: [codex_cli(), "exec", "-C", str(work), "--json", "--ephemeral",
                                   "--skip-git-repo-check", "--dangerously-bypass-approvals-and-sandbox", prompt],
    "oracle": None,
    "none": None,
}


def sh(cmd: str | list[str], cwd: Path, timeout: int = 900) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True,
                          text=True, timeout=timeout)


def must(cmd: str | list[str], cwd: Path) -> str:
    done = sh(cmd, cwd)
    if done.returncode:
        shown = cmd if isinstance(cmd, str) else " ".join(cmd)
        raise RuntimeError(f"{shown} failed in {cwd}: {(done.stderr or done.stdout).strip()[-400:]}")
    return done.stdout.strip()


def git(work: Path, *args: str) -> str:
    return must(["git", *args], work)


def prepare(task: dict, work: Path) -> str:
    """Clone the repo at the commit's parent, install dependencies, and snapshot
    the result so setup artifacts never count as the harness's diff."""
    must(["git", "clone", "--quiet", os.path.expanduser(task["repo"]), str(work)], work.parent)
    if "fetch" in task:
        git(work, "fetch", "--quiet", "origin", task["fetch"])
    git(work, "checkout", "--quiet", f"{task['commit']}^")
    must(task["setup"], work)
    git(work, "add", "-A")
    tree = git(work, "write-tree")
    snapshot = git(work, "-c", "user.name=eval", "-c", "user.email=eval@local",
                   "commit-tree", tree, "-p", "HEAD", "-m", "setup")
    git(work, "reset", "--quiet", "--soft", snapshot)
    return snapshot


def solve(harness: str, task: dict, work: Path) -> str:
    """Run the harness, or apply the human commit for the oracle; return its stdout."""
    if harness == "oracle":
        git(work, "cherry-pick", "--no-commit", task["commit"])
        return ""
    build = HARNESSES[harness]
    if build is None:
        return ""
    try:
        return sh(build(work, task["prompt"]), work, AGENT_TIMEOUT).stdout
    except subprocess.TimeoutExpired:
        return ""


def usage(harness: str, stdout: str) -> dict:
    """Token and cost figures the harness reports, where it reports any."""
    lines = [json.loads(line) for line in stdout.splitlines() if line.startswith("{")]
    if harness == "claude" and lines:
        return {"cost_usd": lines[-1].get("total_cost_usd"), "usage": lines[-1].get("usage")}
    if harness == "codex":
        done = [e["usage"] for e in lines if e.get("type") == "turn.completed" and "usage" in e]
        return {"usage": done[-1]} if done else {}
    return {}


def grade(task: dict, work: Path, base: str) -> dict:
    """Measure the change against base, then restore the hidden tests and run the check."""
    git(work, "add", "-A")
    git(work, "reset", "--quiet", "--soft", base)
    stat = git(work, "diff", "--cached", "--numstat", base).splitlines()
    added = sum(int(row.split("\t")[0]) for row in stat if row.split("\t")[0].isdigit())
    removed = sum(int(row.split("\t")[1]) for row in stat if row.split("\t")[1].isdigit())
    complexity = gate.complexity(work, gate.changed_files(work), time.monotonic() + 300)
    git(work, "checkout", task["commit"], "--", *task["tests"])
    check = sh(task["check"], work)
    tail = (check.stdout + check.stderr).replace(f"{work.resolve()}/", "").replace(f"{work}/", "")
    return {"pass": check.returncode == 0, "files": len(stat), "added": added, "removed": removed,
            "complexity_violations": complexity.count("\n") - 1 if complexity else 0,
            "check_tail": tail[-600:] if check.returncode else ""}


def run(harness: str, task: dict) -> dict:
    with tempfile.TemporaryDirectory(prefix=f"eval-{task['id']}-", ignore_cleanup_errors=True) as tmp:
        work = Path(tmp) / "repo"
        base = prepare(task, work)
        start = time.monotonic()
        stdout = solve(harness, task, work)
        seconds = round(time.monotonic() - start)
        return {"date": date.today().isoformat(), "harness": harness, "task": task["id"],
                "seconds": seconds, **grade(task, work, base), **usage(harness, stdout)}


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in HARNESSES:
        sys.exit(__doc__)
    tasks = json.loads((HERE / "tasks.json").read_text())
    wanted = set(sys.argv[2:])
    with open(HERE / "results.jsonl", "a") as out:
        for task in tasks:
            if wanted and task["id"] not in wanted:
                continue
            result = run(sys.argv[1], task)
            out.write(json.dumps(result) + "\n")
            out.flush()
            print(f"{result['task']:20} {'PASS' if result['pass'] else 'FAIL'}  "
                  f"+{result['added']}/-{result['removed']}  {result['seconds']}s")


if __name__ == "__main__":
    main()
