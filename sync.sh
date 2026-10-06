#!/usr/bin/env bash
# Wire ~/.agents into Claude Code and Codex. Safe to re-run.
#
#   kernel  AGENTS.md  Claude: import in ~/.claude/CLAUDE.md
#                      Codex:  ~/.codex/AGENTS.md link
#   skills  skills/    Claude: links in ~/.claude/skills
#   agents  claude/agents/  Claude: links in ~/.claude/agents
#                      Codex reads ~/.agents/skills natively
#   hooks   hooks/     turn-end gate, bar-raiser review gate, git-bypass guard,
#                      and secret-path guard
#   claude  claude-setup-sync.sh: settings, plugins, plugin runtimes
#
# MCP servers are configured per machine in each harness; mcp.json records
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
# generated: a real ~/.codex/AGENTS.md naming pstack, the model-sheet import and
# links, and its link to the Codex plugin cache of Matt Pocock's skills.
retire_pstack() {
  local codex="$HOME/.codex/AGENTS.md" md="$HOME/.claude/CLAUDE.md" link
  if [ -f "$codex" ] && [ ! -L "$codex" ] && grep -q 'pstack' "$codex"; then
    rm -f "$codex"
    echo "codex: removed the pstack-era AGENTS.md"
  fi
  if grep -qs 'pstack-models\.md' "$md"; then
    sed -i.bak '/pstack-models\.md/d' "$md" && rm -f "$md.bak"
    echo "claude: removed the pstack model sheet import"
  fi
  for link in "$HOME/.claude/pstack-models.md" "$HOME/.codex/pstack-models.md" "$HOME/.codex/skills/mattpocock-skills"; do
    if [ -L "$link" ]; then
      rm -f "$link"
      echo "removed pstack-era link $link"
    fi
  done
  if grep -qs 'pstack@pstack-claude' "$HOME/.codex/config.toml"; then
    echo "codex: pstack is still installed; remove it with: codex plugin remove pstack@pstack-claude" >&2
  fi
}

link_kernels() {
  local md="$HOME/.claude/CLAUDE.md" codex="$HOME/.codex/AGENTS.md"
  mkdir -p "$HOME/.claude" "$HOME/.codex"
  grep -qsE '^@.*AGENTS\.md$' "$md" || printf '@~/.agents/AGENTS.md\n' >> "$md"
  if [ -e "$codex" ] && [ ! -L "$codex" ]; then
    echo "codex: $codex is a real file; preserved" >&2
  else
    ln -sfn "$A/AGENTS.md" "$codex"
  fi
  echo "kernel: Claude import, Codex link"
}

# Rewrite our entries in each harness's hook config. An entry is ours when its
# command names one of our scripts; everything else is kept.
sync_hooks() {
  prune_links "$HOME/.claude/hooks" all
  prune_links "$HOME/.codex/hooks" all
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

# Claude Code and Codex: {"hooks": {Event: [{"matcher", "hooks": [entry]}]}}
# The review gate takes its turn baseline at the first tool call in Claude Code,
# which fires PreToolUse for every tool; Codex takes it at the prompt.
def hooks_for(harness):
    touch = " --first-touch" if harness == "claude" else ""
    gate = {"matcher": "", "hooks": []} if touch else {"matcher": "Bash", "hooks": []}
    gate["hooks"].append({"type": "command", "command": cmd("review-gate.py", args="pre-tool" + touch), "timeout": 60})
    return {
        "UserPromptSubmit": [{"hooks": [{"type": "command", "command": cmd("review-gate.py", stop=True, args="prompt" + touch), "timeout": 60}]}],
        "Stop": [{"hooks": [{"type": "command", "command": cmd("stop-gate.py", stop=True), "timeout": 600},
                            {"type": "command", "command": cmd("review-gate.py", stop=True, args="stop" + touch), "timeout": 120}]}],
        "PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": cmd("block-no-verify.sh")}]},
                       gate,
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

for harness, path in (("claude", "~/.claude/settings.json"), ("codex", "~/.codex/hooks.json")):
    p = Path(path).expanduser()
    try:
        cfg = json.loads(p.read_text()) if p.exists() else {}
    except ValueError as e:
        print(f"{p}: invalid JSON ({e}); skipped", file=sys.stderr)
        continue
    before = json.dumps(cfg, sort_keys=True)
    merge(cfg, hooks_for(harness))
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
  link_kernels
  link_claude_skills
  link_claude_agents
  prune_links "$HOME/.codex/skills" all
  sync_hooks
  bash "$A/claude-setup-sync.sh"
  echo "done. Codex asks you to trust the hooks once: run /hooks in Codex."
}

main "$@"
