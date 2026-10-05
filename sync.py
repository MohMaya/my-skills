#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path


def replace_file(path: Path, content: str) -> None:
    if path.is_file() and not path.is_symlink() and path.read_text() == content:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as output:
        temporary = Path(output.name)
        output.write(content)
    try:
        if path.exists():
            temporary.chmod(path.stat().st_mode & 0o777)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def link_file(path: Path, target: Path) -> None:
    if path.exists() and path.resolve() == target.resolve():
        return
    if path.exists() or path.is_symlink():
        raise FileExistsError(f"{path} already exists; inspect it before replacing it")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.symlink_to(os.path.relpath(target, path.parent))


def sync(agent_root: Path, home_root: Path) -> None:
    claude_root = home_root / ".claude"
    codex_root = home_root / ".codex"
    shared = agent_root / "AGENTS.md"
    claude_models = agent_root / "claude/pstack-models.md"
    codex_models = agent_root / "codex/pstack-models.md"
    settings = agent_root / "claude/settings.json"
    matt_skills = (
        codex_root
        / "plugins/cache/openai-curated-remote/mattpocock-skills/1.2.3/skills"
    )
    for source in (
        shared,
        claude_models,
        codex_models,
        settings,
        matt_skills / "tdd/SKILL.md",
        agent_root / "skills/write-like-shiv/SKILL.md",
    ):
        if not source.is_file():
            raise FileNotFoundError(f"Missing harness source: {source}")
    link_file(
        claude_root / "skills/write-like-shiv", agent_root / "skills/write-like-shiv"
    )
    link_file(claude_root / "pstack-models.md", claude_models)
    link_file(codex_root / "pstack-models.md", codex_models)
    link_file(codex_root / "skills/mattpocock-skills", matt_skills)
    settings_path = claude_root / "settings.json"
    current_settings = (
        json.loads(settings_path.read_text()) if settings_path.exists() else {}
    )
    overrides = json.loads(settings.read_text())
    for key in ("env", "enabledPlugins"):
        if key in overrides:
            current_settings.setdefault(key, {}).update(overrides.pop(key))
    current_settings.update(overrides)
    replace_file(settings_path, json.dumps(current_settings, indent=2) + "\n")
    replace_file(claude_root / "CLAUDE.md", f"@{shared}\n@{claude_models}\n")
    rows = "\n".join(
        line
        for line in codex_models.read_text().splitlines()
        if not line.startswith("session hook:")
    )
    replace_file(
        codex_root / "AGENTS.md", shared.read_text().rstrip() + "\n\n" + rows + "\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Wire the shared instructions, voice skill, and pstack model sheets into Claude Code and Codex."
    )
    parser.parse_args()
    sync(Path(__file__).resolve().parent, Path.home())
    print("Claude and Codex instructions synced. Start fresh sessions to load them.")


if __name__ == "__main__":
    main()
