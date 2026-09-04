# Stack/Python.md

Load for Python work.

## Toolchain

- Use `uv` unless the repo already chose otherwise.
- Follow the repo's formatter, linter, and test runner.
- Do not introduce untyped new code in a typed codebase.

## Types and contracts

- Prefer explicit type hints.
- Use `pydantic` or dataclasses when the repo already models data that way.
- Keep interfaces light. Python does not need class ceremony for simple seams.

## Structure and boundaries

- Domain and schemas stay framework-light.
- Services own orchestration and side effects.
- Handlers or routes stay thin.
- Repositories own data access, not business rules.

## Error handling

- fail loudly and specifically
- do not use empty `except`
- wrap external failures only when the wrapper adds meaning

## Async and IO

- use async where the stack is already async
- do not mix sync and async carelessly
- keep blocking IO off the async path

## Testing

- integration tests with a real database when the repo supports them

## Data access

- batch queries when needed
- keep migration safety in mind for persistent changes

## Anti-patterns

- abstract base classes for one implementation
- decorators that hide core control flow
- classes where a plain function or schema is enough
- silent failure or catch-and-log-only behavior

## Pre-commit check

Pre-commit minimum: see `Workflow/Delivery.md`. Additionally:
- no bare or catch-and-log-only `except` on a changed path
