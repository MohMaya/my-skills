#!/usr/bin/env bash
# Idempotent sync from the canonical ~/.agents tree to each harness.
# Safe to re-run: only touches symlinks this script owns, the generated
# harness rules, Gemini CLI kernel import, mandate mirrors, the repo-owned
# hooks under hooks/, and the stop-gate entry in Claude and Codex settings.
# Never touches non-symlink skill entries (native dirs, vendor skills), other
# hooks, or ~/.agents/AGENTS.md, STANDARDS/, skills/ themselves.

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
  local dest
  for dest in "$HOME/.claude/hooks/mandates.md" "$HOME/.codex/hooks/mandates.md"; do
    mkdir -p "$(dirname "$dest")"
    {
      printf 'MANDATES ACTIVE (generated from ~/.agents/AGENTS.md):\n\n'
      awk '/^## /{copy=($0 ~ /^## (Scope and completion|Engineering judgment|Engineering skills|Design authority|Voice)$/)} copy{print}' "$AGENTS_DIR/AGENTS.md"
    } > "$dest"
    echo "$dest: regenerated"
  done
}

# Link a repo-owned hook into a harness's hooks dir. A real file at the link
# path is preserved and reported; returns 1 so callers skip registration.
link_hook() {
  local harness_dir="$1" name="$2" link="$1/hooks/$2"
  mkdir -p "$harness_dir/hooks"
  if [ -e "$link" ] && [ ! -L "$link" ]; then
    echo "conflict: $link is a real file; preserved" >&2
    return 1
  fi
  ln -sfn "$AGENTS_DIR/hooks/$name" "$link"
}

# Link the turn-end lint and type gate into a harness and register it as a
# Stop hook. The command fails open: if the link dangles, the turn still ends.
# Merge-only: the settings file is rewritten (atomically) only when the entry
# is missing or stale, and other hooks stay as they are. Codex asks to trust
# a new or changed hook on its next run.
sync_stop_gate() {
  local harness_dir="$1" settings="$2" link="$1/hooks/stop-gate.py"
  link_hook "$harness_dir" stop-gate.py || return 0
  python3 - "$settings" "$link" <<'PY' || echo "$settings: stop gate not registered" >&2
import json
import os
import pathlib
import shlex
import sys
import tempfile

path, link = pathlib.Path(sys.argv[1]), sys.argv[2]
q = shlex.quote(link)
command = f"[ -f {q} ] && python3 {q} || true"
try:
    data = json.loads(path.read_text()) if path.exists() else {}
except ValueError as e:
    sys.exit(f"{path}: invalid JSON ({e})")
stop = data.setdefault("hooks", {}).setdefault("Stop", [])
if any(h.get("command") == command for group in stop for h in group.get("hooks", [])):
    print(f"{path}: stop gate present")
    sys.exit()
for group in stop:  # drop earlier registrations of this gate
    group["hooks"] = [h for h in group.get("hooks", []) if "stop-gate.py" not in h.get("command", "")]
stop[:] = [g for g in stop if g.get("hooks")]
stop.append({"hooks": [{"type": "command", "command": command, "timeout": 600}]})
fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".")
with os.fdopen(fd, "w") as f:
    f.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
os.chmod(tmp, path.stat().st_mode if path.exists() else 0o644)
os.replace(tmp, path)
print(f"{path}: stop gate registered")
PY
}

sync_hooks() {
  sync_mandates
  link_hook "$HOME/.claude" format-on-edit.sh || true
  link_hook "$HOME/.codex" format-on-edit.sh || true
  sync_stop_gate "$HOME/.claude" "$HOME/.claude/settings.json"
  sync_stop_gate "$HOME/.codex" "$HOME/.codex/hooks.json"
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
      sync_hooks
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

  sync_hooks
}

main "$@"
