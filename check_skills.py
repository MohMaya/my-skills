import pathlib
import sys

errors: list[str] = []
for skill in sorted(pathlib.Path("skills").glob("*/SKILL.md")):
    text = skill.read_text()
    parts = text.split("---\n", 2)
    if not text.startswith("---\n") or len(parts) < 3:
        errors.append(f"{skill}: no frontmatter")
        continue
    fields: dict[str, str] = dict(line.split(":", 1) for line in parts[1].splitlines() if line and not line[0].isspace() and ":" in line)
    name: str = fields.get("name", "").strip()
    desc: str = fields.get("description", "").strip()
    if name != skill.parent.name:
        errors.append(f"{skill}: name {name!r} differs from its directory")
    if "disable-model-invocation" in fields:
        errors.append(f"{skill}: disable-model-invocation locks the skill away from agents; delete the line")
    if not desc:
        errors.append(f"{skill}: no description")
    elif desc[0] not in "\"'>|" and ": " in desc:
        errors.append(f"{skill}: unquoted ': ' in description breaks YAML; quote it or use a dash")
    elif len(desc) > 1024:
        errors.append(f"{skill}: description over 1024 characters")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print("skills: every frontmatter parses")
