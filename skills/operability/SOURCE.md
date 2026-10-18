# Sources

Written for this repository on 2026-10-18. Ideas adapted, with every rule rewritten and checked against a primary source, from these upstream skills (imported in commit 40c5f7c):

- [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) (MIT, as declared in each SKILL.md): `sre-engineer`, `monitoring-expert`, `chaos-engineer`, `devops-engineer`, `microservices-architect`. Kept: SLO-first alerting, page versus ticket routing, runbook-per-alert, experiment cards with abort criteria, the postmortem outline, liveness and readiness split. Dropped: raw `req.path` metric labels, `ip` and `userAgent` on every log line, the three-pillars framing, a 6x burn rate labelled 1x, the 6h/1d pair in place of 6h/30m, production chaos, decorrelated jitter, catch-and-log, the error-budget freeze policy.
- AWS agent skill `aws-observability` (v8, imported in 40c5f7c; no license file in the directory). Kept only the generalizable rules: percentile over average for latency alarms, an explicit missing-data decision, no unbounded ids as metric dimensions.

## Primary sources, by rule

| Rule | Source |
| --- | --- |
| SLI as a ratio of good events to total events; start with a loose target; few indicators chosen from user needs; percentiles over averages | [SRE Workbook, Implementing SLOs](https://sre.google/workbook/implementing-slos/); [SRE book, Service Level Objectives](https://sre.google/sre-book/service-level-objectives/) |
| "Valid events" as the denominator | Hidalgo, *Implementing Service Level Objectives* (O'Reilly, 2020), ch. 4 (read through a secondary summary; the Workbook says "total events") |
| Rolling window, 30 days assumed by the burn-rate table | Workbook, Alerting on SLOs, Table 5-6 (the Workbook also calls four weeks a good general-purpose window) |
| Page pairs 1 h/5 min at 14.4x (2%) and 6 h/30 min at 6x (5%); ticket pair 3 d/6 h at 1x (10%); short window is 1/12 of the long; burn-rate arithmetic; low-traffic remedies | [Workbook, Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/), Tables 5-6 and 5-8 |
| Page only when urgent, actionable, and user-visible; pages and tickets are the only ways to ask a human to act | [SRE book, Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/); Workbook, Alerting on SLOs |
| Pre-written playbooks improve MTTR roughly 3x | [SRE book, Introduction](https://sre.google/sre-book/introduction/) |
| One wide structured event per request per service, built up and emitted once | Majors, [Logs vs. structured events](https://charity.wtf/2019/02/05/logs-vs-structured-events/) and [Is it time to version observability?](https://charity.wtf/2024/08/07/is-it-time-to-version-observability-signs-point-to-yes/) |
| Route template, not raw path, as the label | [OpenTelemetry HTTP semantic conventions](https://opentelemetry.io/docs/specs/semconv/http/http-metrics/): `http.route` MUST be low-cardinality and the URI path cannot substitute it |
| Duration histograms in seconds | OpenTelemetry `http.server.request.duration` (unit `s`); [Prometheus naming](https://prometheus.io/docs/practices/naming/) (base units; no high-cardinality labels). PostHog's metrics skill shows `ms`; this skill sets seconds with the unit declared |
| PostHog alert capabilities: trends, funnels, and SQL insights; "has value" bounds; check intervals; "has value less than 1" for missing events | [PostHog alerts](https://posthog.com/docs/alerts). Alerting a SQL insight that returns `min(short, long)` is an inference from the documented SQL-insight support and the arithmetic (both windows exceed the rate exactly when the minimum does); the first alert authored this way should be confirmed to save and fire |
| Liveness restarts, readiness gates traffic and may check each required back-end; liveness errors cause cascading failure | [Kubernetes probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/) |
| Dependency health checks risk fleet-wide removal; keep fast checks local; fail open | [AWS Builders' Library, Implementing health checks](https://builder.aws.com/content/3Ev53O39izHCtWLzp4XU6t8PC1O/implementing-health-checks) |
| Railway healthcheck gates a deploy and is not monitored afterward | [Railway healthchecks](https://docs.railway.com/deployments/healthchecks) |
| Load components until they break; check recovery when load drops | [SRE book, Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) |
| Ramping arrival rate; thresholds as pass/fail; `abortOnFail`; pin elasticity off | [k6 breakpoint testing](https://grafana.com/docs/k6/latest/testing-guides/test-types/breakpoint-testing/); [k6 thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) |
| Steady-state hypothesis on measurable output; minimise blast radius | [Principles of Chaos Engineering](https://principlesofchaos.org/). The principles prefer production; Shiv chose staging only, so this skill diverges on purpose. The 30-second abort and one-variable rule are house parameters (the 30 s figure comes from the imported `chaos-engineer` experiment template) |
| Blameless postmortem; "unreviewed postmortem might as well never have existed"; action items with owner and tracking bug | [SRE book, Postmortem Culture](https://sre.google/sre-book/postmortem-culture/); [Example Postmortem](https://sre.google/sre-book/example-postmortem/) (the due date is a house addition) |
| Page also on data loss and security events | House choice, from the imported `sre-engineer` on-call guidelines; no primary source checked |

The step order, the modes, the Done-when criteria, the PostHog mapping, and the `runbooks/<alert-name>.md` convention are this repository's own.
