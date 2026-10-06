---
name: llm-evals
description: Build or extend the eval harness for an LLM feature — golden sets from real traces, one grader per failure mode, calibrated LLM judges, and a baseline every prompt, model, or judge change is compared against. Use when building an LLM feature, changing its prompt or model, adding an LLM judge, or turning traces into a regression suite.
---

# LLM Evals

An LLM feature's behavior changes when its prompt, model, retrieval, or tools change. The eval harness is the measuring stick for every such change: labeled goldens, one grader per failure mode, and a recorded baseline. Build it before tuning, and re-run the same harness after each change.

Extend the repository's existing evaluation contract and runner when one exists. Keep outcome metrics the product already scores against ground truth, and add this harness where quality needs labeled judgment, such as reasoning, faithfulness, or tool use.

## Loop

1. **Collect traces.** Use production or agent traces when they exist. Without them, generate synthetic tasks across the axes that matter (task type, difficulty, edge case, persona) by sampling their cross-product; free-generated prompts cluster around whatever is easiest to write.
2. **Run error analysis.** Open-code at least 100 traces: read each one and tag failures in your own words, with no fixed taxonomy yet. Then axial-code those tags into 4–8 named failure buckets. Fewer than 4 means the pass was too shallow; more than 8 means buckets need merging. A single-failure-surface task, such as strict-schema extraction, may land at 1–2 buckets with per-field sub-metrics inside one grader.
3. **Write one grader per bucket.** A blended score hides which bucket regressed.
4. **Prioritize** buckets by frequency × severity × value.
5. **Record the baseline** by running the full harness against the current prompt and model.
6. **Change one thing** (prompt, model, retrieval, or tool) and re-run the same harness. Compare per bucket against the baseline, then promote the new result to baseline when it ships.
7. **Reopen error analysis** when production surfaces a failure no bucket covers.

## Goldens

Version goldens like code: commit them, diff them in review, and tag them per release. They double as the regression suite the repository's runner executes in CI. Keep each golden's ID stable so results compare across runs.

## Graders

- **Deterministic first.** Regex, schema validation, exact match with normalization, and sandboxed execution are cheap, reproducible, and need no calibration.
- **LLM judge only for genuinely subjective criteria**, such as tone, faithfulness, or which response is better, where no deterministic check can express the criterion.
- **Binary pass/fail.** Collapse Likert scales to pass/fail; they are noisier to calibrate and apply.

Templates for each grader shape, including the sandbox requirement for execution graders: [references/grader-templates.md](references/grader-templates.md).

## Judge calibration

A bucket routed to an LLM judge needs calibration before its verdicts count beyond exploration. An all-deterministic harness has nothing to calibrate; state that explicitly.

- Label at least 100 items and split them into train, dev, and sealed test. Report on the sealed test once.
- Report TPR and TNR separately. A judge can reach 90% accuracy by always saying pass on a skewed set.
- Pin the judge to a fixed model snapshot. Recalibrate when that snapshot changes, and quarterly regardless.
- Use a judge from a different model family than the model under test.
- A judge that misses the agreed TPR/TNR bar stays advisory: it flags items for human review and never gates a ship decision.

Full protocol, bias correction, and recalibration triggers: [references/judge-calibration.md](references/judge-calibration.md).

## Layout

Keep the harness at a stable path the repository chooses, separate from disposable run output. Each run writes its own results; the harness itself changes only through reviewed commits. A common shape:

```
eval/
├── goldens.jsonl         # labeled traces and synthetic goldens, versioned
├── graders/              # one module per failure bucket
└── baseline.json         # current shipped prompt + model, per-bucket results
runs/<run-id>/results.json
```

## Done

1. At least 100 traces open-coded into 4–8 failure buckets, or the single-surface exception stated.
2. Goldens committed and versioned.
3. One grader per bucket, deterministic first.
4. Every judge calibrated with TPR/TNR, snapshot pinned, and a different family; or judge calibration stated as N/A.
5. Baseline recorded for the current prompt and model.
6. The change under test compared per bucket against that baseline, with the result in the delivery summary.
