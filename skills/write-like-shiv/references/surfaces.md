# Surfaces and forms

Use the smallest form that serves the reader. These are working shapes, not compulsory templates. Do not combine every mode or every influence in one piece.

| Surface or mode | Useful shape | What changes from the baseline |
| --- | --- | --- |
| Take; Slack; email; PR discussion | Recommendation or request, decisive reason, material tradeoff, next action if needed | Compress context the reader already has. A message can be one paragraph. No performance, invented urgency, or essay-length windup. |
| Technical explanation; engineering article; incident account | Problem, constraints, mechanism or approach, verified result, remaining tradeoff | Name concrete services, tables, interfaces, failure behavior, and units. Distinguish observation from causal attribution. Use a diagram only when it explains a relationship better. |
| Technical design document | Summary; problem and constraints; current state; proposal; components and responsibilities; interface or contract changes; data or migration; failure modes and tradeoffs; rollout and rollback; observability; testing; alternatives; open questions | This order is an explicit prior preference. Use it for an actual design document, not every engineering response. Mark missing facts as unresolved. Explain how a decision changes future options. |
| Teacher; tutorial | Useful model, steps where sequential, worked example, boundary of the model | Begin at the reader's knowledge gap. For experts, omit prerequisite exposition. Give an analogy a precise mapping and a limit; do not use it as proof. |
| Think; essay | Specific puzzle or observation, developing reasoning, serious complication, earned implication | Allow a longer paragraph or sentence when it carries thought. An opening scene needs supplied facts. No obligatory thesis-roadmap-summary wrapper. |
| Observer; cultural analysis | Observable pattern, concrete instances, mechanism, limits | Direct the wit at the behavior being examined. Do not invent representative anecdotes or infer motives as facts. |
| Manifesto | Defensible conviction, grounds, commitments that change action | Keep ambition specific. A principle should settle an actual choice. Avoid motivational slogans and contempt for imagined opponents. |
| Pitch | What changes, why now, initial customer and wedge, credible ability to execute, requested action | Separate validated traction from plans. Product promise must connect to a user action or outcome. Do not convert confidence into a forecast presented as fact. |
| Journal; private reflection | Actual moment or tension, what was felt or done, reflection that may remain open | Preserve vulnerability, contradiction, and uncertainty. Do not rewrite distress as a lesson about agency or manufacture stoicism. No compulsory moral. |
| Philosopher | Live question, concrete situation, reasoned position or unresolved tension | Keep scale and mortality connected to the particular situation. No detached cosmic sermon or quote-card conclusion. |
| Short public post | One specific idea with enough context to be understood on its own | Vary length only as the thought needs. No bait, thread cadence, forced punchline, or invented extreme claim. |
| Product copy; onboarding; error message | State, user consequence, available action | Reader comprehension dominates literary personality. Keep labels consistent. No humor in errors or irreversible confirmations. Do not expose implementation detail that changes no user decision. |
| Design critique; product rationale | User task, observed friction, reason it occurs, proposed change, inspectable criterion | Ground taste in use, constraints, and alternatives. Use images or examples when they make the claim testable. Avoid unsupported adjectives like “intuitive.” |

## Influence selection

Use Graham's progressive reasoning and Feynman's concrete models as useful defaults for analytical work. Add Airey's practical tradeoffs and d.school's experiments when explaining design. Use Klein's scrutiny of competing explanations when evidence is contested. Reserve Wallace's self-questioning and Didion's observational restraint for forms that can support them. Use Carlin's attention to verbal absurdity as a light editorial lens, never as an instruction to become caustic.

Use Newport's procedural specificity for tutorials, Altman's compression for a decision note, and Lee Kuan Yew's attention to constraints for strategic argument. Treat each as an aspect to study, not an authority that supplies Shiv's beliefs. See the corpus for access limits and provisional selections.

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

Each version changes the reader's task and level of explanation. None obtains personality by changing the facts.
