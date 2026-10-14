# How to write a design doc — Malte Ubl

- Link: https://www.industrialempathy.com/posts/design-docs-at-google/
- Author: Malte Ubl, 6 July 2020
- Genre: guidance for an engineering design doc
- Use when: you are drafting or reviewing a design doc and need the altitude, and the reason each part exists.

## What it teaches

Trade-offs are the point. The doc records the high-level strategy and the key decisions, with the trade-offs considered. A doc that only says how the system will be implemented, with no trade-off and no alternative, is an implementation manual. Write the code instead.

Context is facts, not requirements. Objective background, short, with the detail linked. Some previous knowledge can be assumed.

Non-goals are plausible goals ruled out, not negated goals such as "the system should not crash." His example is ACID compliance while designing a database: the reader needs to know whether it is a goal, and a team may still pick a solution that provides a non-goal when that does not block a goal.

The design opens with a system-context diagram, so the reader places the new system in a landscape they already know.

Sketch only the API and the data that bear on the design and its trade-offs. Full interface definitions and complete schemas are verbose, hide the decision, and go stale. Code and pseudo-code appear for a novel algorithm; otherwise link a prototype.

Alternatives considered is among the most important sections. Succinct on the options not chosen is fine. The section has to show why each loses against the goals, including the option the reader is already wondering about.

Cross-cutting concerns (security, privacy, observability, and whatever the organization standardizes) get a short section on how the design affects them, or a link to a dedicated doc. Engage those reviews while the design can still change.

Length scales with the problem. About 10–20 pages for a large project; past that, split the problem. A 1–3 page mini doc is right for an incremental change, and it still does the same steps, terser.

Keep the doc updated while the system has not shipped. When a later change lands in a new document, link that amendment from the original. Re-read the doc a year or two later and write down what the decision got wrong.

Write a doc when the solution is ambiguous, when senior review would change it, when the design needs consensus, or when the team forgets cross-cutting concerns. Skip it when the design is obvious.

## Where this shape stops

Ubl stops at the decision and the trade-off, and says the form should follow the project. The [design doc](design-doc.md) keeps that rule (skip a part that does not apply) and continues into low-level design where a contract or a trade-off requires it. It stops before an implementation spec.
