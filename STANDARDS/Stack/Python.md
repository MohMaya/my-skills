# Stack/Python.md

Load for Python work.

## Toolchain

- Use `uv` unless the repo already chose otherwise.
- Follow the repo's formatter, linter, and test runner.
- Do not introduce untyped new code in a typed codebase.
- Run analyzers the project does not carry with `uv run --with <tool>`, leaving `pyproject.toml` unchanged.
- In Claude Code and Codex, `stop-gate.py` runs the project's configured ruff, mypy, and basedpyright on changed files at each turn end.

## Skills

Each skill is the Python adapter under the kernel owner named beside it.

| Task | Skill |
| ---- | ----- |
| Requested cleanup or refactor of a codebase | `py-refactor`, which sequences the rest; `code-simplification` owns the method |
| Scanner run or Python-specific security fix | `py-security`, under `security-and-hardening` |
| Coverage gaps or mutation testing | `py-test-quality`; `tdd` owns writing the tests |
| Dead code or duplication | `py-code-health` |
| Complexity hotspots | `py-complexity` |
| Linter and type-checker setup; pre-commit hooks | `py-quality-setup`; `py-git-hooks`, when Shiv asks |
| pip to uv, a raised Python floor, or deprecated APIs | `py-modernize`, on request, planned with `deprecation-and-migration` |

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
