#!/usr/bin/env python3
"""Bar-raiser review gate for Claude Code and Codex hooks.

A snapshot is a git tree: the working tree as `git add -A` would stage it, the
index, or a commit's tree. A review is <git-common-dir>/bar-raiser/<tree>.md,
written by `record` from a bar-raiser report whose `Snapshot:` line names that
tree. A commit counts as reviewed only when its own tree was, so a rebase or
cherry-pick that rewrites commits needs each new commit reviewed.

Hook modes (sync.sh passes the event, so it never depends on payload fields):

  prompt    Files queued reviews, and turns a below-bar review into an accepted
            one when Shiv's prompt says `accept <snapshot>`. Codex takes the
            turn baseline here. With --first-touch (Claude Code) the baseline
            is taken at the turn's first tool call, so edits Shiv makes himself,
            including `!` shell commands, never count as the agent's. A prompt
            that arrives mid-turn keeps the open baseline.
  pre-tool  Early feedback before a shell command: `git commit` needs an
            excellent review of the tree it records; `git push` and
            `gh pr create` need every unpushed commit reviewed and the pushed
            tip reviewed exactly. Fails closed once a command matched.
  stop      The guarantee, judged on outcomes rather than commands: the turn
            ends only when its uncommitted changes have a review (any verdict)
            and every commit it created, on any branch or since reset away, has
            an excellent one. After MAX_BLOCKS blocks in one turn it gives way
            with an UNREVIEWED warning, so a stuck agent cannot loop on usage.

Limits: a global core.hooksPath pre-commit hook would see every commit, but a
repo's own core.hooksPath (husky) silently replaces it and it would gate Shiv's
commits too, so the outcome check at stop is the guarantee instead. That check
sees a push only after it happened: a push from a script ships, and the turn
then blocks on it. A commit that reached a remote during the turn counts unless
its committer date predates the turn, so pulled work made before the turn
passes, while a teammate's commit made during the turn and pulled is flagged,
and a backdated commit pushed from a script is missed. Commit times have
one-second precision, so a pulled commit made in the second the turn began
counts as the turn's. With reflogs off, commits made on a detached HEAD or reset
away are missed. A first push to a remote with no tracking refs is judged on its
tip alone. A review is the agent's attestation, through `record` or the sandbox
inbox, both checked the same way; only `accept` is reserved to Shiv. Submodules
and repositories other than the session's are not watched.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from collections.abc import Callable, Iterator
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

Payload = dict[str, Any]

MAX_BLOCKS = 2
GIT_TIMEOUT = 15
# A baseline whose turn saw no tool call for this long is from an interrupted turn.
OPEN_TURN_SECONDS = 15 * 60
COMMITTABLE = ("excellent", "accepted")
REQUIRED_LINES = ("Snapshot", "Verdict", "Skills", "Tests")
STALE_DAYS = {"sessions": 7, "reviews": 365}
# Codex's sandbox cannot write .git, so `record` queues there and a hook files it.
INBOX = Path(
    os.environ.get("REVIEW_GATE_INBOX") or f"/tmp/agent-review-inbox-{os.getuid()}"
)
GATE = "python3 ~/.agents/hooks/review-gate.py"
HOW_TO_RECORD = (
    f"Run `bar-raiser` on the change. Start by printing the snapshot you are reviewing with "
    f"`{GATE} tree` (`--index` for staged changes only, `--commit <sha>` for a commit), fix "
    f"what the review finds, report the verdict to Shiv, then pipe the final report in:\n\n"
    f"    {GATE} record --verdict <excellent|below-bar> [--index | --commit <sha>] <<'REPORT'\n"
    f"    <report starting with Snapshot:, Verdict:, Skills:, Tests: lines>\n"
    f"    REPORT\n\n"
    f"Any edit after `tree` makes `record` refuse, so review the final state. Below-bar "
    f"work ships only once Shiv replies `accept <snapshot>`. If the matched command only "
    f"mentions git inside a string or heredoc, write that file with the Write or Edit tool."
)

# A command starts a line, follows a shell operator, an assignment, a wrapper, or
# opens an `sh -c` string. Quotes and backticks alone do not start one, so prose
# that mentions `git commit` stays out of it; the stop check backs up any miss.
PREFIX = (
    r"(?:^|[;&|(){}!]\s*|\b\w+=\S*\s+"
    r"|\b(?:env|command|time|exec|xargs|sudo|nohup|then|do|else)\s+"
    r"|\b(?:ba|z)?sh\s+-\w*c\s+[\"'])"
)
GIT = (
    r"(?:\S*/)?git((?:\s+(?:-[Cc]\s+(?:\"[^\"]*\"|'[^']*'|\S+)"
    r"|--git-dir\s+\S+|--?[\w-]+(?:=\S+)?))*)"
)
GIT_VERB = re.compile(PREFIX + GIT + r"\s+(commit|push)(?=[\s;&|)'\"]|$)", re.MULTILINE)
GH_PR_CREATE = re.compile(PREFIX + r"gh\s+pr\s+create\b", re.MULTILINE)
GIT_ADD = re.compile(PREFIX + GIT + r"\s+add(?=[\s;&|)'\"]|$)", re.MULTILINE)
REDIRECTION = re.compile(r"(?<!\S)(?:\d*|&)(?:>>?|<)(?:&\d+|\s*[^\s;&|]+)?")
CD = re.compile(PREFIX + r"cd\s+(\"[^\"]*\"|'[^']*'|[^\s;&|)]+)", re.MULTILINE)
COMMIT_VALUE_FLAGS = {
    "-m", "--message", "-F", "--file", "-C", "-c", "--reuse-message", "--reedit-message",
    "--author", "--date", "-t", "--template", "--fixup", "--squash", "--cleanup", "--trailer",
}  # fmt: skip
WORKTREE_FLAGS = {"--all", "--include", "--only", "--pathspec-from-file", "--"}
TAG_PUSH = "this push sends tags; push tags yourself after review"
WHOLE_PUSHES: dict[str, list[str] | str] = {
    "--tags": TAG_PUSH,
    "--follow-tags": TAG_PUSH,
    "--all": ["--branches"],
    "--mirror": ["--branches"],
    "--branches": ["--branches"],
    "--delete": [],
    "-d": [],
}
PUSH_VALUE_FLAGS = {"-o", "--push-option", "--receive-pack", "--exec", "--repo"}


# git


def git(
    root: Path, *args: str, env: dict[str, str] | None = None, stdin: str | None = None
) -> str | None:
    try:
        r = subprocess.run(
            ["git", *args],
            cwd=root,
            input=stdin,
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT,
            check=False,
            env={**os.environ, **(env or {})},
        )
    except (subprocess.SubprocessError, OSError):
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def repo_root(cwd: Path) -> Path | None:
    top = git(cwd, "rev-parse", "--show-toplevel") if cwd.is_dir() else None
    return Path(top) if top else None


def git_path(root: Path, name: str) -> str | None:
    return git(root, "rev-parse", "--path-format=absolute", "--git-path", name)


def rev(root: Path, name: str) -> str | None:
    return git(root, "rev-parse", "--verify", "-q", name)


def words(out: str | None) -> list[str]:
    return out.split() if out else []


@contextlib.contextmanager
def scratch_git(root: Path) -> Iterator[dict[str, str]]:
    """Env for snapshot commands: a copy of the index, and a throwaway object store
    so snapshots never litter the repository's own."""
    index, objects = git_path(root, "index"), git_path(root, "objects")
    with tempfile.TemporaryDirectory() as tmp:
        scratch = Path(tmp) / "index"
        if index and Path(index).is_file():
            # copy2 keeps the index mtime, which git's racy-file check compares against.
            shutil.copy2(index, scratch)
        scratch_objects = Path(tmp) / "objects"
        scratch_objects.mkdir()
        env = {
            "GIT_INDEX_FILE": str(scratch),
            "GIT_OBJECT_DIRECTORY": str(scratch_objects),
        }
        if objects:
            env["GIT_ALTERNATE_OBJECT_DIRECTORIES"] = objects
        yield env


def head_or_empty_tree(root: Path) -> str | None:
    return rev(root, "HEAD^{tree}") or git(
        root, "hash-object", "-t", "tree", "/dev/null"
    )


REFLOG_MADE = re.compile(r"^(commit|cherry-pick|revert|rebase|merge|am)\b")


def staged_snapshot(root: Path, adds: list[tuple[Path, list[str]]]) -> str | None:
    """The index tree after replaying `git add` calls on a scratch copy of the index."""
    with scratch_git(root) as env:
        for here, args in adds:
            if git(here, "add", *args, env=env) is None:
                return None
        return git(root, "write-tree", env=env)


def worktree_snapshot(root: Path) -> str | None:
    """The tree `git add -A && git commit` would record, leaving the real index alone."""
    return staged_snapshot(root, [(root, ["-A"])])


def commit_tree(root: Path, commit: str) -> str | None:
    return rev(root, f"{commit}^{{tree}}")


def take_snapshot(root: Path, kind: str, commit: str | None = None) -> str | None:
    if kind == "commit" and commit:
        return commit_tree(root, commit)
    return staged_snapshot(root, []) if kind == "index" else worktree_snapshot(root)


# review store


def store(root: Path, *parts: str) -> Path:
    common = git(root, "rev-parse", "--path-format=absolute", "--git-common-dir")
    d = Path(common or root / ".git", "bar-raiser", *parts)
    d.mkdir(parents=True, exist_ok=True)
    return d


def verdict(root: Path, tree: str | None) -> str | None:
    f = store(root) / f"{tree}.md" if tree else None
    if not f or not f.is_file():
        return None
    first = f.read_text().splitlines()[:1]
    return first[0].removeprefix("verdict: ") if first else None


def reviewed_commit(root: Path, commit: str) -> bool:
    return verdict(root, commit_tree(root, commit)) in COMMITTABLE


def file_review(root: Path, tree: str, text: str) -> None:
    (store(root) / f"{tree}.md").write_text(text)


def inbox_is_ours() -> bool:
    st = INBOX.stat() if INBOX.is_dir() else None
    return bool(st) and st.st_uid == os.getuid() and not st.st_mode & 0o077


def file_queued_review(root: Path, f: Path) -> None:
    try:
        entry = json.loads(f.read_text())
        if entry.get("repo") != str(root):
            return
        errors = report_errors(entry["verdict"], entry["report"], entry["tree"])
        if entry["verdict"] not in ("excellent", "below-bar") or errors:
            raise ValueError("; ".join(errors) or "bad verdict")
        stamp = entry.get("recorded", "")
        text = f"verdict: {entry['verdict']}\nrecorded: {stamp}\n\n{entry['report']}"
        file_review(root, entry["tree"], text)
        f.unlink(missing_ok=True)
    except (ValueError, KeyError, TypeError, AttributeError):
        (INBOX / "bad").mkdir(mode=0o700, exist_ok=True)
        f.replace(INBOX / "bad" / f.name)


def file_queued_reviews(root: Path) -> None:
    """Reviews `record` queued because a sandbox blocked .git. Each one is checked the
    way `record` checks it, so the inbox is no cheaper to forge than `record` is."""
    for f in sorted(INBOX.glob("*.json")) if inbox_is_ours() else []:
        file_queued_review(root, f)


def session_file(root: Path, payload: Payload, kind: str) -> Path:
    raw = str(payload.get("session_id") or payload.get("transcript_path") or "default")
    name = re.sub(r"[^\w-]", "_", raw)[-80:]
    return store(root, "sessions") / f"{name}.{kind}"


def prune(root: Path) -> None:
    now = time.time()
    stale = [
        (store(root, "sessions"), STALE_DAYS["sessions"]),
        (store(root), STALE_DAYS["reviews"]),
    ]
    if inbox_is_ours():
        stale.append((INBOX, STALE_DAYS["sessions"]))
    for d, days in stale:
        for f in d.glob("*.*"):
            if f.is_file() and now - f.stat().st_mtime > days * 86400:
                f.unlink(missing_ok=True)


# turn baseline


def ref_tips(root: Path) -> list[str]:
    tips = words(
        git(
            root,
            "for-each-ref",
            "--format=%(objectname)",
            "refs/heads",
            "refs/tags",
            "refs/remotes",
        )
    )
    head = rev(root, "HEAD")
    return sorted({*tips, *([head] if head else [])})


def other_worktrees(root: Path) -> list[str]:
    out = git(root, "worktree", "list", "--porcelain") or ""
    paths = [
        line.removeprefix("worktree ")
        for line in out.splitlines()
        if line.startswith("worktree ")
    ]
    return [p for p in paths if Path(p) != root]


def write_baseline(root: Path, payload: Payload) -> None:
    tree = worktree_snapshot(root)
    if tree:
        base = {
            "tree": tree,
            "time": int(time.time()),
            "turn": uuid.uuid4().hex,
            "tips": ref_tips(root),
            "worktrees": other_worktrees(root),
        }
        session_file(root, payload, "base").write_text(json.dumps(base))


def read_baseline(root: Path, payload: Payload) -> dict[str, Any] | None:
    f = session_file(root, payload, "base")
    try:
        base = json.loads(f.read_text()) if f.is_file() else None
    except ValueError:
        return None
    return base if isinstance(base, dict) and "tree" in base else None


def close_turn(root: Path, payload: Payload) -> None:
    session_file(root, payload, "base").unlink(missing_ok=True)


def accept_from_prompt(root: Path, payload: Payload) -> None:
    for prefix in re.findall(
        r"\baccept\s+([0-9a-f]{12,40})\b", str(payload.get("prompt") or "")
    ):
        for f in store(root).glob(f"{prefix}*.md"):
            text = f.read_text()
            if text.startswith("verdict: below-bar"):
                stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
                f.write_text(f"verdict: accepted\naccepted-by-shiv: {stamp}\n{text}")


def on_prompt(root: Path, payload: Payload, first_touch: bool) -> None:
    prune(root)
    file_queued_reviews(root)
    accept_from_prompt(root, payload)
    base = session_file(root, payload, "base")
    if base.is_file() and time.time() - base.stat().st_mtime < OPEN_TURN_SECONDS:
        return
    close_turn(root, payload)
    if not first_touch:
        write_baseline(root, payload)


# stop


def head_reflog_since(root: Path, since: int) -> list[str]:
    """Commits HEAD moved to by making them (commit, cherry-pick, rebase, ...) since a
    time, so ones made on a detached HEAD or reset away still count."""
    out = (
        git(root, "reflog", "show", "--format=%H %gd %gs", "--date=unix", "HEAD") or ""
    )
    found = []
    for line in out.splitlines():
        sha, _, rest = line.partition(" ")
        selector, _, subject = rest.partition(" ")
        stamp = re.search(r"@\{(\d+)\}", selector)
        if stamp and int(stamp.group(1)) >= since and REFLOG_MADE.match(subject):
            found.append(sha)
    return found


def turn_branches(root: Path, base: dict[str, Any]) -> list[str]:
    """Local branches, minus ones checked out in a worktree that existed before the turn,
    which belongs to another session; worktrees made during the turn count."""
    others = set(base.get("worktrees", []))
    out = git(root, "for-each-ref", "--format=%(refname) %(worktreepath)", "refs/heads")
    rows = (line.partition(" ") for line in (out or "").splitlines())
    return [ref for ref, _, tree in rows if tree not in others]


def new_commits(root: Path, base: dict[str, Any]) -> list[str] | None:
    """Commits that appeared since the baseline on any branch of this session, on a
    detached HEAD, or since reset away. One that already sits on a remote counts only
    if it was made during the turn, so pulled work passes and pushed work does not.
    None when git cannot list them, which the caller treats as unreviewed."""
    heads = turn_branches(root, base) + (["HEAD"] if rev(root, "HEAD") else [])
    sources = heads + head_reflog_since(root, int(base.get("time", 0)))
    if not sources:
        return []
    # The baseline can hold tens of thousands of tips, past the argv limit, so they go
    # in on stdin, where a command-line --not does not reach them.
    known = "".join(f"^{t}\n" for t in base.get("tips", []))
    local = git(
        root, "rev-list", "--stdin", *sources, "--not", "--remotes", stdin=known
    )
    made = git(root, "log", "--stdin", "--format=%H %ct", *sources, stdin=known)
    if local is None or made is None:
        return None
    rows = (line.split() for line in made.splitlines())
    since, unpushed = int(base.get("time", 0)), set(local.split())
    return [c for c, ct in rows if c in unpushed or int(ct) >= since]


def uncommitted_problem(root: Path, base: dict[str, Any] | None) -> str | None:
    tree = worktree_snapshot(root)
    changed = (
        tree and tree != (base or {}).get("tree") and tree != head_or_empty_tree(root)
    )
    if changed and not verdict(root, tree):
        return f"uncommitted changes, snapshot {tree}, have no review"
    return None


def commit_problem(root: Path, base: dict[str, Any] | None) -> str | None:
    made = new_commits(root, base) if base else []
    if made is None:
        return "could not list this turn's commits, so none can count as reviewed"
    first_bad = next((c for c in made if not reviewed_commit(root, c)), None)
    if first_bad:
        return f"commit {first_bad[:12]} (and possibly more) has no excellent review"
    return None


def unreviewed(root: Path, base: dict[str, Any] | None) -> list[str]:
    found = (uncommitted_problem(root, base), commit_problem(root, base))
    return [p for p in found if p]


def blocks_so_far(root: Path, payload: Payload, base: dict[str, Any] | None) -> int:
    turn = str((base or {}).get("turn", "none"))
    f = session_file(root, payload, "blocks")
    seen, _, count = (f.read_text() if f.is_file() else "").partition(" ")
    n = int(count) + 1 if seen == turn and count.isdigit() else 1
    f.write_text(f"{turn} {n}")
    return n - 1


def on_stop(root: Path, payload: Payload, first_touch: bool) -> dict[str, str]:
    file_queued_reviews(root)
    base = read_baseline(root, payload)
    if first_touch and not base:
        return {}
    problems = unreviewed(root, base)
    if problems and blocks_so_far(root, payload, base) < MAX_BLOCKS:
        return {
            "decision": "block",
            "reason": "Not reviewed: " + "; ".join(problems) + ".\n\n" + HOW_TO_RECORD,
        }
    close_turn(root, payload)
    if problems:
        return {
            "systemMessage": f"UNREVIEWED in {root}: "
            + "; ".join(problems)
            + ". Do not ship this until it is reviewed."
        }
    return {}


# pre-tool


def shell_words(text: str) -> list[str]:
    try:
        return shlex.split(text)
    except ValueError:
        return text.split()


def clause(command: str, start: int) -> list[str]:
    """The words of one simple command, without shell redirections such as `2>&1`."""
    text = REDIRECTION.sub(
        " ", re.split(r"[;|)]|&&|(?<![<>])&(?![\d>])", command[start:], maxsplit=1)[0]
    )
    return shell_words(text)


def directory_at(command: str, cwd: Path, end: int) -> Path:
    here = cwd
    for cd in CD.finditer(command, 0, end):
        here = here / Path(shell_words(cd.group(1))[0]).expanduser()
    return here


def git_target(command: str, cwd: Path, m: re.Match[str]) -> Path:
    here = directory_at(command, cwd, m.start())
    opts = shell_words(m.group(1)) if m.re is not GH_PR_CREATE else []
    return (
        here / Path(opts[opts.index("-C") + 1]).expanduser()
        if "-C" in opts[:-1]
        else here
    )


def target_root(command: str, cwd: Path, m: re.Match[str]) -> Path:
    """The repository a git command acts on; the session repo when it cannot be resolved."""
    return repo_root(git_target(command, cwd, m)) or repo_root(cwd) or cwd


def commits_worktree(command: str, m: re.Match[str]) -> bool:
    """Whether the commit records working-tree content rather than the index."""
    expect_value = False
    for w in clause(command, m.end()):
        if expect_value:
            expect_value = False
        elif w in WORKTREE_FLAGS or not w.startswith("-"):
            return True
        elif not w.startswith("--"):
            letters = re.split(r"[mFCct]", w[1:], maxsplit=1)
            if set(letters[0]) & set("aio"):
                return True
            expect_value = len(letters) == 2 and not letters[1]
        else:
            expect_value = w in COMMIT_VALUE_FLAGS
    return False


def adds_before(command: str, cwd: Path, end: int) -> list[tuple[Path, list[str]]]:
    return [
        (git_target(command, cwd, a), clause(command, a.end()))
        for a in GIT_ADD.finditer(command, 0, end)
    ]


def check_commit(root: Path, command: str, cwd: Path, m: re.Match[str]) -> str | None:
    if commits_worktree(command, m):
        tree = worktree_snapshot(root)
    else:
        tree = staged_snapshot(root, adds_before(command, cwd, m.start()))
    if verdict(root, tree) in COMMITTABLE:
        return None
    return f"BLOCKED: this commit records snapshot {tree}, which has no excellent review.\n\n{HOW_TO_RECORD}"


def push_sources(command: str, m: re.Match[str]) -> list[str] | str:
    """What a push ships, as revisions; a string names why the gate cannot tell."""
    if m.re is GH_PR_CREATE:
        return ["HEAD"]
    parts = clause(command, m.end())
    whole = next((w for w in parts if w in WHOLE_PUSHES), None)
    return WHOLE_PUSHES[whole] if whole else refspec_sources(positional(parts)[1:])


def refspec_sources(refspecs: list[str]) -> list[str]:
    """Each refspec's source; a deletion (`:branch`) ships nothing, no refspec ships HEAD."""
    sources = [r.lstrip("+").split(":")[0] for r in refspecs]
    return [x for x in sources if x] or ([] if refspecs else ["HEAD"])


def positional(parts: list[str]) -> list[str]:
    """The non-option words of `git push`: the remote, then its refspecs."""
    args, skip = [], False
    for w in parts:
        if not skip and not w.startswith("-"):
            args.append(w)
        skip = w in PUSH_VALUE_FLAGS
    return args


def resolve_tips(root: Path, sources: list[str]) -> list[str] | str:
    if sources == ["--branches"]:
        return words(git(root, "rev-parse", "--branches"))
    tips = [rev(root, f"{s}^{{commit}}") for s in sources]
    unknown = [s for s, t in zip(sources, tips, strict=True) if not t]
    return f"cannot resolve {', '.join(unknown)}" if unknown else [t for t in tips if t]


def first_unreviewed_push(root: Path, tips: list[str]) -> str | None:
    deadline = time.monotonic() + 40
    has_remotes = bool(git(root, "for-each-ref", "--count=1", "refs/remotes"))
    unpushed = (
        words(git(root, "rev-list", *tips, "--not", "--remotes")) if has_remotes else []
    )
    for c in unpushed:
        if time.monotonic() > deadline:
            return "too many unpushed commits to check in time"
        if not reviewed_commit(root, c):
            return f"commit {c[:12]}"
    bad_tip = next(
        (
            t
            for t in tips
            if verdict(root, rev(root, f"{t}^{{tree}}")) not in COMMITTABLE
        ),
        None,
    )
    return f"tip {bad_tip[:12]}" if bad_tip else None


def check_push(root: Path, command: str, m: re.Match[str]) -> str | None:
    sources = push_sources(command, m)
    tips = resolve_tips(root, sources) if isinstance(sources, list) else sources
    problem = tips if isinstance(tips, str) else first_unreviewed_push(root, tips)
    if not problem:
        return None
    return f"BLOCKED: this push is not fully reviewed: {problem}.\n\n{HOW_TO_RECORD}"


def touch_baseline(payload: Payload, first_touch: bool) -> None:
    """Keeps an open turn's baseline fresh, or with --first-touch starts one."""
    root = repo_root(Path(payload.get("cwd") or "."))
    base = session_file(root, payload, "base") if root else None
    if base and base.is_file():
        os.utime(base)
    elif root and first_touch:
        write_baseline(root, payload)


def check_command(payload: Payload) -> str | None:
    command = str((payload.get("tool_input") or {}).get("command") or "")
    m = GIT_VERB.search(command) or GH_PR_CREATE.search(command)
    if not m:
        return None
    # Once a commit or push matched, any failure below blocks rather than lets it through.
    try:
        cwd = Path(payload.get("cwd") or ".")
        root = target_root(command, cwd, m)
        file_queued_reviews(root)
        is_commit = m.re is GIT_VERB and m.group(2) == "commit"
        return (
            check_commit(root, command, cwd, m)
            if is_commit
            else check_push(root, command, m)
        )
    except (
        OSError,
        ValueError,
        LookupError,
        RuntimeError,
        TypeError,
        AttributeError,
    ) as e:
        return f"BLOCKED: the review gate failed ({e!r}) on a commit or push, so it blocks to be safe."


# entry points


def read_payload() -> Payload:
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return {}
    return payload if isinstance(payload, dict) else {}


def hook_pre_tool(payload: Payload, first_touch: bool) -> int:
    touch_baseline(payload, first_touch)
    reason = check_command(payload)
    print(reason or "", file=sys.stderr, end="")
    return 2 if reason else 0


def hook_prompt(payload: Payload, first_touch: bool) -> int:
    root = repo_root(Path(payload.get("cwd") or "."))
    if root:
        on_prompt(root, payload, first_touch)
    return 0


def hook_stop(payload: Payload, first_touch: bool) -> int:
    root = repo_root(Path(payload.get("cwd") or "."))
    out = on_stop(root, payload, first_touch) if root else {}
    if out:
        json.dump(out, sys.stdout)
    return 0


HOOKS: dict[str, Callable[[Payload, bool], int]] = {
    "prompt": hook_prompt,
    "stop": hook_stop,
    "pre-tool": hook_pre_tool,
}


def report_errors(chosen: str, report: str, tree: str) -> list[str]:
    found = {
        m.group(1).capitalize(): m.group(2).strip()
        for m in re.finditer(
            r"^[\s>*_#-]*(snapshot|verdict|skills|tests)[*_]*\s*:[*_\s]*(.*)$",
            report,
            re.IGNORECASE | re.MULTILINE,
        )
    }
    errors = [
        f"missing a `{label}:` line" for label in REQUIRED_LINES if not found.get(label)
    ]
    snapshot = re.match(r"[0-9a-f]{12,40}", found.get("Snapshot", ""))
    if found.get("Snapshot") and not (snapshot and tree.startswith(snapshot.group())):
        errors.append(
            f"the report reviewed snapshot {found['Snapshot']}, but the code is now {tree}; "
            "review the final state"
        )
    stated = re.sub(r"[^a-z]+", "-", found.get("Verdict", "").lower()).strip("-")
    if found.get("Verdict") and not stated.startswith(chosen):
        errors.append(
            f"--verdict {chosen} contradicts the report's `Verdict: {found['Verdict']}`"
        )
    return errors


def snapshot_args(parser: argparse.ArgumentParser) -> None:
    which = parser.add_mutually_exclusive_group()
    which.add_argument("--index", action="store_true", help="the staged changes only")
    which.add_argument("--commit", help="a commit's tree")


def parsed_snapshot(args: argparse.Namespace) -> tuple[Path | None, str | None]:
    root = repo_root(Path.cwd())
    kind = "commit" if args.commit else "index" if args.index else "worktree"
    return root, take_snapshot(root, kind, args.commit) if root else None


def tree_command(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="review-gate.py tree")
    snapshot_args(parser)
    _, tree = parsed_snapshot(parser.parse_args(argv))
    if not tree:
        print("not a git repository, or no such commit", file=sys.stderr)
        return 1
    print(f"Snapshot: {tree}")
    return 0


def queue_review(root: Path, tree: str, verdict_: str, report: str) -> None:
    INBOX.mkdir(mode=0o700, parents=True, exist_ok=True)
    if not inbox_is_ours():
        raise OSError(f"{INBOX} is not a private directory owned by you")
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    entry = {
        "repo": str(root),
        "tree": tree,
        "verdict": verdict_,
        "report": report,
        "recorded": stamp,
    }
    final = INBOX / f"{tree}-{uuid.uuid4().hex[:8]}.json"
    partial = final.with_suffix(".tmp")
    partial.write_text(json.dumps(entry))
    os.replace(partial, final)


def save_review(root: Path, tree: str, verdict_: str, report: str) -> str:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    try:
        file_review(root, tree, f"verdict: {verdict_}\nrecorded: {stamp}\n\n{report}")
        return "recorded"
    except OSError:
        queue_review(root, tree, verdict_, report)
        return "queued (the sandbox blocks .git; the gate files it at the next hook)"


def record(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="review-gate.py record")
    parser.add_argument("--verdict", required=True, choices=("excellent", "below-bar"))
    snapshot_args(parser)
    args = parser.parse_args(argv)
    root, tree = parsed_snapshot(args)
    report = sys.stdin.read()
    if not root or not tree:
        print(
            "review not recorded: not a git repository, or no such commit",
            file=sys.stderr,
        )
        return 1
    errors = report_errors(args.verdict, report, tree)
    if errors:
        print("review not recorded: " + "; ".join(errors), file=sys.stderr)
        return 1
    try:
        outcome = save_review(root, tree, args.verdict, report)
    except OSError as e:
        print(f"review not recorded: {e}", file=sys.stderr)
        return 1
    print(f"{outcome}: {args.verdict} for snapshot {tree[:12]} of {root}")
    return 0


COMMANDS: dict[str, Callable[[list[str]], int]] = {
    "record": record,
    "tree": tree_command,
}


def main() -> int:
    mode, rest = (sys.argv[1:2] or [""])[0], sys.argv[2:]
    if mode in COMMANDS:
        return COMMANDS[mode](rest)
    if mode in HOOKS:
        return HOOKS[mode](read_payload(), "--first-touch" in rest)
    print(
        "usage: review-gate.py prompt|stop|pre-tool [--first-touch] | tree | record",
        file=sys.stderr,
    )
    return 0 if not mode else 2


if __name__ == "__main__":
    sys.exit(main())
