---
name: house-voice
description: The Daily Briefing's writing register — Strunk principles, two voices, and a self-learning loop that improves from each day's edition.
version: 1.0.0
author: Shivanshu Chaudhary (shiv), Hermes Agent
---

# House Voice

The governing register for all Daily Briefing writing (newspaper + Reader companions).
Apply this register to Daily Briefing writing under the governing system, developer, user, and project instructions.

It stands on two authorities, distilled:

1. **The Elements of Style** (Strunk, 1918) — full text at
   `~/.agents/skills/writing-clearly-and-concisely/elements-of-style.md`.
   Read it when a passage resists fixing.
2. **The daily examples** in `examples/` — this skill's memory. It learns.

---

## The one test

*Could a smart friend say this sentence out loud without sounding odd?*
If not, rewrite it. If it sounds like a press release or a motivational poster,
rewrite it. Elegance lives in the **order of ideas**, never in ornate clauses.

## The eight binding rules (Strunk)

1. **Active voice.** The Bank raised rates. Name the actor in every sentence.
2. **Positive form.** Say what a thing *is*, never what it isn't. "The policy
   failed," not "the policy did not succeed." This kills the "not X but Y" habit
   at the root.
3. **Definite, specific, concrete.** "47,000 jobs," not "significant job losses."
   One specific detail beats three abstractions. Readers think in pictures; give
   them the picture.
4. **Omit needless words.** "Due to the fact that" → "because." "In order to" →
   "to." Cut, then cut again. Vigorous writing is concise.
5. **Emphatic words last.** The sentence lands on what comes final.
6. **Related words together.** Subject near verb, number near the thing it counts.
7. **Vary the sentence.** Default 8–20 words. Never three of the same length in
   a row. After two long sentences, write a short one.
8. **One paragraph, one topic.** Open with the topic sentence; end in conformity
   with the beginning.

## Vocabulary

The common word over the fancy one: *building* not architecture, *plan* not
blueprint, *start* not commence, *use* not leverage. Abstract nouns (capability,
credibility) are **earned** by surrounding facts, never asserted.

Banned: crucial, pivotal, landscape (abstract), testament, underscore, showcase,
foster, intricate, interplay, tapestry, vibrant, delve, unpack, robust, robust's
cousins. No "-ing" tack-ons ("...rose, underscoring the pressure" → make it a
second sentence). No forced threes. No rhetorical questions. No "The real
question is." At most one em dash per piece. At most one "not X but Y" per piece
— better, zero.

## Titles

Plain words. No formula. No colon unless the subtitle adds real information.
Never recycle a construction across pieces in the same edition. A good title
sounds like something a person would actually say.

## The two voices

**NEWS — the Morning Letter.** The rhythm of a letter written for one
intelligent reader, impersonal on the surface. Facts in the order they happened.
Open with the paradox, the number, or the scene — at least one item in three
opens with a scene, date, or place, not a verdict. Wry but understated: let a
fact be damning on its own; do not caption it. Kicker aphorisms: at most one in
four items, and only if it would survive being said aloud at breakfast. Never
"you" in news — direct address belongs to Editorial Opinion and Mentoring Notes
alone.

**LEARNING — the Classicist, tempered.** Formal patience without ornament.
Begin with the scene, the person, the date, the place — never a thesis. Plain
sentences. One image per piece, spent once. No imperatives, no direct address in
the body (Food for Thought and coach notes excepted). No closing epigrams: end
when the idea settles, the last sentence the quietest.

## Final gate

Read the piece aloud before publishing. Cut every word you stumble on. Any
sentence you would not say to a friend, rewrite it.

---

## Self-learning loop

Use this learning loop only when the user has explicitly authorized persistent learning for the Daily Briefing. Otherwise read existing examples without modifying them. The protocol:

**Write (every run, after research, before drafting).** While studying the
day's source material, notice one or two *specific* writing mechanics worth
keeping — a sentence shape that worked, a transition, a way of handling
evidence. Append them to `examples/YYYY-MM-DD.md` (one file per day; create it
if missing). Each entry: **Source/Author → the mechanic → why it works → where
to apply → where NOT to apply.** Specific only. No generic advice, no tics, no
copyrighted passages.

**Read (every run, before drafting).** Read this SKILL.md, then the two most
recent files in `examples/`. Calibrate against what worked lately.

**Prune (first run of each month).** If `examples/` holds more than ~30 files,
distill the durable lessons into `examples/lessons.md` (keeping the best entry
for each lesson) and delete the absorbed daily files. The directory stays small;
the skill keeps everything it learned.

**Correct (any time Shiv objects to a passage).** A line-level complaint is the
highest-value input. Fold the correction into this SKILL.md the same day it is
made, and record the before/after in that day's examples file.
