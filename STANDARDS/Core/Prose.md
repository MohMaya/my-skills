# Core/Prose.md

Apply `write-like-shiv` whenever writing or revising anything, including short chat replies, progress updates, documents, tickets, comments, commit and PR text, product copy, and delegated-agent output.

Read `~/.agents/skills/write-like-shiv/SKILL.md` before drafting and select the relevant guidance in its `references/surfaces.md`. Read these files directly when the skill is absent from the runtime list. The skill owns voice, argument construction, editorial preferences, and final review. Load only the references needed for the current piece.

## Operator communication

Lead with the outcome or current state, then explain its practical consequence. Keep ownership and material uncertainty explicit. Give the reader enough detail to understand the situation and the next step.

Distinguish implemented, deployed, and verified. A completed foundation does not prove an end-to-end launch. State a missed target plainly; give a revised date only when supported. Document shapes and length guidance live in `Core/Documents.md`.

## Formats and review

Current user direction and required formats govern. Preserve quotations, identifiers, code semantics, and exact technical terminology. Specialist writing skills refine the relevant surface while `write-like-shiv` supplies the shared voice and review pass.

Use `humanizer` when requested or when prose needs an edit for AI-sounding patterns. Preserve facts, uncertainty, quotations, code, and required formats. When embedded in another writing workflow, return the final text.

Use `human-writing` for a requested edit that benefits from its checklist. `write-like-shiv` remains the voice and review owner. Choose the relevant editing pass; preserve the ADHD formatting and prose-artifact exceptions below when an imported skill suggests a different default.

Apply `i-have-adhd` by default in every harness and session. Read `~/.agents/skills/i-have-adhd/SKILL.md` before responding, including when the runtime omits it. It owns action-first formatting for chat, updates, questions, comments, Linear tickets, commit messages, PR bodies, and delegated-agent output. `write-like-shiv` owns voice and editorial review. Write these surfaces in plain English: name the action or result, explain necessary unfamiliar terms, and retain exact identifiers and required formats.

Requested prose artifacts, including PRDs, technical design documents, specs, essays, and long-form documents, use their document structure and `write-like-shiv`. Apply ADHD formatting to those artifacts only on explicit request. Surrounding chat and delivery updates retain ADHD formatting. `stop adhd mode` or `normal mode` disables it for the current session; each new session starts enabled. Follow task and harness requirements. Base estimates on evidence.

Use `write-like-shiv` for editorial review of every output. Run its local `scripts/voice_check.py` for substantial saved prose when Python is available. Resolve findings in context; diagnostic statistics do not prove voice fidelity.

## Technical documentation

Use ASD-STE100 principles for technical documentation: active voice, approved word senses, and one instruction per sentence. Keep procedural sentences within 20 words and descriptive sentences within 25 words.
