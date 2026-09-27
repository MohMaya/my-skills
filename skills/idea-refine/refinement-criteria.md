# Refinement & Evaluation Criteria

Use this rubric during Phase 2 (Evaluate & Converge) to stress-test idea directions. Not every criterion applies to every idea — use judgment about which dimensions matter most for the specific context.

## Core Evaluation Dimensions

### 1. User Value

The most important dimension. If the value isn't clear, nothing else matters.

**Painkiller vs. Vitamin:**
- **Painkiller:** Solves an acute, frequent problem. Users will actively seek this out. They'll switch from their current solution. Signs: people describe the problem with emotion, they've built workarounds, they'll pay for a solution.
- **Vitamin:** Nice to have. Makes something marginally better. Users won't go out of their way. Signs: people nod politely, say "that's cool," then don't change behavior.

**Questions to ask:**
- Can you name 3 specific people who have this problem right now?
- What are they doing today instead? (The real competitor is always the current workaround.)
- Would they switch from their current approach? What would make them switch?
- How often do they encounter this problem? (Daily problems > monthly problems)
- Is this a "pull" problem (users are asking for this) or a "push" problem (you think they should want this)?

**Red flags:**
- "Everyone could use this" — if you can't name a specific user, the value isn't clear
- "It's like X but better" — marginal improvements rarely drive adoption
- The problem is real but rare — high intensity but low frequency rarely justifies a product

### 2. Feasibility

Can you actually build this? Not just technically, but practically.

**Technical feasibility:**
- Does the core technology exist and work reliably?
- What's the hardest technical problem? Is it a known-hard problem or a novel one?
- Are there dependencies on third parties, APIs, or data sources you don't control?
- What's the minimum technical stack needed? (If the answer is "a lot," that's a signal.)

**Resource feasibility:**
- What's the minimum team/effort to build an MVP?
- Does it require specialized expertise you don't have?
- Are there regulatory, legal, or compliance requirements?

**Time-to-value:**
- How quickly can you get something in front of users?
- Is there a version that delivers value in days/weeks, not months?
- What's the critical path? What has to happen first?

**Red flags:**
- "We just need to solve [very hard research problem] first"
- Multiple dependencies that all need to work simultaneously
- MVP still requires months of work — likely not minimal enough

### 3. Differentiation

What makes this genuinely different? Not better — *different*.

**Questions to ask:**
- If a user described this to a friend, what would they say? Is that description compelling?
- What's the one thing this does that nothing else does? (If you can't name one, that's a problem.)
- Is this differentiation durable? Can a competitor copy it in a week?
- Is the difference something users actually care about, or just something builders find interesting?

**Types of differentiation (strongest to weakest):**
1. **New capability:** Does something that was previously impossible
2. **10x improvement:** So much better on a key dimension that it changes behavior
3. **New audience:** Brings an existing capability to people who were excluded
4. **New context:** Works in a situation where existing solutions fail
5. **Better UX:** Same capability, dramatically simpler experience
6. **Cheaper:** Same thing, lower cost (weakest — easily competed away)

**Red flags:**
- Differentiation is entirely about technology, not user experience
- "We're faster/cheaper/prettier" without a structural reason why
- The feature that differentiates is not the feature users care most about

## Assumption Audit

For every idea direction, explicitly list assumptions in three categories:

### Must Be True (Dealbreakers)
Assumptions that, if wrong, kill the idea entirely. These need validation before building.

Example: "Users will share their data with us" — if they won't, the entire product doesn't work.

### Should Be True (Important)
Assumptions that significantly impact success but don't kill the idea. You can adjust the approach if these are wrong.

Example: "Users prefer self-serve over talking to a person" — if wrong, you need a different go-to-market, but the core product can still work.

### Might Be True (Nice to Have)
Assumptions about secondary features or optimizations. Don't validate these until the core is proven.

Example: "Users will want to share their results with teammates" — a growth feature, not a core value proposition.

## Risk Lenses

Before building a product, MVP, or major feature, check the Must Be True assumptions through each lens. Separate product risk from engineering difficulty, and name missing evidence rather than inventing market claims. Adapted from Seth Hobson's `before-you-build` (wshobson/agents, MIT).

- **Demand:** Who has the painful problem today, and what workaround do they use? What behavior shows urgency: payment, repeated manual work, switching tools, or asking for the same outcome more than once?
- **Positioning:** Can the target user say what this is for without hearing implementation details? Is the promise tied to a concrete outcome, and what alternative must it beat?
- **Monetization:** Who controls the budget or the time saved? Is the value large enough to cover build and maintenance cost, and would the first useful version justify payment, adoption, or internal sponsorship?
- **Retention:** What makes it useful after the first session: a saved workflow, history, a collaboration loop, or a recurring decision? Would users come back without reminders?
- **Trust:** What data, permissions, integrations, or behavior change does it require? What proof would make a cautious user try it, and what failure would make it feel unsafe or unserious?
- **Distribution:** Where can the exact target user be reached repeatedly? Which existing channel, community, workflow, or integration exposes it beyond one launch post?
- **Feature adoption:** What existing behavior will this feature change? Is it tied to an active pain, and can adoption be measured with one clear event?

Rate the idea low, medium, or high risk from the weakest lens. The MVP then tests that lens first, and the Not Doing list names what waits for the evidence.

## Decision Framework

When choosing between directions, rank on this matrix:

|                    | High Feasibility | Low Feasibility |
|--------------------|-------------------|-----------------|
| **High Value**     | Do this first     | Worth the risk   |
| **Low Value**      | Only if trivial   | Don't do this    |

Then use differentiation as the tiebreaker between options in the same quadrant.

## MVP Scoping Principles

When defining MVP scope for the chosen direction:

1. **One job, done well.** The MVP should nail exactly one user job. Not three jobs done partially.
2. **The riskiest assumption first.** The MVP's primary purpose is to test the assumption most likely to be wrong.
3. **Time-box, not feature-list.** "What can we build and test in [timeframe]?" is better than "What features do we need?"
4. **The 'Not Doing' list is mandatory.** Explicitly name what you're cutting and why. This prevents scope creep and forces honest prioritization.
5. **If it's not embarrassing, you waited too long.** The first version should feel incomplete to the builder. If it doesn't, you over-built.
