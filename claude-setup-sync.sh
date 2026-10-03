#!/usr/bin/env bash
# Make this machine's Claude Code match every other one. Safe to re-run.
#
#   settings  claude/settings.json merged key by key into ~/.claude/settings.json;
#             machine-only keys (hooks, autoMode, local plugins) are kept
#   plugins   every marketplace and plugin below is added if missing
#   runtimes  Python packages that plugin MCP servers import
#
# sync.sh runs this; it also runs on its own.

set -euo pipefail

A="$HOME/.agents"

CLAUDE_MARKETPLACES=(
  anthropics/claude-plugins-official
  anthropics/claude-plugins-community
  supermemoryai/claude-supermemory
)
CLAUDE_PLUGINS=(
  supermemory@supermemory-plugins
  agent-memory@claude-community
  next-steps@claude-community
  typescript-lsp@claude-plugins-official pyright-lsp@claude-plugins-official
  gopls-lsp@claude-plugins-official rust-analyzer-lsp@claude-plugins-official
  cloudflare@claude-plugins-official firebase@claude-plugins-official
  figma@claude-plugins-official posthog@claude-plugins-official
  railway@claude-plugins-official
)
# agent-memory launches `python` and is written against the mcp 1.x server API.
PLUGIN_PYTHON_PACKAGES=("mcp>=1,<2" pyyaml aiosqlite anthropic)

merge_settings() {
  python3 - "$A/claude/settings.json" "$HOME/.claude/settings.json" <<'PY'
import json, os, sys
from pathlib import Path

src, dst = Path(sys.argv[1]), Path(sys.argv[2])

def merge(into, new):
    for key, value in new.items():
        if isinstance(value, dict) and isinstance(into.get(key), dict):
            merge(into[key], value)
        else:
            into[key] = value

cfg = json.loads(dst.read_text()) if dst.exists() else {}
before = json.dumps(cfg, sort_keys=True)
merge(cfg, json.loads(src.read_text()))
if json.dumps(cfg, sort_keys=True) == before:
    print(f"{dst}: settings current")
    sys.exit(0)
dst.parent.mkdir(parents=True, exist_ok=True)
tmp = dst.with_name(dst.name + ".tmp")
tmp.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
os.replace(tmp, dst)
print(f"{dst}: settings updated")
PY
}

sync_plugins() {
  command -v claude >/dev/null 2>&1 || { echo "claude: CLI not found; plugins skipped" >&2; return 0; }
  local installed m p
  installed=$(claude plugin list --json 2>/dev/null || echo "[]")
  for m in "${CLAUDE_MARKETPLACES[@]}"; do claude plugin marketplace add "$m" >/dev/null 2>&1 || true; done
  for p in "${CLAUDE_PLUGINS[@]}"; do
    grep -q "\"$p\"" <<<"$installed" || claude plugin install "$p" >/dev/null 2>&1 || echo "claude: $p not installed" >&2
  done
  echo "claude: ${#CLAUDE_PLUGINS[@]} plugins checked"
}

sync_plugin_python() {
  command -v python >/dev/null 2>&1 || { echo "python: not on PATH; agent-memory will not start" >&2; return 0; }
  python -m pip install -q "${PLUGIN_PYTHON_PACKAGES[@]}" || echo "python: plugin packages failed to install" >&2
  echo "python: plugin packages present for $(python --version)"
}

merge_settings
sync_plugins
sync_plugin_python
