import importlib.util
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("stop_gate", Path(__file__).with_name("stop-gate.py"))
assert spec and spec.loader
stop_gate = importlib.util.module_from_spec(spec)
sys.modules["stop_gate"] = stop_gate
spec.loader.exec_module(stop_gate)


class StopRootTest(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory()
        self.repo = Path(self.scratch.name).resolve() / "repo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)

    def tearDown(self) -> None:
        self.scratch.cleanup()

    def test_cursor_payload_checks_the_workspace_root(self) -> None:
        payload = {"cwd": "", "workspace_roots": [str(self.repo)], "loop_count": 0}
        self.assertEqual(stop_gate.stop_root(payload), self.repo)

    def test_cursor_retry_after_a_block_passes(self) -> None:
        payload = {"cwd": "", "workspace_roots": [str(self.repo)], "loop_count": 1}
        self.assertIsNone(stop_gate.stop_root(payload))

    def test_a_malformed_workspace_roots_falls_back_to_the_cwd(self) -> None:
        payload = {"cwd": str(self.repo), "workspace_roots": 5}
        self.assertEqual(stop_gate.stop_root(payload), self.repo)

    def test_claude_retry_after_a_block_passes(self) -> None:
        self.assertIsNone(stop_gate.stop_root({"cwd": str(self.repo), "stop_hook_active": True}))


class GatedFilesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory()
        self.repo = Path(self.scratch.name).resolve() / "repo"
        (self.repo / "skills" / "vendored" / "scripts").mkdir(parents=True)
        (self.repo / "skills" / "ours").mkdir(parents=True)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        (self.repo / "skills" / "vendored" / "scripts" / "tool.js").write_text("x\n")
        (self.repo / "skills" / "ours" / "tool.js").write_text("x\n")
        (self.repo / "app.py").write_text("x = 1\n")

    def tearDown(self) -> None:
        self.scratch.cleanup()

    def gated(self) -> list[str]:
        return [str(f.relative_to(self.repo)) for f in stop_gate.gated_files(self.repo)]

    def lock(self) -> None:
        (self.repo / ".skill-lock.json").write_text(
            '{"skills": {"vendored": {"sourceUrl": "https://github.com/o/r.git"}}}'
        )

    def test_a_fresh_install_from_the_lock_is_vendored_and_skipped(self) -> None:
        self.lock()
        self.assertEqual(self.gated(), [".skill-lock.json", "app.py", "skills/ours/tool.js"])

    def test_a_local_edit_to_a_tracked_vendored_skill_is_still_checked(self) -> None:
        subprocess.run(["git", "add", "skills/vendored"], cwd=self.repo, check=True)
        subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "vendor"],
            cwd=self.repo,
            check=True,
        )
        (self.repo / "skills" / "vendored" / "scripts" / "tool.js").write_text("y\n")
        self.lock()
        self.assertIn("skills/vendored/scripts/tool.js", self.gated())

    def test_a_staged_fresh_install_is_still_vendored(self) -> None:
        subprocess.run(["git", "add", "skills/vendored"], cwd=self.repo, check=True)
        self.lock()
        self.assertNotIn("skills/vendored/scripts/tool.js", self.gated())

    def test_a_lock_entry_without_a_source_vendors_nothing(self) -> None:
        (self.repo / ".skill-lock.json").write_text('{"skills": {"vendored": {}}}')
        self.assertIn("skills/vendored/scripts/tool.js", self.gated())

    def test_without_a_lock_every_changed_file_is_checked(self) -> None:
        self.assertEqual(
            self.gated(), ["app.py", "skills/ours/tool.js", "skills/vendored/scripts/tool.js"]
        )

    def test_a_malformed_lock_vendors_nothing(self) -> None:
        (self.repo / ".skill-lock.json").write_text("{not json")
        self.assertIn("skills/vendored/scripts/tool.js", self.gated())


class NamingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory()
        self.repo = Path(self.scratch.name).resolve() / "repo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)

    def tearDown(self) -> None:
        self.scratch.cleanup()

    def test_a_vacuous_name_in_a_changed_file_is_reported(self) -> None:
        bad = "data"
        (self.repo / "app.ts").write_text(f"const {bad} = 1\n")
        found = stop_gate.naming(
            self.repo, [self.repo / "app.ts"], time.monotonic() + 30
        )
        self.assertIsNotNone(found)
        assert found is not None
        self.assertIn("app.ts:1", found)

    def test_a_clean_file_passes(self) -> None:
        (self.repo / "app.ts").write_text("const unpaidInvoices = 1\n")
        self.assertIsNone(
            stop_gate.naming(self.repo, [self.repo / "app.ts"], time.monotonic() + 30)
        )

    def test_the_turn_gate_includes_naming(self) -> None:
        bad = "data"
        (self.repo / "app.ts").write_text(f"const {bad} = 1\n")
        found = stop_gate.gate(self.repo, time.monotonic() + 30)
        self.assertTrue(any("=== naming ===" in entry for entry in found))


if __name__ == "__main__":
    unittest.main()
