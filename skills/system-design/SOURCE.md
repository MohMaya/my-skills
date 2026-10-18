# Sources

Written for this repository on 2026-10-18. Ideas adapted, with rules rewritten rather than copied, from skills imported in commit `40c5f7c`:

- [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) (MIT, per the `license` field on disk):
  - `architecture-designer`: the NFR categories, kept as the targets table in step 2.
  - `microservices-architect`: the split-benefit checklist (independent scaling, separate teams, failure isolation, deploy cadence), kept in step 5, and the event-versioning idea, kept in step 7.
  - `cloud-architect`, `legacy-modernizer`: read; nothing kept. Restore drills belong to `operability`.
- [wshobson/agents](https://github.com/wshobson/agents) (MIT upstream; the imported `architecture-patterns` and `microservices-patterns` carry no license field on disk): read; nothing kept. Their layer-per-abstraction and database-per-service rules conflict with the monolith-first default.

Not carried over: microservices-first, database-per-service as non-negotiable, abstract interfaces at every layer, hand-rolled sagas, the 116-line ADR template, two-phase commit, `hash % N` sharding, MongoDB for changing schemas, multi-region by default.

Temporal facts (durable execution, timers, one running execution per Workflow ID, the 10,240-event warning and 51,200-event termination limits, Continue-As-New, plain-text Workflow IDs) were checked against docs.temporal.io on 2026-10-18. The step order, the capacity-before-topology rule, and the monolith default are this repository's own.
