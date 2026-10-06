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
| A local fix with no new behavior | The catalogue sections the changed lines touch; the report fits in a few lines |
| A feature or refactor | Every catalogue section, against the diff and the modules it touches |
| A new service, data model, public API, migration, or infrastructure | Everything below, including numbers and the failure walkthrough for every external call |

One owner per concern: SQL and ORM queries go through `query-design`, whose findings count here; module depth and seams use the `codebase-design` vocabulary; UI goes to `pe-review`; Cubic findings to `cubic-review`.

## Evidence gate

Treat the implementation, its explanation, and every proposed simplification as claims to disprove. Apply the same scrutiny to your own recommendations and to previously approved changes. User approval authorizes work; it does not establish the truth of the rationale you supplied.

Before accepting a removal or calling work redundant, cheaper, bounded, safe, or idempotent:

1. **Separate correctness from cost.** Prove the observable result and account for the work needed to produce it. Equal outputs and passing tests alone say nothing about rows scanned, bytes transferred, allocations, lock duration, or external effects.
2. **Trace the whole path.** For each boundary, record what enters, what leaves, and where filtering, deduplication, sorting, limiting, validation, or retries actually happen. Work eliminated downstream may already have consumed upstream resources.
3. **Prove the bound.** Name the constraint, limit, or algorithm that enforces it. A bounded number of parents does not bound their children or historical rows. Small fixtures, current observations, and “usually a handful” are assumptions, not enforced bounds.
4. **Try to falsify the claim.** Construct a valid counterexample: large history or fan-out, duplicates, empty inputs, concurrent calls, or partial failure as applicable. For SQL changes, obtain `query-design` evidence for both semantics and execution cost. Test the claimed invariant at the boundary where it matters; final-output assertions can hide excessive intermediate work.
5. **Check the final diff.** Simplification edits invalidate the affected review conclusions. Re-read the changed path and rerun the evidence those edits could invalidate before assigning a verdict. Record the reviewed revision or diff and any remaining material uncertainty.

For example, a Python `set` proves final uniqueness; it does not make SQL `DISTINCT` redundant in cost. The driver may transfer and materialize every duplicate first. Conversely, a database uniqueness constraint may prove that the query cannot return duplicates. Choose from the caller's required cardinality and measured plan; neither “always keep DISTINCT” nor “always remove it” is a review rule.

**Done when** every material claim has its mechanism or evidence, a falsifier, and a checked result. Keep an unverified claim open. A completed checklist or another reviewer's approval cannot close it.

## 1. Map

Write down, before judging:

- **Job**: what the work is for and who calls it.
- **Invariants**: what must always hold, including absences ("nothing outside `billing/` writes invoices").
- **Data path**: where each piece of data lives; rows scanned, returned, transferred, and materialized at each boundary; bytes, round trips, and lock duration per operation. Distinguish enforced bounds from assumed workload sizes and price the work against [the latency table](references/catalogue.md#numbers).
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

Keep the arguments honest. A performance claim needs a measured hot path or a back-of-envelope number. A simplicity claim names the braided construct (state with time, a decision leaked across modules), not a preference. Label every finding **measured**, **sourced** (a catalogue citation), or **judgment**. Measured and sourced findings count toward the verdict; a judgment finding, whatever its severity, goes to Shiv as a question and counts once he agrees.

A candidate leaves the list only with the written sentence explaining why it is fine. If you cannot write that sentence, it is not fine.

**Done when** every candidate has all five parts, or its dismissal sentence.

## 4. Scope

- **Inside the blast radius** (code the change writes, or behavior it alters): fix it in this change.
- **Outside**: list it as a drilled proposal, all five parts, at the end of the report for Shiv to schedule.
- **Contract changes** (API shape, schema, staleness, cost): state the objection once with a recommendation and follow Shiv's call.

## 5. Verdict

Severity: **critical** (data loss or corruption, security, outage, wrong money), **major** (design that compounds: leaked decisions, invariants held only in application code, unbounded work, non-idempotent effects), **minor** (local clarity).

- **excellent**: no measured or sourced critical or major findings remain, every fix is verified against the final diff, and no unverified material claim could conceal such a finding.
- **below bar**: the work is not done until each such finding is fixed and verified, or Shiv accepts it in writing.

Missing evidence is an open verification gap, not a reason to mark a section clear or downgrade a concern to taste. State the limit on the verdict. If a reviewer catches a defect this review should have caught, acknowledge the review failure, reopen the invalidated conclusions, and correct any persistent guidance that taught the faulty rationale. A later fix does not retroactively validate the failed review.

Report:

1. Four header lines: `Snapshot:` the tree you reviewed; `Verdict: excellent` or `Verdict: below bar`; `Skills:` the workflow skills the work used (such as `tdd`, `diagnosing-bugs`, `query-design`); `Tests:` the bug each new test catches, or why the change needs none.
2. Findings, most severe first: `file:line`, smell, why (with source), ideal, decision and first step, proof, evidence tier.
3. Proposals outside the change's scope.
4. The reviewed revision or diff, evidence for material claims, and what was not checked and why.

For code in a git repository, the review gate needs the report recorded. Before you read the diff, print the snapshot you are reviewing; add `--index` to review only the staged changes of a split commit, or `--commit <sha>` for a commit:

```sh
python3 ~/.agents/hooks/review-gate.py tree
```

Fixes made during the review change the snapshot, so take `tree` again on the final state and review that. Then pipe the report in on stdin, so no report file enters the repository:

```sh
python3 ~/.agents/hooks/review-gate.py record --verdict <excellent|below-bar> [--index | --commit <sha>] <<'REPORT'
<the report>
REPORT
```

`record` refuses a report whose `Snapshot:` is not the current code. Only Shiv turns a below-bar review into an accepted one, by replying `accept <snapshot>`.
