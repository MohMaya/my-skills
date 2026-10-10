#!/usr/bin/env bash
# Run sync.sh's link_kernel twice against each CLAUDE.md starting state in a
# scratch HOME, and check the kernel lands in CLAUDE.md without being edited.

set -u
cd "$(dirname "$0")"
eval "$(sed -n '/^link_kernel() {/,/^}/p' sync.sh)"
fail=0

run() {
  H=$(mktemp -d)
  A="$H/.agents"
  M="$H/.claude/CLAUDE.md"
  mkdir -p "$A" "$H/.claude"
  echo KERNEL > "$A/AGENTS.md"
  eval "$1"
  HOME="$H" link_kernel 2>/dev/null
  HOME="$H" link_kernel 2>/dev/null
}

check() {
  if eval "$2" && [ "$(cat "$A/AGENTS.md")" = KERNEL ]; then
    echo "ok   $1"
  else
    echo "FAIL $1"
    fail=1
  fi
}

linked='[ "$(readlink "$M")" = ../.agents/AGENTS.md ] && [ "$(cat "$M")" = KERNEL ]'

run ':';                                            check "missing: linked" "$linked"
run ': > "$M"';                                     check "empty: linked" "$linked"
run 'echo "@~/.agents/AGENTS.md" > "$M"';           check "import only: linked" "$linked"
run 'ln -s ../.agents/AGENTS.md "$M"';              check "linked: unchanged" "$linked"
run 'ln -s "$A/AGENTS.md" "$M"';                    check "absolute link to the kernel: relinked" "$linked"
run 'ln -s nowhere "$M"';                           check "dangling link: linked" "$linked"
run 'echo mine > "$M"';                             check "own content: kept, kernel imported once" \
  '[ ! -L "$M" ] && [ "$(cat "$M")" = "$(printf "mine\n@~/.agents/AGENTS.md")" ]'
run 'printf "mine\n@~/.agents/AGENTS.md\n" > "$M"'; check "own content and import: unchanged" \
  '[ "$(cat "$M")" = "$(printf "mine\n@~/.agents/AGENTS.md")" ]'
run 'echo mine > "$H/my.md"; ln -s ../my.md "$M"';  check "link to own file: kept, kernel imported" \
  '[ "$(readlink "$M")" = ../my.md ] && grep -q "^@~/.agents/AGENTS.md$" "$H/my.md"'

exit $fail
