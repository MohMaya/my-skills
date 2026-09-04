# Product/Architecture.md

Load for product-level architecture doctrine.

## Core posture

- Boring by default: record an ADR for consequential, durable choices of runtime dependencies, datastores, or protocols. Compare actual alternatives; never invent rejected options.
- Keep domain boundaries explicit.
- Prefer additive evolution over rewrites hidden inside feature work.

## Domain boundaries

- services and domains own their data and behavior
- cross-domain access goes through clear contracts
- no reach-through persistence access across boundaries

## Data classes

Keep the system honest about what kind of data it is handling:

- static reference data
- event data
- current state
- sensor or telemetry data
- logs and operational traces

Different classes have different retention, consistency, and query needs. Do not force one storage shape to act like all five.

## Event-sourced or history-sensitive systems

If the product uses event history or versioned entities:
- treat events as immutable
- keep write ordering explicit
- derive current state deliberately
- never hide mutation rules in the UI layer

## Identifiers

- internal identifiers should be stable and machine-friendly
- external identifiers should be safe to expose
- do not overload one identifier for every surface

## Service architecture

- commands and queries can diverge when it earns clarity
- async communication is useful when the domain and failure model justify it
- synchronous APIs still need clear ownership and timeout behavior
- BFF logic belongs in application services, not in presentation

## Runtime posture

Rollback is a first-class design concern: every architecture here must have a contained failure path. Trunk-based branching, feature flags, caching rules, observability, and the deploy baseline are operational -- `Workflow/Delivery.md` owns them.

## Modular repo posture

Shared types belong in shared modules. Feature-internal types stay internal. Do not let convenience collapse the repo into hidden coupling.

## Divergence protocol

If you need to diverge from an architectural standard:

1. document the divergence in an ADR
2. state what changed
3. state blast radius
4. get approval for consequential architectural choices outside the existing authorization
5. set a review date

Never drift silently.
