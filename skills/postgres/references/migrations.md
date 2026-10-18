# Migrations reference

Consult from `postgres` in **migrate** mode: DDL, index builds, backfills, and data migrations on a database serving traffic. The kernel requires Shiv's confirmation before a migration runs against any shared database.

## The machine

A change moves through four states, each its own deploy, and every deploy runs against both the previous and the next app version.

| State | The release contains | Exit when | Undo |
| --- | --- | --- | --- |
| **expand** | Additive DDL only: new nullable column, table, or index; constraints `NOT VALID` | Old and new app versions both run on the new schema | Drop what was added |
| **backfill** | Code writing both shapes, plus a job filling history in batches | The job's predicate query returns zero rows | Stop the job |
| **switch** | Reads move to the new shape (behind a flag); `VALIDATE CONSTRAINT`; `SET NOT NULL` | Nothing reads the old shape for one full release cycle | Flip the flag back |
| **contract** | Drop the old column, index, or constraint | Nothing reads or writes it: code search clean, `idx_scan` zero | Restore from backup, or roll forward |

A release never mixes states, and a state starts only after the previous exit is observed.

## Steps

1. **Classify.** Give each statement its lock and its rewrite verdict from the table below. **Done when** every statement has both.
2. **Place.** Assign each statement a state; split any release that mixes states. **Done when** each release holds one state and works with the previous app version.
3. **Guard.** Apply the rules in Guards and Backfills. **Done when** every `ACCESS EXCLUSIVE` statement runs under `lock_timeout` with a retry, and none scans or rewrites a large table while holding that lock.
4. **Rehearse** on staging with production-shaped rows, recording lock wait and duration per statement. **Done when** the numbers are in the PR.
5. **Run** after Shiv's confirmation; then confirm `pg_index.indisvalid` is true for every index touched and `\d+` shows no leftover `NOT VALID`. **Done when** both checks pass.

## Lock and rewrite per statement

`ALTER TABLE` takes `ACCESS EXCLUSIVE` unless this table says otherwise; with several subcommands, the strictest applies.

| Statement | Lock | Cost | Safe form |
| --- | --- | --- | --- |
| `ADD COLUMN` nullable, or with a non-volatile `DEFAULT` | `ACCESS EXCLUSIVE`, brief | No rewrite; the default lives in metadata | Direct |
| `ADD COLUMN` with a volatile default, stored generated column, identity, or constrained-domain type | `ACCESS EXCLUSIVE` | Rewrites table and indexes | Add nullable, backfill, then `SET DEFAULT` |
| `ALTER COLUMN TYPE` | `ACCESS EXCLUSIVE` | Rewrites table and rebuilds indexes unless the types are binary-coercible and the contents unchanged; drops column statistics, so `ANALYZE` after | New column through the four states |
| `SET NOT NULL` | `ACCESS EXCLUSIVE` | Full scan unless a valid `CHECK` proves no nulls | `ADD CONSTRAINT … CHECK (c IS NOT NULL) NOT VALID`, `VALIDATE CONSTRAINT`, `SET NOT NULL`, drop the `CHECK`. PG18 also accepts `NOT NULL … NOT VALID` |
| `ADD CHECK` | `ACCESS EXCLUSIVE` | Full scan | `NOT VALID`, then `VALIDATE CONSTRAINT` |
| `ADD FOREIGN KEY` | `SHARE ROW EXCLUSIVE` on both tables | Full scan | `NOT VALID`, then `VALIDATE CONSTRAINT` |
| `VALIDATE CONSTRAINT` | `SHARE UPDATE EXCLUSIVE` (and `ROW SHARE` on the referenced table) | Full scan while writes continue | Run in its own migration |
| `ADD UNIQUE` / `PRIMARY KEY` | `ACCESS EXCLUSIVE` | Builds the index | `CREATE UNIQUE INDEX CONCURRENTLY`, then `ADD CONSTRAINT … USING INDEX` (index must be non-partial, non-expression, default b-tree; not on partitioned tables; a primary key over nullable columns still scans) |
| `CREATE INDEX` | `SHARE`: blocks writes | Reads the table | `CONCURRENTLY` |
| `CREATE INDEX CONCURRENTLY` | `SHARE UPDATE EXCLUSIVE` | Two scans; waits for older transactions | Outside a transaction |
| `DROP INDEX` | `ACCESS EXCLUSIVE` | None | `DROP INDEX CONCURRENTLY`: one index, no `CASCADE`, not for constraint-backed or partitioned indexes |
| `DROP COLUMN` | `ACCESS EXCLUSIVE` | No rewrite; space returns as rows update | Contract state |
| `ALTER TABLE … SET (fillfactor / toast / autovacuum parameter)` | `SHARE UPDATE EXCLUSIVE` | None | Direct |
| `DETACH PARTITION … CONCURRENTLY` | `SHARE UPDATE EXCLUSIVE` on the parent | Not with a default partition; outside a transaction | Direct |

A rename breaks the previous app version: add the new name as a column and walk the four states.

## Guards

- **Time-box every lock wait.** Run `SET LOCAL lock_timeout = '…'` and a larger `statement_timeout` inside the migration's transaction before `ACCESS EXCLUSIVE` DDL, and retry with backoff on SQLSTATE `55P03` (`lock_not_available`); after the retry budget, fail loudly. A waiting DDL statement is itself in the lock queue, and sessions requesting a conflicting lock behind it wait on it too. Set both per transaction, never globally ([operations.md](operations.md#causes-and-fixes) holds the rule). Check `pg_stat_activity` for old `xact_start` rows on the table first, since DDL waits for open transactions.
- **Constraints are added in two steps**: `NOT VALID` skips the scan and enforces new writes at once; `VALIDATE CONSTRAINT` scans later under a lock that lets writes continue.
- **Concurrent builds** run outside a transaction and wait for older transactions to finish. A failure leaves an `INVALID` index that costs write overhead and is never read; a unique build keeps enforcing uniqueness even when invalid. Find leftovers with `SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid`, then `DROP INDEX CONCURRENTLY` and rebuild, or `REINDEX INDEX CONCURRENTLY`. `CREATE INDEX IF NOT EXISTS` passes over any same-named relation, so never use it to make a build rerunnable.
- **Partitioned tables** do not support `CONCURRENTLY` on the parent: `CREATE INDEX … ON ONLY parent`, build each partition's index concurrently, then `ALTER INDEX … ATTACH PARTITION`.

## Backfills

- Run as a separate job, never inside the DDL migration, whose transaction holds locks.
- Key batches on the primary key: `UPDATE t SET new = f(old) WHERE id > $last AND id <= $hi AND new IS DISTINCT FROM f(old)`, each batch its own short transaction. The predicate makes a rerun a no-op; persist `$last` so the job resumes after a crash.
- Size batches by measured duration, and throttle: sleep in proportion to batch time, and pause while replica `replay_lag` or the table's `n_dead_tup` exceeds a threshold.
- One unbatched `UPDATE` of a large table writes a new version of every row in a single transaction, holds every row lock until commit, and keeps vacuum from cleaning dead rows meanwhile.
- **Done when** the batch predicate returns zero rows, a rerun updates zero, and `ANALYZE` has run.

## Downgrades

Expand and backfill migrations get a `downgrade()` that drops what they added. A contract migration's `downgrade()` raises with "restore from backup or roll forward", so a rollback that cannot work fails loudly.

## Alembic

- Set `transaction_per_migration=True` in `env.py`. `autocommit_block()` commits the preceding transaction unconditionally, and Alembic recommends per-migration transactions wherever autocommit blocks exist.
- A concurrent index is a migration of its own:

```python
def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.create_index("ix_orders_account_id", "orders", ["account_id"], postgresql_concurrently=True)
```

  `op.drop_index(..., postgresql_concurrently=True)` follows the same shape. After a failed build, drop the leftover `INVALID` index before rerunning.
- `ALTER TYPE … ADD VALUE` also runs inside `autocommit_block()`.
- `NOT VALID`: `op.create_foreign_key(..., postgresql_not_valid=True)`. For `CHECK`, use `op.execute("ALTER TABLE … ADD CONSTRAINT … CHECK (…) NOT VALID")`, since `op.create_check_constraint` documents no such flag. `VALIDATE CONSTRAINT` is also `op.execute`, in its own migration.
- Postgres DDL is transactional, so a revision that fails on `lock_timeout` rolls back whole; the deploy step reruns it with backoff.
