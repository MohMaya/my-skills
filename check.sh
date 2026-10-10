#!/usr/bin/env bash
# Fail when a tracked or new file names a path that exists on only one machine:
# absolute home, volume, or system-temp paths, Windows drive paths, and
# home-relative paths outside the directories this setup and its plugins own.
# Run locally or in CI. Safe to re-run.

set -euo pipefail
cd "$(dirname "$0")"

home='(~|\$HOME)/'
owned='\.(agents|claude|supermemory-claude)([/.,;:]|$)'
paths="(${home}[A-Za-z0-9._-][^[:space:]\`\"')]*|/(Users|home|Volumes|opt|private)/[A-Za-z0-9][^[:space:]\`\"')]*|[A-Z]:\\\\[^[:space:]\`\"')]*)"

found=$(git grep --untracked -nIoE "$paths" -- . ':!check.sh' \
  | grep -vE ":${home}${owned}" || true)

if [ -n "$found" ]; then
  printf '%s\n' "$found" >&2
  echo "machine-specific paths above: use ~/.agents, ~/.claude, a repo-relative path, or a URL" >&2
  exit 1
fi
echo "portable: no machine-specific paths"

bash test_link_kernel.sh >/dev/null || { bash test_link_kernel.sh | grep FAIL >&2; exit 1; }
echo "link_kernel: every CLAUDE.md state handled"
