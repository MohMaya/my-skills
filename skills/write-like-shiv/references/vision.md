# Vision prose

Shiv approved this canon on September 26, 2026. It is the shape for a vision or product thesis, a founding document, a public post, and other ambition prose. Voice rules in `SKILL.md` still hold. Quality belongs to [`writing-taste`](../../writing-taste/SKILL.md). This file wins on the shape below, and nowhere else. A toast or a late product line that runs past the evidence fails the taste check.

Ops chat, status, plans, and digests stay with `i-have-adhd`. A research or history essay is not vision prose: ordinary clarity, sources linked inline, no footnote apparatus. Pass `--min-words` and `--max-words` when that essay has a length bound.

## Shape

1. **Opening.** The claim in its obvious form. A product or vision thesis opens on the human pain or need. A nation-scale or belief essay opens on the belief, the vision, or a shared problem the reader has felt. Skip scene-setting that delays that claim.
2. **Body.** The failure in physical terms from the reader's domain, then the mechanism that clears it. Widen the frame only when the wider frame changes the claim.
3. **Product.** One sentence, late and quiet. Features and roadmaps stay out.
4. **Ending.** A toast or dedication. A hard call to action only in an explicit launch note. The ending stays as strong as the evidence.
5. **Length.** A thesis runs about 300 to 450 words.

Moral charge belongs when it names a human cost, once. A physical metaphor stays sparse and only when it carries meaning. `we` or `everyone` for shared agency. `I` only for a verified personal claim, or when the piece speaks as Shiv. A vision or product piece cites nothing.

## Revision loop

1. Draft two genuinely different openings and show Shiv those openings.
2. He picks one.
3. Grill the weak lines.
4. Revise once.

Show the rest of an exploratory draft only when asked.

## Check

Save the draft. Run the checker, then the writing-taste checklist on every line this file does not override. Resolve every finding, or state why it stands:

```bash
python3 <skill-directory>/scripts/voice_check.py --surface vision --strict <draft-file>
```

Vision mode adds a word-count check (300 to 450) and a list-density check. The argument stays in paragraphs. A list is a real set.
