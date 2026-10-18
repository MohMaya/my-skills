# ~/.agents

One agent setup for Claude Code and Cursor.

`sync.sh` wires Claude Code. Cursor picks up the same kernel, skills, and hooks on its own: it reads `~/.agents/skills`, and imports `~/.claude/CLAUDE.md` and the hooks in `~/.claude/settings.json` while Cursor Settings → Agents → Third-Party Imports → "Include third-party Plugins, Skills, and other configs" is on (the default). In a multi-root Cursor workspace the gates check only the first root.

## New machine

```sh
git clone https://github.com/MohMaya/my-skills.git ~/.agents
bash ~/.agents/sync.sh
```

Then, once per machine, add the MCP servers it needs. `mcp.json` records every server's URL, and which Claude plugin provides it.

Update third-party skills with `npx skills@latest update -g`, then commit `skills/` and `.skill-lock.json`. Several third-party skills carry local edits, so read the update's diff and restore any edit it overwrote. AWS skills are not installed here: the `aws-mcp` server serves them live through `retrieve_skill`.

Re-run `sync.sh` after every `git pull`. It is safe to repeat. It runs `claude-setup-sync.sh`, which you can also run alone after changing Claude settings or plugins.

## What lives here

| Path | Holds |
| ---- | ----- |
| `AGENTS.md` | The kernel every harness loads: only what a model cannot infer |
| `skills/` | One owner skill per concern: ours plus third-party skills pinned in `.skill-lock.json` |
| `lint/` | Baseline lint and type-checker configs a new repository adopts |
| `hooks/` | Turn-end gate (lint, types, complexity ratchet), bar-raiser review gate, git-bypass guard, secret-path guard |
| `claude/` | Claude Code subagents (`agents/`), settings every machine shares, merged key by key (Opus main, Sonnet subagents, Fable advisor), and the status line |
| `claude-setup-sync.sh` | Applies `claude/`, installs the shared plugins, and installs the Python packages plugin servers need |
| `check.sh` | Fails on a skill frontmatter that would not load, and on any machine-specific path, so the setup works on every machine; CI runs it on each push |
| `mcp.json` | Record of every MCP server and its URL; not synced |
| `evals/` | Real past commits replayed as tasks; run after every model or kernel change |

## Measuring a change

```sh
python3 evals/run.py claude
```

Compare pass rate, diff size, and complexity violations in `evals/results.jsonl` against the `oracle` (the human commit) and `none` (no change) rows.
