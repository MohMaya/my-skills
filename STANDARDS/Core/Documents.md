# Core/Documents.md

Load when creating or rewriting documents humans will read.

Use these shapes when the requested document benefits from them. Targets are guidance, not minimum lengths. A template or user-specified format takes precedence. Apply `write-like-shiv` to every document; it owns voice and editorial review. `Core/Prose.md` supplies loading and operator guidance.

## Project update

Use two or three short paragraphs, usually 100–180 words; write less when enough.

1. Current state: what is complete and what that enables.
2. Remaining work: the blocker or dependency, its owner when known, and its impact.
3. Next step: the concrete action and supported timing, including any missed target.

Use only the parts the facts support. Keep implementation details in linked tickets or designs. A draft stays a draft until publication is authorized.

## Project description

Write for executive readers. Use a few short paragraphs, usually 80–150 words, covering the outcome, launch scope, and what completion means. Name a dependency only when it changes the delivery picture. Tickets own implementation and acceptance detail; linked designs own architecture and research.

## Tickets and technical writeups

Use the same plain-English register. Include contracts, edge cases, dependencies, and verification that the implementer needs. Detail follows the task and audience; the short project-update shape is not a limit on technical accuracy.

## Implementation plan

Use when an implementation plan is a requested deliverable or coordinates substantial work.

Suggested sections:
- Summary
- Key changes
- Test plan
- Assumptions

Target:
- 300 to 900 words
- enough detail that another engineer can execute without inventing design

## Technical design doc

Use when the change crosses boundaries or introduces a durable pattern.

Suggested sections:
- Problem
- Constraints
- Proposal
- Interfaces / contracts
- Failure modes
- Rollout
- Verification
- Alternatives considered

Target:
- 700 to 1800 words
- concrete interfaces beat generic narrative

## ADR

Triggers are in `Core/Planning.md`. Format:

```markdown
# NNNN. Title

## Status
Accepted | Superseded | Deprecated

## Context

## Decision

## Consequences
```

Store ADRs under `docs/decisions/`.

## Internal memo or take

Use for recommendations, positioning, or internal argument.

Suggested shape:
- claim first
- reasoning second
- recommendation or next move last

Target:
- 150 to 600 words

## PR body

Suggested shape:
- first line in the tracker format from `Workflow/Git.md`
- short summary
- concrete changes
- verification
- closure line if the tracker supports it

Do not turn a PR into an essay.

## Technical explanation

Use for docs, comments, or replies where someone needs to understand a system.

Suggested shape:
- what it is
- why it exists
- how it behaves
- failure mode or tradeoff if relevant

Prefer one worked example over five generic statements.
