#!/usr/bin/env bash
# Claude Code statusline. Reads JSON on stdin, prints one line.
# Fields: model, cwd (basename), git branch, tokens used (if present),
# plus the Supermemory saving-status renderer appended at the end.

set -eu

input=$(cat)

jq_get() {
  printf '%s' "$input" | /usr/bin/env jq -r "$1" 2>/dev/null || printf ''
}

model=$(jq_get '.model.display_name // .model.id // ""')
cwd=$(jq_get '.workspace.current_dir // .cwd // ""')
tokens=$(jq_get '.cost.total_tokens // ""')

[ -z "$cwd" ] && cwd="$PWD"
base=$(basename "$cwd")

branch=""
if git -C "$cwd" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  branch=$(git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null || git -C "$cwd" rev-parse --short HEAD 2>/dev/null || echo "")
fi

parts=()
[ -n "$model" ]  && parts+=("\033[36m${model}\033[0m")
[ -n "$base" ]   && parts+=("\033[32m${base}\033[0m")
[ -n "$branch" ] && parts+=("\033[33m${branch}\033[0m")
[ -n "$tokens" ] && parts+=("\033[90m${tokens}t\033[0m")

IFS=" · "
line=$(printf '%b' "${parts[*]}")

supermemory=$(printf '%s' "$input" | node "$HOME/.supermemory-claude/statusline-current" 2>/dev/null || printf '')

if [ -n "$supermemory" ]; then
  printf '%s  %s' "$line" "$supermemory"
else
  printf '%s' "$line"
fi
