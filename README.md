# ~/.agents

One agent setup for Claude Code, Codex, and Cursor.

## New machine

```sh
git clone https://github.com/MohMaya/my-skills.git ~/.agents
bash ~/.agents/sync.sh
```

Then, once per machine:

1. In Codex, run `/hooks` and trust the two hooks.
2. Sign in to each MCP server: `codex mcp login <name>` for Codex, and Settings > MCP in Cursor. Claude's servers come from its plugins and your claude.ai connectors.

Re-run `sync.sh` after every `git pull`. It is safe to repeat.

## What lives here

| Path | Holds |
| ---- | ----- |
| `AGENTS.md` | The kernel every harness loads: only what a model cannot infer |
| `skills/` | 30 skills, each carrying knowledge or a procedure a model lacks |
| `hooks/` | Turn-end gate (lint, types, complexity ratchet), git-bypass guard, Cursor kernel injection |
| `mcp.json` | Tool servers for Codex and Cursor |
| `evals/` | Real past commits replayed as tasks; run after every model or kernel change |

## Measuring a change

```sh
python3 evals/run.py claude    # or codex, cursor
```

Compare pass rate, diff size, and complexity violations in `evals/results.jsonl` against the `oracle` (the human commit) and `none` (no change) rows.
