---
name: media-library-bulk
description: Safe bulk mutations on music playlists or liked libraries (Apple Music primary; Spotify only after Vikram confirm). Use when filling, clearing, rebuilding, or mass-adding tracks under API quotas — not for one-off single-track adds. Not for YouTube Music writes.
---

# Media library bulk ops

For music/media curator bots only. One-off "add this song" skips this skill.

## Legion music-platform writes (role-fit)

Music-queue curator (Devika, Music) write path:

1. **Primary writes → Apple Music** for Legion music queues and mood shelves.
2. **YouTube Music** — no writes. Subscription ending ~2026-10-06; do not dual-write, fill, clear, or rebuild YTM playlists or likes.
3. **Regular YouTube** (youtube.com playlists / video playlists) — OK for non-music-queue bots (e.g. Karan coffee/podcast lanes). That is not YouTube Music and is out of this skill's music-queue path.
4. **Spotify** — no hard dependency until Vikram confirms.

If a bot brief or routine still names YouTube Music as a write target, treat Apple Music as the write surface and skip YTM mutations; report the stale brief once.

## Before any destructive clear or rebuild

1. **Backup** — write every affected track/video/song id to a dated file the bot can re-read.
2. **Confirm** — clear/rebuild of Liked / Favorites / a shared playlist needs explicit user go-ahead in this conversation. Draft the plan (counts in, counts out, platforms). Do not treat a fill request as clear permission.
3. **Scope freeze** — stay inside the platforms and playlists named in the bot brief, filtered by the Legion music-platform rules above. Expanding to another allowed catalog needs a fresh confirm.

## Under rate limits and quotas

- Throttle writes (~0.4–0.5s or whatever the API tolerates). Retry 409/429 a few times with backoff; treat **quota exhausted** as pause, not a hot loop.
- **Checkpoint** after each small batch (mood, page, or N ids). Resume from the checkpoint after reset — never restart from zero and duplicate.
- Soft-cap playlist sizes the brief names (e.g. ≤3000). Stop at the cap; report remainder.

## Classify before mass-like or mass-slot

When cleaning a Liked / Favorites dump:

- Prefer heuristics that separate **genuine likes** from **album/sync dumps** (dense same album+artist clusters).
- Auto-slot only the high-confidence set. Leave dump/uncertain for the user.
- After apply: re-fetch counts, compare to plan, run one corrective pass for residuals — then stop and report.

## Verify and report

- Read back track counts (API + fetched rows) after clear and after apply.
- Report: attempted, succeeded, failed, residual, checkpoint path, quota status, platforms written.
- No Slack notify — in-app / agent messaging only for this Legion.
