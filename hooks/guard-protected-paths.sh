#!/usr/bin/env bash
# PreToolUse guard for Write/Edit/MultiEdit.
# Blocks writes to .env files, secrets dirs, and private keys.
# Reads JSON on stdin; exit 2 with stderr reason blocks the tool call.

set -eu

input=$(cat)
path=$(printf '%s' "$input" | /usr/bin/env jq -r '.tool_input.file_path // .tool_input.path // ""' 2>/dev/null || printf '')

[ -z "$path" ] && exit 0

base=$(basename "$path")

case "$path" in
  */.env|*/.env.*|.env|.env.*)
    echo "blocked: refusing to write to env file ($path)" >&2; exit 2 ;;
  */secrets/*|*/.secrets/*)
    echo "blocked: refusing to write inside a secrets directory ($path)" >&2; exit 2 ;;
  *.pem|*.key|*_rsa|*_ed25519|*.p12|*.pfx)
    echo "blocked: refusing to write to private key material ($path)" >&2; exit 2 ;;
esac

case "$base" in
  id_rsa|id_ed25519|id_ecdsa|credentials|credentials.json|service-account.json)
    echo "blocked: refusing to write to credential file ($base)" >&2; exit 2 ;;
esac

exit 0
