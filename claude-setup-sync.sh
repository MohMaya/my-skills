#!/usr/bin/env bash
# Install the Claude Code marketplaces and plugins every machine shares. Safe to re-run.
#
# sync.sh runs this; it also runs on its own.

set -euo pipefail

CLAUDE_MARKETPLACES=(anthropics/claude-plugins-official supermemoryai/claude-supermemory)
# Plugins every machine gets. Plugins that only carry an MCP server are per
# machine; mcp.json records which plugin provides each one.
CLAUDE_PLUGINS=(
  supermemory@supermemory-plugins
  typescript-lsp@claude-plugins-official pyright-lsp@claude-plugins-official
  gopls-lsp@claude-plugins-official rust-analyzer-lsp@claude-plugins-official
)

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

sync_plugins
