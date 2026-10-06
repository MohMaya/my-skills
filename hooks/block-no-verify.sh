#!/usr/bin/env bash
# PreToolUse guard for shell commands. Blocks git's hook and signing bypasses
# so a failing pre-commit check gets fixed rather than skipped: --no-verify,
# --no-gpg-sign, and the prefixes git accepts for them; a short option group
# containing n after `commit` (-n is --no-verify); and core.hooksPath
# overrides. The match is textual and fails safe: a commit message that
# quotes a flag is blocked too. Adapted from wshobson/agents block-no-verify.
# Registered by ~/.agents/sync.sh as a PreToolUse Bash hook in Claude Code and
# Codex; exit 2 blocks the command in both.

set -u

input=$(cat)
cmd=$(printf '%s' "$input" | /usr/bin/env jq -r '.tool_input.command // empty' 2>/dev/null) || cmd=$input
[ -n "$cmd" ] || cmd=$input

if printf '%s' "$cmd" | grep -qE -- '--no-(veri|g)|commit[^;&|]*[[:space:]]-[a-zA-Z]*n|core\.hooks[Pp]ath'; then
  echo 'BLOCKED: git hook and signing bypasses (--no-verify, -n, --no-gpg-sign, core.hooksPath) are not allowed. Fix what the hook reports, then commit without the bypass.' >&2
  exit 2
fi
exit 0
