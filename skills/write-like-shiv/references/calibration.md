# Calibration and checks

## What is known

Version 1 is based on explicit writing preferences, named reading influences, and inspected source passages. No verified set of independently authored, representative Shiv prose samples has been established. Confidence is high about the explicit preferences, moderate about the proposed synthesis, and unknown about a numerical personal style fingerprint.

The April 15, 2026 “Writing Voice” document was retrieved as a model-generated writing block. Its rules are supported by prior user instructions, but its examples are not evidence that Shiv experienced the events they describe. Several examples use patterns the same guide bans. Preserve the explicit preferences; do not use those examples as imitation targets.

The May 2026 Cosmic Agency guide is a public brand source. Its preference for em dashes and ideological themes has narrower scope than Shiv's general voice. The September 7 “Voice & Writing Craft” page explicitly keeps private reflection separate from that brand voice.

## Revision example

**Fictional supplied facts:** an importer sustained 330 objects per second on one run; database capacity was not measured; a rewrite has been proposed.

**Generic draft:**

> In today's fast-paced landscape, leveraging a robust rewrite is a game-changer. It will unlock significant throughput improvements, ensuring seamless scalability. It's not just about speed, it's about transforming the entire pipeline.

**Revision using the same evidence:**

> The importer sustained 330 objects per second in one run. That result does not tell us whether a rewrite would help. Measure where the time goes before choosing a new language. If the database is saturated, faster parsing will leave the main constraint in place.

The revision removes promises that the facts cannot support, keeps the unit “objects,” and identifies the missing measurement. The longer conditional sentence earns its length by carrying the decision boundary. This is an original illustration, not a user-approved voice sample.

## What the checker measures

Run `python3 <skill-directory>/scripts/voice_check.py <draft-file>`. It reports local editorial candidates and simple rhythm diagnostics. It skips fenced code, Markdown blockquotes, headings, table rows, standalone URLs, and inline code. It is a lightweight Markdown heuristic, not a full parser. Inline quotations and unusual markup can still produce false positives; inspect the reported context before editing.

| Output | Purpose and consumer | Limit |
| --- | --- | --- |
| findings | Lets the writing agent locate stock language, a formulaic contrast, or repeated openings | A finding is a review candidate. The checker cannot determine whether the phrase is quoted, necessary, ironic, or explicitly requested. |
| rhythm | Gives the editor sentence count, mean words per sentence, sentence lengths, and coefficient of variation | The segmentation is heuristic. Abbreviations, equations, and multilingual text can distort it. No personal target is inferred. |
| notes | Keeps measurement exclusions and limits beside the result | Removing these would make an approximate diagnostic easier to mistake for a style score. |

The coefficient of variation is population standard deviation divided by the mean sentence length. It is reported only for at least eight nonempty detected sentences; eight is a conservative display threshold chosen for this tool, not a validated research cutoff. A uniform set of instructions can be excellent. Do not maximize this metric or call it perplexity.

Default execution exits successfully after reporting. `--strict` returns exit code 1 if it finds review candidates, allowing an application to require manual review before publication. That is an optional editorial gate, not proof of bad prose or AI authorship. No external publishing hook is installed by this skill.

Code map: `prose_lines` is called by the CLI to isolate likely authored prose while preserving source line numbers; without it, quoted passages and code dominate false positives. The remaining top-level CLI reads the file, produces the report, and sets the requested exit status; without it the skill has no repeatable local check.

## How to improve the voice model

Collect a small set of real pieces across the surfaces Shiv actually uses. For each, retain the task, audience, draft, Shiv's revision, and the reason for the change. Keep factual context with the sample. Separate liked passages by other authors from Shiv's own prose.

Compare candidate output with its baseline on factual fidelity, usefulness to the reader, specificity, reasoning, rhythm, and recognizability to Shiv. Prefer a blind comparison when it is convenient. A winning example is evidence for that surface; it is not a universal law.

Before tightening a style rule, check another relevant piece. Keep the shortest correction that explains the repeated preference. Do not accumulate a ban for every word disliked once. Do not send private drafts to detection or comparison services unless Shiv requests that action.
