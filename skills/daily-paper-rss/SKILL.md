---
name: daily-paper-rss
description: Publish a recurring Economist-style daily paper to an image-capable RSS feed for Readwise Reader. Use for newspaper/paper bots (Sameer-role) — not one-off research briefs or Karan media digests.
---

# Daily paper → Readwise RSS

For bots whose job is one morning edition, not ad-hoc research. Load `research` only for source-quality judgment inside a story; this skill owns edition mix, geography, and publish DoD.

## Before you write

1. **Read the bot brief** for geography order, paid stack, cadence, and anti-jobs. Do not invent a second map.
2. **Paid stack first** when the brief lists one (e.g. NYT, WSJ, Bloomberg, Economist, New Yorker, Atlantic, Indian Express, Economic Times, Swarajya). Aim for a clear majority of story cites from that stack, left/right balanced across the edition.
3. **Wire/free outlets** (Reuters, TOI, Hindu, CNBC, …) are fillers when the stack is thin or paywalled — not the default spine. If the edition would be mostly free substitutes, either revise or stay quiet per the brief; do not ship an unlabeled free-press dump.

## Paywalls and bot blocks

- Prefer the paid outlet as the primary cite when you have a verified headline + URL, even if full text is blocked.
- On 401/403/paywall: note the degradation in a private handoff; still avoid replacing every stack link with a free mirror.
- Do not scrape behind auth you do not have. No credential fishing.

## Edition shape

- Tight Economist-style briefs: dek, one short graf, then the source link. Images when they help Reader.
- Follow the brief's geography sequence; skip empty regions rather than padding.
- ~20 min read unless the brief says otherwise.

## Publish DoD (all required)

Markdown in chat or an attachment alone is **not** done.

1. Write the edition under the paper feed repo's `editions/YYYY-MM-DD/`.
2. Append the item to the tokenized `store.json` (title, link, description/html, optional image, guid, pubDate).
3. Render `feeds/<token>/rss.xml` at repo root (mirror the `shiv-podcast-feeds` / `sameer-paper-feed` pattern — unguessable token path, no directory listing of tokens).
4. Commit + push so GitHub Pages (or the brief's host) updates.
5. Optional short in-app ping with the public RSS URL. **No Slack** as primary notify.

Keep the token and private feed paths out of Slack and public canals; read them from `feed_meta.json` / repo README.

## Verify

- Public RSS URL returns 200 and shows today's item.
- Outlet mix: count paid-stack vs other; report the count if mix is thin.
- Stay inside anti-jobs (not music, not CoS triage, not memes).
