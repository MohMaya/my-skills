# Sources

Written for this repository on 2026-10-05. Ideas adapted, with rules rewritten rather than copied, from these MIT-licensed projects:

- [Sanoy24/backend-performance-review](https://github.com/Sanoy24/backend-performance-review) at `2239a1894d6f10ccf37e9c77ec26d665757ad75c`: the remove → bound → move → cheapen → cache ladder, the falsifier in validation, safety labels on diagnostics, the cartesian-explosion warning, and query-count assertions as mechanism tests.
- [supabase/agent-skills](https://github.com/supabase/agent-skills) at `c9be0e931b7930f7d02126d04774d904c381e7d7`: `= ANY` batching, partial and covering indexes, unindexed foreign keys.
- [planetscale/database-skills](https://github.com/planetscale/database-skills) at `73b20b7eb64716d8c7100c054f0677c0c6e77e30`: keyset pagination with a tie-breaker, transaction-pooling breakage, `INVALID` index traps.
- [yuribodo/postgres-query-optimization-skill](https://github.com/yuribodo/postgres-query-optimization-skill) at `e675a4904b689445c231ce3ea6f51dcfb6d7a89c`: per-loop plan timings, estimate-versus-actual checks, ranking by total time.
- [neondatabase/agent-skills](https://github.com/neondatabase/agent-skills) at `9e4a5705922fddb540c396111a7979e0dca79cc2` (Apache-2.0): join repetition of parent columns, `rows/calls` as an over-fetch signal.

PostgreSQL behaviour was checked against the PostgreSQL 18 manual (Tiger MCP `search_docs`); SQLAlchemy options against the SQLAlchemy 2.0 docs. The intent card, necessity verdicts, and equivalence proof are this repository's own.
