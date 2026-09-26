---
name: create-grok-bot
description: Pack a Grok Bot CreateAgent or send_task brief under the handoff character limit without dropping constraints. Use when creating or updating a Legion/Grok bot (CreateAgent, voice send_task, bot-master handoffs).
---

# Create Grok Bot

Write the bot contract once, dense. Prefer calling `CreateAgent` / `UpdateAgent` directly in text chat when the brief is long. Use this skill when a handoff channel (for example voice `send_task`) enforces a hard character budget.

## Hard limit

Voice / `send_task` requests must stay **≤ 2000 characters**. If a send fails with a length error, **reformulate in one pass** — keep every constraint, prohibition, and approval. Do not drop constraints. Do not split into multiple executable tasks that each omit part of the contract.

## Pack order (keep all of these)

1. **Name** — everyday Hindu South Asian coworker name + comma + short role (not gods/mythic). Example shape: `Karan, Media Curator`.
2. **One job** — single sentence outcome. No second mandate.
3. **Lanes / deliverable** — bullet the recurring output only (what, cadence, format). Cap detail: name sources as examples, not encyclopedias.
4. **Mandatory quality bar** — e.g. two-line "why this sharpens taste" (idea/craft move, not plot summary).
5. **Wiring** — concrete sinks (playlists, Reader, calendars). Mark what is pre-approved vs needs confirm.
6. **Notify path** — in-app / agent messaging. This Legion does **not** use Slack as primary notify.
7. **Anti-jobs** — explicit list of what the bot must never do.
8. **Doctrine one-liners** — one job / one voice / no leftover tools; load matching skills via Routing only; `write-like-shiv` + `i-have-adhd` for Shiv-facing prose; no external send without explicit confirm.
9. **Return** — what the builder must report back (name, instruction summary, wiring live vs auth needed).

## Compress without loss

- Prefer short labels over paragraphs (`anti-jobs: no news, no memes, no Slack`).
- Collapse repeated doctrine into one line.
- Drop flavor and process narration; keep prohibitions and approvals.
- Count characters before send. If still over budget, cut examples first, never anti-jobs or auth rules.

## Coding vs non-coding

- **Coding bots:** one job, verified with the repo's own checks, written to `write-like-shiv`.
- **Non-coding bots:** same tightness — one job, one voice, explicit anti-jobs, no leftover tools.

## After create

Confirm wiring. Offer one sample run when useful. Apply mid-flight preference changes (`mix it up`, schedule moves) with a short follow-up brief, not a full rewrite.
