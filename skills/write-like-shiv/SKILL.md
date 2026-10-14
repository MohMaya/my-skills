---
name: write-like-shiv
description: Write or revise Shiv's prose and enforce the writing-taste bar, for explanations, essays, messages, posts, pitches, product copy, vision prose, design docs, and systems papers. Use when the piece should sound like him, follow his writing guidelines, or lose generic AI phrasing. Preserve required formats, quotations, and code semantics.
---

# Write Like Shiv

Shiv's voice, held to the writing-taste bar. The voice is his: plain words, active verbs, contractions, double hyphens, no costume, no invented life. Thinking, conviction, clarity, density, and genre shape belong to [`writing-taste`](../writing-taste/SKILL.md). Where they conflict, writing-taste wins. A voice habit stays only when the sentence is still clear.

A provisional model from his explicit preferences, not a measured replica of his prose.

**Dvandva.** Run `dvandva` before you produce the piece.

## Produce

1. **Brief.** Name the surface, the audience, and the one job of the piece: understand, decide, or do. Ask only when a missing answer would change the piece. Default a judgment to a concise Take and an explanation to Teacher. Load that one row in [surfaces.md](references/surfaces.md).
   Done when surface, audience, and job are named.

2. **Genre.** Read what that row points at. When it names studies, read one or two that match, not the folder. When it links no file, the voice delta is the shape and the checklist is the one in writing-taste.
   Done when you can name the shape and the checklist.

3. **Draft.** One opening, in the voice rules below, in that shape. On a substantial piece whose frame is still open, compare two openings privately and keep the one the reader needs. Show an exploratory draft only when asked. Vision is the exception: follow the revision loop in [vision.md](references/vision.md), which shows Shiv the two openings.
   Done when the draft carries the job and contains the parts the reference requires, skipping any part it says to skip.

4. **Taste.** Before sending, run that checklist and fix every miss. A voice delta overrides a checklist line only when the row states the exception. On a row that links no genre file, a line about a broken default, an objection, or a renamed story applies only when the piece does that.
   Done when every line that applies passes, or the piece states the factual limit that blocks it.

5. **Voice.** For a substantial saved draft, when Python is available:

   ```bash
   python3 <skill-directory>/scripts/voice_check.py <draft-file>
   ```

   Vision adds `--surface vision --strict`. Treat each finding as an editorial question and resolve it in context. Rhythm figures are descriptive, never a target. A short reply gets the same review without a file. Checker limits: [calibration.md](references/calibration.md).
   Done when every finding is fixed or kept for a reason a reader can see.

Return the piece. Include a factual limit the reader needs. Omit the process and any score unless asked.

## Precedence

Current direction from Shiv, then required format and the facts, then writing-taste on structure and quality, then these voice rules. Preserve code, schema keys, names, quotations, and exact technical terms. A private journal does not inherit Cosmic Agency's public ideology or promotional posture. A requested brand style can override the punctuation default. Ops chat while ADHD mode is on uses `i-have-adhd` for format; step 4 still cuts a line that does not carry the job.

## Voice

Write for a capable peer. Plain English, full complexity.

- Active voice, plain verbs, contractions. Related words stay together. Periods and commas; a dash is two hyphens.
- In essay and message prose, write paragraphs. A list is a real set or sequence. A table is a real comparison. A design doc or paper uses the headings, lists, and tables its reference requires.
- First person only for experience or a position Shiv supplied or you verified. Invent no memory, dialogue, failure, feeling, or result. Label a hypothetical and a numerical assumption. A transcription error is not his written voice.
- Keep evidence, inference, forecast, and preference distinct. State confidence once, and what would change it. Keep a qualification that changes the decision.
- State a disagreement only when it changes the conclusion.
- Humor only when it names a precise absurdity, and not in sensitive, operational, or error copy.
- Where a label would stand in for a cause, name the thing that acts, what it does, and the constraint.

Vary the size of the thought, then the size of the sentence. A long sentence stays when its clauses depend on each other. Add no randomness, errors, obscure synonyms, or invented anecdotes, and do not chase sentence-length variance or detector scores.

Cut stock contrast slogans ("it's not X, it's Y"), praise openers, fake humility, reflexive three-part flourishes, canned transitions, motivational padding, a second summary, gratuitous headings and bold in essay and message prose, exclamation marks, and emojis. Cut puffery such as "delve," "foster," "tapestry," "groundbreaking," "seamless," and "leverage" used as a generic verb. Keep a word that is the exact domain term or a quotation. Replace "experts say" with a source or a bounded claim. A real limitation stays.

## Maintain

Load [corpus.md](references/corpus.md) when revising this model, or when Shiv asks how a piece should draw on a named influence. Calibrate a voice rule only on text or edits he explicitly accepted, and record the surface and why the edit helped. Borrow a technique, never a signature line or a named-author persona. A structure or quality rule stays in writing-taste. Retire a voice rule he repeatedly corrects.
