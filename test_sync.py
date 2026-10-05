import tempfile
import json
import unittest
from pathlib import Path

from sync import sync


class SyncTest(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.home_root = Path(self.directory.name).resolve()
        self.agent_root = self.home_root / ".agents"
        for name in ("claude", "codex", "skills/write-like-shiv"):
            (self.agent_root / name).mkdir(parents=True)
        (self.agent_root / "AGENTS.md").write_text("Shared instructions.\n")
        (self.agent_root / "skills/write-like-shiv/SKILL.md").write_text(
            "Shiv's voice.\n"
        )
        (self.agent_root / "claude/pstack-models.md").write_text(
            "feature, refactoring: inherit-parent\n"
        )
        (self.agent_root / "codex/pstack-models.md").write_text(
            "feature, refactoring: inherit-parent\nsession hook: off\n"
        )
        (self.agent_root / "claude/settings.json").write_text(
            '{"syncClaudeAiSkills": false, "syncClaudeAiPlugins": false}\n'
        )
        matt = (
            self.home_root
            / ".codex/plugins/cache/openai-curated-remote/mattpocock-skills/1.2.3/skills/tdd"
        )
        matt.mkdir(parents=True)
        (matt / "SKILL.md").write_text("Matt TDD.\n")

    def test_both_harnesses_read_current_sources_after_repeated_sync(self) -> None:
        sync(self.agent_root, self.home_root)
        sync(self.agent_root, self.home_root)
        claude = self.home_root / ".claude"
        codex = self.home_root / ".codex"
        self.assertEqual(
            (claude / "skills/write-like-shiv").resolve(),
            self.agent_root / "skills/write-like-shiv",
        )
        self.assertEqual(
            (codex / "pstack-models.md").read_text(),
            "feature, refactoring: inherit-parent\nsession hook: off\n",
        )
        self.assertEqual(
            (codex / "AGENTS.md").read_text(),
            "Shared instructions.\n\nfeature, refactoring: inherit-parent\n",
        )
        self.assertEqual(
            (codex / "skills/mattpocock-skills/tdd/SKILL.md").read_text(), "Matt TDD.\n"
        )
        imports = (claude / "CLAUDE.md").read_text().splitlines()
        self.assertEqual(
            [Path(line[1:]).read_text() for line in imports],
            ["Shared instructions.\n", "feature, refactoring: inherit-parent\n"],
        )
        (self.agent_root / "AGENTS.md").write_text("Updated instructions.\n")
        sync(self.agent_root, self.home_root)
        self.assertEqual(
            (codex / "AGENTS.md").read_text(),
            "Updated instructions.\n\nfeature, refactoring: inherit-parent\n",
        )

    def test_existing_shared_skill_directory_is_supported(self) -> None:
        claude = self.home_root / ".claude"
        claude.mkdir()
        (claude / "skills").symlink_to(self.agent_root / "skills")
        sync(self.agent_root, self.home_root)
        self.assertTrue((claude / "skills").is_symlink())

    def test_conflicting_skill_is_preserved(self) -> None:
        skill = self.home_root / ".claude/skills/write-like-shiv"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("Independent skill.\n")
        with self.assertRaisesRegex(FileExistsError, "inspect it before replacing"):
            sync(self.agent_root, self.home_root)
        self.assertEqual((skill / "SKILL.md").read_text(), "Independent skill.\n")
        self.assertFalse((self.home_root / ".claude/CLAUDE.md").exists())

    def test_missing_source_stops_before_writing_harnesses(self) -> None:
        (self.agent_root / "codex/pstack-models.md").unlink()
        with self.assertRaisesRegex(FileNotFoundError, "Missing harness source"):
            sync(self.agent_root, self.home_root)
        self.assertFalse((self.home_root / ".claude").exists())

    def test_cloud_sync_stays_off_without_overwriting_other_preferences(self) -> None:
        settings = self.home_root / ".claude/settings.json"
        settings.parent.mkdir()
        settings.write_text(
            '{"model": "fable", "syncClaudeAiSkills": true, "syncClaudeAiPlugins": true}\n'
        )
        settings.chmod(0o600)
        sync(self.agent_root, self.home_root)
        self.assertEqual(
            json.loads(settings.read_text()),
            {
                "model": "fable",
                "syncClaudeAiSkills": False,
                "syncClaudeAiPlugins": False,
            },
        )
        self.assertEqual(settings.stat().st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()
