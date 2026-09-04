# Core/Planning.md

Load before multi-step work, cross-layer changes, new features, migrations, and irreversible decisions.

## What planning is for

Planning is how you avoid spending hours implementing the wrong shape of the right idea.

The output is not a brainstorm. It is a decision-ready spec that another strong engineer could implement without having to invent the missing half.

## Minimum plan shape

Every non-trivial plan should answer:

1. Objective -- what done looks like
2. Constraints -- stack, compatibility, security, time, data, rollout
3. Current state -- what exists today that matters
4. Options -- real alternatives, not fake menu padding
5. Recommendation -- one choice and why
6. Failure modes -- what breaks if the choice is wrong
7. Verification -- tests, checks, metrics, or review gates
8. Out of scope -- what is explicitly not being done
9. Assumptions -- defaults taken because the repo or user did not decide them

## Option quality bar

Good options are:
- materially different: two options qualify only if they touch disjoint file sets or invert a data-ownership boundary. Otherwise it is one option with a parameter -- present it that way.
- realistic in this repo
- compared on cost, blast radius, and maintainability

Bad options are:
- one real option and two straw men
- vague choices with no implementation implications
- options that ignore repo truth

## Implementation-ready standard

A plan is not done until it is clear:

- which files or subsystems change
- which public contracts or interfaces change
- what new invariants appear
- how the work is sequenced
- how success is verified
- how the change is rolled back or contained if it goes bad

If major design decisions still remain after the plan, the plan is not done.

## When to write ADRs or design notes

Write an ADR or design note when:
- the decision constrains future work
- the change introduces a new architecture pattern
- the team could reasonably revisit the same question later
- you are deliberately diverging from an existing standard

ADR format and document templates live in `Core/Documents.md`.

## Anti-patterns

- spike first, rationale later
- vague "implement X" plans with no failure model
- plan longer than the work
- undocumented assumptions
- cargo-cult rollout steps that do not fit the actual change
