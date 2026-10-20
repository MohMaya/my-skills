---
name: writing-taste
description: Taste library of how the highest-signal writers think and write. Use before drafting or revising essays, technical posts, product or leadership writing, research explainers, engineering design docs, and systems papers, to borrow the matching moves and run the pre-send checklist. Voice stays with write-like-shiv.
---

# Writing taste

A library of moves studied from the highest-signal writers, so prose earns its conviction. `write-like-shiv` owns the voice; this skill supplies the thinking and craft that voice applies.

**Dvandva.** Run `dvandva` before you produce the piece.

**Write for the human reader.** A person reads the page slowly, once, and has to understand it deeply, so take the time that reader deserves. Care shows on the page: each fact said once, in one place, and current; the reader's path in order; nothing left for them to reconcile. A page that clears this bar serves an agent too, without bloat or drift.

## Use it

1. Name the piece and read its reference.
   - Engineering design doc (HLD, LLD, or a decision that answers requirements that already exist): [`references/genres/design-doc.md`](references/genres/design-doc.md), then the exemplar it names.
   - Systems research paper: [`references/genres/systems-paper.md`](references/genres/systems-paper.md).
   - Essay, technical post, product or leadership writing, or research explainer: one or two matching studies in [`references/studies/`](references/studies/). Each ends with an exercise.
2. Think before writing: draft the core claim in one sentence. If you cannot, you do not understand the subject yet; write to find out, then rewrite. For a design doc, that sentence is the decision plus the boundary invariant.
3. Draft, then run that reference's checklist and fix every miss. Essays, posts, and explainers use the checklist below.

## Principles

Promoted only after a pattern appears in two or more studies, each naming its sources.

- **Start from what the reader already accepts, then climb one step at a time.** Open with the claim in its most obvious form or on a scene the reader already lives in, and let each step add exactly one new demand until you reach the part that surprises. Graham pushes a shared experience to a shocking conclusion; Bussink climbs from a query that needs no decoding to one that needs every value; Saarinen grants that building is cheap, then shows the bill moved to carrying; Rivaton and Southwood open on a YC-runs-San-Francisco analogy the reader already feels, then climb from firm cases to the cadre scorecard to the Chicago rhyme; Mann opens on a pricey cooktop and "What on earth is Dekton?" before any kiln or chemistry. ([Graham, words](references/studies/2026-10-11-putting-ideas-into-words.md); [Bussink, Neki](references/studies/2026-10-12-designing-neki-for-performance.md); [Saarinen, features](references/studies/2026-10-13-every-feature-should-earn-its-place.md); [Rivaton & Southwood, China](references/studies/2026-10-14-chinas-growth-machines.md); [Mann, porcelain](references/studies/2026-10-18-everything-rhymes-with-porcelain.md))
- **Name the default you are breaking, and give it its due.** State the convention or usual approach plainly, and its real benefit, before departing from it. Graham names the polite fiction that you wrote what you already thought; Bussink calls decode-everything "a sensible default"; Saarinen calls "just build it and see" a tactic that works for exploration before saying it is not free; Rivaton and Southwood state the Western story that Beijing picks winners, then replace it with a tournament of cities. (Graham, words; Bussink, Neki; Saarinen, features; Rivaton & Southwood, China)
- **Concede with a boundary.** Answer the strongest counterexample by stating exactly where the claim stops holding, not by retreating. Graham fences off chess and math; Bussink gives aggregates their own section; Saarinen keeps cheap building for prototypes and isolated experiments, and stops the claim at features that enter the product; Rivaton and Southwood put overcapacity, fudged GDP, and deal-greasing corruption on the page so the tournament claim survives its failure modes. (Graham, words; Bussink, Neki; Saarinen, features; Rivaton & Southwood, China)
- **Tell the reader where they are.** Use transitions that place the reader in the argument or pose the next question, so the piece needs few headings to stay navigable. Graham: "This much, I assume, won't be that controversial"; Bussink: "but what if it did?"; Saarinen: "In a world where building is easy, the real cost comes later."; Rivaton and Southwood: headings that name the next demand ("Local heroes"; "Growth is the best policy"; "The Chicago way"). (Graham, words; Bussink, Neki; Saarinen, features; Rivaton & Southwood, China)
- **End at the claim's true size.** Close by stating how far the idea reaches, including the case where it stops, instead of inflating it. Graham ends on necessary but not sufficient; Bussink ends on the one query that must go through every layer; Saarinen ends by flipping the reason—existence is expensive, not implementation; Rivaton and Southwood end by refusing the fashionable ask for a new model and naming the old one the West abandoned. (Graham, words; Bussink, Neki; Saarinen, features; Rivaton & Southwood, China)
- **Rename the story the reader brought.** When a popular account misnames the cost or the actor, swap the label and make the new name the claim. Saarinen renames cheap building so the bill that still bites is *carrying*; Rivaton and Southwood rename China's "command economy" as a continent-sized tournament of local growth machines. (Saarinen, features; Rivaton & Southwood, China)
- **Hold one subject and change one axis at a time.** Keep a single concrete example through the piece, and let each step alter one demand on it, so the reader tracks the idea instead of new setups. Bussink climbs one query from decoding nothing to decoding every value; Rieseberg keeps one quarterly deck and changes only the kind of ambition. ([Bussink, Neki](references/studies/2026-10-12-designing-neki-for-performance.md); [Rieseberg, ambition](references/studies/2026-10-15-how-to-be-more-ambitious.md))
- **Rhyme the unfamiliar case with one the reader already knows.** Pair a distant or foreign case with a familiar one of the same shape, so the lesson lands as recognition, not import. Rivaton and Southwood close by finding China's growth machine in Daley, Moses, and Hartsfield; Mann sets porcelain's resurgence beside iron's Bessemer-era second flowering, and calls Renaissance china sets "the private jets and invite-only clubs of the Renaissance era." ([Rivaton & Southwood, China](references/studies/2026-10-14-chinas-growth-machines.md); [Mann, porcelain](references/studies/2026-10-18-everything-rhymes-with-porcelain.md))

## Candidate moves (one study each)

- **Writing is the test of the idea.** Write to find out what you think; expect half the ideas to arrive while writing. (Graham, words)
- **Pass the neutral stranger.** Reread as a reader who knows only the page; add what they need even if it costs nice sentences. (Graham, words)
- **Show the rejected path in real code.** Put the usual approach on the page, ideally from your own earlier system, so the cost is visible before the alternative. (Bussink, Neki)
- **Pay the bill for the cleverness.** After the win, list the invariants it depends on and what breaks if they fail. (Bussink, Neki)
- **Point at the oddity.** When the principle produces a surprising result, call it out; it is the best evidence the principle is real. (Bussink, Neki)
- **Name the harder failure mode.** Prefer the case that looks like success (partial adoption that sticks) over the obvious failure everyone already fears. (Saarinen, features)
- **Flip the reason in the last line.** Restate the rule, then change *why* it holds, so the ending sharpens the claim instead of repeating the title. (Saarinen, features)
- **Cases first, scorecard second.** Show named actors winning or losing before you open the incentive file that explains them, so the system feels discovered. (Rivaton & Southwood, China)
- **Split the slogan, then skip the settled kind.** Break a command the reader already repeats into a few kinds, grant the kind that already works, and teach only the rest. (Rieseberg, ambition)
- **Demand the instrument, not the costume.** When a fancier version would only change the voice or the role, name the raw material, the method a leading practitioner would use, and a judge other than the maker. (Rieseberg, ambition)
- **Give the opening question two true answers.** One makes the thing new, the other makes it old; state the gap between them as the claim. (Mann, porcelain)
- **Explain the failure by the missing fact.** Teach the mechanism first, then tell the history through what people did not know, so centuries of failure read as proof of the mechanism. (Mann, porcelain)

## Checklist before sending

- The core claim fits in one sentence, and the opening states it in its most obvious form.
- Each section or step adds exactly one new demand or idea.
- When a tutorial or a design is taught by climbing, one concrete subject carries it, and each step changes one thing about that subject.
- The default being broken is named, with its real benefit, before the alternative.
- A neutral stranger would find it correct and complete.
- The strongest objection is answered, with the boundary of the claim stated.
- Every abstraction has one concrete example, image, or piece of real code.
- Each paragraph moves the argument; asides live in notes or are cut.
- The ending is as strong as the evidence and no stronger.
- If the piece renames a popular story, the new name appears early and the rest of the argument is evidence for the swap.

## Genres

- [Engineering design doc](references/genres/design-doc.md): HLD and LLD after requirements exist, from the decision down to the detail a reviewer must see. Exemplars: [how to write one](references/genres/design-docs-at-google.md), [a requirements-driven decision](references/genres/oxide-rfd-110.md).
- [Systems research paper](references/genres/systems-paper.md): Dynamo and the S3 ShardStore paper. Requirements up front, lessons from production, and where a paper parts from an internal design doc.

## Studies

- [Paul Graham, "Putting Ideas into Words"](references/studies/2026-10-11-putting-ideas-into-words.md): entrepreneurial essay on writing as the test of ideas.
- [Dirkjan Bussink, "Designing Neki for performance"](references/studies/2026-10-12-designing-neki-for-performance.md): technical post that teaches a layered design by climbing one query at a time.
- [Karri Saarinen, "Every feature should earn its place"](references/studies/2026-10-13-every-feature-should-earn-its-place.md): product essay that separates the cost of building from the cost of carrying.
- [Robin Rivaton & Ben Southwood, "China's growth machines"](references/studies/2026-10-14-chinas-growth-machines.md): economics explainer that replaces Beijing-as-command with a tournament of local growth machines.
- [Felix Rieseberg, "How to be more ambitious"](references/studies/2026-10-15-how-to-be-more-ambitious.md): tutorial that turns a rallying cry into three climbs on one ordinary task.
- [Charles C. Mann, "Everything rhymes with porcelain"](references/studies/2026-10-18-everything-rhymes-with-porcelain.md): science explainer that answers a kitchen question twice, new material and ancient porcelain.

## Sources

[`references/tastemakers.md`](references/tastemakers.md) is the roster of writers and where they publish.
