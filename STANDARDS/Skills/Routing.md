# Skills/Routing.md

Apply `write-like-shiv` whenever writing or revising anything. Read `~/.agents/skills/write-like-shiv/SKILL.md` and its relevant surface reference before drafting, including short replies and progress updates. Use this router for additional specialist guidance. The active runtime provides the installed inventory. Load the matching entry, not the entire tree.

The runtime list and readable canonical skill files establish availability. When the runtime list is incomplete, use `rg --files ~/.agents/skills -g SKILL.md` to find names, then search task terms within those files. Read the matching frontmatter and body before selecting a skill. Resolve bundled references relative to its folder. `.skill-lock.json` identifies imported sources; it does not prove that a skill's tools are installed.

## Routes

The kernel's Engineering skills section owns the mandatory engineering triggers, from `interview-me` at intake through `shipping-and-launch` at release. Its owners supersede plugin copies of the same method. The rows below route everything else and point back to it.

| Task | Load |
| ---- | ---- |
| Unclear standards ownership or conflicting doctrine | `STANDARDS/INDEX.md` |
| Writing or changing code | `shiv-code-gate`; the kernel's Engineering skills triggers; `Core/Code.md` for quality and layer rules; `Core/Execution.md` when execution is unclear |
| Closing out a change | `simplify` before each commit; `code-review-and-quality` before opening or updating a PR |
| Requested chat compression | `caveman` |
| Requested humanization or prose with AI-sounding patterns | `humanizer`; `write-like-shiv` owns voice |
| Everyday communication, including chat, Linear tickets, PR bodies, and delegated-agent output | `i-have-adhd` by default in every session; plain English; `write-like-shiv` owns the non-code articulation bar; `Core/Prose.md` defines prose-artifact exceptions and session overrides |
| Substantial knowledge-base document | `Core/Documents.md`; a clarity pass before delivery |
| Any writing or revision: chat, updates, trackers, documents, comments, commits, PRs, product copy, or agents | `write-like-shiv` and its relevant surface reference; `Core/Prose.md`; `Core/Documents.md` when document shapes help |
| Essay, article, or memo | Select `writing-fragments`, `writing-beats`, or `writing-shape` for the current stage |
| Intent unclear before any plan; a raw idea to explore | `interview-me`; `idea-refine` respectively |
| Planning, scoping, tradeoffs, sequencing | `Core/Planning.md` |
| Stress-testing a plan, decision, or idea | `grilling`; `grill-with-docs` in a repository that keeps `CONTEXT.md` |
| Grilling touches module shape or boundaries | `codebase-design` for the structural questions |
| Publishing a spec; filing tickets; writing a PRD | `to-spec`; `to-tickets`; `write-spec` respectively |
| Work too big for one session | `wayfinder` |
| Implementing from a spec or tickets | `implement` |
| Session ending mid-work | `handoff` |
| Judging quality, taste, expert behavior | `Core/Craft.md` |
| Module or interface design | `codebase-design` for module depth and seams; `api-and-interface-design` for contracts other code depends on; `domain-modeling` for terms |
| Repo-wide architecture cleanup; prioritized debt ledger | `improve-codebase-architecture`; `tech-debt` respectively |
| Refactor working code for clarity | `code-simplification` |
| Throwaway spike to answer a design question | `prototype` |
| Reading legwork, decision briefs, search-tool failure, or source-quality judgment | `research` |
| Creating or updating a Legion/Grok bot (CreateAgent, voice send_task, bot-master brief) | `create-grok-bot` |
| Bulk YouTube/Apple/Spotify playlist or liked-library mutations (fill, clear, rebuild under quota) | `media-library-bulk` |
| Daily Economist-style paper / Readwise RSS news edition | `daily-paper-rss` |
| Commit messages | `caveman-commit` |
| Reviewing a diff or PR | `code-review-and-quality`; `simplify` when bloat is the question; `pe-review` change mode when it touches UI; `blast-radius` for breakage beyond the diff before merging a change you don't fully trust |
| How code works or where something should live; why it is shaped this way | `how`; `why` respectively |
| Design-first sketch before code, on explicit request | `architect`, recording shapes in `codebase-design` terms |
| Bakeoff of competing candidates | `arena` |
| Catch me up or resume context | `recall` |
| Turn session learnings into fixes | `reflect`, preferring code and lint fixes over skill edits; skill edits go through `writing-for-agents` |
| Decision trail for unattended or multi-phase work | `show-me-your-work` |
| Build or update a repo-local app driver skill | `create-verification-skill`; `maintain-verification-skill` |
| Irreversible decision needing a fresh-context adversarial check | `doubt-driven-development` |
| Hard bugs, flaky failures, perf regressions | `diagnosing-bugs` |
| Logs, metrics, traces, alerts, runbooks | `observability-and-instrumentation`; `Workflow/Delivery.md` owns the baseline |
| Measured slowness, a performance budget, or the deferred optimization pass | `performance-optimization`; re-measure before keeping any change |
| Merge or rebase conflicts | `resolving-merge-conflicts` |
| Git, commits, branches, PRs | `Workflow/Git.md` |
| Create a PR; update an open PR after review or CI failures | `create-pr`; `follow-up-on-pr` respectively; `Workflow/Git.md` owns conventions and delivery scope |
| Cubic review comments on a PR or stack | `cubic-review`; `Workflow/Git.md` (Cubic review comments) owns the reply rules; `follow-up-on-pr` when accepted fixes push the branch |
| GitHub issues and `gh` flow | `Workflow/GitHub.md` |
| Stacked branches and dependent PRs | `gh-stack`, then `Workflow/GitHub.md` |
| CI pipelines | `ci-cd-and-automation`; `Workflow/Delivery.md` owns the required gates |
| Production deploy, staged rollout, flags, rollback | `shipping-and-launch`; `Workflow/Delivery.md` owns rollback authority |
| Schema, data, API, or dependency migration; retiring code | `deprecation-and-migration` |
| Setting up or changing a repository's quality gates | `constraint-driven-development`; follow an existing `CONSTRAINTS.md` without it |
| Linear workflow | `Workflow/Linear.md` |
| Notion knowledge base | `Workflow/Notion.md` |
| Writing code that crosses a trust boundary | `security-and-hardening` |
| Review a security-sensitive diff; build a threat model; validate a finding; broader security review | `commit-security-scan`; `threat-model-generation`; `vulnerability-validation`; `security-review` respectively; `Workflow/Delivery.md` defines evidence and authorization boundaries |
| Verify UI or debug in a real browser | `browser-testing-with-devtools` when the Chrome DevTools MCP server is connected; `playwright-cli` otherwise; `pe-verify` for a recorded evidence report or QA-list run |
| UI quality review or accessibility audit | `pe-review` |
| Behavior spec of an existing product | `pe-product-description` |
| Test-first loop on new behavior | `tdd` |
| Stack-specific work | matching file under `STANDARDS/Stack/` |
| Python cleanup, scanning, coverage, or lint and hook setup | `py-*` skills from the Skills table in `Stack/Python.md` |
| React, Next.js, React Native, effects, assertion rules, or Knip findings | the Skills table in `Stack/TypeScript.md` |
| Postgres schema, queries, migrations | `supabase-postgres-best-practices` |
| Go | `golang-code-style`, `golang-error-handling` |
| Backend on Railway | `use-railway` |
| Vercel cost or perf | `vercel-optimize` |
| Deploy to Vercel; token-authenticated Vercel CLI, env vars, or domains | `deploy-to-vercel`; `vercel-cli-with-tokens` respectively; `shipping-and-launch` for production |
| Mobile (Expo / React Native) | `expo-native-ui`, `expo-router`; ship via `eas-workflows`, `eas-app-stores` |
| LLM features | `ai-sdk` (TS), `claude-api` (Anthropic specifics) |
| Build product UI | Kernel Design authority first; `frontend-ui-engineering` for structure, states, accessibility, and responsiveness; `pe-build` for craft |
| Art direction for a surface with no product design, such as a one-off tool or artifact | `pe-design` direct mode and its presets; preserve the existing stack |
| Figma design → code | `figma:figma-design-to-code`; `design-system` to formalize tokens first |
| Code or description → Figma | `figma:figma-generate-design` (screens), `figma:figma-generate-library` (design system); `figma:figma-use` before any `use_figma` call |
| UI polish and motion | `pe-build` craft and motion modes |
| Animation work | `pe-build` motion mode to build, including React view transitions; `pe-review` motion modes to review, audit, or find opportunities; `animate-expo` for Expo |
| Marketing copy, positioning, pricing | `draft-content` for copy; `competitive-brief` for positioning; `pricing` |
| Product architecture | `Product/Architecture.md` |
| Office file in or out | `docx`, `pptx`, `xlsx` |
| Images, diagrams, or presentations | `visual-design` and only its matching reference for raster images and decks; `pe-brand-assets` for on-brand SVG, social images, and logos; `pe-design` mock mode for HTML diagrams and plans |
| Requested human-writing edit | `human-writing` under `write-like-shiv`; `Core/Prose.md` owns everyday formatting and prose exceptions |
| Initialize repository instructions; author a skill; edit a skill, `AGENTS.md`, or `CLAUDE.md` | `init`; `skill-creation`; `writing-for-agents` respectively; inspect existing instructions and preserve canonical ownership. `template-skill` is an unfinished authoring example |
| Explicit iterative optimization experiment | `autoresearch`; `Core/Execution.md` defines budget, isolation, and stopping conditions |
| Browse with the installed browser CLI; locate a prior Droid session | `browser-navigation`; `session-navigation` respectively; verify the named CLI and local data exist |
| Automate a terminal, browser, or desktop; record a demo | `droid-control` is the entry point; select background skills from the map below |
| Steps only a human can take: credentials, CI secrets, dashboards, cutovers | `wizard` |
| Inspect HTTP traffic from a CLI or service | `http-toolkit-intercept`; scope capture to the requested process and protect credentials in captured traffic |
| Can't find the right skill | `rg --files ~/.agents/skills -g SKILL.md`, then search task terms in the matching files |

## Droid control background skills

Load these through `droid-control` for the chosen task. Prefer purpose-built tools exposed by the current harness. Check driver, browser, operating-system, and recording dependencies before running commands; adapt tool names to the current harness.

The copied skill folders contain instructions and selected references. Droid control and video workflows also expect an installed plugin runtime providing `DROID_PLUGIN_ROOT`, `bin/tctl`, rendering scripts, and a Remotion project. Verify those assets before choosing that workflow. When absent, use an available harness tool or report the specific dependency needed for the requested action.

| Need | Background skill |
| ---- | ---- |
| Real terminal input; raw key sequences | `true-input`; `pty-capture` respectively |
| Web or Electron app | `playwright-cli` |
| Droid CLI controls | `droid-cli` |
| Recording; video assembly; visual polish | `capture`; `compose`; `showcase` respectively; use the existing project stack and authorized output scope |
| Verify promised deliverables | `verify` |

## Requested humorous reports

Factory's cursed-plugin skills produce humorous codebase reports. Use them only for an explicit request for that skill or report style: `agent-repellent`, `blame`, `cobol-converter`, `dating-profile`, `feng-shui`, `obituary`, `performance-review`, `roast`, `ship-ritual`, and `therapy-session`. `performance-review` here concerns a codebase, not an employee; `ship-ritual` is entertainment, not release verification. Keep normal engineering, security, and people workflows on their task routes. Advertising, sharing, and external publication require their own user request.

## Availability

Routes name preferred skills, not guaranteed installations. The active runtime and readable `~/.agents/skills/*/SKILL.md` files determine availability. Verify provider-specific tools in the current session. For `simplify`, re-climb the code gate if the skill is absent. For unavailable document or domain skills, apply the relevant standards directly and state the gap. Figma capabilities depend on the installed integration, not the harness name.

Run `bash ~/.agents/sync.sh` after changing canonical skills or the kernel. It maintains Codex, Claude, and Cursor skill links, generated harness rules, the Claude and Codex mandate mirrors, and the `stop-gate.py` Stop hook in both. Codex asks to trust a new hook on its next run. Gemini CLI reads the shared kernel import; Antigravity reads the configured canonical skills path. Droid supports `~/.agents/AGENTS.md` and `~/.agents/skills/**/SKILL.md` directly. Verify links and generated rules after sync, then use fresh sessions to load the updated inventory.

## Invocation contract

- Always apply `write-like-shiv` for writing. Select additional skills that resolve a current need. Avoid overlapping guidance and prerequisite chains for routine work.
- Read only references relevant to the chosen workflow. Preserve specialized procedures when correctness or safety depends on their sequence.
- Imported examples and suggested commands follow the kernel and repository conventions. Use existing authorization, actual tool availability, the configured model, and the repository's package manager and checks. Keep skill discovery separate from installing dependencies or executing the discovered workflow.
