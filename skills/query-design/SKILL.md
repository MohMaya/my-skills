---
name: query-design
description: Intent-first design of SQL and ORM queries, from what the caller needs to a statement proven equivalent and measured. Use before writing or changing any SQL statement or ORM query, and when a query, endpoint, or job is slow: N+1, EXPLAIN plans, indexes, pagination, counts, or pg_stat_statements.
---

# Query design

A query answers a question someone downstream asked. Optimize the question before the SQL: establish the **intent**, justify every element against it, rebuild from the cheapest design that still answers it, then prove **equivalence** and measure. An index on a query nobody needs is waste with a write cost.

## Modes

| Mode | When | Steps |
| --- | --- | --- |
| **write** | A new query, repository method, loader, or relationship | 1–4; 5 against the spec's fixtures; 6 when it sits on a request path or a per-row loop |
| **optimize** | An existing query, endpoint, or job is slow or suspicious | 1–6; step 5 compares old and new |
| **audit** | "What is slow in this service?" | Rank statements by `total_exec_time` in `pg_stat_statements` (and traces when Datadog is wired), then run **optimize** on the top paths in order |

## Safety

- Inspect through a read-only role with `statement_timeout` set, on staging or a branch holding production-shaped data.
- `EXPLAIN ANALYZE` executes the statement. Run DML under `BEGIN … ROLLBACK`, and only off production; rollback leaves sequences advanced and keeps any external side effect a trigger caused.
- On production, plain `EXPLAIN` plus catalog and statistics views are the default; anything heavier needs Shiv's approval.
- Indexes and schema changes ship as migrations, which the kernel requires confirming first.

## 1. Intent

Write an **intent card** before studying the SQL:

- **Question**: one sentence in domain terms ("does this system have an active membership?").
- **Callers**: every call site of the public entry points (when several share one private query core, list each entry point and name the shared core), each with its frequency (per request, per list row, per job batch, per keystroke). Take frequency from telemetry when it exists; otherwise derive it from the code path and mark it inferred.
- **Consumption**: for each caller, the fields actually read, traced through the serializer, DTO, GraphQL type and field resolvers, or template, and on to the client documents that select them when the client lives in a reachable repository (alpha-web's GraphQL documents for alpha-core). The client's selection is the real consumer.
- **Shape**: the answer's cardinality (yes/no, one row, a bounded page, the full set), the ordering a consumer relies on, the pagination contract.
- **Envelope**: tenant or organization scope, the database role and its grants, lifecycle predicates (`removed_at`, `deleted_at`), time zones and bound inclusivity, tolerated staleness, read-your-writes needs, locks.

When consumers disagree or the question itself looks wrong, ask Shiv one question with a recommended answer (`grilling`); intent is a product decision.

**Done when** every returned column maps to a named consumer or is marked unused, and every caller is listed with its frequency.

## 2. Evidence

Read the system, not the code's beliefs about it. Commands and their safety labels are in [references/postgres.md](references/postgres.md); ORM capture is in [references/sqlalchemy.md](references/sqlalchemy.md).

- **Generated SQL**: the exact statements the ORM emits and how many per call, including those fired from resolvers, serializers, and per-field loaders. Capture them by running the repository's existing test for the path with statement logging on; compiling by hand fails when building the statement needs a session or auth context.
- **Schema**: `\d+` for every table touched: keys, uniqueness, foreign keys and their nullability, checks, indexes (partial, expression), triggers, RLS policies, hypertable status. Without a database, read the repository's own index and schema docs first, then confirm against the ORM models and migrations, grepping migrations for raw `CREATE INDEX` and `op.execute` since those never appear on the models.
- **Data shape**: row counts, `pg_stats` null fraction and distinct counts on filter and join columns, and the real fan-out of each join (max and p95 children per parent).
- **Workload**: calls, total and mean time, and rows per call from `pg_stat_statements`.
- **Plan**: `EXPLAIN (ANALYZE, BUFFERS)` on production-shaped data, as the service's role, with the worst realistic parameters (largest tenant, deepest page).

**Done when** you hold the generated SQL, a plan, and row counts and fan-outs for every table touched, or have written down each one you could not get and why.

Without database access, ask Shiv for a read-only connection and continue on **static** evidence meanwhile: schema from docs, models, and migrations; fan-out bounded by constraints. Static conclusions carry the label through steps 3–6, and step 4 cannot choose between shapes until a plan exists.

## 3. Necessity

Give every element of the statement a written verdict (keep, drop, change, or unverified when only a plan can decide) with its reason:

- **Column** → which consumer reads it?
- **Join** → does it supply a read column, a filter, or a row multiplication the intent wants? Filter-only joins become `EXISTS`. A `LEFT JOIN` contributing no column to the result is removable when a unique key guarantees at most one match. A join followed by `DISTINCT` or `GROUP BY` to collapse its own duplicates is the defect.
- **Filter** → does a constraint already guarantee it? Is it sargable (bare column, matching type)?
- **Aggregation** → needed at this grain? Would existence, a capped count, or an estimate answer the question?
- **Sort** → does a consumer depend on it? Does paging have a unique tie-breaker?
- **Eager load, relationship, or per-field loader** → does a consumer read what it fetches? A loader that pulls whole rows for one field, or runs when the client never selects its field, is dead weight.
- **Subquery or CTE** → evaluated once, or once per outer row?
- **The query itself** → is the answer already in memory, in the request context, in another query on the same path, or implied by a constraint?

**Done when** every column, join, filter, aggregate, sort, load, and subquery has a verdict.

## 4. Redesign

Climb the ladder and stop at the first rung that answers the intent:

1. **Remove** the query, or the elements step 3 dropped.
2. **Combine** N+1 and repeated reads into one set-based read: `= ANY(array)`, `selectinload`, a DataLoader.
3. **Bound** the work: `EXISTS` for presence, `LIMIT`, keyset pagination, narrow column lists.
4. **Move** the work to write time (a state row, a counter, a continuous aggregate) or off the request path, when the envelope's staleness allows.
5. **Cheapen** the shape (aggregate before joining, `LATERAL` top-N, `DISTINCT ON`), then index for the access path.
6. **Cache**, with its invalidation rule written, then capacity: last.

In **optimize**, design it twice: carry at least two candidate shapes into `EXPLAIN` and choose on measured difference. State every index's write-side cost (write amplification, lost HOT updates, size). When a rewrite touches a new table, give every role that runs it the grants the repository requires.

When the cheapest correct design changes a contract (API shape, staleness, pagination), state the objection once with a recommendation and follow Shiv's call.

**Done when** the chosen design and each rejected alternative have a plan, and the choice cites the measured difference.

## 5. Equivalence

Prove the new statement answers the same question, or name each intended difference. Diff both directions with multiset semantics on production-shaped data:

```sql
WITH old AS (/* original */), new AS (/* rewrite */)
SELECT 'missing' AS side, * FROM (SELECT * FROM old EXCEPT ALL SELECT * FROM new) m
UNION ALL
SELECT 'extra', * FROM (SELECT * FROM new EXCEPT ALL SELECT * FROM old) e;
```

Run it for several parameter sets: the largest tenant, an empty one, and rows that hit each edge below. When order is part of the contract, compare `row_number() OVER (ORDER BY …)` alongside the columns.

Edge semantics, each covered by a fixture or test:

- **NULLs** in join keys, filters, `NOT IN` subqueries, and aggregates (`count(col)` versus `count(*)`, `sum` over no rows).
- **Duplicates**: JOIN→EXISTS collapses repeated parents; `UNION` versus `UNION ALL`; `DISTINCT`.
- **Empty children**: `LEFT` versus `INNER`; aggregates over no rows.
- **Order**: deterministic ties; page boundaries stable under concurrent inserts.
- **Scope**: tenant, role, RLS, and lifecycle predicates intact.
- **Time**: zone, truncation, inclusive and exclusive bounds.
- **Concurrency**: isolation level, row locks, advisory locks intact.

Lock it in with tests that assert results on fixtures holding those edge rows, plus a query-count assertion for the path; counts catch regressions without timing flakes. Use the repository's real-database tests when it has them.

**Done when** the diff returns zero rows on every parameter set and each edge has a passing test or a written reason it cannot occur.

## 6. Measure

Compare old and new on the same data, parameters, and cache state. Before measuring, write the **falsifier**: the observation that would show the change failed ("shared buffers stay above 10k, so the index is unused").

- `EXPLAIN (ANALYZE, BUFFERS)`: median of at least five warm runs; record execution time, shared hit and read, rows.
- Statements per request or job.
- A `pg_stat_statements` delta under representative load, when available.

**Done when** a before/after table holds numbers you observed and the falsifier stayed silent.

## Report

Open with what the query is for and what changed. Then: what was removed and why, the before/after table, the equivalence evidence, residual risks. Keep verified, inferred, and not checked (no production-shaped data, no database access) in separate lists.

## Tools

- [references/postgres.md](references/postgres.md): diagnostics with safety labels, plan reading, index design, query shapes, TimescaleDB, pooling.
- [references/sqlalchemy.md](references/sqlalchemy.md): SQLAlchemy 2.0 async, psycopg, asyncpg, Alembic.
- Tiger MCP `search_docs` (source `postgres_<major>`) for the manual matching the server's version.
- `postgres-mcp`, when configured for the project: hypothetical indexes, workload index advice, database health.
