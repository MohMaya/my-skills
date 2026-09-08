# Core/Prose.md

Apply `write-like-shiv` whenever writing or revising anything, including short chat replies, progress updates, documents, tickets, comments, commit and PR text, product copy, and delegated-agent output.

Read `~/.agents/skills/write-like-shiv/SKILL.md` before drafting and select the relevant guidance in its `references/surfaces.md`. Read these files directly when the skill is absent from the runtime list. The skill owns voice, argument construction, editorial preferences, and final review. Load only the references needed for the current piece.

## Operator communication

Lead with the outcome or current state, then explain its practical consequence. Keep ownership and material uncertainty explicit. Give the reader enough detail to understand the situation and the next step.

Distinguish implemented, deployed, and verified. A completed foundation does not prove an end-to-end launch. State a missed target plainly; give a revised date only when supported. Document shapes and length guidance live in `Core/Documents.md`.

## Formats and review

Current user direction and required formats govern. Preserve quotations, identifiers, code semantics, and exact technical terminology. Specialist writing skills refine the relevant surface while `write-like-shiv` supplies the shared voice and review pass.

Use `humanizer` when requested or when prose needs an edit for AI-sounding patterns. Preserve facts, uncertainty, quotations, code, and required formats. When embedded in another writing workflow, return the final text.

Activate `i-have-adhd` only when the user explicitly invokes it. The mode persists until `stop adhd mode` or `normal mode`. Installation alone leaves it inactive. Apply its action-first formatting within task and harness requirements. Base estimates on evidence.

Use `write-like-shiv` for editorial review of every output. Run its local `scripts/voice_check.py` for substantial saved prose when Python is available. Resolve findings in context; diagnostic statistics do not prove voice fidelity.

## Technical documentation

Use ASD-STE100 principles for technical documentation: active voice, approved word senses, and one instruction per sentence. Keep procedural sentences within 20 words and descriptive sentences within 25 words.
