# Catalogue

Each entry pairs a smell, as it shows in code, with the design that replaces it. Tags in parentheses name the source in [canon.md](canon.md); `[pe]` marks established practice without a single source. The kernel's own rules (complexity limit, fail loudly, no speculative seams) apply on top.

## Numbers

Price every hop before judging a design. Orders of magnitude:

| Operation | Cost |
| --- | --- |
| Main memory reference | 100 ns |
| Local NVMe random read | 50–150 µs |
| Network block storage (EBS) read | ~250 µs, capped by provisioned IOPS (gp3 default 3,000) |
| Round trip within a datacenter | 500 µs |
| Postgres query over the network, indexed | ~1 ms |
| Cross-region round trip | 50–150 ms |
| Process context switch / thread switch | ~5 µs / ~1 µs |

(Dean, Dicken-io, Dicken-threads)

## Architecture and boundaries

- **Shallow module**: an interface as complex as its body, or a wrapper that only forwards. → Merge it into its caller or pull more of the decision inside it; apply the `codebase-design` deletion test. (Ousterhout)
- **Leaked decision**: one decision (a status set, a retry policy, a wire format, a pricing rule) spelled out in several modules. → One owner; everyone else asks it. (Ousterhout)
- **Pass-through layers**: controller → service → repository each renaming the same fields and hiding nothing. → Collapse to the layers that each own a decision. (Ousterhout)
- **Temporal decomposition**: modules split by the order things happen (read, process, write) so each carries the same knowledge. → Split by the information each module hides. (Ousterhout)
- **Junk-drawer module** (`utils`, `common`, `helpers`) or import cycles. → Move each function to its one real owner; break cycles by inverting the dependency. `[pe]`
- **Business logic in handlers, components, or hooks.** → A service with an IO-free core, called by thin adapters. (matklad-test)
- **Distributed monolith**: services that deploy together, share tables, or call each other in synchronous chains. → A modular monolith, or real entity boundaries talking through asynchronous, idempotent messages. (Helland, Nygard)
- **Service split with no named benefit**: a new service whose reason is none of independent scaling, a separate team, failure isolation, or deploy cadence. → A module in the modular monolith until one of the four is named and measured. (Fowler-monolith)
- **Unversioned message schema**: a published event or message with no version, or a consumer that rejects the previous version. → Versioned schemas; consumers accept N-1 and ignore unknown fields. (Kleppmann-schema)
- **Per-entity timers, waits, or multi-step flows hand-rolled** as polling sweeps over rows or saga tables. → One durable workflow per entity. (kernel, Temporal)
- **Dual write**: commit to the database, then publish to a queue or a second store. → Transactional outbox or change data capture. (Kleppmann, outbox)
- **Outbox without idempotent consumers**: the relay can deliver twice and the consumer applies twice. → A dedupe key per message, recorded atomically with its effect. (outbox, Helland)
- **Cross-entity atomicity assumed**: one request updating several aggregates or services as if in one transaction. → Atomicity inside one entity; a workflow of idempotent steps with recorded intents and compensations across entities. (Helland, Brandur-idem)
- **Derived copy updated in-request** (cache, search index, counter) with no reconciliation. → Derive it from the log of changes, with staleness made explicit and a rebuild path. (Helland, Kleppmann)
- **Invisible boundary**: layering that exists only in someone's head. → An architecture document with a codemap and the invariants stated as absences, enforced by an import lint or test. (matklad-arch)
- **Configuration as an unreviewed control surface**: flags and config changed live without staging. → Config reviewed, staged, and rolled out like code. (Luu-postmortem)
- **A wire contract decided in code** (an error shape, a pagination scheme, a version, a retry header chosen ad hoc per handler). → The contract designed through `api-design`; its rules count here.
- **An auth path, secret, or untrusted input changed without the security walk.** → `security`'s checklist sections the diff touches; its findings count here.

## Data and persistence

- **Random primary keys on a B-tree** (UUIDv4): scattered inserts, half-empty pages, every secondary index carrying the wide key. → `bigint` identity, or UUIDv7/ULID when global uniqueness is needed. (Dicken-uuid, Dicken-btree)
- **Wide key stored as text** (UUID in `CHAR(36)`). → The native `uuid` type or 16 bytes. (Dicken-uuid)
- **Invariant held only in application code**: uniqueness, non-null, ranges, references, one-active-per-parent. → `NOT NULL`, `CHECK`, `UNIQUE` (partial when scoped), foreign keys, exclusion constraints. A second writer or a race cannot bypass the database. `[pe]`
- **Check-then-act race**: select to see if it exists, then insert or update. → A constraint plus `INSERT … ON CONFLICT`, or one conditional `UPDATE … WHERE`. `[pe]`
- **Read-modify-write without concurrency control.** → A version column (optimistic) or `SELECT … FOR UPDATE`, or a single atomic statement. `[pe]`
- **N+1 or unbounded reads, missing or misordered indexes, offset pagination at depth.** → `postgres`. (TigerStyle: put a limit on everything)
- **A parent/page bound presented as a bound on joined children or history.** → State the output grain and prove each fan-out bound from constraints or query shape; exercise a parent with a large valid history. (`postgres`, TigerStyle)
- **Transaction held across a network call** (HTTP, LLM, queue, user wait): holds locks and the snapshot, stalls vacuum, and couples the database to someone else's latency. → Atomic phases between foreign calls, with recovery points. (Brandur-idem, Brandur-queues)
- **Table-as-queue without care**: long transactions, no `SKIP LOCKED`, no watch on transaction age. → `FOR UPDATE SKIP LOCKED`, short transactions, alerts on oldest transaction age. (Brandur-queues)
- **Breaking migration**: a schema change the previous app version cannot run against, or a non-resumable backfill. → Expand, backfill in resumable batches, switch reads, contract in a later release. `[pe]`
- **No connection pool, or a pool sized by hope.** → A pooler holding a small fixed set of server connections; total connections priced against `max_connections`. (Dicken-threads)
- **Shard key chosen ad hoc, or sharding before replicas and vertical splits.** → Escalate in order, and pick the key from the dominant access pattern. (Dicken-shard)

## Reliability

- **Network call without a timeout.** → A timeout on every call, derived from the caller's deadline. (Nygard, SRE-cascade)
- **Fresh timeouts at every hop.** → One deadline propagated end to end. (SRE-cascade)
- **Retries without jitter.** → Capped exponential backoff with full jitter. (Brooker-jitter)
- **Retries without a budget, or at several layers.** → Retry at one layer, under a per-process budget. (SRE-overload, Brooker-metastable)
- **Retrying a non-transient error** (validation, auth, any other 4xx, a bug). → Retry only timeouts, connection errors, 429, 502, 503, and 504, honouring `Retry-After`; surface everything else. (AWS-retries)
- **Retrying a non-idempotent effect.** → An idempotency key stored with the result, so a retry returns the first outcome. (Brandur-idem)
- **Unbounded queue, buffer, batch, or fan-out.** → A bound on each, rejecting or shedding when full. (TigerStyle, SRE-overload)
- **No backpressure or load shedding.** → Bounded concurrency; reject early with an explicit "overloaded, retry later". (SRE-overload)
- **A sustaining loop**: retries, cache misses, or queue growth that keep the system down after the trigger passes. → Name the loop and cap it (budgets, breakers, shedding). (Brooker-metastable)
- **One pool shared by unrelated dependencies.** → Bulkheads: a pool per dependency. (Nygard)
- **One tenant able to exhaust a shared pool, queue, or rate.** → A per-tenant quota that rejects the excess. (AWS-fairness)
- **Liveness probe that checks a dependency, or readiness probe that checks downstream services** beyond the service's own hard dependencies. → Liveness checks the process; readiness checks its own hard dependencies. A shared outage must not restart or de-register the fleet. (AWS-health)
- **Async consumer with no dead-letter destination, or a DLQ with no depth or age alarm.** → A DLQ per queue, with an alarm on its depth and oldest-message age. (SQS-DLQ)
- **Batch consumer that fails the whole batch on one bad record.** → Report partial failures per record, so only the failed ones are redelivered. (Lambda-SQS)
- **Lease or visibility timeout shorter than worst-case processing.** → A timeout above the maximum processing time including retries, or a heartbeat that extends it. (SQS-visibility)
- **Slow work inside the request cycle** (export, report, third-party sync). → Accept, return a job id, and expose a status the caller can poll. (Azure-async)
- **A backup never restored.** → A scheduled restore drill that validates the data and measures the actual RTO and RPO. (AWS-restore)
- **Works only with a warm cache.** → Capacity for a cold start, and a ramped warm-up. (SRE-cascade)
- **Risky change without a kill switch, canary, or rollback.** → A flag and a staged rollout. `[pe]`
- **A human step as the only safeguard.** → Automate the guard. (Luu-postmortem)
- **Never loaded to failure.** → Know the breaking point before launch. (SRE-cascade)

## Performance

- **Design with no numbers.** → A back-of-envelope estimate of network, disk, memory, and CPU, slowest first, written before the code. (TigerStyle)
- **Chatty IO**: a call per item inside a loop. → Batch at the boundary; push loops down into the callee. (matklad-ifs)
- **Network disk assumed to behave like local disk.** → Storage chosen from working-set size and required IOPS. (Dicken-io)
- **Quadratic work hidden in nested loops or repeated linear lookups.** → A set or map, or sort once. `[pe]`
- **Allocation or dynamic dispatch in a measured hot loop.** → Table-driven or batched data layouts, applied only where measurement shows the loop is hot. (Muratori)
- **A performance claim without method.** → Fixed hardware, repetitions, warm-up, and stated limits, or it is an anecdote. (Dicken-bench)
- **Downstream cleanup used to justify removing an upstream bound**: application sets, filters, sorts, or slices preserve the answer after excess rows or bytes have already crossed a boundary. → Prove result semantics and end-to-end resource cost separately; measure at the boundary where the work occurs. Fewer operators or lines do not prove less work. (`postgres`, Dicken-bench)

## Code design

- **Wrong abstraction**: a shared function accreting flags and branches as callers diverge. → Inline it back into each caller, delete what each does not need, re-extract only what is truly common. (Metz)
- **Boolean or option-bag parameters switching behavior.** → Separate functions, or a discriminated union. `[pe]`
- **Stringly typed domain**: statuses, IDs of different entities, money, and times as bare strings or numbers. → Domain types parsed once at the boundary. (King)
- **Validation that returns nothing**, leaving data in its weak type. → A parser that returns a stronger type. (King)
- **Shotgun parsing**: checks scattered through processing. → Parse everything up front, then process trusted types. (King)
- **Hand-rolled check beside an existing parser** for the same value (an ID, email, money amount). → Reuse the codebase's parser; search for one by the value's type and format before accepting a new check. (King)
- **Illegal states representable**: two nullable fields where exactly one must be set, flags that contradict. → A tagged union or a state machine. (King)
- **Swallowed error**: empty catch, catch-and-log, ignored return codes. Mishandled errors are behind most catastrophic failures. → Handle it or fail loudly with a specific message. (Luu-testing)
- **Error logged at several layers** (log, rethrow, log again up the stack). → Log once, where it is handled. `[pe]`
- **Wrapped error that drops its cause** (`raise New()` inside `except`, `%v` in `fmt.Errorf`, `new Error(msg)` in a catch). → Keep the cause chain: `raise … from err`, `%w`, `{ cause: err }`. (Go-errors)
- **Expected failures thrown as exceptions** (not found, invalid input, insufficient funds). → Typed results for expected outcomes; exceptions for bugs. (Wlaschin)
- **`forEach(async …)` or an unawaited async call in a loop** whose result matters. → `for…of` with `await`, or `Promise.all`. (typescript-eslint)
- **Event handler whose write re-fires its own trigger** (database trigger, webhook, change listener). → A re-entrancy guard, or a write that is a no-op when the value is unchanged. `[pe]`
- **Global mutable state or singletons.** → Values passed explicitly; dependencies injected. (Hickey)
- **Temporal coupling**: methods that must be called in a fixed order. → One operation, or types that make the wrong order unrepresentable. (Ousterhout)
- **Branching mixed with work deep in the call tree.** → Decisions in the parent, straight-line leaves. (TigerStyle, matklad-ifs)
- **A name that is hard to choose.** → Treat it as a design signal: the thing likely does two jobs. (Ousterhout)
- **Unasserted invariant at a boundary or state transition.** → An assertion on both sides of the boundary, covering what must not happen as well as what must. (TigerStyle)

## Operability

- **Free-text logs without request context.** → One wide structured event per request per service, built up through the request and emitted once. (Majors)
- **Unbounded-cardinality metric labels.** → High-cardinality fields on events, not metrics. (Majors)
- **No trace or request id across async hops.** → Propagate it through every queue and job, and put it on every event. `[pe]`
- **A named failure mode with no SLO, alert, or runbook.** → An alert per failure mode and per sustaining loop, each with a runbook; `operability` owns the design. (Luu-postmortem)
- **Production code without its logs, metrics, and error tracking.** → They ship in the same change (kernel).

## Testing

- **Mock-heavy tests asserting calls.** → Observable outcomes through the public interface, with a real or in-memory database. (matklad-test)
- **No failure-path tests.** → A test per error branch, timeout, and retry; simple tests catch most catastrophic failures. (Luu-testing)
- **Logic entangled with IO, making tests slow.** → An IO-free core tested directly. (matklad-test)
- **Tests and types as the only argument for correctness.** → A design simple enough to reason about; tests confirm it. (Hickey)

## Evolution

- **Big-bang rewrite.** → Strangle one boundary at a time; replace a bad data model or boundary as its own migration. (Spolsky)
- **Behavior change to untested legacy code.** → Characterization tests pinning current behavior land first, in their own commit. (Feathers)
- **Cutover without a numeric rollback trigger, an owner, and a ramp.** → Write all three: the metric and threshold that roll back, one named owner, and steps such as 1/5/25/50/100%. (AWS-deploy)
- **Traffic flipped to the new path without comparing.** → A shadow run: return the old result, compute the new, and compare. (Scientist)
- **Legacy path, flag, or adapter with no deletion date.** → A dated deletion, ticketed with the cutover. (Fowler-strangler)
- **Speculative generality**: a seam, plugin point, or option with one real case. → Delete it until the second case exists. (Pocock, kernel)
- **Tidying mixed into a behavior change.** → Separate commits. (Beck)
- **A review verdict reused after simplification edits, or prior approval treated as proof.** → Reopen the affected claims and verify the final diff; challenge the reviewer's own rationale with a counterexample. `[pe]`
- **Tactical patching**: "clean it up later," repeated. → Spend design effort on every change; the debt compounds. (Ousterhout)

## Delivery

- **Production image not pinned by digest or version, running as root, or with `.env` in the build context.** → A pinned base, a non-root `USER`, and a `.dockerignore`. (Docker-bp)
- **Infrastructure plan that destroys or replaces a data-holding resource** (database, bucket, volume, queue). → Explicit acceptance before apply, and deletion protection on the resource. (Terraform-lifecycle)
- **Deploy with no post-deploy check of error rate and latency.** → An automated check after each stage that rolls back on breach. (AWS-deploy)
- **Deploy PR without the rollback command.** → The command and how to verify it worked, written before the deploy. `[pe]`
