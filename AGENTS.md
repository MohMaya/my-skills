# Working with Shiv

Use pstack and Matt Pocock Skills as the engineering workflow. Read their installed skill files when needed. Keep workflow knowledge in those plugins and project facts in the repository.

## Choose the workflow

For multi-file work, signature changes, design decisions, unknown-cause bugs, and performance work, load `pstack:poteto-mode` and follow its matching playbook. This is the default across turns, including after compaction. Complete small, obvious edits directly and verify the real result.

Matt's reusable skills supply requirements discovery, domain language, module design, and test-first technique. Use `mattpocock-skills:grilling` and `domain-modeling` when a real product decision remains. Use `codebase-design` for module boundaries and `tdd` for testable behavior at the public seams agreed in the task or spec. Requirements already settled by Shiv or the repository stay settled.

Matt's `ask-matt`, `grill-with-docs`, `to-spec`, `to-tickets`, `implement`, `wayfinder`, and setup flows require user invocation. Honor a request for one and let it own that phase. Its idea-to-ship route is discovery, a spec and tickets when work spans sessions, then implementation in dependency order. Compose pstack's architecture, real-app verification, and required independent review within that flow. Keep one execution owner instead of recursively restarting both routers.

Use qualified names for overlapping skills such as `tdd` and `teach`. The Codex CLI may list Matt's linked skills by their bare names; resolve them from its `skills/mattpocock-skills/` source. Read the selected skill instead of reconstructing it from its name. Read existing project instructions and `docs/agents/` before Matt's planning workflows. Use `setup-matt-pocock-skills` when Shiv requests repository setup. Tracker choices, domain vocabulary, and ADRs belong in that repository.

## Verify the real product

At the start of behavior-changing work, find the project's verification skill and Feature Map. If the project has no working way to drive and observe its real UI, CLI, or service, use pstack's `create-verification-skill` first. Reuse existing tools. Execute the generated verification instructions once before relying on them.

For a project used from both harnesses, keep one verification skill under `.agents/skills/verify/` and link `.claude/skills/verify` to it. Respect an existing project layout instead of creating a duplicate. Keep launch, health checks, driving commands, evidence, cleanup, and feature navigation together.

Use `maintain-verification-skill` when the driver or Feature Map lacks coverage or has drifted. After a change, run the relevant repository checks and exercise the affected real user path. Preserve reviewable evidence. Report exactly what passed and what remains unverified. A passing build alone does not prove behavior.

## Use the current harness

Claude Code uses the native `pstack` and `mattpocock-skills` plugins. Codex uses the full `pstack` port from `pstack-claude`, plus `mattpocock-skills`. The curated `pstack-plugin` ChatGPT subset lacks the router and verification workflows and is not the engineering installation.

On Codex, read pstack's `poteto-mode/references/codex-tools.md` before translating its tool calls. Use the tools actually exposed by the session when the mapping is older than the host. The runtime's pstack model configuration chooses roles. Respect agent capacity and report reduced model diversity honestly.

Delegate substantial, independent work as the selected skill prescribes. Give each writer isolated state and a bounded task. Read the returned diff and evidence yourself. Use cloud workers only when the current harness actually provides them. Local subagents are local.

## Write for Shiv

Use `write-like-shiv` for authored prose and communication with Shiv. It owns voice when plugin writing advice differs. In operational updates, lead with the result or next action, number multi-step work, and state what remains. Keep substantial prose in its natural form.
