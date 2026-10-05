# SQLAlchemy 2.0 reference

Consult on demand from `query-design`. Covers SQLAlchemy 2.0 async with psycopg 3 or asyncpg, Alembic, and raw asyncpg. Check loader and dialect options against the installed version (`uv pip show sqlalchemy` or the lockfile).

## Seeing the SQL

- Local run: `create_async_engine(url, echo=True)`, or set the `sqlalchemy.engine` logger to `INFO`.
- One statement: `str(stmt.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))` gives runnable SQL for `EXPLAIN`; some types will not render as literals, so bind those by hand.
- Statements per path in a test: count with `event.listen(engine.sync_engine, "before_cursor_execute", …)`. Reuse the repository's helper when one exists (alpha-core: `tests/livedb/test_service_address_count_live.py`).
- GraphQL: field resolvers run after the root query, so the statement count belongs to the whole operation, not the resolver alone.

## Loading relationships

| Relationship | Strategy | Why |
| --- | --- | --- |
| Many-to-one / one-to-one | `joinedload` | One query; LEFT OUTER JOIN unless `innerjoin=True` |
| One-to-many / many-to-many | `selectinload` | A second query with `IN` over parent keys, batched; no row multiplication |
| Several collections | `selectinload` each | Chained `joinedload` on collections multiplies rows (A × B × C) |
| Already joined for filtering | `contains_eager` | Reuses the join instead of adding another |

- `joinedload` on a collection requires `.unique()` on the result and repeats every parent column per child; it is the wrong default.
- Make hidden loads fail loudly: `raiseload("*")` on the statement, `lazy="raise"` on the relationship, or `load_only(cols, raiseload=True)`. Under asyncio an implicit lazy load raises `MissingGreenlet`; treat that as an unplanned query and load it up front. Awaiting `awaitable_attrs` inside a loop is an N+1 with extra steps.
- Read-only lists: select columns (`select(A.id, A.name)`) and map rows to DTOs; skips identity-map and change-tracking overhead.
- `with_loader_criteria` applies a predicate (lifecycle, tenant) to eager loads too; verify it in the emitted SQL.
- Strawberry: batch per-row field reads through a `DataLoader` keyed per request, its load function issuing one `= ANY` query.

## Shapes

- **Existence**: `session.scalar(select(exists().where(…)))`.
- **Count**: count from a narrow statement. `select(func.count()).select_from(big_stmt.subquery())` drags along every join and eager option of `big_stmt`.
- **Batch reads**: `col.in_(ids)` renders one bind parameter per value, so statement text varies with list length (churning prepared-statement caches and splitting `pg_stat_statements` entries). For large or widely varying lists bind one array with `any_()`, giving custom column types an explicit `ARRAY(...)` bind type, and confirm the rendering with the compile recipe. Under a small page cap the variation is harmless.
- **Bulk writes**: `session.execute(insert(Model), [dict, …])` batches via insertmanyvalues; `postgresql.insert(...).on_conflict_do_nothing()` / `on_conflict_do_update()` for idempotent upserts; `update(Model).where(…).values(…)` replaces a loop of ORM mutations. Bulk statements bypass ORM flush events, so check the repository's flush guards and audit hooks first.
- **Session concurrency**: one `AsyncSession` serves one task at a time; `asyncio.gather` on a shared session fails. Parallel queries need separate sessions, and each takes a pool slot.
- **Expiry**: with `expire_on_commit=True`, touching an attribute after commit reloads it (and raises under asyncio); read what you need before commit or configure the session factory.

## Drivers and pooling

- **psycopg 3** prepares a statement server-side after it runs five times (`prepare_threshold`). Behind PgBouncer transaction pooling without prepared-statement support (before 1.21, or `max_prepared_statements = 0`), pass `connect_args={"prepare_threshold": None}`.
- **asyncpg** (SQLAlchemy dialect) caches 100 prepared statements per connection. Behind PgBouncer, set `?prepared_statement_cache_size=0`, or give statements unique names with `connect_args={"prepared_statement_name_func": lambda: f"__asyncpg_{uuid4()}__"}` and `NullPool`.
- **Raw asyncpg** (`asyncpg.create_pool`): `statement_cache_size=0` behind PgBouncer; `copy_records_to_table` for bulk loads; `executemany` for batched writes.

## Roles and grants

When a repository runs each service as its own database role (alpha-core: `CLAUDE.md` § Database role grants), a rewrite that reads or writes a new table follows those rules: grant every role that runs the statement, and test the statement under each role. Run `EXPLAIN` under that role so RLS and permissions match production.

## Alembic

- Index on a live table: `op.create_index(..., postgresql_concurrently=True)` inside `with op.get_context().autocommit_block():`, since `CONCURRENTLY` cannot run in a transaction.
- Keep schema changes compatible with the previous app version: add, backfill in throttled batches, switch reads, then drop in a later release.
