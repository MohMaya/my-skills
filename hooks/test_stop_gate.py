import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("stop_gate", Path(__file__).with_name("stop-gate.py"))
assert spec and spec.loader
stop_gate = importlib.util.module_from_spec(spec)
sys.modules["stop_gate"] = stop_gate
spec.loader.exec_module(stop_gate)


class StopRootTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name).resolve() / "repo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)

    def tearDown(self) -> None:
        self.tmp.cleanup()

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


if __name__ == "__main__":
    unittest.main()
