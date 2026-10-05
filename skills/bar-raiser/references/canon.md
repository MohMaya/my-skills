# Canon

The sources behind the catalogue's tags. Rules in the catalogue are paraphrased; read the source before quoting it to anyone.

| Tag | Source | Teaches |
| --- | --- | --- |
| Dicken-btree | Ben Dicken, [B-trees and database indexes](https://planetscale.com/blog/btrees-and-database-indexes) | Pages, key order, and why secondary indexes carry the primary key |
| Dicken-uuid | Ben Dicken, [The problem with using a UUID primary key in MySQL](https://planetscale.com/blog/the-problem-with-using-a-uuid-primary-key-in-mysql) | Random keys halve page fill; sequential alternatives |
| Dicken-io | Ben Dicken, [IO devices and latency](https://planetscale.com/blog/io-devices-and-latency) | The latency and IOPS cost of each storage tier |
| Dicken-threads | Ben Dicken, [Processes and threads](https://planetscale.com/blog/processes-and-threads) | Context-switch costs; why Postgres needs a pooler |
| Dicken-bench | Ben Dicken, [Benchmarking Postgres 17 vs 18](https://planetscale.com/blog/benchmarking-postgres-17-vs-18) | Benchmark method: fixed hardware, repetitions, warm-up, stated limits |
| Dicken-shard | PlanetScale, [How to scale your database and when to shard](https://planetscale.com/blog/how-to-scale-your-database-and-when-to-shard-mysql) | Escalation order and shard-key choice |
| TigerStyle | TigerBeetle, [TIGER_STYLE.md](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/TIGER_STYLE.md) | Limits on everything, assertions, design-phase performance sketches |
| matklad-arch | Alex Kladov, [ARCHITECTURE.md](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html) | Codemaps and invariants as absences |
| matklad-ifs | Alex Kladov, [Push ifs up and fors down](https://matklad.github.io/2023/11/15/push-ifs-up-and-fors-down.html) | Decisions in parents, batches at the bottom |
| matklad-test | Alex Kladov, [How to test](https://matklad.github.io/2021/05/31/how-to-test.html) | Boundary tests, IO-free cores, no mocks |
| Ousterhout | John Ousterhout, *A Philosophy of Software Design* | Deep modules, information leakage, design it twice |
| Hickey | Rich Hickey, [Simple Made Easy](https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/SimpleMadeEasy.md) | Simple versus easy; braided constructs |
| King | Alexis King, [Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/) | Parsers return stronger types; shotgun parsing |
| Brandur-idem | Brandur Leach, [Implementing Stripe-like idempotency keys in Postgres](https://brandur.org/idempotency-keys) | Atomic phases, recovery points, staged jobs |
| Brandur-queues | Brandur Leach, [Postgres job queues and long transactions](https://brandur.org/postgres-queues) | How one long transaction degrades a queue |
| Brooker-jitter | Marc Brooker, [Exponential backoff and jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) | Full jitter |
| Brooker-metastable | Marc Brooker, [Metastability and distributed systems](https://brooker.co.za/blog/2021/05/24/metastable.html) | Sustaining loops that outlive their trigger |
| SRE-cascade | Google SRE, [Addressing cascading failures](https://sre.google/sre-book/addressing-cascading-failures/) | Deadlines, small queues, load testing to failure |
| SRE-overload | Google SRE, [Handling overload](https://sre.google/sre-book/handling-overload/) | Retry budgets, rejecting early, client throttling |
| Kleppmann | Martin Kleppmann, [Using logs to build a solid data infrastructure](https://martin.kleppmann.com/2015/05/27/logs-for-data-infrastructure.html) | Why dual writes diverge; logs and CDC |
| Helland | Pat Helland, [Life beyond distributed transactions](https://www.ics.uci.edu/~cs223/papers/cidr07p15.pdf) | Entities as the unit of atomicity; idempotent messaging |
| outbox | Chris Richardson, [Transactional outbox](https://microservices.io/patterns/data/transactional-outbox.html) | Publishing atomically with the state change |
| Nygard | Michael Nygard, *Release It!*; Martin Fowler, [Circuit breaker](https://martinfowler.com/bliki/CircuitBreaker.html) | Timeouts, bulkheads, circuit breakers |
| Majors | Charity Majors, [Logs vs structured events](https://charity.wtf/2019/02/05/logs-vs-structured-events/) | Wide events, high cardinality |
| Luu-postmortem | Dan Luu, [Postmortem lessons](https://danluu.com/postmortem-lessons/) | Config changes and error handling behind outages |
| Luu-testing | Dan Luu, [Testing](https://danluu.com/testing/) | Simple tests catch most catastrophic failures |
| Muratori | Casey Muratori, [Clean code, horrible performance](https://www.computerenhance.com/p/clean-code-horrible-performance) | Cost of indirection in hot loops |
| Metz | Sandi Metz, [The wrong abstraction](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction) | Duplication is cheaper than the wrong abstraction |
| Beck | Kent Beck, *Tidy First?* | Separate tidying from behavior change |
| Spolsky | Joel Spolsky, [Things you should never do, part I](https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/) | Why whole-product rewrites fail |
| Pocock | Matt Pocock, [skills](https://github.com/mattpocock/skills) (`codebase-design`) | Deletion test; one adapter is a hypothetical seam |
| Dean | Jeff Dean, [Latency numbers every programmer should know](https://gist.github.com/jboner/2841832) | Orders of magnitude per operation |
