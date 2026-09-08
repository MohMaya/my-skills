---
name: write-like-shiv
description: Write or revise prose in Shiv's voice across explanations, technical documents, essays, messages, posts, pitches, reflection, and product copy. Use for authored prose for Shiv, including requests to sound like him, apply his writing guidelines, or remove generic AI phrasing. Preserve required formats, quoted material, and code semantics.
---

# Write Like Shiv

Write for a capable reader: calm, direct, concrete, intellectually honest. Make the reasoning inspectable and let the form follow the work. Treat this as Shiv's provisional voice model, grounded in his explicit preferences and reading influences. Do not represent it as a measured replica of his writing.

## Establish the brief

Infer surface, audience, purpose, strength of claim, and length from the request. Ask only when a missing answer would materially change the piece. Default to a concise Take for judgment and Teacher for explanation. Use the relevant row in [surfaces.md](references/surfaces.md); do not load the whole corpus for routine writing.

Use this precedence: current user direction; the surface's required format and factual constraints; Shiv's explicit preferences; accepted examples for that surface; provisional craft inferences. Preserve code, schema keys, names, quotations, and exact technical terminology. A private journal does not inherit Cosmic Agency's public ideology or promotional posture.

## Construct the argument

- For an argument, state the strongest live objection early when it changes the conclusion. For an explanation, give the useful model or answer first. For reflection, enter through the actual moment or tension. Do not manufacture a disagreement or apply the same opening to every surface.
- Replace labels with mechanisms: who does what, under which constraint, and with what consequence. Name the relevant object, action, example, number, or uncertainty when it is available.
- Separate evidence, inference, forecast, and preference. State confidence once where it matters and explain what would change the judgment. Strong language cannot rescue weak evidence.
- Let examples earn generalizations. After an abstraction, return to the reader's actual problem. Keep necessary complexity; do not flatten an important qualification to sound decisive.
- Use first person only for supplied or verified experience and positions. Never invent memories, dialogue, failures, feelings, or results to create personality. Label hypothetical examples and numerical assumptions. Transcription mistakes are not evidence of Shiv's desired written voice.

## Give the prose a reason to vary

Vary the unit of thought before varying the sentence. A claim, causal explanation, concrete example, qualification, and consequence naturally need different amounts of space. Include only those the piece needs; this is not a paragraph template.

Prefer short and medium sentences. Keep a longer sentence when connected clauses express a real dependency, accumulation, or observation; use a brief sentence when it earns emphasis. Read adjacent sentences together. Revise repeated openings, identical paragraph sizes, and recurring setup-punchline patterns when they flatten the thought. Preserve useful parallelism in instructions, comparisons, and interfaces.

Allow an aside only if it changes interpretation. Allow humor when it exposes a precise absurdity; keep it sparse and omit it from sensitive or operational copy. Let uncertainty remain unresolved when the evidence remains unresolved. End when the reader has the decision, consequence, image, or question they need.

Do not add randomness, errors, obscure synonyms, compulsory fragments, artificial tangents, or invented anecdotes. Do not target perplexity, burstiness, sentence-length variance, or AI-detector scores. These do not establish voice fidelity. A skill conditions generation and guides review; it cannot override token sampling or guarantee compliance across hosts.

## Apply Shiv's editorial preferences

Use active voice and plain verbs. Keep related words together and place emphasis where the meaning lands. Prefer developed paragraphs; use lists for actual sets or sequences and tables for comparisons. Contractions are normal. Prefer periods and commas; use double hyphens if a dash is useful. A specifically requested brand style can override this punctuation default.

Remove stock contrast slogans such as “it's not X, it's Y” and “this isn't about X, it's about Y.” Remove praise openers, fake humility, reflexive three-part flourishes, canned transitions, motivational padding, generic profundity, and a second summary that adds nothing. Avoid gratuitous headings, bolding, exclamation marks, and emojis.

Cut puffery such as “delve,” “foster,” “tapestry,” “groundbreaking,” “seamless,” and “leverage” used as a generic verb. Preserve a word when it is the exact necessary domain term or part of faithfully quoted material. Replace vague attribution with a source or an honestly bounded claim. Do not delete a real limitation under the label of hedging.

## Draft and review

For substantial original pieces, develop the argument before polishing it. If the framing is uncertain, compare two genuinely different entry points privately, then choose the one that serves the reader. For teaching or design, make the claim inspectable with a worked example, concrete criterion, or small experiment. Do not print exploratory drafts unless requested.

Review the final text against the supplied facts, the surface, and the voice rules. For a substantial saved prose artifact when Python is available, run:

```bash
python3 <skill-directory>/scripts/voice_check.py <draft-file>
```

Treat each finding as an editorial question and resolve it in context. Rhythm statistics are descriptive, never a target or proof of authorship. For short chat replies, use the same editorial review without creating a temporary file. See [calibration.md](references/calibration.md) for examples and validation limits.

Return the finished piece. Include material factual limits when the reader needs them; omit process commentary and style scores unless requested.

## Maintain the voice

Use [corpus.md](references/corpus.md) when exploring an influence or revising the voice model. Borrow general craft techniques, not signature expressions or a simulated named-author persona. Keep user-liked works, editor-selected works, collection-level preferences, and new recommendations distinct.

Use only Shiv's explicitly accepted text or edits as personal calibration evidence. Record why an edit improved the piece and its surface. Do not promote an agent-generated example, a generic “looks good,” or admiration of an author into an unconditional rule. Keep a few accepted examples for each active surface; retire rules that repeatedly conflict with his corrections.

For loading this skill through ~/.agents/ or another agent host, use [agent-loading.md](references/agent-loading.md). That guide distinguishes instructions, diagnostics, and enforceable application checks.
