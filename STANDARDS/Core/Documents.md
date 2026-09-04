# Core/Documents.md

Load when creating or rewriting documents humans will read.

Shapes and targets only. Length discipline and the writing pipeline are the kernel's; tone is `Core/Prose.md`.

## Implementation plan

Use for multi-step execution work.

Required sections:
- Summary
- Key changes
- Test plan
- Assumptions

Target:
- 300 to 900 words
- enough detail that another engineer can execute without inventing design

## Technical design doc

Use when the change crosses boundaries or introduces a durable pattern.

Required sections:
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

Required shape:
- claim first
- reasoning second
- recommendation or next move last

Target:
- 150 to 600 words

## PR body

Required shape:
- first line in the tracker format from `Workflow/Git.md`
- short summary
- concrete changes
- verification
- closure line if the tracker supports it

Do not turn a PR into an essay.

## Technical explanation

Use for docs, comments, or replies where someone needs to understand a system.

Required shape:
- what it is
- why it exists
- how it behaves
- failure mode or tradeoff if relevant

Prefer one worked example over five generic statements.
