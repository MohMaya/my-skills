# Core/Code.md

Load for any code change, review, or "is this shippable?" question. `shiv-code-gate` loads with it. Skill routing: `Skills/Routing.md`.

## What good looks like

- Smallest diff that solves the real problem.
- Obvious structure over clever structure.
- Types, tests, and contracts carry truth.
- Boundaries stay intact.
- Every line pays rent. A net-negative diff that solves the problem is the best diff.
- Review functions over 40 lines, three nesting levels, or four parameters for clarity. Split only when that improves cohesion. Reuse clear imports and domain types; avoid duplicating definitions to make files self-contained.

## Layer contract

| Layer | Owns | May depend on | Must not depend on |
| ----- | ---- | ------------- | ------------------ |
| Model / domain | Types, validation, domain rules, persistence shape | Inward only | View, UI framework |
| Service / application | Use cases, orchestration, side effects, state mutation | Domain | View |
| View / presentation | Rendering, user input, display formatting | Service contracts, read-only DTOs | Domain mutation, direct IO |

The litmus test is simple: if you swapped the UI surface, would this code still make sense where it lives? If not, move it.

## Tests by layer

| Layer | Test style | Mock |
| ----- | ---------- | ---- |
| Model / domain | Pure unit | Nothing |
| Service / application | Unit | IO edges only |
| View / presentation | UI/component tests | Service seams only |
| HTTP / handler | Integration | Third-party APIs, not the real service logic |

If the repo already has contract-first API workflow, honor it. Update the contract before implementation.

## Test quality bar

The job of a test is to fail when the behavior breaks. Anything that cannot fail for a real reason is dead weight.

Before writing a test, answer: what production bug would this catch? If the only answer is "the function would stop existing," skip it.

Hard bans on tests:

- Mocking a dependency and asserting the mock's own return value. That tests the mock setup, not the code under test.
- Asserting that a function calls another function you just implemented. Implementation tests rot the moment you refactor and prove nothing about behavior.
- String-comparing generated SQL, generated JSON, or generated HTML when the underlying library is what is being exercised. You are testing the library, not your code.
- One-branch tests with no boundary, error, or empty-state coverage. If a single happy-path call is the entire suite for a function, the test is decoration.
- Coverage-padding tests on trivial getters, passthroughs, or wiring code.
- Tests that exist only because the LLM "thought a function should have a test."

What a real test looks like:

- Pure functions: fixed input, asserted output, including edges and failure modes.
- Service code: real or in-memory dependencies where credible, mocks only at true IO seams, assertions on observable outcomes (return value, persisted state, emitted event), not on call sequences.
- Repository / data code: hit a real database (in-memory or test container) when the repo supports it. A repository test against a mocked session is almost always test theater.
- Handlers / endpoints: integration-shaped, asserting status, body, and side effects.

When generated tests come back overgrown, prune first. A smaller suite that fails for real reasons beats a larger suite that fails only when you delete a line.

## Hard bans

- Secrets or credentials in repo
- `any` in strict TypeScript
- Untyped new code in typed Python
- Empty catches, silent swallow, `pass` on real failures
- N+1 queries or unbounded materialization
- Business rules in UI glue
- UI code in domain core
- Pass-through wrappers that add nothing

One implementation means a concrete type. To keep an interface, name the second implementer or the process-boundary test double it exists for; otherwise delete the interface.

## Bloat detector

Use the artifact questions in `Core/Execution.md` when a proposed addition has unclear purpose or ownership.

Speculative scaffolding -- IDs, roles, tables, helpers, hooks added "so we can use them later" -- is the most expensive kind of bloat because it looks responsible. Defer it until a real caller exists.

## Review bar

- Correctness first: behavior, failure modes, data integrity, security.
- Then subtraction: what can be removed before anything is polished.
- Then structure: boundaries, naming, cohesion, deletion over accretion.
- Then tests: enough to prove behavior, not a second implementation.
- Then docs: update only the docs that actually changed meaning or workflow.

## Default comment policy

Default comment count for new code: zero.

Comment only:
- security invariants
- subtle bug traps
- non-obvious constraints from an external system

If you need comments to explain what the code does, the code still needs work.
