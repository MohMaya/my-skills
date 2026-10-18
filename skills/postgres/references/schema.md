# Schema reference

Consult from `postgres` in **schema** mode. The `bar-raiser` catalogue's "Data and persistence" section holds the review findings (random keys, wide keys, app-only invariants, check-then-act, breaking migrations); this file is the construction procedure and the PostgreSQL-specific rules behind them. Changes to an existing schema ship through [migrations.md](migrations.md).

## Steps

1. **Access paths.** From the intent card (SKILL step 1), list per table: tenant scope, lifecycle states, and the two or three reads and writes that dominate, each with frequency. **Done when** every table carries those three.
2. **Types and keys.** Choose each column's type and the key by the rules below. **Done when** every column's type follows a rule or has a written reason.
3. **Invariants.** Every statement the business makes about a row, or between rows, becomes a constraint. **Done when** each is a constraint, or its reason for living elsewhere is written (a cross-row rule `CHECK` cannot hold).
4. **Indexes.** Derive them from the access paths with Index design in [postgres.md](postgres.md), including the foreign-key verdict. **Done when** each access path has an index or a written reason it needs none.
5. **Prove.** One test per constraint that attempts the violating write and expects rejection; `EXPLAIN` each access path on production-shaped row counts. **Done when** every constraint has its rejection test and every path has a plan.

## Types and keys

- **Surrogate key**: `bigint GENERATED ALWAYS AS IDENTITY`. `ALWAYS` rejects client-supplied values unless the insert says `OVERRIDING SYSTEM VALUE`. A 32-bit key ends at 2,147,483,647, and sequences leave gaps after rollbacks, so never promise gapless numbers.
- **Global or client-generated ids**: the `uuid` type, never text. `uuidv7()` (PG18) is time-ordered, which avoids the scattered-insert cost the catalogue names for random keys, and embeds a millisecond creation timestamp, so use it where leaking creation time is harmless. `gen_random_uuid()` (v4, random) fits a token column that must carry no order; as a primary key it brings the random-key cost. Both are built in, so `uuid-ossp` has no job here.
- **Instants**: `timestamptz`, stored as UTC and shown in the session `TimeZone`. `timestamp` silently drops a zone designation in its input. Calendar dates use `date`; `time with time zone` is discouraged by the manual.
- **Exact quantities and money**: `numeric(p,s)` with an explicit scale, currency in its own column. It computes slower than integer or float; the exactness is the point.
- **Text**: `text`. Enforce a business limit with `CHECK (char_length(col) <= n)`: the manual finds no performance difference among `text`, `varchar(n)`, and `char(n)`, with `char(n)` usually slowest, and a `CHECK` is a limit you can change through `NOT VALID` plus `VALIDATE` ([migrations.md](migrations.md)).
- **Lifecycle**: a status column constrained to the named states (`CHECK` or enum); the transitions live in one service function.

## Constraints carry the invariants

- **`NOT NULL` by default.** A nullable column states what `NULL` means.
- **`CHECK`** reads only the row's own columns; Postgres cannot enforce a rule that references other rows. It assumes the condition is immutable and never rechecks old rows, so a condition that changes with time or another table can make dump and restore fail.
- **Scoped uniqueness** is a unique partial index: `CREATE UNIQUE INDEX … (tenant_id, email) WHERE removed_at IS NULL`; one-active-per-parent is the same shape. Nulls are distinct by default; add `NULLS NOT DISTINCT` when a null should collide.
- **Foreign keys** state `ON DELETE` every time. `NO ACTION` (default) can be deferred to the end of the transaction; `RESTRICT` blocks at once; `CASCADE` only for children that have no life without the parent; `SET NULL` when the child outlives the parent (nullable column). A foreign key must reference a primary key or unique key. Declare referencing columns `NOT NULL`: by default a row with any null referencing column escapes the check.
- **Non-overlap**: `EXCLUDE USING gist (room_id WITH =, during WITH &&)`; scalar `=` inside GiST needs the `btree_gist` extension. On PG18, `PRIMARY KEY (room_id, during WITHOUT OVERLAPS)` expresses the same rule when the key is an entity plus a range or multirange validity period.
- **No polymorphic `*_type` + `*_id` pair**: a foreign key references one table, so the pair has no referential integrity. Use one nullable foreign key per target with `CHECK (num_nonnulls(a_id, b_id) = 1)`, or a join table per relation.
- **Tenant scope**: `tenant_id NOT NULL` on every tenant-scoped table, inside every unique key, and in a composite foreign key, `(tenant_id, parent_id) REFERENCES parent (tenant_id, id)` over a `UNIQUE (tenant_id, id)` on the parent, so a child cannot point at another tenant's parent. Lead indexes with `tenant_id` when every query filters by it. Row-level policy belongs to `security`.

## JSONB

- Use `jsonb`; `json` keeps an exact text copy that every operation reparses, and the manual lists indexing as a `jsonb` advantage.
- A key that is filtered, joined, sorted, constrained, or updated on its own becomes a column. `jsonb` holds sparse or caller-defined attributes with a roughly fixed structure.
- An update locks the whole row, so keep documents small.
- Index with GIN. The default `jsonb_ops` serves `?`, `?|`, `?&`, `@>`, `@?`, `@@`; `jsonb_path_ops` is smaller and faster but serves only `@>`, `@?`, `@@`, and indexes nothing for structures without values such as `{"a": {}}`. Use `jsonb_path_ops` when queries use only those operators.
- A collection that grows without bound, or whose elements are queried, referenced, or constrained, is a child table, whether it started as `jsonb` or an array.

## Large values

Files and blobs live in object storage; the row holds the key, size, and content hash. TOAST moves values over about 2 kB out of line and caps any value at 1 GB, but bytes in rows still travel through WAL, replicas, and backups.

## Partitioning

- Name the access pattern first: drop-by-time retention, or pruning on a key every hot query filters. The manual finds partitioning worthwhile only for a very large table, with a rule of thumb of a table larger than the server's memory.
- The primary key and every unique constraint must include all partition-key columns, and such a table cannot partition on an expression. A uuid key on a partitioned table is therefore `(id, created_at)`, with global uniqueness resting on the id generator alone.
- Pruning works only when the query constrains the partition key. Planning stays healthy up to a few thousand partitions provided queries prune to a few.
- Retire a partition with `DETACH PARTITION … CONCURRENTLY` (not allowed with a default partition, and outside a transaction block), then drop it. Index builds on a partitioned table go partition by partition ([migrations.md](migrations.md)).

## Immutable expressions

- Index expressions and partial-index predicates accept only immutable functions: `NOW()` and `CURRENT_DATE` are rejected. A "recent rows" subset becomes a status column a job flips, or a range predicate in the query.
- A `timestamptz`-to-`date` cast depends on the session `TimeZone`, so it cannot back an expression index. Filter a half-open range on the bare column: `ts >= $1 AND ts < $2`.
