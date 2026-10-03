#!/usr/bin/env python3
"""Cursor sessionStart hook: inject the kernel, since Cursor has no global rules file."""

import json
import sys
from pathlib import Path

text = (Path(__file__).resolve().parent.parent / "AGENTS.md").read_text()
if text.startswith("---\n"):
    text = text.split("\n---\n", 1)[-1]
json.dump({"additional_context": text.strip()}, sys.stdout)
