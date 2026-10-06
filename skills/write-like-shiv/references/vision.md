# Vision prose

Shiv approved this canon on September 26, 2026. It applies to vision prose: a vision or product thesis, a founding document, a public post, and other ambition prose. For those surfaces it overrides conflicting length and compression guidance in `SKILL.md`. Every other rule in `SKILL.md` still holds. Operational writing (chat, status, plans, digests, checklists) keeps the action-first shape in `i-have-adhd`.

Research and history essays use the same clarity, with inline source links on the relevant prose.

## Reader

A capable peer. Write plain English without simplifying the idea.

## Structure

1. **Opening.** For a product or vision thesis, open on the human pain or need. For a nation-scale or belief essay, open on the belief, the vision, or a shared problem the reader has felt, then move to what we do about it. Skip scene-setting that delays the point.
2. **Body.** Name the failure in physical terms from the reader's own domain: the form, the gatekeeper, the call that never got made. Then build the mechanism that clears the path. Widen the frame only when the wider frame earns its place.
3. **Product.** It arrives late and quietly, in one sentence. Leave features and roadmaps out.
4. **Ending.** Close on a toast or dedication by default. Use a hard call to action only in an explicit launch note.
5. **Length.** A vision or product thesis runs about 300 to 450 words. Cut until every sentence earns its place.

## Craft

- **Rhythm.** Mix short sentences that land a point with longer ones where the clauses depend on each other or accumulate.
- **Charge.** Moral charge is welcome when earned: name the human cost. State it once and let it stand, without sermon or keynote cadence.
- **Imagery.** Use sparse physical metaphor, and only when it carries meaning.
- **Examples.** Draw from the reader's actual domain.
- **Pronouns.** Use `we` or `everyone` for shared agency. Use `I` only for a verified personal claim, or when the piece speaks as Shiv.
- **Humor.** Use it sparingly, and only to expose a precise absurdity. Leave it out of sensitive copy.
- **Format.** Light headers are fine. Carry the argument in paragraphs; a list is for an actual set.
- **Sources.** A vision or product piece carries none. A research or history essay links sources inline, with no footnote apparatus.
- **Influence.** Study exemplars for craft. Write every phrase fresh; borrowed signature lines read as costume.

## Revision loop

1. Draft two genuinely different openings.
2. Shiv picks one.
3. Grill the weak lines.
4. Revise once.

Show exploratory drafts only when asked.

## Check

Save the draft and run the checker in vision mode. Resolve every finding before sending, or state why it stands:

```bash
python3 <skill-directory>/scripts/voice_check.py --surface vision --strict <draft-file>
```

Vision mode adds a word-count check (300 to 450) and a list-density check to the standard stock-phrase, contrast-slogan, and repeated-opening checks. Use `--min-words` and `--max-words` for a research or history essay, where the thesis length does not apply.
