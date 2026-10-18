# Operations reference

Consult from `postgres` in **operate** mode: vacuum, bloat, locks, wraparound, replication, connections, and monitoring on a running database. Alert wiring, runbooks, and restore drills belong to `operability`; the thresholds here are its inputs. Managed hosts (Railway, RDS) own backups, failover, and patching; settings change through the provider's parameter interface, and a restore drill is `operability`'s.

## Safety labels

| Action | Label |
| --- | --- |
| Statistics views, `pg_locks`, `pg_replication_slots`, `age()` | **Safe** |
| `pgstattuple_approx`, `pgstattuple` (a read lock and a full scan) | **Replica or off-peak**; production with approval |
| Plain `VACUUM`, `ANALYZE` (run alongside traffic, cost I/O) | **Approval** on production |
| `ALTER TABLE … SET (autovacuum_*)` (`SHARE UPDATE EXCLUSIVE`) | **Approval**, as a migration |
| `REINDEX … CONCURRENTLY` (`SHARE UPDATE EXCLUSIVE`, extra disk) | **Approval** |
| `pg_repack` (brief `ACCESS EXCLUSIVE`, cancels conflicting queries) | **Approval** and a quiet window |
| `VACUUM FULL`, `CLUSTER` (`ACCESS EXCLUSIVE` for the whole run, space for a copy) | **Offline window only** |
| `pg_cancel_backend`, `pg_terminate_backend`, `pg_drop_replication_slot` | **Approval**, naming the pid or slot |
| Server settings | **Approval**; the provider's interface on a managed host |

## Steps

1. **Observe.** Take every reading in Signals, read-only. **Done when** each signal has a value or a stated gap.
2. **Diagnose.** For each out-of-range signal, name the cause (Causes and fixes). **Done when** each has a cause, or "unknown, needs X".
3. **Fix** with the smallest change that moves the signal, after approval where the label says so. **Done when** the signal, re-read, is in range.
4. **Alert.** Each signal gets an alert at the threshold below; `operability` wires it. **Done when** each signal maps to an alert or a written reason it has none.

## Signals

| Signal | Read | Alert |
| --- | --- | --- |
| XID age | `SELECT datname, age(datfrozenxid) FROM pg_database`; per table, `age(relfrozenxid)` | Warn at 50% of `autovacuum_freeze_max_age` (default 200M); page when it exceeds that and keeps rising. The server warns only 40M XIDs before wraparound and refuses new XIDs at 3M |
| Multixact age | `mxid_age(relminmxid)` per table | The same, against `autovacuum_multixact_freeze_max_age` (default 400M) |
| Horizon holders | `pg_prepared_xacts` (`age(transaction)`); `pg_stat_activity` (`age(backend_xid)`, `age(backend_xmin)`); `pg_replication_slots` (`age(xmin)`, `age(catalog_xmin)`) | Oldest holder's age against the XID-age thresholds above |
| Autovacuum lag | `pg_stat_user_tables`: `n_dead_tup`, `last_autovacuum`, `n_ins_since_vacuum` | Dead tuples rising across vacuums; `last_autovacuum` stale for a churning table |
| Idle in transaction, long transactions | `pg_stat_activity` where `state = 'idle in transaction'` (`now() - state_change`); `now() - xact_start` | Oldest transaction age |
| Connections | `count(*) FILTER (WHERE backend_type = 'client backend')` against `max_connections` | 80% |
| Lock waits | `pg_stat_activity` rows where `cardinality(pg_blocking_pids(pid)) > 0` | Any wait beyond the request deadline |
| Replication lag | `pg_stat_replication`: `write_lag`, `flush_lag`, `replay_lag` | `replay_lag` past the staleness the intent card tolerates |
| Slot WAL | `pg_replication_slots`: `wal_status`, `safe_wal_size`, `inactive_since`, `pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)` | Retained bytes against WAL disk headroom; `wal_status` other than `reserved`; any inactive slot |
| Slow statements | `pg_stat_statements` by `total_exec_time` and `mean_exec_time` ([postgres.md](postgres.md)) | Per statement against its latency budget |
| Checkpoints | `pg_stat_checkpointer`: `num_timed`, `num_requested` (PG17+; the columns left `pg_stat_bgwriter`) | `num_requested` rivalling `num_timed` |

## Causes and fixes

**Autovacuum**
- Leave autovacuum on globally; the manual calls disabling it unwise, and it launches anti-wraparound vacuums regardless.
- A table triggers a vacuum at `autovacuum_vacuum_threshold + autovacuum_vacuum_scale_factor × table size`. At the default 0.2, a 100M-row table gathers 20M dead tuples first. PG18's `autovacuum_vacuum_max_threshold` (default 100M tuples) caps the trigger only on very large tables: a 1B-row table would otherwise wait for 200M. Give high-churn tables their own `ALTER TABLE t SET (autovacuum_vacuum_scale_factor = 0.02, autovacuum_vacuum_threshold = 1000, autovacuum_analyze_scale_factor = 0.01)` and tune against `n_dead_tup`.
- Dead tuples that survive a vacuum point at a held horizon: work the Horizon holders row before touching vacuum settings.
- `autovacuum_vacuum_cost_limit` is divided among the running workers, so raising `autovacuum_max_workers` alone adds no throughput; raise the limit with it. Tables with their own cost settings sit outside that balancing.
- Wraparound warnings: commit or roll back old prepared transactions and long transactions, and drop slots whose consumer is gone; `VACUUM` still runs.

**Bloat**
- Plain `VACUUM` makes space reusable inside the table and returns it to the OS only by truncating empty pages at the end. Measure before acting with `pgstattuple_approx` (exact dead tuples, approximate free space).
- Index bloat: `REINDEX INDEX CONCURRENTLY`, outside a transaction, with disk for the second copy. A failure leaves an `INVALID` `_ccnew` index to drop before retrying. Exclusion-constraint indexes cannot be rebuilt this way.
- Table bloat: `pg_repack`. It holds `ACCESS EXCLUSIVE` briefly at the start and end and `SHARE UPDATE EXCLUSIVE` between, needs a primary key or a unique index on `NOT NULL` columns, needs about twice the table's disk, and after `--wait-timeout` (default 60 s) cancels conflicting queries and later terminates their backends; `--no-kill-backend` skips the table instead. Confirm the host offers the extension.
- `VACUUM FULL` and `CLUSTER` hold `ACCESS EXCLUSIVE` throughout; offline only.

**Replication**
- `max_slot_wal_keep_size` defaults to `-1`, unlimited WAL retention per slot. Set a cap below WAL disk headroom: a slot that falls behind it loses WAL and its consumer must re-sync. `safe_wal_size` shows the bytes left before `lost`.
- PG18 `idle_replication_slot_timeout` (default 0, off) invalidates slots inactive for that long at the next checkpoint; set it where a rebuilt consumer costs less than a full disk.
- Drop slots whose consumer no longer exists.

**Timeouts**
- `idle_in_transaction_session_timeout` per application role (`ALTER ROLE app SET …`), above the longest legitimate pause. It ends the session, freeing its locks and letting vacuum proceed; the app must survive the dropped connection.
- `statement_timeout` and `lock_timeout` per role or session, sized to the workload (request path short, batch jobs their own). The manual advises against `postgresql.conf` for both, since a global value reaches every session, migrations and batch jobs included.
- Apply `idle_session_timeout` per interactive role (`ALTER ROLE`) and leave pooled application roles at 0; poolers react badly to closed connections.
- `transaction_timeout` (PG17+) caps total transaction length; where it overlaps another timeout, the longer one is ignored.

**Connections**
- Budget pool size × processes × services under `max_connections`, minus `superuser_reserved_connections` (default 3) and `reserved_connections` (default 0), with room for migrations.
- `max_connections` is fixed at server start, and raising it enlarges shared-memory allocations; prefer a pooler holding a small server-connection set over a bigger limit.

**Settings**
- `work_mem` (default 4MB) applies per sort or hash node, per query, per session, and hash nodes get `hash_mem_multiplier` (default 2.0) times that. Budget peak memory as sessions × nodes × `work_mem`; keep the default and raise it with `SET LOCAL` for a named query.
- `shared_buffers`: start at 25% of RAM on a dedicated server; beyond 40% rarely helps. `maintenance_work_mem` (default 64MB) is used by each autovacuum worker unless `autovacuum_work_mem` is set.
- `random_page_cost` defaults to 4.0, which assumes most random reads hit cache. Lower it when data is cached or random reads are cheap (SSD storage; around 1.1 is the common choice, a convention beyond the manual), never below `seq_page_cost`, and confirm in `EXPLAIN` that plans improve.
- `max_wal_size` (default 1GB): raise it when `num_requested` rivals `num_timed`.
- `synchronous_commit = off` via `SET LOCAL` inside the transaction of a named, loss-tolerant write (telemetry, counters). A crash can drop up to three `wal_writer_delay` intervals of recent commits and leaves the database consistent. Money, auth, and anything a caller was told succeeded keep the default.
- Logging: `log_lock_waits = on` (default off; logs waits past `deadlock_timeout`); `log_min_duration_statement` at the latency budget (default off); `log_temp_files = 0` to see spills; `log_autovacuum_min_duration` defaults to 10min, so lower it to see routine runs. `log_checkpoints` defaults on.
