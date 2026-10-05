---
name: bar-raiser
description: Principal-engineer excellence review of a plan, diff, module, or service. Sweeps for architecture, data, reliability, performance, and code-design anti-patterns, then drills each finding to the best design, unconstrained by what the codebase or tooling already does. Use before calling any work done, when reviewing a plan, diff, or PR, and when auditing a codebase's architecture or quality.
---

# Bar raiser

Hold the bar a world-class engineering organization holds, independent of who wrote the work or what it cost to get here. Good is below the bar. The existing codebase is evidence of what is, never precedent for what should be: judge every design from first principles, then cost the path to the best one.

## Proportion

Sweep depth scales with blast radius, and nothing is exempt:

| Target | Sweep |
| --- | --- |
| A local fix with no new behavior | The catalogue sections the changed lines touch |
| A feature or refactor | Every catalogue section, against the diff and the modules it touches |
| A new service, data model, public API, migration, or infrastructure | Everything below, including numbers and the failure walkthrough for every external call |

One owner per concern: SQL and ORM queries go through `query-design`, whose findings count here; module depth and seams use the `codebase-design` vocabulary; UI goes to `pe-review`; Cubic findings to `cubic-review`.

## 1. Map

Write down, before judging:

- **Job**: what the work is for and who calls it.
- **Invariants**: what must always hold, including absences ("nothing outside `billing/` writes invoices").
- **Data path**: where each piece of data lives, and per operation the rows, bytes, and round trips, each priced against [the latency table](references/catalogue.md#numbers).
- **Effects**: every external call and every piece of state mutated.
- **Change friction** (codebase audits): files that change together, from `git log --format= --name-only` over recent history.

**Done when** every item is written, with numbers as orders of magnitude.

## 2. Sweep

Walk [references/catalogue.md](references/catalogue.md) section by section against the target. Record each hit as a candidate: the smell, `file:line` evidence, and the catalogue entry.

For every external call (network, database, queue, file system), answer: what happens when it times out, succeeds but the reply is lost, runs twice, arrives out of order, or runs concurrently with itself?

**Done when** each in-scope catalogue section is marked with its hits or "clear", and every external call has all five answers.

## 3. Drill

Take each candidate through five parts:

1. **Ideal**: the best design for the job if nothing existed (no legacy code, schema, framework, or tooling constraint), named concretely.
2. **Alternatives**: at least one more materially different design. The current code does not count as an alternative.
3. **Gap**: the cost of reaching each design (files, migrations, backfills, risk) against the cost of leaving the smell (incidents, latency, change friction).
4. **Decision**: the chosen design and the first step that closes most of the gap. Replace a bad boundary or data model piece by piece behind a seam; a whole-product rewrite discards the bug fixes the old code encodes.
5. **Proof**: the test, measurement, assertion, or metric that will show it worked.

Keep the arguments honest. A performance claim needs a measured hot path or a back-of-envelope number. A simplicity claim names the braided construct (state with time, a decision leaked across modules), not a preference. Label every finding **measured**, **sourced** (a catalogue citation), or **judgment**; only measured and sourced findings block, and judgment findings go to Shiv as questions.

A candidate leaves the list only with the written sentence explaining why it is fine. If you cannot write that sentence, it is not fine.

**Done when** every candidate has all five parts, or its dismissal sentence.

## 4. Scope

- **Inside the blast radius** (code the change writes, or behavior it alters): fix it in this change.
- **Outside**: raise it as a drilled proposal, all five parts, for Shiv to schedule. Every finding reaches him.
- **Contract changes** (API shape, schema, staleness, cost): state the objection once with a recommendation and follow Shiv's call.

## 5. Verdict

Severity: **critical** (data loss or corruption, security, outage, wrong money), **major** (design that compounds: leaked decisions, invariants held only in application code, unbounded work, non-idempotent effects), **minor** (local clarity).

- **excellent**: no critical or major findings remain, and every fix is verified.
- **below bar**: the work is not done until each finding is fixed and verified, or Shiv accepts it in writing.

Report:

1. Verdict, in one line.
2. Findings, most severe first: `file:line`, smell, why (with source), ideal, decision and first step, proof, evidence tier.
3. Proposals outside the change's scope.
4. What was not checked, and why.
