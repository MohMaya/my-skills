# ~/.agents

One agent setup for Claude Code and Codex.

## New machine

```sh
git clone https://github.com/MohMaya/my-skills.git ~/.agents
bash ~/.agents/sync.sh
```

Then, once per machine:

1. In Codex, run `/hooks` and trust the two hooks.
2. Add the MCP servers this machine needs in each harness. `mcp.json` records every server's URL, and which Claude plugin provides it.

Re-run `sync.sh` after every `git pull`. It is safe to repeat. It runs `claude-setup-sync.sh`, which you can also run alone after changing Claude settings or plugins.

## What lives here

| Path | Holds |
| ---- | ----- |
| `AGENTS.md` | The kernel every harness loads: only what a model cannot infer |
| `skills/` | 27 skills, each carrying knowledge or a procedure a model lacks |
| `hooks/` | Turn-end gate (lint, types, complexity ratchet), git-bypass guard, secret-path guard |
| `claude/` | Claude Code subagents (`agents/`), settings every machine shares, merged key by key (Opus main, Sonnet subagents, Fable advisor), and the status line |
| `claude-setup-sync.sh` | Applies `claude/`, installs the shared plugins, and installs the Python packages plugin servers need |
| `mcp.json` | Record of every MCP server and its URL; not synced |
| `evals/` | Real past commits replayed as tasks; run after every model or kernel change |

## Measuring a change

```sh
python3 evals/run.py claude    # or codex
```

Compare pass rate, diff size, and complexity violations in `evals/results.jsonl` against the `oracle` (the human commit) and `none` (no change) rows.
