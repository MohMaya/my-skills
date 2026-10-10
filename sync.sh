#!/usr/bin/env bash
# Wire ~/.agents into Claude Code and Cursor. Safe to re-run.
#
#   kernel  AGENTS.md  ~/.claude/CLAUDE.md link
#   skills  skills/    Claude: links in ~/.claude/skills
#   agents  claude/agents/  Claude: links in ~/.claude/agents
#   hooks   hooks/     turn-end gate, bar-raiser review gate, git-bypass guard,
#                      and secret-path guard, in ~/.claude/settings.json
#   claude  claude-setup-sync.sh: settings, plugins, plugin runtimes
#
# Cursor reads ~/.agents/skills itself, and imports ~/.claude/CLAUDE.md and
# the hooks in ~/.claude/settings.json while its "Include third-party
# Plugins, Skills, and other configs" setting is on (the default).
#
# MCP servers are configured per machine; mcp.json records
# them and is not synced. Adds what is missing and replaces only entries it
# owns. Plugins it did not add stay as they are.

set -euo pipefail

A="$HOME/.agents"

# Remove links in DIR that point into ~/.agents; with "all", remove every
# such link, otherwise only dangling ones.
prune_links() {
  local dir="$1" mode="$2" link
  [ -d "$dir" ] || return 0
  while IFS= read -r -d '' link; do
    case "$(readlink "$link")" in
      *".agents/"*) if [ "$mode" = all ] || [ ! -e "$link" ]; then rm -f "$link"; fi ;;
    esac
  done < <(find "$dir" -maxdepth 1 -type l -print0)
}

link_claude_skills() {
  local d="$HOME/.claude/skills" skill name
  mkdir -p "$d"
  prune_links "$d" dangling
  for skill in "$A"/skills/*/; do
    name=$(basename "$skill")
    if [ -f "$skill/SKILL.md" ] && [ ! -e "$d/$name" ]; then
      ln -s "../../.agents/skills/$name" "$d/$name"
    fi
  done
  echo "claude: $(find "$d" -maxdepth 1 -type l | wc -l | tr -d ' ') skills linked"
}

link_claude_agents() {
  local d="$HOME/.claude/agents" agent name
  mkdir -p "$d"
  prune_links "$d" dangling
  for agent in "$A"/claude/agents/*.md; do
    [ -e "$agent" ] || continue
    name=$(basename "$agent")
    if [ -L "$d/$name" ] || [ ! -e "$d/$name" ]; then
      ln -sfn "../../.agents/claude/agents/$name" "$d/$name"
    else
      echo "claude: $d/$name is a real file; preserved" >&2
    fi
  done
  echo "claude: $(find "$d" -maxdepth 1 -type l | wc -l | tr -d ' ') agents linked"
}

# Undo what the retired pstack setup's sync wrote, so pulling and re-syncing on any
# machine leaves no pstack instructions behind. Each target is a file that setup
# generated: the model-sheet import and its link.
retire_pstack() {
  local md="$HOME/.claude/CLAUDE.md"
  if grep -qs 'pstack-models\.md' "$md"; then
    sed -i.bak '/pstack-models\.md/d' "$md" && rm -f "$md.bak"
    echo "claude: removed the pstack model sheet import"
  fi
  if [ -L "$HOME/.claude/pstack-models.md" ]; then
    rm -f "$HOME/.claude/pstack-models.md"
    echo "removed pstack-era link ~/.claude/pstack-models.md"
  fi
}

# Cursor reads CLAUDE.md, and nothing documents it following @-imports, so the
# kernel is linked in. A CLAUDE.md with Shiv's own content stays, and imports
# the kernel instead.
link_kernel() {
  local md="$HOME/.claude/CLAUDE.md" kernel=../.agents/AGENTS.md
  mkdir -p "$HOME/.claude"
  if [ "$md" -ef "$A/AGENTS.md" ] || { [ -L "$md" ] && [ ! -e "$md" ]; } \
    || ! grep -qsvE '^(@.*AGENTS\.md)?$' "$md"; then
    ln -sfn "$kernel" "$md"
    echo "kernel: ~/.claude/CLAUDE.md linked"
  else
    grep -qsE '^@.*AGENTS\.md$' "$md" || printf '@~/.agents/AGENTS.md\n' >> "$md"
    echo "kernel: $md has its own content; kernel imported, which Cursor may not follow" >&2
  fi
}

# Rewrite our entries in Claude Code's hook config. An entry is ours when its
# command names one of our scripts; everything else is kept.
sync_hooks() {
  prune_links "$HOME/.claude/hooks" all
  python3 - "$A/hooks" <<'PY'
import json, os, shlex, sys
from pathlib import Path

hooks = sys.argv[1]
OURS = ("stop-gate.py", "review-gate.py", "block-no-verify.sh", "guard-protected-paths.sh")

def cmd(script, stop=False, args=""):
    path = shlex.quote(f"{hooks}/{script}")
    run = (f"python3 {path}" if script.endswith(".py") else path) + (f" {args}" if args else "")
    return f"[ -f {path} ] && {run} || true" if stop else f"[ ! -f {path} ] || {run}"

def ours(entry):
    return any(n in entry.get("command", "") for n in OURS)

# {"hooks": {Event: [{"matcher", "hooks": [entry]}]}}
# The review gate takes its turn baseline at the first tool call, which fires
# PreToolUse for every tool.
def our_hooks():
    return {
        "UserPromptSubmit": [{"hooks": [{"type": "command", "command": cmd("review-gate.py", stop=True, args="prompt"), "timeout": 60}]}],
        "Stop": [{"hooks": [{"type": "command", "command": cmd("stop-gate.py", stop=True), "timeout": 600},
                            {"type": "command", "command": cmd("review-gate.py", stop=True, args="stop"), "timeout": 120}]}],
        "PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": cmd("block-no-verify.sh")}]},
                       {"matcher": "", "hooks": [{"type": "command", "command": cmd("review-gate.py", args="pre-tool"), "timeout": 60}]},
                       {"matcher": "Write|Edit|MultiEdit", "hooks": [{"type": "command", "command": cmd("guard-protected-paths.sh")}]}],
    }

def merge(cfg, ours_now):
    events = cfg.setdefault("hooks", {})
    for name in list(events):
        groups = [{**g, "hooks": [h for h in g.get("hooks", []) if not ours(h)]} for g in events[name]]
        events[name] = [g for g in groups if g["hooks"]]
    for name, groups in ours_now.items():
        events.setdefault(name, []).extend(groups)
    cfg["hooks"] = {k: v for k, v in events.items() if v}

p = Path("~/.claude/settings.json").expanduser()
try:
    cfg = json.loads(p.read_text()) if p.exists() else {}
except ValueError as e:
    sys.exit(f"{p}: invalid JSON ({e})")
before = json.dumps(cfg, sort_keys=True)
merge(cfg, our_hooks())
if json.dumps(cfg, sort_keys=True) != before:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    os.replace(tmp, p)
    print(f"{p}: hooks updated")
else:
    print(f"{p}: hooks current")
PY
}

main() {
  retire_pstack
  link_kernel
  link_claude_skills
  link_claude_agents
  sync_hooks
  bash "$A/claude-setup-sync.sh"
  echo "done."
}

main "$@"
