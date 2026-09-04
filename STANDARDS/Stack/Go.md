# Stack/Go.md

Load for Go work.

## Toolchain

- Use `go mod`.
- Respect the repo's formatter and test commands.

## Types and interfaces

- keep interfaces consumer-side and small
- prefer plain structs and functions

## Structure and boundaries

- domain types stay simple
- services own orchestration
- handlers stay thin
- repositories own database access

## Error handling

- return explicit errors
- wrap only when the extra context helps
- no error-wrapper hierarchies

## Context and concurrency

- pass `context.Context` through request and IO boundaries
- stop goroutines cleanly
- use channels and goroutines because they make the code clearer, not because Go has them

## Testing

- table-driven tests are fine when they help clarity
- integration tests use the real dependencies the repo already uses

## Data access

- keep query ownership obvious
- watch for connection leaks
- prefer boring query structure over clever abstraction

## Anti-patterns

- interface theater
- premature generics
- package sprawl for tiny features
- hidden concurrency

## Pre-commit check

Pre-commit minimum: see `Workflow/Delivery.md`. Additionally:
- `context.Context` flows through every IO boundary touched
- errors are actionable, wrapped only where context helps
