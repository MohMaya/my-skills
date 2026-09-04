# Stack/Java.md

Load for Java or Quarkus work.

## Toolchain

- Use Maven.
- Respect the repo's existing formatter, test, and build setup.

## Structure and boundaries

Recommended split:
- `domain/` for entities and value objects
- `service/` for business logic
- `resource/` for HTTP resources
- `repository/` for persistence
- `config/` and `exception/` for framework concerns

Resources stay thin. Services own behavior.

## Types and contracts

- prefer clear domain types over annotation-heavy cleverness
- use interfaces when they create a real seam, not by ritual
- keep DTOs explicit at boundaries

## Error handling

- map domain or application failures to stable HTTP responses deliberately
- do not swallow exceptions
- keep exception mappers honest and specific

## Persistence

- repositories own query logic
- services do not reach around repositories into persistence details

## Testing

- resource and persistence paths: integration tests with real infrastructure when the repo already does that

## Anti-patterns

- annotation piles hiding weak design
- giant services
- resources doing business logic
- generic base classes that exist only to look enterprise

## Pre-commit check

Pre-commit minimum: see `Workflow/Delivery.md`. Additionally:
- exception mapping is explicit for every new failure path
