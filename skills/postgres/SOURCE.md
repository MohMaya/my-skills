# Sources

Written for this repository on 2026-10-05. Ideas adapted, with rules rewritten rather than copied, from these MIT-licensed projects:

- [Sanoy24/backend-performance-review](https://github.com/Sanoy24/backend-performance-review) at `2239a1894d6f10ccf37e9c77ec26d665757ad75c`: the remove → bound → move → cheapen → cache ladder, the falsifier in validation, safety labels on diagnostics, the cartesian-explosion warning, and query-count assertions as mechanism tests.
- [supabase/agent-skills](https://github.com/supabase/agent-skills) at `c9be0e931b7930f7d02126d04774d904c381e7d7`: `= ANY` batching, partial and covering indexes, unindexed foreign keys.
- [planetscale/database-skills](https://github.com/planetscale/database-skills) at `73b20b7eb64716d8c7100c054f0677c0c6e77e30`: keyset pagination with a tie-breaker, transaction-pooling breakage, `INVALID` index traps.
- [yuribodo/postgres-query-optimization-skill](https://github.com/yuribodo/postgres-query-optimization-skill) at `e675a4904b689445c231ce3ea6f51dcfb6d7a89c`: per-loop plan timings, estimate-versus-actual checks, ranking by total time.
- [neondatabase/agent-skills](https://github.com/neondatabase/agent-skills) at `9e4a5705922fddb540c396111a7979e0dca79cc2` (Apache-2.0): join repetition of parent columns, `rows/calls` as an over-fetch signal.

PostgreSQL behaviour was checked against the PostgreSQL 18 manual (via the Tiger docs MCP); SQLAlchemy options against the SQLAlchemy 2.0 docs. The intent card, necessity verdicts, and equivalence proof are this repository's own.

## 2026-10-18: schema, migrate, and operate modes

Ideas adapted, with every rule rewritten against the PostgreSQL 18 manual rather than copied, from skills imported in commit `40c5f7c`:

- [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) (`postgres-pro`, `sql-pro`, and `database-optimizer` declare `license: MIT` in their frontmatter; no LICENSE file was imported): `postgres-pro`, `sql-pro`, and `database-optimizer`. Adopted: the maintenance topics (autovacuum tuning per table, wraparound monitoring, bloat removal options, lock and replication-slot monitoring), JSONB index operator classes, the database-design topics (constraints, temporal data), the recursive-CTE cycle guard, and the `last_value` frame trap.
- [wshobson/agents](https://github.com/wshobson/agents) `sql-optimization-patterns` (imported in commit `40c5f7c`; no license recorded on disk, so nothing is copied): batched writes and keyset pagination, already covered by the query workflow; no new rule.

Not carried over, each contradicted by the manual or by current behaviour: prepared statements as the injection defense (binding is); `uuid-ossp` v4 and `SERIAL` keys; `pgcrypto` password hashing (`security` owns it); `pg_repack` taking no locks; `CHECK` constraints needing PG15; CTEs materializing by default; `EXISTS` always beating `IN`; indexing every foreign key; selectivity-first index column order; `NOW()` and `DATE(timestamptz)` in index definitions; `pg_stat_bgwriter` checkpoint columns and `total_time` / `mean_time`; a global `statement_timeout`; `work_mem = RAM × 0.25 / connections`; `timestamp` without time zone in examples.

Checked against the PostgreSQL 18 manual: `ALTER TABLE`, `CREATE INDEX`, `REINDEX`, `DROP INDEX`, `VACUUM`, `CREATE TABLE`, explicit locking, routine vacuuming, the vacuum, replication, client, logging, WAL, query, resource, and connection settings, `pg_replication_slots`, `pg_stat_activity`, `pg_stat_checkpointer`, `pg_stat_statements`, `pgstattuple`, UUID functions, JSON types, partitioning, and `WITH` queries. Alembic and SQLAlchemy options were checked against their current documentation; `pg_repack` behaviour against its project documentation.

