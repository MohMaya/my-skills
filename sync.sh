#!/usr/bin/env bash
# Wire ~/.agents into Claude Code, Codex, and Cursor. Safe to re-run.
#
#   kernel  AGENTS.md  Claude: import in ~/.claude/CLAUDE.md
#                      Codex:  ~/.codex/AGENTS.md link
#                      Cursor: sessionStart hook (Cursor has no global rules file)
#   skills  skills/    Claude: links in ~/.claude/skills
#                      Codex and Cursor read ~/.agents/skills natively
#   hooks   hooks/     turn-end gate and git-bypass guard in all three
#
# MCP servers are configured per machine in each harness; mcp.json records
# them and is not synced. Adds what is missing and replaces only entries it
# owns. Plugins it did not add stay as they are.

set -euo pipefail

A="$HOME/.agents"
CODEX=$(command -v codex || echo "/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex")

CLAUDE_MARKETPLACES=(anthropics/claude-plugins-official supermemoryai/claude-supermemory)
# Plugins every machine gets. Plugins that only carry an MCP server are per
# machine; mcp.json records which plugin provides each one.
CLAUDE_PLUGINS=(
  supermemory@supermemory-plugins
  typescript-lsp@claude-plugins-official pyright-lsp@claude-plugins-official
  gopls-lsp@claude-plugins-official rust-analyzer-lsp@claude-plugins-official
)

has() { command -v "$1" >/dev/null 2>&1 || [ -x "$1" ]; }

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

link_kernels() {
  local md="$HOME/.claude/CLAUDE.md" codex="$HOME/.codex/AGENTS.md"
  mkdir -p "$HOME/.claude" "$HOME/.codex"
  grep -qsE '^@.*AGENTS\.md$' "$md" || printf '@~/.agents/AGENTS.md\n' >> "$md"
  if [ -e "$codex" ] && [ ! -L "$codex" ]; then
    echo "codex: $codex is a real file; preserved" >&2
  else
    ln -sfn "$A/AGENTS.md" "$codex"
  fi
  rm -f "$HOME/.cursor/rules/kernel.mdc" "$HOME/.claude/hooks/mandates.md" "$HOME/.codex/hooks/mandates.md"
  echo "kernel: Claude import, Codex link, Cursor sessionStart hook"
}

# Rewrite our entries in each harness's hook config. An entry is ours when its
# command names one of our scripts or a retired one; everything else is kept.
sync_hooks() {
  prune_links "$HOME/.claude/hooks" all
  prune_links "$HOME/.codex/hooks" all
  python3 - "$A/hooks" <<'PY'
import json, os, shlex, sys
from pathlib import Path

hooks = sys.argv[1]
OURS = ("stop-gate.py", "block-no-verify.sh", "session-kernel.py",
        "format-on-edit.sh", "mandates.md", "shiv-code-gate.md")

def cmd(script, stop=False):
    path = shlex.quote(f"{hooks}/{script}")
    run = f"python3 {path}" if script.endswith(".py") else path
    return f"[ -f {path} ] && {run} || true" if stop else f"[ ! -f {path} ] || {run}"

def ours(entry):
    return any(n in entry.get("command", "") for n in OURS)

# Claude Code and Codex: {"hooks": {Event: [{"matcher", "hooks": [entry]}]}}
NESTED = {
    "Stop": [{"hooks": [{"type": "command", "command": cmd("stop-gate.py", stop=True), "timeout": 600}]}],
    "PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": cmd("block-no-verify.sh")}]}],
}
# Cursor: {"version": 1, "hooks": {event: [entry]}}
FLAT = {
    "sessionStart": [{"command": cmd("session-kernel.py", stop=True)}],
    "stop": [{"command": cmd("stop-gate.py", stop=True), "timeout": 600, "loop_limit": 1}],
    "beforeShellExecution": [{"command": cmd("block-no-verify.sh")}],
}

def merge_nested(cfg):
    events = cfg.setdefault("hooks", {})
    for name in list(events):
        groups = [{**g, "hooks": [h for h in g.get("hooks", []) if not ours(h)]} for g in events[name]]
        events[name] = [g for g in groups if g["hooks"]]
    for name, groups in NESTED.items():
        events.setdefault(name, []).extend(groups)
    cfg["hooks"] = {k: v for k, v in events.items() if v}

def merge_flat(cfg):
    cfg.setdefault("version", 1)
    events = cfg.setdefault("hooks", {})
    for name in list(events):
        events[name] = [h for h in events[name] if not ours(h)]
    for name, entries in FLAT.items():
        events.setdefault(name, []).extend(entries)
    cfg["hooks"] = {k: v for k, v in events.items() if v}

for path, merge in (("~/.claude/settings.json", merge_nested),
                    ("~/.codex/hooks.json", merge_nested),
                    ("~/.cursor/hooks.json", merge_flat)):
    p = Path(path).expanduser()
    try:
        cfg = json.loads(p.read_text()) if p.exists() else {}
    except ValueError as e:
        print(f"{p}: invalid JSON ({e}); skipped", file=sys.stderr)
        continue
    before = json.dumps(cfg, sort_keys=True)
    merge(cfg)
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

sync_claude_plugins() {
  has claude || { echo "claude: CLI not found; plugins skipped" >&2; return 0; }
  local installed m p
  installed=$(claude plugin list --json 2>/dev/null || echo "[]")
  for m in "${CLAUDE_MARKETPLACES[@]}"; do claude plugin marketplace add "$m" >/dev/null 2>&1 || true; done
  for p in "${CLAUDE_PLUGINS[@]}"; do
    grep -q "\"$p\"" <<<"$installed" || claude plugin install "$p" >/dev/null 2>&1 || echo "claude: $p not installed" >&2
  done
  echo "claude: ${#CLAUDE_PLUGINS[@]} plugins checked"
}

main() {
  link_kernels
  link_claude_skills
  prune_links "$HOME/.codex/skills" all
  prune_links "$HOME/.cursor/skills" all
  sync_hooks
  sync_claude_plugins
  echo "done. Codex asks you to trust the hooks once: run /hooks in Codex."
}

main "$@"
