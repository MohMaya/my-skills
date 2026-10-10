import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

GATE = Path(__file__).with_name("review-gate.py")


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()


def report(snapshot: str, verdict: str = "excellent") -> str:
    return (
        f"Snapshot: {snapshot}\nVerdict: {verdict}\nSkills: tdd, bar-raiser\n"
        "Tests: test_total catches the off-by-one in total()\n\nFindings: none\n"
    )


class Gate(unittest.TestCase):
    first_touch = False

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = self.new_repo("repo")
        (self.repo / "app.py").write_text("x = 1\n")
        self.commit_all("init")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def new_repo(self, name: str) -> Path:
        repo = Path(self.tmp.name) / name
        repo.mkdir()
        git(repo, "init", "-q", "-b", "main")
        git(repo, "config", "user.email", "t@example.com")
        git(repo, "config", "user.name", "T")
        return repo

    def commit_all(self, message: str, repo: Path | None = None) -> str:
        git(repo or self.repo, "add", "-A")
        git(repo or self.repo, "commit", "-q", "-m", message)
        return git(repo or self.repo, "rev-parse", "HEAD")

    def run_gate(
        self, *args: str, stdin: str = "", cwd: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(GATE), *args],
            input=stdin,
            capture_output=True,
            text=True,
            cwd=cwd or self.repo,
            check=False,
            env={**os.environ, "REVIEW_GATE_INBOX": str(Path(self.tmp.name) / "inbox")},
        )

    def hook(self, mode: str, **payload: object) -> subprocess.CompletedProcess[str]:
        flags = ["--first-touch"] if self.first_touch else []
        body = {"session_id": "s1", "cwd": str(self.repo), **payload}
        return self.run_gate(mode, *flags, stdin=json.dumps(body))

    def prompt(self, text: str = "do the thing") -> None:
        self.assertEqual(self.hook("prompt", prompt=text).returncode, 0)

    def tool(self, command: str = "ls") -> subprocess.CompletedProcess[str]:
        return self.hook("pre-tool", tool_name="Bash", tool_input={"command": command})

    def stop(self) -> dict[str, object]:
        result = self.hook("stop", stop_hook_active=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout) if result.stdout.strip() else {}

    def snapshot(self, *args: str) -> str:
        out = self.run_gate("tree", *args)
        self.assertEqual(out.returncode, 0, out.stderr)
        return out.stdout.strip().removeprefix("Snapshot: ")

    def record(
        self, verdict: str = "excellent", *args: str, text: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        body = (
            text
            if text is not None
            else report(self.snapshot(*args), verdict.replace("-", " "))
        )
        return self.run_gate("record", "--verdict", verdict, *args, stdin=body)


class StopGateTest(Gate):
    def test_clean_tree_ends_the_turn(self) -> None:
        self.prompt()
        self.assertEqual(self.stop(), {})

    def test_unreviewed_change_blocks_the_turn(self) -> None:
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        out = self.stop()
        self.assertEqual(out.get("decision"), "block")
        self.assertIn("bar-raiser", str(out.get("reason")))
        self.assertIn("review-gate.py tree", str(out.get("reason")))

    def test_new_untracked_file_counts_as_a_change(self) -> None:
        self.prompt()
        (self.repo / "new.py").write_text("y = 1\n")
        self.assertEqual(self.stop().get("decision"), "block")

    def test_same_size_edit_in_the_index_timestamp_second_is_a_change(self) -> None:
        self.prompt()
        app = self.repo / "app.py"
        while True:
            git(self.repo, "add", "app.py")
            app.write_text("x = 9\n")
            second = int(app.stat().st_mtime)
            if second == int((self.repo / ".git" / "index").stat().st_mtime):
                break
            app.write_text("x = 1\n")
        time.sleep(second + 1.1 - time.time())
        self.assertEqual(self.stop().get("decision"), "block")

    def test_a_review_of_any_verdict_ends_the_turn(self) -> None:
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        self.assertEqual(self.record("below-bar").returncode, 0)
        self.assertEqual(self.stop(), {})

    def test_edit_after_review_needs_a_new_review(self) -> None:
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        self.record()
        (self.repo / "app.py").write_text("x = 3\n")
        self.assertEqual(self.stop().get("decision"), "block")

    def test_work_that_predates_the_turn_is_not_gated(self) -> None:
        (self.repo / "app.py").write_text("x = 2  # Shiv's own edit\n")
        self.prompt()
        self.assertEqual(self.stop(), {})

    def test_without_a_turn_baseline_changes_still_block(self) -> None:
        (self.repo / "app.py").write_text("x = 2\n")
        self.assertEqual(self.stop().get("decision"), "block")

    def test_blocks_give_way_per_turn_even_while_files_keep_changing(self) -> None:
        self.prompt()
        for n in range(2):
            (self.repo / "app.py").write_text(f"x = {n + 10}\n")
            self.assertEqual(self.stop().get("decision"), "block")
        (self.repo / "app.py").write_text("x = 99\n")
        out = self.stop()
        self.assertNotIn("decision", out)
        self.assertIn("UNREVIEWED", str(out.get("systemMessage")))

    def test_a_new_prompt_resets_the_block_count(self) -> None:
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        for _ in range(3):
            self.stop()
        self.prompt()
        (self.repo / "app.py").write_text("x = 3\n")
        self.assertEqual(self.stop().get("decision"), "block")


class CommitOutcomeTest(Gate):
    def test_a_commit_made_any_way_during_the_turn_needs_an_excellent_review(
        self,
    ) -> None:
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        subprocess.run(
            ["sh", "-c", "git add -A && git commit -qm sneaky"],
            cwd=self.repo,
            check=True,
        )
        out = self.stop()
        self.assertEqual(out.get("decision"), "block")
        self.assertIn("commit", str(out.get("reason")))

    def test_a_reviewed_commit_ends_the_turn(self) -> None:
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        self.record()
        self.commit_all("reviewed")
        self.assertEqual(self.stop(), {})

    def test_a_below_bar_commit_still_blocks(self) -> None:
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        self.record("below-bar")
        self.commit_all("below bar")
        self.assertEqual(self.stop().get("decision"), "block")

    def test_a_commit_can_be_reviewed_after_the_fact(self) -> None:
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        sha = self.commit_all("first")
        (self.repo / "app.py").write_text("x = 3\n")
        self.record()
        self.commit_all("second")
        self.assertEqual(self.record("excellent", "--commit", sha).returncode, 0)
        self.assertEqual(self.stop(), {})

    def test_commits_from_before_the_turn_are_not_gated(self) -> None:
        (self.repo / "app.py").write_text("x = 2\n")
        self.commit_all("Shiv's commit")
        self.prompt()
        self.assertEqual(self.stop(), {})


class RecordTest(Gate):
    def test_record_refuses_when_the_code_changed_after_the_review_began(self) -> None:
        (self.repo / "app.py").write_text("x = 2\n")
        reviewed = self.snapshot()
        (self.repo / "app.py").write_text("x = 3  # unreviewed fix\n")
        result = self.record(text=report(reviewed))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("review the final state", result.stderr)

    def test_record_rejects_a_report_without_skills_or_tests(self) -> None:
        tree = self.snapshot()
        result = self.record(text=f"Snapshot: {tree}\nVerdict: excellent\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Skills:", result.stderr)
        self.assertIn("Tests:", result.stderr)

    def test_record_rejects_a_report_without_a_snapshot(self) -> None:
        result = self.record(
            text="Verdict: excellent\nSkills: tdd\nTests: none needed\n"
        )
        self.assertIn("Snapshot:", result.stderr)

    def test_record_rejects_a_verdict_that_contradicts_the_report(self) -> None:
        result = self.record("excellent", text=report(self.snapshot(), "below bar"))
        self.assertNotEqual(result.returncode, 0)

    def test_the_agent_cannot_record_accepted(self) -> None:
        self.assertNotEqual(
            self.record(
                "accepted", text=report(self.snapshot(), "accepted")
            ).returncode,
            0,
        )


class AcceptTest(Gate):
    def test_shivs_accept_lets_a_below_bar_snapshot_commit(self) -> None:
        (self.repo / "app.py").write_text("x = 2\n")
        git(self.repo, "add", "-A")
        self.record("below-bar")
        self.assertEqual(self.tool("git commit -m change").returncode, 2)
        self.prompt(f"accept {self.snapshot()[:12]}")
        self.assertEqual(self.tool("git commit -m change").returncode, 0)

    def test_accept_needs_an_existing_below_bar_review(self) -> None:
        (self.repo / "app.py").write_text("x = 2\n")
        git(self.repo, "add", "-A")
        self.prompt(f"accept {self.snapshot()[:12]}")
        self.assertEqual(self.tool("git commit -m change").returncode, 2)


class PreToolTest(Gate):
    def stage(self, text: str = "x = 2\n") -> None:
        (self.repo / "app.py").write_text(text)
        git(self.repo, "add", "-A")

    def test_unreviewed_commit_is_blocked(self) -> None:
        self.stage()
        result = self.tool("git commit -m change")
        self.assertEqual(result.returncode, 2)
        self.assertIn("bar-raiser", result.stderr)

    def test_reviewed_commit_is_allowed(self) -> None:
        self.stage()
        self.record()
        self.assertEqual(self.tool("git commit -m change").returncode, 0)

    def test_plain_commit_is_judged_on_the_index_not_the_working_tree(self) -> None:
        self.stage("bad = 1\n")
        (self.repo / "app.py").write_text("good = 2\n")
        self.record()
        self.assertEqual(self.tool("git commit -m change").returncode, 2)

    def test_commit_all_is_judged_on_the_working_tree(self) -> None:
        self.stage()
        self.record()
        (self.repo / "app.py").write_text("x = 3  # unreviewed\n")
        for command in (
            "git commit -a -m x",
            "git commit -am x",
            "git commit app.py -m x",
            "git add -A && git commit -m x",
        ):
            with self.subTest(command=command):
                self.assertEqual(self.tool(command).returncode, 2)

    def test_add_and_commit_in_one_command_passes_when_the_working_tree_is_reviewed(
        self,
    ) -> None:
        (self.repo / "new.py").write_text("y = 1\n")
        self.record()
        self.assertEqual(self.tool("git add -A && git commit -m change").returncode, 0)

    def test_wrapped_commits_are_caught(self) -> None:
        self.stage()
        for command in (
            "env git commit -m x",
            "FOO=1 git commit -m x",
            "/usr/bin/git commit -m x",
            'sh -c "git commit -m x"',
            "bash -lc 'git commit -m x'",
            "if true; then git commit -m x; fi",
            "git -c user.name=x commit -m x",
            "git --git-dir .git commit -m x",
        ):
            with self.subTest(command=command):
                self.assertEqual(self.tool(command).returncode, 2)

    def test_commit_in_another_repo_is_judged_there(self) -> None:
        other = self.new_repo("other")
        (other / "b.py").write_text("z = 1\n")
        git(other, "add", "-A")
        self.stage()
        self.record()
        self.assertEqual(self.tool(f"git -C {other} commit -m b").returncode, 2)
        self.assertEqual(self.tool(f"cd {other} && git commit -m b").returncode, 2)
        self.assertEqual(self.tool(f"cd {self.repo} && git commit -m a").returncode, 0)

    def test_unresolvable_target_falls_back_to_the_session_repo(self) -> None:
        self.stage()
        self.assertEqual(
            self.tool(
                'cd "$(git rev-parse --show-toplevel)" && git commit -m x'
            ).returncode,
            2,
        )

    def test_malformed_quoting_fails_closed(self) -> None:
        self.stage()
        self.assertEqual(self.tool('cd "unterminated && git commit -m x').returncode, 2)

    def test_commands_that_do_not_commit_pass(self) -> None:
        self.stage()
        for command in (
            "git log --grep commit",
            "git status",
            "echo git commit",
            "git commit-graph write",
        ):
            with self.subTest(command=command):
                self.assertEqual(self.tool(command).returncode, 0)

    def test_push_needs_every_unpushed_commit_reviewed(self) -> None:
        remote = Path(self.tmp.name) / "remote.git"
        git(self.repo, "init", "-q", "--bare", str(remote))
        git(self.repo, "remote", "add", "origin", str(remote))
        git(self.repo, "push", "-q", "origin", "main")
        (self.repo / "app.py").write_text("x = 2\n")
        sha = self.commit_all("unreviewed")
        for command in ("git push", "gh pr create --fill"):
            with self.subTest(command=command):
                self.assertEqual(self.tool(command).returncode, 2)
        self.record("excellent", "--commit", sha)
        for command in ("git push", "gh pr create --fill"):
            with self.subTest(command=command):
                self.assertEqual(self.tool(command).returncode, 0)

    def test_prose_that_mentions_git_commands_passes(self) -> None:
        self.stage()
        for command in (
            "echo 'run `git commit` after review'",
            'printf "%s" "use gh pr create"',
        ):
            with self.subTest(command=command):
                self.assertEqual(self.tool(command).returncode, 0)


class FirstTouchTest(Gate):
    first_touch = True

    def test_shivs_shell_edit_before_the_first_tool_call_is_not_gated(self) -> None:
        self.prompt()
        (self.repo / "app.py").write_text("x = 2  # Shiv's ! command\n")
        self.tool()
        self.assertEqual(self.stop(), {})

    def test_a_turn_without_tool_calls_is_not_gated(self) -> None:
        self.prompt()
        (self.repo / "app.py").write_text("x = 2  # Shiv's ! command\n")
        self.assertEqual(self.stop(), {})

    def test_changes_after_the_first_tool_call_are_gated(self) -> None:
        self.prompt()
        self.tool()
        (self.repo / "app.py").write_text("x = 2\n")
        self.assertEqual(self.stop().get("decision"), "block")

    def test_a_finished_turn_does_not_carry_its_baseline_into_the_next(self) -> None:
        self.prompt()
        self.tool()
        self.assertEqual(self.stop(), {})
        (self.repo / "app.py").write_text("x = 2  # Shiv's ! command between turns\n")
        self.assertEqual(self.stop(), {})


class CursorTest(Gate):
    """Cursor runs Claude Code hooks from ~/.claude with an empty cwd and names
    the project only in workspace_roots."""

    first_touch = True

    def hook(self, mode: str, **payload: object) -> subprocess.CompletedProcess[str]:
        body = {"session_id": "c1", "cwd": "", "workspace_roots": [str(self.repo)], **payload}
        return self.run_gate(
            mode, "--first-touch", stdin=json.dumps(body), cwd=Path(self.tmp.name)
        )

    def tool(self, command: str = "ls") -> subprocess.CompletedProcess[str]:
        return self.hook(
            "pre-tool", tool_name="Shell", tool_input={"command": command, "cwd": ""}
        )

    def test_an_unreviewed_change_blocks_the_turn(self) -> None:
        self.prompt()
        self.tool()
        (self.repo / "app.py").write_text("x = 2\n")
        self.assertEqual(self.stop().get("decision"), "block")

    def test_an_unreviewed_commit_is_blocked(self) -> None:
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        result = self.tool("git commit -am change")
        self.assertEqual(result.returncode, 2)
        self.assertIn("has no excellent review", result.stderr)

    def test_a_reviewed_commit_is_allowed(self) -> None:
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        self.record()
        result = self.tool("git commit -am change")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_a_shell_cwd_names_the_repository_the_command_runs_in(self) -> None:
        other = self.new_repo("other")
        (other / "b.py").write_text("y = 1\n")
        self.commit_all("init", other)
        (other / "b.py").write_text("y = 2\n")
        snap = self.run_gate("tree", cwd=other).stdout.strip().removeprefix("Snapshot: ")
        self.run_gate("record", "--verdict", "excellent", stdin=report(snap), cwd=other)
        result = self.hook(
            "pre-tool",
            tool_name="Shell",
            tool_input={"command": "git commit -am change", "cwd": str(other)},
        )
        self.assertEqual(result.returncode, 0, result.stderr)


    def test_a_relative_shell_cwd_resolves_against_the_workspace_root(self) -> None:
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        self.record()
        result = self.hook(
            "pre-tool",
            tool_name="Shell",
            tool_input={"command": "git commit -am change", "cwd": "."},
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_malformed_workspace_fields_do_not_crash_the_stop_hook(self) -> None:
        result = self.hook(
            "stop", workspace_roots=str(self.repo), tool_input={"cwd": 3}
        )
        self.assertEqual(result.returncode, 0, result.stderr)


class CommitsOffTheMainLineTest(Gate):
    def unreviewed_commit(self) -> str:
        (self.repo / "app.py").write_text(f"x = {time.time_ns()}\n")
        return self.commit_all("unreviewed")

    def test_a_commit_on_another_branch_is_caught(self) -> None:
        self.prompt()
        git(self.repo, "switch", "-q", "-c", "feat")
        self.unreviewed_commit()
        git(self.repo, "switch", "-q", "main")
        self.assertEqual(self.stop().get("decision"), "block")

    def test_a_commit_on_a_detached_head_is_caught(self) -> None:
        self.prompt()
        git(self.repo, "checkout", "-q", "--detach")
        self.unreviewed_commit()
        git(self.repo, "checkout", "-q", "main")
        self.assertEqual(self.stop().get("decision"), "block")

    def test_a_commit_reset_away_is_caught(self) -> None:
        self.prompt()
        self.unreviewed_commit()
        git(self.repo, "reset", "-q", "--hard", "HEAD~1")
        self.assertEqual(self.stop().get("decision"), "block")

    def test_an_old_committer_date_hides_nothing(self) -> None:
        self.prompt()
        self.unreviewed_commit()
        (self.repo / "app.py").write_text("x = 'old'\n")
        git(self.repo, "add", "-A")
        subprocess.run(
            ["git", "commit", "-qm", "backdated"],
            cwd=self.repo,
            check=True,
            env={**os.environ, "GIT_COMMITTER_DATE": "2001-01-01T00:00:00"},
        )
        self.assertEqual(self.stop().get("decision"), "block")
        self.record("excellent", "--commit", "HEAD")
        self.assertEqual(self.stop().get("decision"), "block")

    def test_pulling_others_work_is_not_gated(self) -> None:
        remote = Path(self.tmp.name) / "remote.git"
        git(self.repo, "init", "-q", "--bare", str(remote))
        git(self.repo, "remote", "add", "origin", str(remote))
        git(self.repo, "push", "-q", "-u", "origin", "main")
        teammate = Path(self.tmp.name) / "teammate"
        git(Path(self.tmp.name), "clone", "-q", str(remote), str(teammate))
        git(teammate, "config", "user.email", "o@example.com")
        git(teammate, "config", "user.name", "O")
        (teammate / "other.py").write_text("z = 1\n")
        self.commit_all("their work", teammate)
        git(teammate, "push", "-q")
        time.sleep(1.1)  # committer times have one-second precision
        self.prompt()
        git(self.repo, "pull", "-q", "--ff-only")
        self.assertEqual(self.stop(), {})

    def test_work_merged_to_the_default_branch_during_the_turn_is_not_gated(
        self,
    ) -> None:
        remote = Path(self.tmp.name) / "remote.git"
        git(self.repo, "init", "-q", "--bare", str(remote))
        git(self.repo, "remote", "add", "origin", str(remote))
        git(self.repo, "push", "-q", "-u", "origin", "main")
        git(self.repo, "remote", "set-head", "origin", "main")
        teammate = Path(self.tmp.name) / "teammate"
        git(Path(self.tmp.name), "clone", "-q", str(remote), str(teammate))
        git(teammate, "config", "user.email", "o@example.com")
        git(teammate, "config", "user.name", "O")
        self.prompt()
        (teammate / "other.py").write_text("z = 1\n")
        self.commit_all("their work, merged while the turn runs", teammate)
        git(teammate, "push", "-q")
        git(self.repo, "pull", "-q", "--ff-only")
        self.assertEqual(self.stop(), {})

    def test_a_commit_pushed_to_a_side_branch_during_the_turn_is_still_gated(
        self,
    ) -> None:
        remote = Path(self.tmp.name) / "remote.git"
        git(self.repo, "init", "-q", "--bare", str(remote))
        git(self.repo, "remote", "add", "origin", str(remote))
        git(self.repo, "push", "-q", "-u", "origin", "main")
        git(self.repo, "remote", "set-head", "origin", "main")
        self.prompt()
        git(self.repo, "switch", "-q", "-c", "feat")
        (self.repo / "feature.py").write_text("f = 1\n")
        self.commit_all("feature")
        git(self.repo, "push", "-q", "-u", "origin", "feat")
        self.assertEqual(self.stop().get("decision"), "block")

    def test_a_rebased_commit_needs_its_own_review(self) -> None:
        git(self.repo, "switch", "-q", "-c", "feat")
        (self.repo / "feature.py").write_text("f = 1\n")
        self.record()
        self.commit_all("feature")
        git(self.repo, "switch", "-q", "main")
        (self.repo / "app.py").write_text("x = 'main moved'\n")
        self.commit_all("main moved")
        self.prompt()
        git(self.repo, "switch", "-q", "feat")
        git(self.repo, "rebase", "-q", "main")
        self.assertEqual(self.stop().get("decision"), "block")
        self.record("excellent", "--commit", "HEAD")
        self.assertEqual(self.stop(), {})


class SplitCommitTest(Gate):
    def test_staged_changes_alone_can_be_reviewed_and_committed(self) -> None:
        (self.repo / "app.py").write_text("x = 2  # refactor\n")
        (self.repo / "new.py").write_text("y = 1  # behavior, next commit\n")
        git(self.repo, "add", "app.py")
        self.assertEqual(self.record("excellent", "--index").returncode, 0)
        self.assertEqual(self.tool("git commit -m refactor").returncode, 0)

    def test_attached_message_flag_is_judged_on_the_index(self) -> None:
        (self.repo / "app.py").write_text("bad = 1\n")
        git(self.repo, "add", "-A")
        (self.repo / "app.py").write_text("good = 2\n")
        self.record()
        self.assertEqual(self.tool("git commit -mfix").returncode, 2)

    def test_add_of_some_paths_then_commit_is_judged_on_what_gets_staged(self) -> None:
        (self.repo / "app.py").write_text("x = 2\n")
        (self.repo / "new.py").write_text("y = 1\n")
        self.record()
        self.assertEqual(
            self.tool("git add app.py && git commit -m part").returncode, 2
        )


class PushTargetTest(Gate):
    def setUp(self) -> None:
        super().setUp()
        remote = Path(self.tmp.name) / "remote.git"
        git(self.repo, "init", "-q", "--bare", str(remote))
        git(self.repo, "remote", "add", "origin", str(remote))
        git(self.repo, "push", "-q", "origin", "main")

    def test_pushing_another_branch_judges_that_branch(self) -> None:
        git(self.repo, "switch", "-q", "-c", "feat")
        (self.repo / "app.py").write_text("x = 2\n")
        self.commit_all("unreviewed feat")
        git(self.repo, "switch", "-q", "main")
        self.assertEqual(self.tool("git push origin feat").returncode, 2)

    def test_a_rebased_tip_needs_its_own_review_before_push(self) -> None:
        git(self.repo, "switch", "-q", "-c", "feat")
        (self.repo / "feature.py").write_text("f = 1\n")
        self.record()
        self.commit_all("feature")
        git(self.repo, "switch", "-q", "main")
        (self.repo / "app.py").write_text("x = 'main moved'\n")
        self.record()
        main = self.commit_all("main moved")
        git(self.repo, "push", "-q", "origin", "main")
        git(self.repo, "switch", "-q", "feat")
        git(self.repo, "rebase", "-q", main)
        self.assertEqual(self.tool("git push origin feat").returncode, 2)
        self.record("excellent", "--commit", "HEAD")
        self.assertEqual(self.tool("git push origin feat").returncode, 0)


class MidTurnPromptTest(Gate):
    def test_a_prompt_mid_turn_keeps_the_open_baseline(self) -> None:
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        self.prompt("also do this")
        self.assertEqual(self.stop().get("decision"), "block")


class MidTurnPromptFirstTouchTest(MidTurnPromptTest):
    first_touch = True

    def prompt(self, text: str = "do the thing") -> None:
        super().prompt(text)
        self.tool()


class RoundFourTest(Gate):
    def remote(self) -> Path:
        remote = Path(self.tmp.name) / "remote.git"
        git(self.repo, "init", "-q", "--bare", str(remote))
        git(self.repo, "remote", "add", "origin", str(remote))
        git(self.repo, "push", "-q", "-u", "origin", "main")
        return remote

    def test_a_push_the_pre_check_cannot_see_still_fails_the_turn(self) -> None:
        self.remote()
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        self.commit_all("unreviewed")
        (Path(self.tmp.name) / "ship.sh").write_text("git push -q\n")
        subprocess.run(
            ["bash", str(Path(self.tmp.name) / "ship.sh")], cwd=self.repo, check=True
        )
        self.assertEqual(self.stop().get("decision"), "block")

    def test_a_whitespace_only_difference_is_a_different_change(self) -> None:
        (self.repo / "app.py").write_text("def f():\n    x = 1\n")
        self.commit_all("base")
        (self.repo / "app.py").write_text("def f():\n    x = 1\n    y = 2\n")
        self.record()
        git(self.repo, "checkout", "-q", "--", "app.py")
        self.prompt()
        (self.repo / "app.py").write_text("def f():\n    x = 1\ny = 2\n")
        self.commit_all("same text, different scope")
        self.assertEqual(self.stop().get("decision"), "block")

    def test_a_corrupt_queued_review_is_set_aside(self) -> None:
        inbox = Path(self.tmp.name) / "inbox"
        inbox.mkdir(mode=0o700)
        (inbox / "broken.json").write_text('{"repo": ')
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        self.assertEqual(self.stop().get("decision"), "block")
        self.assertTrue((inbox / "bad" / "broken.json").is_file())

    def test_a_forged_queued_review_is_rejected(self) -> None:
        inbox = Path(self.tmp.name) / "inbox"
        inbox.mkdir(mode=0o700)
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        forged = {
            "repo": str(self.repo),
            "tree": self.snapshot(),
            "verdict": "excellent",
            "report": report("0" * 40),
        }
        (inbox / "forged.json").write_text(json.dumps(forged))
        self.assertEqual(self.stop().get("decision"), "block")

    def test_pushes_the_gate_cannot_fully_judge_are_blocked(self) -> None:
        self.remote()
        git(self.repo, "switch", "-q", "-c", "feat")
        (self.repo / "app.py").write_text("x = 2\n")
        self.commit_all("unreviewed feat")
        git(self.repo, "switch", "-q", "main")
        for command in (
            "git push origin feat other",
            "git push origin tag v1",
            "git push --tags",
            "git push --follow-tags",
        ):
            with self.subTest(command=command):
                self.assertEqual(self.tool(command).returncode, 2)

    def test_a_commit_in_another_worktree_is_that_sessions_business(self) -> None:
        other = Path(self.tmp.name) / "wt"
        git(self.repo, "worktree", "add", "-q", "-b", "wt/other", str(other))
        self.prompt()
        (other / "app.py").write_text("x = 'other agent'\n")
        self.commit_all("other session", other)
        self.assertEqual(self.stop(), {})

    def test_checking_out_an_unreferenced_commit_is_not_making_it(self) -> None:
        git(self.repo, "switch", "-q", "-c", "side")
        (self.repo / "app.py").write_text("x = 'side'\n")
        side = self.commit_all("side work")
        git(self.repo, "switch", "-q", "main")
        git(self.repo, "branch", "-q", "-D", "side")
        time.sleep(1.1)  # reflog times have one-second precision
        self.prompt()
        git(self.repo, "checkout", "-q", side)
        git(self.repo, "checkout", "-q", "main")
        self.assertEqual(self.stop(), {})

    def test_an_interrupted_turn_does_not_hold_its_baseline(self) -> None:
        self.prompt()
        base = self.repo / ".git" / "bar-raiser" / "sessions" / "s1.base"
        old = time.time() - 3600
        os.utime(base, (old, old))
        (self.repo / "app.py").write_text(
            "x = 2  # Shiv's edit after the interruption\n"
        )
        self.prompt()
        self.assertEqual(self.stop(), {})


class RoundFiveTest(Gate):
    def remote(self) -> Path:
        remote = Path(self.tmp.name) / "remote.git"
        git(self.repo, "init", "-q", "--bare", str(remote))
        git(self.repo, "remote", "add", "origin", str(remote))
        git(self.repo, "push", "-q", "-u", "origin", "main")
        return remote

    def test_a_reviewed_binary_does_not_cover_other_bytes(self) -> None:
        (self.repo / "logo.png").write_bytes(b"\x89PNG\x00first")
        self.record()
        git(self.repo, "checkout", "-q", "--", ".")
        (self.repo / "logo.png").unlink()
        self.prompt()
        (self.repo / "logo.png").write_bytes(b"\x89PNG\x00second")
        self.commit_all("swapped logo")
        self.assertEqual(self.stop().get("decision"), "block")

    def test_a_different_committer_identity_hides_nothing(self) -> None:
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        git(self.repo, "add", "-A")
        git(self.repo, "-c", "user.email=bot@example.com", "commit", "-qm", "bot")
        self.assertEqual(self.stop().get("decision"), "block")

    def test_a_worktree_made_during_the_turn_is_checked(self) -> None:
        self.prompt()
        work = Path(self.tmp.name) / "agentwork"
        git(self.repo, "worktree", "add", "-q", "-b", "agentwork", str(work))
        (work / "app.py").write_text("x = 'isolated subagent'\n")
        self.commit_all("isolated", work)
        self.assertEqual(self.stop().get("decision"), "block")

    def test_pulling_shivs_own_commits_from_another_machine_is_not_gated(self) -> None:
        remote = self.remote()
        laptop = Path(self.tmp.name) / "laptop"
        git(Path(self.tmp.name), "clone", "-q", str(remote), str(laptop))
        git(laptop, "config", "user.email", "t@example.com")
        git(laptop, "config", "user.name", "T")
        (laptop / "app.py").write_text("x = 'from the laptop'\n")
        self.commit_all("laptop work", laptop)
        git(laptop, "push", "-q")
        time.sleep(1.1)  # committer times have one-second precision
        self.prompt()
        git(self.repo, "pull", "-q", "--ff-only")
        self.assertEqual(self.stop(), {})

    def test_deleting_a_remote_branch_ships_nothing(self) -> None:
        self.remote()
        (self.repo / "app.py").write_text("x = 2\n")
        self.commit_all("unreviewed local work")
        for command in ("git push origin --delete feat", "git push origin :feat"):
            with self.subTest(command=command):
                self.assertEqual(self.tool(command).returncode, 0)


class RoundSixTest(Gate):
    def rewrite_baseline(self, tips: list[str]) -> None:
        base = self.repo / ".git" / "bar-raiser" / "sessions" / "s1.base"
        data = json.loads(base.read_text())
        data["tips"] = tips
        base.write_text(json.dumps(data))

    def test_a_huge_baseline_still_finds_the_turns_commits(self) -> None:
        self.prompt()
        self.rewrite_baseline([git(self.repo, "rev-parse", "HEAD")] * 30000)
        (self.repo / "app.py").write_text("x = 2\n")
        self.commit_all("unreviewed")
        self.assertEqual(self.stop().get("decision"), "block")

    def test_a_turn_whose_commits_cannot_be_listed_is_blocked(self) -> None:
        self.prompt()
        self.rewrite_baseline(["0" * 40])
        out = self.stop()
        self.assertEqual(out.get("decision"), "block")
        self.assertIn("could not list", str(out.get("reason")))


class RedirectionTest(Gate):
    def test_shell_redirections_are_not_refspecs_or_pathspecs(self) -> None:
        remote = Path(self.tmp.name) / "remote.git"
        git(self.repo, "init", "-q", "--bare", str(remote))
        git(self.repo, "remote", "add", "origin", str(remote))
        git(self.repo, "push", "-q", "-u", "origin", "main")
        (self.repo / "app.py").write_text("x = 2\n")
        git(self.repo, "add", "-A")
        self.record("excellent", "--index")
        for command in (
            "git commit -m x 2>&1",
            "git commit -m x > /dev/null",
            "git commit -m x 2>err.log",
        ):
            with self.subTest(command=command):
                self.assertEqual(self.tool(command).returncode, 0)
        sha = self.commit_all("reviewed")
        self.record("excellent", "--commit", sha)
        for command in (
            "git push origin main 2>&1",
            "git push 2>/dev/null",
            "git push origin main >> push.log",
            "git push origin main &> push.log",
            "git push origin main &",
        ):
            with self.subTest(command=command):
                self.assertEqual(self.tool(command).returncode, 0)


class SandboxTest(Gate):
    def test_a_review_the_sandbox_cannot_store_is_queued_and_filed_at_the_next_hook(
        self,
    ) -> None:
        self.prompt()
        (self.repo / "app.py").write_text("x = 2\n")
        reviews = self.repo / ".git" / "bar-raiser"
        reviews.chmod(0o500)
        try:
            result = self.record()
        finally:
            reviews.chmod(0o700)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("queued", result.stdout)
        self.assertEqual(self.stop(), {})

    def test_the_write_guard_keeps_agents_out_of_the_review_store(self) -> None:
        guard = GATE.with_name("guard-protected-paths.sh")
        target = {
            "tool_input": {"file_path": str(self.repo / ".git/bar-raiser/abc.md")}
        }
        result = subprocess.run(
            [str(guard)],
            input=json.dumps(target),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
