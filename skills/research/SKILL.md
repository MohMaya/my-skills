---
name: research
description: Investigate a question against high-trust primary sources. Use for reading legwork, decision briefs, search-tool fallback after a rate limit, and source-quality judgment. Capture a repo note or a cited brief; do not treat SEO or net-worth farms as evidence.
---

Pick the deliverable from the request:

- **Repo note:** spin a **background agent** so you keep working while it reads. Investigate against primary sources, write one cited Markdown file, and save it where the repo already keeps such notes. If there is no convention, put it somewhere sensible and say where.
- **Decision brief:** answer in this session. Lead with the answer, then 3–7 evidence bullets with sources, then residual unknowns.

Follow every claim back to the source that owns it.

## Source quality

- **Tier A:** primary / first-party. Official docs, filings, source code, specs, first-party APIs, named primary data. Prefer this.
- **Tier B:** reputable secondary. Major papers, established newsrooms, known analyst houses. Use only when Tier A is unavailable, and say so.
- **Tier C:** blogs, SEO pages, affiliate lists, net-worth-estimate farms. Not evidence. If only Tier C is available, say the claim is unverified and stop stacking junk URLs.

## Search tools

Prefer the harness's best research/search MCP when it is available (for example Exa). On rate-limit, auth failure, or hard failure, fall back to other available search or fetch tools. Do not ask the user to paste an API key mid-brief.

After fallback, apply the source ladder more strictly. Weak tools are not a reason to cite more Tier C pages. Flag confidence when the brief rests on degraded tools or Tier B only.

## Intake

If the user gave a concrete brief, run it. Do not open with preference menus. If they dismissed a question, do not re-ask; decide from context. Ask only when a missing fact would change the outcome and the request is otherwise unanswerable.
