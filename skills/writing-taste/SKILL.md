---
name: writing-taste
description: Taste library of how the highest-signal writers think and write. Use before drafting or revising essays, technical posts, product or leadership writing, research explainers, engineering design docs, and systems papers, to borrow the matching moves and run the pre-send checklist. Voice stays with write-like-shiv.
---

# Writing taste

A library of moves studied from the highest-signal writers, so prose earns its conviction. `write-like-shiv` owns the voice; this skill supplies the thinking and craft that voice applies.

**Dvandva.** Run `dvandva` before you produce the piece.

## Use it

1. Name the piece and read its reference.
   - Engineering design doc (HLD, LLD, or a decision that answers requirements that already exist): [`references/genres/design-doc.md`](references/genres/design-doc.md), then the exemplar it names.
   - Systems research paper: [`references/genres/systems-paper.md`](references/genres/systems-paper.md).
   - Essay, technical post, product or leadership writing, or research explainer: one or two matching studies in [`references/studies/`](references/studies/). Each ends with an exercise.
2. Think before writing: draft the core claim in one sentence. If you cannot, you do not understand the subject yet; write to find out, then rewrite. For a design doc, that sentence is the decision plus the boundary invariant.
3. Draft, then run that reference's checklist and fix every miss. Essays, posts, and explainers use the checklist below.

## Principles

Promoted only after a pattern appears in two or more studies, each naming its sources.

- **Start from what the reader already accepts, then climb one step at a time.** Open with the claim in its most obvious form, and let each step add exactly one new demand until you reach the part that surprises. Graham pushes a shared experience to a shocking conclusion; Bussink climbs from a query that needs no decoding to one that needs every value; Saarinen grants that building is cheap, then shows the bill moved to carrying. ([Graham, words](references/studies/2026-10-11-putting-ideas-into-words.md); [Bussink, Neki](references/studies/2026-10-12-designing-neki-for-performance.md); [Saarinen, features](references/studies/2026-10-13-every-feature-should-earn-its-place.md))
- **Name the default you are breaking, and give it its due.** State the convention or usual approach plainly, and its real benefit, before departing from it. Graham names the polite fiction that you wrote what you already thought; Bussink calls decode-everything "a sensible default"; Saarinen calls "just build it and see" a tactic that works for exploration before saying it is not free. (Graham, words; Bussink, Neki; Saarinen, features)
- **Concede with a boundary.** Answer the strongest counterexample by stating exactly where the claim stops holding, not by retreating. Graham fences off chess and math; Bussink gives aggregates their own section; Saarinen keeps cheap building for prototypes and isolated experiments, and stops the claim at features that enter the product. (Graham, words; Bussink, Neki; Saarinen, features)
- **Tell the reader where they are.** Use transitions that place the reader in the argument or pose the next question, so the piece needs few headings to stay navigable. Graham: "This much, I assume, won't be that controversial"; Bussink: "but what if it did?"; Saarinen: "In a world where building is easy, the real cost comes later." (Graham, words; Bussink, Neki; Saarinen, features)
- **End at the claim's true size.** Close by stating how far the idea reaches, including the case where it stops, instead of inflating it. Graham ends on necessary but not sufficient; Bussink ends on the one query that must go through every layer; Saarinen ends by flipping the reason—existence is expensive, not implementation. (Graham, words; Bussink, Neki; Saarinen, features)

## Candidate moves (one study each)

- **Writing is the test of the idea.** Write to find out what you think; expect half the ideas to arrive while writing. (Graham, words)
- **Pass the neutral stranger.** Reread as a reader who knows only the page; add what they need even if it costs nice sentences. (Graham, words)
- **One running example, one change per section.** Keep a single concrete example (a table, a query, a user) and change one thing per section, so the reader tracks the idea instead of new setups. (Bussink, Neki)
- **Show the rejected path in real code.** Put the usual approach on the page, ideally from your own earlier system, so the cost is visible before the alternative. (Bussink, Neki)
- **Pay the bill for the cleverness.** After the win, list the invariants it depends on and what breaks if they fail. (Bussink, Neki)
- **Point at the oddity.** When the principle produces a surprising result, call it out; it is the best evidence the principle is real. (Bussink, Neki)
- **Rename the cost the reader forgot.** When a popular story says one thing got cheap, name the cost that moved elsewhere and make that the claim. (Saarinen, features)
- **Name the harder failure mode.** Prefer the case that looks like success (partial adoption that sticks) over the obvious failure everyone already fears. (Saarinen, features)
- **Flip the reason in the last line.** Restate the rule, then change *why* it holds, so the ending sharpens the claim instead of repeating the title. (Saarinen, features)

## Checklist before sending

- The core claim fits in one sentence, and the opening states it in its most obvious form.
- Each section or step adds exactly one new demand or idea.
- The default being broken is named, with its real benefit, before the alternative.
- A neutral stranger would find it correct and complete.
- The strongest objection is answered, with the boundary of the claim stated.
- Every abstraction has one concrete example, image, or piece of real code.
- Each paragraph moves the argument; asides live in notes or are cut.
- The ending is as strong as the evidence and no stronger.

## Genres

- [Engineering design doc](references/genres/design-doc.md): HLD and LLD after requirements exist, from the decision down to the detail a reviewer must see. Exemplars: [how to write one](references/genres/design-docs-at-google.md), [a requirements-driven decision](references/genres/oxide-rfd-110.md).
- [Systems research paper](references/genres/systems-paper.md): Dynamo and the S3 ShardStore paper. Requirements up front, lessons from production, and where a paper parts from an internal design doc.

## Studies

- [Paul Graham, "Putting Ideas into Words"](references/studies/2026-10-11-putting-ideas-into-words.md): entrepreneurial essay on writing as the test of ideas.
- [Dirkjan Bussink, "Designing Neki for performance"](references/studies/2026-10-12-designing-neki-for-performance.md): technical post that teaches a layered design by climbing one query at a time.
- [Karri Saarinen, "Every feature should earn its place"](references/studies/2026-10-13-every-feature-should-earn-its-place.md): product essay that separates the cost of building from the cost of carrying.

## Sources

[`references/tastemakers.md`](references/tastemakers.md) is the roster of writers and where they publish.
