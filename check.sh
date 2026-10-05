#!/usr/bin/env bash
# Fail when a tracked file names a path that exists on only one machine.
# Allowed home paths are the three this setup owns: ~/.agents, ~/.claude, ~/.codex.
# Run locally or in CI. Safe to re-run.

set -euo pipefail
cd "$(dirname "$0")"

found=$(git grep -nIoE '(/Users/[A-Za-z][^[:space:]`"'\'')]*|/home/[a-z][^[:space:]`"'\'')]*|~/[A-Za-z.][^[:space:]`"'\'')]*)' -- . ':!check.sh' \
  | grep -vE ':~/\.(agents|claude|codex)([/.,;:]|$)' || true)

if [ -n "$found" ]; then
  printf '%s\n' "$found" >&2
  echo "machine-specific paths above: use ~/.agents, ~/.claude, ~/.codex, a repo-relative path, or a URL" >&2
  exit 1
fi
echo "portable: no machine-specific paths"
