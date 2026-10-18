---
name: system-design
description: Build-time design of a service, data flow, or feature before any code. Use when designing a new service or system; when a feature adds a datastore, queue, workflow, or external dependency; when choosing between architectures (monolith or services, sync or async, which store); and for capacity or scale planning. The `planner` agent runs it before writing a plan.
---

# System design

Fix the numbers, the state machines, and the failure answers on paper while changing them costs a paragraph. The default is one modular monolith on one Postgres; every departure names the figure that forced it.

**Dvandva.** Run `dvandva` before you produce a design.

Open the design with its crux in two sentences (what we want), then one section per step. Pointers: `grilling` pins open decisions with Shiv, `domain-modeling` owns terms and ADR format, `codebase-design` owns module seams, `postgres` owns schema and queries, `api-design` owns wire contracts, `security` owns auth, `operability` owns SLOs and alerts, `bar-raiser` reviews the result.

## Proportion

| Target | Steps |
| --- | --- |
| A feature on existing stores, with no new dependency | 1, 2 (the rows it moves), 4 when it adds states, 7 for new calls, 8 |
| A feature that adds a datastore, queue, workflow, or external dependency | All |
| A new service or system | All; step 3 in writing, with a load-test plan |

## 1. Mandate

Write who it serves, the job it does, how we will know it worked (a number or an observable), and what is out of scope. When any is missing, run `grilling` with Shiv; no later step starts on a guessed mandate.

**Done when** all four are written, and the success signal names its metric.

## 2. Targets

Fill one row per user-facing operation or data flow:

| Target | Value | Basis |
| --- | --- | --- |
| p95 and p99 latency | | given, or assumed |
| Availability | | |
| RPO and RTO | | |
| Peak RPS, and peak-to-average ratio | | |
| Data volume now, and growth per month | | |
| Staleness tolerated; read-your-writes needed | | |

Write `assumed: <value>, because <reason>` for every number nobody has given; an invented number reads as a requirement. Take each assumption to Shiv as one question with your lean when it would change the design.

**Done when** every cell holds a value and a basis, and each assumed cell names who can confirm it.

## 3. Capacity

Estimate the hottest path, slowest resource first: network, then disk, memory, CPU. Per operation write queries, rows, bytes, and round trips, and price each hop against [the Numbers table](../bar-raiser/references/catalogue.md#numbers). Concurrency in flight is peak RPS times latency; size connection pools from it, and price the total against the database's `max_connections`.

One Postgres and one app process family (web and worker from one codebase) is the default. Leave it only when a figure exceeds it: name the resource, the figure, and the limit. Spend the cheaper levers first, in order: query and index shape (`postgres`), a bigger machine, read replicas, then a split.

**Done when** each hop on the hot path carries a priced number marked enforced (by a constraint, a limit, an algorithm) or assumed, and the default is kept or broken by a named figure.

## 4. Entities and state machines

For each entity, write its states (an enum or discriminated union), one transition table (from, event, to, guard), its terminal states, and the single owner of each transition. The database holds what it can: a `CHECK` on the state column, constraints for one-active-per-parent (`postgres`).

Reason from what Temporal is for: durable execution, with timers recorded in its history and at most one running execution per Workflow ID. A timer, a wait on an outside event, or a multi-step flow that must survive a crash or deploy becomes one workflow per entity, with the entity's ID as the Workflow ID (never PII; IDs are stored in plain text). Activities carry the side effects and take idempotency keys. A workflow's history is capped (a warning at 10,240 events, termination at 51,200), so a long-lived entity loop ends in Continue-As-New. A hand-rolled saga, a status table with a sweeper job, or a cron that scans every row for "due" work is the smell this replaces. A change that fits inside one entity's single transaction stays a Postgres transaction; Temporal earns its operating cost only when time or crashes sit inside the flow.

**Done when** every entity has its transition table, and every timer, wait, and multi-step flow is assigned to a workflow or to one transaction, with the reason.

## 5. Topology

- **Services.** A split names the benefit it buys (independent scaling by a step-3 figure, a separate owning team, isolation of a named failure, a deploy cadence that differs) and the cost it adds: a priced network hop and a failure mode. Without a named benefit, stay in the monolith, with module boundaries enforced by an import rule.
- **Datastores.** A second store names the access pattern Postgres cannot serve at the step-3 numbers. Each table has one writing module.
- **Cross-entity change.** Atomicity lives inside one entity. Across entities, use a transactional outbox and idempotent consumers, with a dedupe key recorded atomically with the effect (catalogue entries: dual write, outbox without idempotent consumers, cross-entity atomicity assumed).

**Done when** each boundary lists its benefit and cost, each datastore its access pattern, and each cross-entity change its atomicity path.

## 6. Design it twice

A choice forks when reversing it costs a migration or a quarter: topology, store, sync or async, workflow or transaction, data ownership. For each, write two materially different designs, score both against the step 2 and 3 numbers, and name the number that decides. For module interfaces inside the design, follow `codebase-design`'s DESIGN-IT-TWICE.

**Done when** every fork shows two designs, the deciding number, and the reason the loser lost.

## 7. Failure and change

For every external call, including Temporal, a queue, and each datastore beyond Postgres, answer `bar-raiser`'s five questions: times out, succeeds with the reply lost, runs twice, arrives out of order, runs concurrently with itself. Name the kill switch: the flag that disables the call or its feature, flippable without a deploy, and the degraded behaviour while it is off.

Every message, event, and workflow input carries a version field. Consumers accept version N and N-1 and ignore unknown fields; deploy consumers before producers. In-flight workflow executions replay on old definitions, so the version covers them too.

**Done when** each external call has five answers and a kill switch, and each schema names its version field and the N-1 rule.

## 8. Record and hand off

Write an ADR for each choice that is hard to reverse, surprising without context, and a real trade-off, in the format `domain-modeling` defines. Hand `bar-raiser` the filled Map: job (step 1), invariants stated as absences (steps 4 and 5), the data path with its numbers (step 3), and the effects (step 7).

**Done when** the Map has all four items and each qualifying choice has an ADR.
