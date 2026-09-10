#!/usr/bin/env bash
# Idempotent sync from the canonical ~/.agents tree to each harness.
# Safe to re-run: only touches symlinks this script owns and the generated
# harness rules, Gemini CLI kernel import, and mandate mirror. Never touches non-symlink skill entries (native dirs,
# vendor skills) or ~/.agents/AGENTS.md, STANDARDS/, skills/ themselves.

set -euo pipefail

AGENTS_DIR="$HOME/.agents"
SKILLS_SRC="$AGENTS_DIR/skills"

sync_skills() {
  local harness_dir="$1" link_style="$2" linked=0 removed=0
  local link target resolved skill_dir name

  mkdir -p "$harness_dir"

  # Remove dangling symlinks that point into $SKILLS_SRC.
  while IFS= read -r -d '' link; do
    target=$(readlink "$link")
    resolved=$(python3 -c 'import os,sys; print(os.path.abspath(os.path.join(os.path.dirname(sys.argv[1]), sys.argv[2])))' "$link" "$target")
    if [[ "$resolved" == "$SKILLS_SRC"/* && ! -e "$link" ]]; then
      rm -f "$link"
      removed=$((removed + 1))
    fi
  done < <(find "$harness_dir" -maxdepth 1 -type l -print0 2>/dev/null)

  # Ensure a symlink for every canonical skill.
  for skill_dir in "$SKILLS_SRC"/*/; do
    [ -f "$skill_dir/SKILL.md" ] || continue
    name=$(basename "$skill_dir")
    link="$harness_dir/$name"

    if [ -L "$link" ]; then
      if [ "$link" -ef "$skill_dir" ]; then
        continue
      fi
      echo "conflict: $link points elsewhere; preserved" >&2
      continue
    elif [ -e "$link" ]; then
      continue # native/vendor entry with the same name -- never touch
    fi

    if [ "$link_style" = "relative" ]; then
      target=$(python3 -c "import os,sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))" "$skill_dir" "$harness_dir")
    else
      target="$skill_dir"
    fi
    ln -s "${target%/}" "$link"
    linked=$((linked + 1))
  done

  echo "$harness_dir: $linked skills linked, $removed dangling removed"
}

# Regenerate a harness rules file from the kernel. $2 is the harness-specific
# frontmatter body (delimiters are added here); the kernel's own frontmatter
# (first --- ... --- block) is stripped.
sync_rules() {
  local dest="$1" frontmatter="$2" src="$AGENTS_DIR/AGENTS.md"
  mkdir -p "$(dirname "$dest")"

  {
    printf -- '---\n%s---\n\n' "$frontmatter"
    awk 'BEGIN{fm=0} /^---$/{fm++; next} fm>=2{print}' "$src"
  } > "$dest"

  echo "$dest: regenerated ($(wc -c < "$dest" | tr -d ' ') bytes)"
}

# Keep injected mandates derived from the kernel, including its prose policy.
sync_mandates() {
  local dest="$HOME/.claude/hooks/mandates.md"
  mkdir -p "$(dirname "$dest")"
  {
    printf 'MANDATES ACTIVE (generated from ~/.agents/AGENTS.md):\n\n'
    awk '/^## /{copy=($0 ~ /^## (Scope and completion|Engineering judgment|Voice)$/)} copy{print}' "$AGENTS_DIR/AGENTS.md"
  } > "$dest"
  echo "$dest: regenerated"
}

# Antigravity loads skills from paths declared in the global skills.json,
# so the canonical tree needs no per-skill symlinks. The path must be absolute:
# this build rejects "~/" despite its own docs claiming home-relative support.
sync_antigravity_skills_config() {
  local dest="$HOME/.gemini/config/skills.json"
  mkdir -p "$(dirname "$dest")"
  printf '{\n  "entries": [\n    { "path": "%s" }\n  ]\n}\n' "$SKILLS_SRC" > "$dest"
  echo "$dest: written"
}

main() {
  local do_skills=1 gemini_context="$HOME/.gemini/GEMINI.md"
  case "${1:-}" in
    --codex-claude)
      sync_skills "$HOME/.claude/skills" relative
      sync_skills "$HOME/.codex/skills" relative
      sync_mandates
      return
      ;;
    --rules-only) do_skills=0 ;;
    "") ;;
    *) echo "usage: $0 [--codex-claude|--rules-only]" >&2; return 2 ;;
  esac

  if [ "$do_skills" = 1 ]; then
    sync_skills "$HOME/.claude/skills" relative
    sync_skills "$HOME/.codex/skills" relative
    sync_skills "$HOME/.cursor/skills" absolute
  fi

  sync_rules "$HOME/.cursor/rules/kernel.mdc" \
    'description: Global engineering kernel
alwaysApply: true
'
  sync_rules "$HOME/.gemini/config/rules/kernel.md" \
    'trigger: always_on
description: Global engineering kernel
'
  [ "$do_skills" = 0 ] || sync_antigravity_skills_config

  if ! grep -Fxq "@$AGENTS_DIR/AGENTS.md" "$gemini_context" 2>/dev/null; then
    printf '\n@%s/AGENTS.md\n' "$AGENTS_DIR" >> "$gemini_context"
  fi
  echo "$gemini_context: kernel import present"

  sync_mandates
}

main "$@"
