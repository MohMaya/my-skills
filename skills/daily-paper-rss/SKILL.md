---
name: daily-paper-rss
description: Publish a recurring Economist-style daily paper to an image-capable RSS feed for Readwise Reader. Use for newspaper/paper bots (Sameer-role) — not one-off research briefs or Karan media digests.
---

# Daily paper → Readwise RSS

For bots whose job is one morning edition, not ad-hoc research. Load `research` only for source-quality judgment inside a story; this skill owns edition mix, geography, and publish DoD.

## Before you write

1. **Read the bot brief** for geography order, paid stack, cadence, and anti-jobs. Do not invent a second map.
2. **Paid stack first** when the brief lists one (e.g. NYT, WSJ, Bloomberg, Economist, New Yorker, Atlantic, Indian Express / New Indian Express, Economic Times, Suraj/Swarajya). Target a clear majority of story cites from that stack, left/right balanced across the edition. Suraj/Swarajya counts toward paid-stack when the brief lists it.
3. **Wire/free outlets** (Reuters, TOI, Hindu, CNBC, …) are fillers when the stack is thin or paywalled — not the default spine. A free-wire majority is a ship blocker (see Fail-closed ship gate), not a soft preference.

## Paywalls and bot blocks

- Prefer the paid outlet as the primary cite when you have a verified headline + URL, even if full text is blocked.
- On 401/403/paywall: keep the paid cite as the story link when the headline is verified; note the degradation in a private handoff. Do not mass-replace stack links with free mirrors to pad the edition.
- Do not scrape behind auth you do not have. No credential fishing.

## Edition shape

- Tight Economist-style briefs: dek, one short graf, then the source link. Images when they help Reader.
- Follow the brief's geography sequence; skip empty regions rather than padding.
- ~20 min read unless the brief says otherwise.

## Fail-closed ship gate (before Publish DoD)

Run the mix check on the edition markdown. Non-zero exit is the ship blocker. Do not write `store.json`, render `rss.xml`, or push until this exits 0.

```bash
scripts/check_paid_stack.py <edition.md>
```

`--threshold` defaults to `0.5`. `--stack` overrides host suffixes; the script default is Sameer's brief paid stack. The script counts **story cite** http(s) URLs (one mix row per cite) and classifies hosts by suffix (strip `www.`).

| Result | Action |
| ------ | ------ |
| Paid-stack cites **≥ 50%** of story links | Proceed to Publish DoD. |
| Paid-stack cites **< 50%** | **Do not** push RSS. **Do not** treat markdown/chat as done. Stay quiet per the brief, **or** post a private degradation note with the mix counts (paid N / total M). Never ship an unlabeled free-press dump as THE BRIEF. |

This gate is numeric and fail-closed. Soft intent (“aim for majority”) is not enough; below the bar means no Pages/RSS update.

## Publish DoD (all required)

Markdown in chat or an attachment alone is **not** done. Pass the fail-closed ship gate first.

1. Write the edition under the paper feed repo's `editions/YYYY-MM-DD/`.
2. Append the item to the tokenized `store.json` (title, link, description/html, optional image, guid, pubDate).
3. Render `feeds/<token>/rss.xml` at repo root (mirror the `shiv-podcast-feeds` / `sameer-paper-feed` pattern — unguessable token path, no directory listing of tokens).
4. Commit + push so GitHub Pages (or the brief's host) updates.
5. Optional short in-app ping with the public RSS URL. **No Slack** as primary notify.

Keep the token and private feed paths out of Slack and public canals; read them from `feed_meta.json` / repo README.

## Verify

- Run `scripts/check_paid_stack.py` on the edition markdown **before** any Publish DoD step that writes `store.json`, renders `rss.xml`, or pushes. Non-zero exit: stop; do not publish.
- Public RSS URL returns 200 and shows today's item.
- Re-run the script on the edition markdown after publish; the ship gate numbers must still hold.
- Stay inside anti-jobs (not music, not CoS triage, not memes). Role-fit: Sameer / paper bots only.
