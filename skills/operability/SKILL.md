---
name: operability
description: What production code measures, alerts on, and proves before launch - SLO, wide-event instrumentation, burn-rate alerts, runbooks, health endpoints, load and failure tests, postmortems. Use when launching a service, job, or queue consumer; adding an endpoint, queue, or external dependency to one; defining an SLO or alert; adding a health endpoint; or after an incident.
---

# Operability

A service is operable when it tells you users are hurting before they do, wakes a human only for that, and has been broken on purpose before launch. Every metric, alert, and test below serves a named user-visible job or a named failure mode, and each is cut when it serves neither.

**Dvandva.** Run `dvandva` before you produce an SLO, an alert, or a runbook.

## Modes

| Mode | When | Steps |
| --- | --- | --- |
| **launch** | A new service, job, or queue consumer | 1–7, with 6 before traffic arrives |
| **change** | A new endpoint, job, queue, or external dependency | 2; 3 and 4 for each new failure mode or sustaining loop; 5 when health endpoints change |
| **learn** | An incident has ended | 8, then re-enter the steps its actions name |

## Owners

- Wiring: `posthog:instrument-logs`, `posthog:instrument-metrics`, `posthog:instrument-error-tracking` send; `posthog:authoring-log-alerts`, `posthog:authoring-error-tracking-alerts` author. This skill decides what to measure and alert on, then hands off by name.
- `bar-raiser` holds the review checks for this work (catalogue "Reliability" and "Operability"); `shipper` owns deploy and rollback posture; `use-railway` operates Railway; `postgres` (`references/operations.md`) names the database signals; `security` names what logs never contain; `engineering:incident-response` runs a live incident.

## 1. SLO

- **Job**: one sentence in the user's terms ("a new user receives their confirmation email").
- **SLI**: good events ÷ valid events, each defined in a sentence. Valid events are the ones the service is answerable for (exclude health checks, bots, and requests the client malformed). A good event is correct and fast enough, with the latency bar written in it ("under 2 s"), so burn-rate alerts cover latency too.
- **Target**: one percentage over a rolling 30-day window. Start looser than you hope and tighten later; current performance is a data point, never the target.

Until an SLO exists every alert below is a ticket. No SLO, no page.

**Done when** the job, the numerator and denominator as queries, the target, and the window are written down.

## 2. Instrument

Meet the catalogue's "Operability" entries (one wide event per request or job per service, bounded metric labels, a request id through every queue and job), then add:

- **Route template as the label.** `http.route`-style (`/users/:id`), from the framework's matched route. Raw paths and ids belong on the event only.
- **Redact list in the logger config**, covering at least password, token, authorization, cookie, and set-cookie fields, as defence beyond `security`'s rules.
- **Business-outcome fields on the event**: the outcome of the job (`confirmation_sent`, `payment_captured`), the tenant, and the error class.
- **Latency histograms in seconds**, with the unit set explicitly.
- **At least one business-job signal** that moves when the job in step 1 breaks while HTTP stays green (emails delivered, jobs completed, rows reconciled).

Send events through `posthog:instrument-logs` and metrics through `posthog:instrument-metrics`; exceptions through `posthog:instrument-error-tracking`.

**Done when** one request or job, replayed in staging, yields one event holding the request id, route template, outcome, and duration; the redacted fields show as redacted; and the step 1 SLI computes from stored data.

## 3. Alert

**SLO burn**, multiwindow and multi-burn-rate: an alert fires when both of its windows exceed its burn rate.

| Severity | Long window | Short window | Burn rate | Budget consumed |
| --- | --- | --- | --- | --- |
| Page | 1 h | 5 min | 14.4 | 2% |
| Page | 6 h | 30 min | 6 | 5% |
| Ticket | 3 d | 6 h | 1 | 10% |

The pairs assume a 30-day window; for another, burn rate = budget fraction × window hours ÷ alert-window hours. Express each pair as one PostHog SQL insight returning `min(short burn, long burn)` with a "has value more than" alert at the burn rate. When the short window holds too few events to mean anything, lengthen both windows or probe with synthetic traffic. Set the check interval at or below the short window; where the plan's finest interval is coarser, note it in the alert and treat the page as late.

Then:

- **One alert per named failure mode and per sustaining loop**: queue depth, consumer lag, DLQ size, oldest message age, each with a bound derived from the SLO's latency bar. Gauges come from `posthog:instrument-metrics`.
- **Page** on user impact, data loss, or a security event, and open a ticket (Linear) for everything else.
- **Latency alerts use percentiles**; averages hide the tail.
- **Missing data is a decision**: for each alert write whether silence means healthy or broken, and add a volume-floor alert on valid events ("has value less than" a floor) so an outage that stops traffic still alerts.

Author log and error alerts through `posthog:authoring-log-alerts` and `posthog:authoring-error-tracking-alerts`, and SLO alerts as PostHog insight alerts.

**Done when** every named failure mode and loop has an alert, each alert is page or ticket with its missing-data decision, and a back-test over recent data shows it would have fired on the last known bad period or stayed quiet through a good week.

## 4. Runbook

One file per alert, `runbooks/<alert-name>.md` in the service repository, five lines (see [references/templates.md](references/templates.md)): what it means, triage query or link, mitigation, rollback, verify recovery. Rollback is a Railway redeploy of the last good deployment, run through `use-railway`.

**Done when** each alert's message links its runbook, and someone who did not write the service could run the triage line.

## 5. Health endpoints

- **Liveness** returns 200 when the process can answer, with no I/O; a failed dependency must not restart healthy processes.
- **Readiness** checks the service's own hard dependencies (the datastore it cannot answer without) and its initialisation, and no other service.
- On Railway the healthcheck gates a deploy only and is never polled afterward, so runtime failure comes from the step 3 alerts. Where a platform removes unready instances at runtime, confirm it keeps serving when every instance fails together.

**Done when** killing the datastore in staging turns readiness red while liveness stays green, and stopping a downstream service changes neither.

## 6. Prove before launch

Staging only, with autoscaling and replica growth pinned off so a run ends at the breaking point, never at the bill.

- **Load to failure** (catalogue "Never loaded to failure"): a ramping arrival-rate script whose thresholds sit inside it: the SLI's latency bar and error rate, with `abortOnFail`, so the run stops at the first failure and exits non-zero. Record the arrival rate at that point, the first resource to saturate, whether the service sheds load or collapses, and whether it recovers once load drops.
- **One fault per external dependency** (latency past the caller's timeout, or errors), each as an experiment card ([references/templates.md](references/templates.md)): a numeric steady state read before injection, one variable changed, a scripted abort that restores the system within 30 s, and a written learning with a tracked fix.

**Done when** the breaking point and its first bottleneck are written down, every dependency has a card with a measured result, and every learning has a ticket.

## 7. Hand off to `shipper`

Give `shipper` a table of alert name, page or ticket, and runbook path, plus the load result and experiment cards.

**Done when** `shipper`'s observability line names each alert.

## 8. Postmortem

After a page, an SLO miss, or data loss, write a one-page blameless postmortem within a working week ([template](references/templates.md)): impact, timeline, contributing causes, what went well, what went wrong, where we got lucky, actions. Every action carries an owner, a due date, and a Linear ticket.

**Done when** a second person has reviewed it and every action is ticketed.
