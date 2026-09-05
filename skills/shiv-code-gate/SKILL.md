---
name: shiv-code-gate
description: Choose the smallest maintainable code change using the repository's reuse-first ladder and a subtractive diff review.
---

# Code gate

Apply this ladder to the requested behavior. Stop at the first sufficient option.

1. Remove speculative work that has no current caller or requirement.
2. Reuse an existing repository symbol or pattern.
3. Reshape existing code when that makes the requested change smaller.
4. Use the standard library.
5. Use a native platform capability.
6. Use an already-installed dependency.
7. Write the minimum new code needed.

Search the relevant implementation and callers before introducing a sibling abstraction. Expand the search when the initial evidence is insufficient.

For unfamiliar APIs or behavior, verify against primary documentation and the installed version. Existing repository evidence can settle familiar cases.

## Structure Note

Before a non-trivial code change, briefly state:

- The reuse candidates and the chosen approach.
- The files or interfaces that change and why.
- Any preparatory refactor and its separate commit.
- The expected diff size and verification.

Keep the note proportional to the decision. A small, direct edit needs only `gate: trivial`; no public interface or architectural choice should be hidden by that label.

## Design constraints

Preserve validation at trust boundaries, data-loss prevention, security, accessibility, and explicit user requirements.

Add an abstraction or configuration option when a real caller needs it. Prefer invariants enforced by types, construction, or database constraints over repeated caller checks.

A preparatory refactor is in scope when it reduces the feature diff. Commit it separately before the behavior change. Ship standalone deletions as their own change.

## Verification and subtraction

Use checks that exercise the changed behavior or its important invariants. Follow repository-required checks. Avoid tests that merely restate implementation details.

Before commit or PR, use `simplify` if available or reapply the ladder to the diff. Remove duplication and unnecessary scaffolding. Retain necessary error handling.

Report verification and line counts as `+N/-M` in the commit or PR. Completion and authorization follow the kernel and the user's request.
