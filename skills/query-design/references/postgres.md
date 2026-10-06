# PostgreSQL reference

Consult on demand from `query-design`. Check version-specific behaviour against the manual for the server's major version (`SHOW server_version;`): the Tiger docs MCP's `search_docs` when configured, otherwise `postgresql.org/docs/<major>`.

## Diagnostics and safety

| Command | Answers | Safety |
| --- | --- | --- |
| `EXPLAIN <stmt>` | The chosen plan and estimates | Safe everywhere |
| `EXPLAIN (ANALYZE, BUFFERS) <select>` | Actual rows, time, pages per node | Executes the query: staging or replica; production only with approval and `statement_timeout` |
| `BEGIN; EXPLAIN (ANALYZE, BUFFERS) <dml>; ROLLBACK;` | The same for a write | Executes the write and takes its locks: staging only |
| `EXPLAIN (GENERIC_PLAN) <stmt with $1>` | The plan a prepared statement gets once it goes generic (PG16+) | Safe; cannot combine with `ANALYZE` |
| `EXPLAIN (ANALYZE, SERIALIZE)` | Adds output conversion and de-TOAST cost (PG17+) | As `ANALYZE` |
| `\d+ <table>` | Columns, constraints, indexes, triggers, policies | Safe |
| `pg_stat_statements` | Where the time goes across the workload | Safe; needs the extension |
| `pg_stats` | Null fraction, distinct counts, common values per column | Safe |
| `pg_stat_user_tables` / `pg_stat_user_indexes` | Seq versus index scans, dead tuples, last analyze, index use | Safe |
| `pg_stat_activity` | Running and idle-in-transaction sessions | Safe |

PG18 includes `BUFFERS` in every `EXPLAIN ANALYZE`; on PG16–17 spell it out.

```sql
-- Workload: where total time goes
SELECT calls, round(total_exec_time) AS total_ms, round(mean_exec_time, 2) AS mean_ms,
       rows / NULLIF(calls, 0) AS rows_per_call, left(query, 120)
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 20;

-- Data shape of the columns a query filters or joins on
SELECT attname, null_frac, n_distinct, most_common_vals
FROM pg_stats WHERE schemaname = 'public' AND tablename = 'orders';

-- Real fan-out of a join
SELECT max(n), percentile_disc(0.95) WITHIN GROUP (ORDER BY n), avg(n)
FROM (SELECT count(*) AS n FROM order_lines GROUP BY order_id) s;

-- Indexes never scanned since stats reset (check stats age before acting)
SELECT relname, indexrelname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes WHERE idx_scan = 0 ORDER BY pg_relation_size(indexrelid) DESC;
```

Run `EXPLAIN` as the service's role (`SET LOCAL ROLE <role>` inside a transaction): an owner or superuser bypasses RLS and sees a faster plan than production.

## Reading a plan

- Read innermost nodes first. `actual time` and `rows` are per loop; multiply by `loops` for the node's true cost.
- Estimated versus actual rows off by 10x or more points at statistics: run `ANALYZE`, raise `ALTER TABLE … ALTER COLUMN … SET STATISTICS`, or add `CREATE STATISTICS (dependencies, ndistinct, mcv)` for correlated columns.
- `Rows Removed by Filter` far above rows returned: the predicate is applied after the scan; it needs an index condition or an earlier filter.
- `Heap Fetches` on an Index Only Scan: the visibility map is stale; vacuum is behind.
- `Sort Method: external merge` or `Hash … Batches` above 1: spilled to disk. Shrink the input earlier, or raise `work_mem` for that transaction with `SET LOCAL`.
- `shared read` far above `shared hit`: cold cache or too many pages touched; compare warm runs.
- Nested Loop with a large `loops` count over an inner Seq Scan: the join key lacks an index.
- `Index Searches` (PG18) counts index descents across loops; PG18 skip scan can use a multicolumn index whose leading column is unfiltered when that column has few distinct values.
- `Subplans Removed` or a short list of scanned partitions or chunks: pruning worked.
- A `LIMIT` stops child nodes early, so their actual rows sit below estimates by design.
- Plans on dev-sized tables mislead: the planner rightly seq-scans a table of a few pages. Judge plans on production-shaped row counts.

## Index design

- Design from the access path: equality columns first, then the range or sort column, in the `ORDER BY` order and direction the query uses.
- **Partial** (`WHERE removed_at IS NULL`, `WHERE status = 'active'`) for a hot subset. The planner uses it only when it can prove the query's predicate implies the index's, so a parameter (`status = $1`) under a generic plan misses an index written for a literal.
- **Covering** (`INCLUDE (cols)`) to serve hot reads from the index alone; depends on vacuum keeping the visibility map current.
- **Expression** indexes match only the identical expression: `lower(email)` in the index and in the query, or a `citext` column instead.
- Foreign keys get no automatic index. Index the referencing column when you join on it or delete parents.
- Every index taxes every write and can turn HOT updates into full updates when it covers a frequently updated column. Check `pg_stat_user_indexes` for a near-duplicate before adding one, and write the cost down.
- Build on live tables with `CREATE INDEX CONCURRENTLY` outside a transaction. A failed build leaves an `INVALID` index that is maintained on writes and never read, and `IF NOT EXISTS` reports success over it; check `pg_index.indisvalid`.
- Prototype with hypothetical indexes (hypopg via `postgres-mcp`), which yield estimates only; confirm with a real index on staging before writing the migration.

## Query shapes

- **Existence**: `EXISTS (SELECT 1 …)` stops at the first match; a count compared to zero reads every match.
- **Counting**: an exact count scans every qualifying row. For "99+" displays, count a `LIMIT 100` subquery; for dashboards, `pg_class.reltuples` or the plan estimate.
- **Pagination**: keyset, `WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC LIMIT n`, backed by an index on those columns in that order, with a unique tie-breaker. Nullable sort columns need explicit `NULLS` handling in the predicate, ordering, and index. Offset cost grows with depth.
- **Anti-join**: `NOT EXISTS`. `NOT IN` returns no rows once the subquery yields a single NULL.
- **Semi-join**: the planner treats `IN (subquery)` and `EXISTS` alike. Rewriting either as `JOIN` changes cardinality.
- **Fan-out**: joining two one-to-many children multiplies rows and inflates sums and counts. Aggregate each child in its own subquery or `LATERAL`, then join. `DISTINCT` patching a join is a symptom.
- **Top-N per group**: `LATERAL (SELECT … ORDER BY … LIMIT n)` over an index; `DISTINCT ON` for n = 1.
- **CTEs** (PG12+): a non-recursive, side-effect-free CTE referenced once is inlined; `MATERIALIZED` forces a single evaluation and fences optimization; `NOT MATERIALIZED` forces inlining.
- **Correlated scalar subqueries** in the select list run once per outer row; check `loops`.
- **OR across columns** defeats a single index; `UNION ALL` of indexable branches works when the branches cannot overlap.
- **Batching**: `= ANY(<one array parameter>)` keeps the statement text stable across list lengths; worth it when lists are large or vary widely, and unnecessary under a small page cap. Placeholder syntax is the driver's (`$1` in asyncpg, `%s` in psycopg); chunk lists in the tens of thousands.
- **Parent with children in one round trip**: `json_agg` in a `LATERAL` works when fan-out is bounded; past that, two queries move fewer bytes than a join repeating parent columns per child.

## TimescaleDB

- Filter hypertables on the time column so the plan scans few chunks; confirm the chunk count in `EXPLAIN`.
- Repeated rollups belong in a continuous aggregate (the Move rung) rather than a request-time `GROUP BY`.
- Compressed chunks read fastest when filters match `segmentby` columns and the sort matches `orderby`.

## Sessions, pooling, transactions

- Transaction pooling (PgBouncer) breaks session state: use `SET LOCAL` inside the transaction, transaction-scoped advisory locks (`pg_advisory_xact_lock`), and driver settings for prepared statements (see `sqlalchemy.md`).
- Keep transactions free of network calls (HTTP, Kafka, S3). A session idle in transaction holds its snapshot, blocks vacuum cleanup database-wide, and holds its locks; `idle_in_transaction_session_timeout` caps the damage.
- `work_mem` applies per sort or hash node, per query; raise it per transaction, not globally.
- Total connections = pool size × processes × services; keep it under `max_connections` with headroom for migrations and admin.

## postgres-mcp (when configured)

Run as `uvx postgres-mcp --access-mode=restricted` against a read-only role. Tools: `get_top_queries`, `explain_query` (accepts `hypothetical_indexes`; cannot combine them with `analyze`), `analyze_query_indexes`, `analyze_workload_indexes`, `analyze_db_health`, `execute_sql` (read-only in restricted mode).
