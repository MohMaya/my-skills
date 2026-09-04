# Stack/TypeScript.md

Load for TypeScript, React, and Next.js work.

## Toolchain

- Respect the existing formatter, linter, test runner, and package manager.

## Types and contracts

- Prefer concrete types over clever generic scaffolding.
- Avoid `any`.
- Use generated API types if the repo is contract-led.
- Flatten types when a flat type is clearer than a nested alias web.

## Structure and boundaries

- Models: types, schemas, validation.
- Services: business logic, API clients, orchestration.
- Components: presentation only.
- Hooks: bridge between services and views, not a second home for business logic.

In Next.js:
- keep server and client boundaries explicit
- route handlers stay thin
- BFF logic belongs in services, not in components

## Error handling

- represent expected failures clearly
- do not bury failure inside broad catches
- surface actionable messages to the caller

## Testing

- keep component tests about rendering and interaction
- keep service tests about logic and side effects

## Performance and accessibility

- avoid avoidable client work
- watch bundle shape and render waterfalls
- use semantic HTML and accessible interactions by default

## Anti-patterns

- type theater
- boolean-prop explosion
- hook ceremony
- API calls inside presentation components
- state management bloat for local state

## Pre-commit check

Pre-commit minimum: see `Workflow/Delivery.md`. Additionally:
- no new `any`
- no unnecessary client component promotion
