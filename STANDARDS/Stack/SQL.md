# Stack/SQL.md

Load for schema design, migrations, queries, and database tuning.

## Schema design

- name things clearly
- use the simplest type that preserves truth
- add constraints that encode invariants
- prefer explicit foreign keys and indexes where the workload needs them

## Query patterns

- write for correctness first
- batch reads and writes when the workload warrants it
- keep joins readable

## Performance

- index based on real query shape
- validate with explain plans when performance matters
- materialize only what the caller needs

## Migrations

- backward compatibility with the running app version is required (`Workflow/Delivery.md`)
- split risky migrations into multiple deploy-safe steps

## Security

- parameterize queries
- do not interpolate untrusted input
- classify sensitive columns and treat them accordingly

## Anti-patterns

- query spaghetti
- premature micro-optimization
- over-normalization that makes the common path miserable
- hidden data copies with unclear ownership

## Pre-commit check

Pre-commit minimum: see `Workflow/Delivery.md`. Additionally:
- indexes support the real access pattern, checked against an explain plan
- no interpolated untrusted input
