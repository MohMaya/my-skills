---
name: diagnosing-bugs
description: Diagnose hard bugs and performance regressions using reproducible signals, falsifiable hypotheses, and targeted verification.
---

# Diagnosing Bugs

Use the stages that reduce uncertainty for this bug. Scale investigation and verification to its impact and available evidence.

When exploring the codebase, read `CONTEXT.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against env vars, so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal.

If available evidence is insufficient, name the missing signal and continue independent investigation. Ask for access or a redacted artifact when needed.

## Phase 1: Build a feedback loop

Build a pass/fail signal for the reported symptom when practical. Use it for bisection, hypothesis testing, and targeted instrumentation.

Invest in a useful signal. Stop improving the harness when it can distinguish the likely causes and verify the fix.

### Ways to construct one, in roughly this order

1. **Failing test** at whatever seam reaches the bug: unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) that drives the UI and asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** For intermittent wrong output, test generated inputs with a recorded seed and a bounded trial count.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **HITL bash script.** Last resort. If a human must click, drive _them_ with `scripts/hitl-loop.template.sh` so the loop is still structured. Captured output feeds back to you.

Use the loop to distinguish causes and verify the eventual fix.

### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

Prefer a fast, repeatable loop. Slow or imperfect signals remain useful when stronger evidence is unavailable.

### Non-deterministic bugs

Increase the reproduction rate with repeated triggers, controlled concurrency, or narrowed timing windows where safe. Record the trial count and observed failures. Choose enough trials to test the hypothesis without unbounded stress or load.

### When you genuinely cannot build a loop

State what prevents reproduction. Continue with incident traces, logs, code paths, configuration differences, or a known-good comparison. Label hypotheses as unconfirmed. Ask only for the access, redacted artifact, or production instrumentation approval needed to resolve the gap. A missing reproduction limits confidence; it does not block read-only diagnosis.

### Preferred signal: a loop that catches the bug

When available, run a command that reaches the bug and record its decisive result. Aim for a signal with these properties:

- [ ] **Red-capable**: it drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. Not "runs without erroring"; it must be able to _catch this specific bug_.
- [ ] **Deterministic**: same verdict every run (flaky bugs: a pinned, high reproduction rate, per above).
- [ ] **Fast enough** to support repeated investigation.
- [ ] **Agent-runnable** where possible. Use `scripts/hitl-loop.template.sh` when human interaction is needed and the template fits.

Read relevant code and form tentative hypotheses whenever that helps construct the signal. Keep observed facts separate from inferred causes.

## Phase 2: Reproduce + minimise

When reproduction is available, run the loop and inspect the failure. Otherwise, use the alternative evidence from Phase 1.

Confirm:

- [ ] The loop produces the failure mode the **user** described, not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

### Minimise

Once it's red, shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut, and keep only what's load-bearing for the failure.

Why bother: a minimal repro shrinks the hypothesis space in Phase 3 (fewer moving parts left to suspect) and becomes the clean regression test in Phase 5.

Stop minimising when the scenario isolates the responsible behavior and supports a useful check. Full minimisation is optional when its cost exceeds its diagnostic value.

## Phase 3: Hypothesise

Rank plausible hypotheses by evidence and the cost of falsification. Consider alternatives when the evidence permits more than one explanation.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe: discard or sharpen it.

Share material uncertainty or a finding that changes the investigation. Continue authorized probes without a confirmation checkpoint.

## Phase 4: Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

**Perf branch.** For performance regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5: Fix + regression test

Apply a fix when implementation is authorized and evidence supports the cause. A diagnosis-only request ends with the finding and verification limits.

Write the regression test **before the fix**, but only if there is a **correct seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

## Phase 6: Cleanup

Required before declaring done:

- [ ] Original reproduction passes, or alternative evidence and remaining verification limits are stated
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes deleted (or moved to a clearly-marked debug location)
- [ ] The supported cause and any remaining uncertainty are stated in the final report and any commit / PR message
