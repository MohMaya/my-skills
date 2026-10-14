# Engineering design doc

Written after the requirements exist. It records the decision and the design that follows, between a trade-off argument and an implementation spec. One shape, from the decision down to the detail a reviewer has to see.

A component is a mini doc of 1–3 pages, same parts, terser. A platform is two documents: a high-level design (HLD) and a separate low-level design (LLD). The HLD ends by marking where design stops and specification starts, and the LLD opens by pointing back. Mixing the two at one heading level hides that line. A 15,000-word doc for one component is the wrong altitude: split it, or cut it.

Read the exemplar that matches the job, then draft:

- How to write one, and when not to: [Design Docs at Google](design-docs-at-google.md).
- A decision that answers requirements that already exist: [Oxide RFD 110](oxide-rfd-110.md).

## Terms

Link each organizational term to the canonical glossary that owns it, internal engineering and external-facing. A glossary inside the doc drifts the day that definition changes.

Define a term locally only when it is new and absent from that glossary, and mark it as a candidate to add there. If no canonical glossary exists, say so once and link the document that owns the concept.

## Style

Present tense, active voice. Invariants, not hopes. A number, not an adjective. The diagram comes before the prose about the same structure. Every choice carries its reason beside it.

## Shape

Skip a part that does not apply. A concern with no impact is one line that says so. A heading whose body is "None" or "TBD" is an unfinished decision.

1. **Header and reader routing.** Status, author, reviewers, link to the requirements. One line on who reads which parts: where a reviewer who only needs the decision can stop, and what a reviewer who must check the design reads through.
2. **Requirement and decision.** Two to four sentences: what the requirements demand, and the decision this doc makes. Then one line, the thesis or the boundary invariant: what this design owns, and what it never does. Link the requirements. Do not restate them.
3. **Context.** Facts only: the current system, the constraints, the forces. Pain points appear only when engineering started the work.
4. **Goals and non-goals.** Goals are checkable. A non-goal is something a reasonable reader would expect in scope, ruled out on purpose. A deferred item is marked "designed for, deferred" and names the trigger that reopens it.
5. **System context and boundary.** A context diagram first: what calls this system, and what it calls. Then an ownership and guarantees table: the caller owns X; this system guarantees Y.
6. **High-level design.** One numbered end-to-end flow. Key decisions as a table or list, each with a one-clause reason. Failure semantics and idempotency stated as guarantees.
7. **Alternatives considered.** In the body, not an appendix. For each real option: what it would buy, and why it lost against the stated goals. Name the ideal option that is not available yet, and what would unlock it. Name the fallback and the trigger that selects it.
8. **Low-level design.** Data model, interfaces, algorithms, and state machines, with a sequence diagram before the prose. Sketch an API or a schema only where it bears on a trade-off or is a contract others depend on. Extensibility is a recipe: the cost of the N+1 case. On a platform, stop at the marker and continue in the LLD.
9. **Cross-cutting.** Security and privacy, observability, scale and cost, migration and rollout (flags, order, rollback), operational ownership. One line when a concern has no impact. Skip a concern that does not apply.
10. **Risks.** One table: risk, likelihood, impact, mitigation.
11. **Untested assumptions.** What the design relies on that nobody has tested or verified, so a reviewer can attack it.
12. **Open questions.** Each has an owner. When it is answered, fold the answer into the body and remove the question.
13. **Why this shape.** Optional, and only on a platform-scale doc. A short closing argument for the shape as a whole, after the decisions are already on the page.

## Before sending

- The decision and the boundary invariant are in the opening, and the requirements are linked, not copied.
- Every organizational term links to its canonical source, or is flagged as a new candidate.
- The context diagram precedes the prose about the boundary. The ownership table states guarantees.
- Each decision has its reason. Each real alternative says what it would buy and why it lost. No straw man, and no "rejected by consensus" with no reason.
- Failure behavior and idempotency are guarantees. Risks are one table, not scattered sentences.
- Assumptions nobody has tested are listed. Open questions have owners; answered ones are gone from the list.
- Code, decorators, and full schemas appear only where they decide a trade-off or bind another team.
- The doc was rewritten. Strikethroughs and ticket-numbered bolt-on sections are not history; they are an unrevised draft.
- HLD and LLD are separate documents when the scope is a platform, with the marker between them.
