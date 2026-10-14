# Surfaces and forms

One row per piece. Read the file it links, apply the voice delta, then run the checklist the row names. [`writing-taste`](../../writing-taste/SKILL.md) owns quality and structure. The delta overrides a checklist line only where the row says so. Do not combine rows.

| Surface | Read, then its checklist | Voice delta |
| --- | --- | --- |
| Vision thesis; product story; founding document; public ambition | [vision.md](vision.md) | ADHD formatting stays off. |
| Ops chat; status; plan; digest | The writing-taste checklist | Action, state, next step, via `i-have-adhd`. Not vision prose. |
| Take; Slack; email; PR discussion | The writing-taste checklist | The recommendation or request, the decisive reason, the material tradeoff, the next action if there is one. Compress context the reader already has. One paragraph can be the whole piece. |
| Technical explanation; engineering article; incident account | One or two matching [studies](../../writing-taste/references/studies/), then the writing-taste checklist | Name the service, table, interface, failure, and unit. An observation is not a cause. A diagram only when it shows a relationship. |
| Engineering design doc; HLD; LLD | [design-doc.md](../../writing-taste/references/genres/design-doc.md), then its Before sending list | Use it for a design doc, not for every engineering reply. |
| Systems research paper | [systems-paper.md](../../writing-taste/references/genres/systems-paper.md), then the writing-taste checklist | No second outline on top of that file. |
| Teacher; tutorial | One or two matching [studies](../../writing-taste/references/studies/), then the writing-taste checklist | Start at the reader's gap. An expert skips the prerequisite. An analogy has a mapping and a limit. |
| Essay | One or two matching [studies](../../writing-taste/references/studies/), then the writing-taste checklist | A scene needs supplied facts. No opening roadmap. |
| Observer; cultural analysis | One or two matching [studies](../../writing-taste/references/studies/), then the writing-taste checklist | Wit aims at the behavior. No invented anecdote, and no motive stated as fact. |
| Manifesto | The writing-taste checklist | A conviction, its grounds, and the commitment that changes an action. Specific enough to settle a choice. |
| Pitch | The writing-taste checklist | What changes, why now, the first customer and wedge, the ability to execute, the ask. Traction stays separate from the plan. A promise connects to a user action. Confidence is not a forecast. |
| Journal; private reflection | The writing-taste checklist. The ending may stay open. | The moment or the tension, what was felt or done. Distress stays distress. No compulsory moral. |
| Philosopher | The writing-taste checklist | A live question, a concrete situation, a position or an open tension. Scale stays tied to that situation. |
| Short public post | The writing-taste checklist | One idea, with enough context to stand alone. Length follows the thought. No bait and no invented extreme. |
| Product copy; onboarding; error | The writing-taste checklist | State, consequence, action. Comprehension over personality. Keep labels consistent. No humor in an error or an irreversible confirmation. No implementation detail that changes no decision. |
| Design critique; product rationale | The writing-taste checklist | The user's task, the friction, why it happens, the change, a criterion someone can check. |

## An original worked example across surfaces

The facts below are fictional and supplied for this exercise: a pilot screens 30 HVAC service tickets; nine need a technician to supply missing equipment history; the review queue is not yet built. These are not claims about Shiv or SmartAC.

**Internal take:**

Keep the pilot in review mode. Nine of the 30 tickets needed equipment history from a technician. Build the review queue before expanding it.

**Technical explanation:**

The pilot screened 30 tickets. Nine needed equipment history that the ticket did not contain, so the system could not complete those cases from its available context. A review queue would make that dependency explicit and give a technician somewhere to supply the missing information. Until it exists, expansion would carry the same unresolved handoff into more tickets.

**Product copy, if this state is confirmed:**

Equipment history needed. Ask a technician to add the missing details before continuing.

**Reflective observation, not personal testimony:**

A complete ticket can conceal an unfinished job. The missing history only becomes visible when someone tries to decide what to do next. That distinction matters when the product is being judged on whether it can finish the work.

Each version changes the reader's task and the level of explanation. None obtains personality by changing the facts.
