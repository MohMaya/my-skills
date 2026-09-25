#!/usr/bin/env bash
# PostToolUse formatter. Runs best-effort formatters on the edited file.
# Silent on missing tools; never blocks the pipeline.
# Python formats only where the project adopts a formatter, matching
# stop-gate.py: ruff where it formats with ruff, black where it configures
# black. A project that chose neither is left as written.
# Synced by ~/.agents/sync.sh into ~/.claude/hooks and ~/.codex/hooks.

set -u

input=$(cat)
path=$(printf '%s' "$input" | /usr/bin/env jq -r '.tool_input.file_path // .tool_input.path // ""' 2>/dev/null || printf '')

[ -z "$path" ] && exit 0
[ ! -f "$path" ] && exit 0

has() { command -v "$1" >/dev/null 2>&1; }

# Print the Python formatter the nearest configuring directory adopts, if any.
python_formatter() {
  local dir root
  dir=$(cd "$(dirname "$1")" && pwd)
  root=$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null || printf '/')
  while :; do
    if grep -qs '^\[tool\.ruff\.format' "$dir/pyproject.toml" ||
      grep -qs '^\[format' "$dir/ruff.toml" "$dir/.ruff.toml" ||
      grep -qs 'id: ruff-format' "$dir/.pre-commit-config.yaml"; then
      echo ruff; return
    fi
    if grep -qs '^\[tool\.black' "$dir/pyproject.toml" ||
      grep -qs 'id: black' "$dir/.pre-commit-config.yaml"; then
      echo black; return
    fi
    [ "$dir" = "$root" ] || [ "$dir" = / ] && return
    dir=$(dirname "$dir")
  done
}

case "$path" in
  *.go)
    has gofmt && gofmt -w "$path" >/dev/null 2>&1 || true
    ;;
  *.py)
    case "$(python_formatter "$path")" in
      ruff) has ruff && ruff format --force-exclude "$path" >/dev/null 2>&1 || true ;;
      black) has black && black -q "$path" >/dev/null 2>&1 || true ;;
    esac
    ;;
  *.rs)
    has rustfmt && rustfmt --edition 2021 "$path" >/dev/null 2>&1 || true
    ;;
  *.tf|*.tfvars)
    has terraform && terraform fmt "$path" >/dev/null 2>&1 || true
    ;;
  *.json)
    has jq && tmp=$(mktemp) && jq . "$path" >"$tmp" 2>/dev/null && mv "$tmp" "$path" || rm -f "$tmp" 2>/dev/null || true
    ;;
esac

exit 0
