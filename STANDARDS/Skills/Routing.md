# Skills/Routing.md

Apply `write-like-shiv` whenever writing or revising anything. Read `~/.agents/skills/write-like-shiv/SKILL.md` and its relevant surface reference before drafting, including short replies and progress updates. Use this router for additional specialist guidance. The active runtime provides the installed inventory. Load the matching entry, not the entire tree.

The runtime list and readable canonical skill files establish availability. When the runtime list is incomplete, use `rg --files ~/.agents/skills -g SKILL.md` to find names, then search task terms within those files. Read the matching frontmatter and body before selecting a skill. Resolve bundled references relative to its folder. `.skill-lock.json` identifies imported sources; it does not prove that a skill's tools are installed.

## Routes

| Task | Load |
| ---- | ---- |
| Unclear standards ownership or conflicting doctrine | `STANDARDS/INDEX.md` |
| Writing or changing code | `shiv-code-gate`; `Core/Code.md` for quality and layer rules; `Core/Execution.md` when execution is unclear |
| Closing out a diff (pre-commit/PR) | `simplify` |
| Requested chat compression | `caveman` |
| Requested humanization or prose with AI-sounding patterns | `humanizer`; `write-like-shiv` owns voice |
| Everyday communication, including chat, Linear tickets, PR bodies, and delegated-agent output | `i-have-adhd` by default in every session; plain English; `Core/Prose.md` defines prose-artifact exceptions and session overrides |
| Substantial knowledge-base document | `Core/Documents.md`; a clarity pass before delivery |
| Any writing or revision: chat, updates, trackers, documents, comments, commits, PRs, product copy, or agents | `write-like-shiv` and its relevant surface reference; `Core/Prose.md`; `Core/Documents.md` when document shapes help |
| Essay, article, or memo | Select `writing-fragments`, `writing-shape`, or `edit-article` for the current stage |
| Planning, scoping, tradeoffs, sequencing | `Core/Planning.md` |
| Stress-testing a plan, decision, or idea | `grilling` |
| Grilling touches module shape or boundaries | `codebase-design` for the structural questions |
| Publishing a spec | `to-spec` |
| Filing tickets | `to-tickets` |
| Writing a PRD | `writing-prds` |
| Work too big for one session | `wayfinder` |
| Implementing from a spec or tickets | `implement` |
| Session ending mid-work | `handoff` |
| Judging quality, taste, expert behavior | `Core/Craft.md` |
| Module or interface design | `codebase-design`, `design-an-interface`, `domain-modeling` |
| Repo-wide architecture cleanup | `improve-codebase-architecture` |
| Throwaway spike to answer a design question | `prototype` |
| Reading legwork against primary sources | `research` |
| Commit messages | `caveman-commit` |
| Reviewing a diff or PR | `code-review` for correctness; `ponytail-review` for bloat |
| Whole-repo bloat audit | `ponytail-audit`; `ponytail-debt` for the deferred-shortcut ledger |
| Hard bugs, perf regressions | `diagnosing-bugs` |
| Merge or rebase conflicts | `resolving-merge-conflicts` |
| Git, commits, branches, PRs | `Workflow/Git.md` |
| Create a PR; update an open PR after review or CI failures | `create-pr`; `follow-up-on-pr` respectively; `Workflow/Git.md` owns conventions and delivery scope |
| GitHub issues and `gh` flow | `Workflow/GitHub.md` |
| Stacked branches and dependent PRs | `gh-stack`, then `Workflow/GitHub.md` |
| CI, deploys, rollback, flags, runtime safety | `Workflow/Delivery.md` |
| Linear workflow | `Workflow/Linear.md` |
| Notion knowledge base | `Workflow/Notion.md` |
| Auth-touching code or pre-launch | `security-review` |
| Review a security-sensitive diff; build a threat model; validate a finding | `commit-security-scan`; `threat-model-generation`; `vulnerability-validation` respectively; `Workflow/Delivery.md` defines evidence and authorization boundaries |
| E2E or browser testing | `playwright-cli` |
| Test-first loop on new behavior | `tdd` |
| Stack-specific work | matching file under `STANDARDS/Stack/` |
| React effects, TypeScript assertion rules, or unused exports reported by Knip | `no-use-effect`, `ban-type-assertions`, or `fix-knip-unused-exports` for the specific change; `Stack/TypeScript.md` |
| Postgres schema, queries, migrations | `supabase-postgres-best-practices` |
| FastAPI / Python API work | `fastapi` |
| Go | `golang-code-style`, `golang-error-handling` |
| Backend on Railway | `use-railway` |
| Vercel cost or perf | `vercel-optimize` |
| Mobile (Expo / React Native) | `expo-native-ui`, `expo-router`; ship via `eas-workflows`, `eas-app-stores` |
| LLM features | `ai-sdk` (TS), `claude-api` (Anthropic specifics) |
| Implement a responsive UI; choose an art direction | `frontend-design`; `design-taste-frontend` for direction and `high-end-visual-design` for premium surfaces; preserve the existing stack |
| Figma design → code | `figma:figma-design-to-code`; `extract-design-system` to formalize tokens first |
| Code or description → Figma | `figma:figma-generate-design` (screens), `figma:figma-generate-library` (design system); `figma:figma-use` before any `use_figma` call |
| UI polish and motion | `emil-design-eng`, `apple-design`, `web-design-guidelines` |
| Animation work | `improve-animations` to plan, `review-animations` to review, `animation-vocabulary` to name the effect |
| Marketing copy, GTM, pricing | `product-marketing` context first, then `copywriting` / `positioning` / `pricing` |
| Product architecture | `Product/Architecture.md` |
| Office file in or out | `docx`, `pptx`, `xlsx` |
| Images, diagrams, or presentations | `visual-design` and only its matching reference; existing image and presentation workflows own delivery |
| Requested human-writing edit | `human-writing` under `write-like-shiv`; `Core/Prose.md` owns everyday formatting and prose exceptions |
| Initialize repository instructions; author a skill | `init`; `skill-creation` respectively; inspect existing instructions and preserve canonical ownership. `template-skill` is an unfinished authoring example |
| Explicit iterative optimization experiment | `autoresearch`; `Core/Execution.md` defines budget, isolation, and stopping conditions |
| Browse with the installed browser CLI; locate a prior Droid session | `browser-navigation`; `session-navigation` respectively; verify the named CLI and local data exist |
| Automate a terminal, browser, or desktop; record a demo | `droid-control` is the entry point; select background skills from the map below |
| Inspect HTTP traffic from a CLI or service | `http-toolkit-intercept`; scope capture to the requested process and protect credentials in captured traffic |
| Can't find the right skill | `find-skills` |

## Droid control background skills

Load these through `droid-control` for the chosen task. Prefer purpose-built tools exposed by the current harness. Check driver, browser, operating-system, and recording dependencies before running commands; adapt tool names to the current harness.

The copied skill folders contain instructions and selected references. Droid control and video workflows also expect an installed plugin runtime providing `DROID_PLUGIN_ROOT`, `bin/tctl`, rendering scripts, and a Remotion project. Verify those assets before choosing that workflow. When absent, use an available harness tool or report the specific dependency needed for the requested action.

| Need | Background skill |
| ---- | ---- |
| Virtual terminal; real terminal input; raw key sequences | `tuistory`; `true-input`; `pty-capture` respectively |
| Web or Electron app; native desktop app | `agent-browser`; `desktop-control` respectively |
| Droid CLI controls | `droid-cli` |
| Recording; video assembly; visual polish | `capture`; `compose`; `showcase` respectively; use the existing project stack and authorized output scope |
| Verify promised deliverables | `verify` |

## Requested humorous reports

Factory's cursed-plugin skills produce humorous codebase reports. Use them only for an explicit request for that skill or report style: `agent-repellent`, `blame`, `cobol-converter`, `dating-profile`, `feng-shui`, `obituary`, `performance-review`, `roast`, `ship-ritual`, and `therapy-session`. `performance-review` here concerns a codebase, not an employee; `ship-ritual` is entertainment, not release verification. Keep normal engineering, security, and people workflows on their task routes. Advertising, sharing, and external publication require their own user request.

## Availability

Routes name preferred skills, not guaranteed installations. The active runtime and readable `~/.agents/skills/*/SKILL.md` files determine availability. Verify provider-specific tools in the current session. For `simplify`, re-climb the code gate if the skill is absent. For unavailable document or domain skills, apply the relevant standards directly and state the gap. Figma capabilities depend on the installed integration, not the harness name.

Run `bash ~/.agents/sync.sh` after changing canonical skills or the kernel. It maintains Codex, Claude, and Cursor skill links and generated harness rules. Gemini CLI reads the shared kernel import; Antigravity reads the configured canonical skills path. Droid supports `~/.agents/AGENTS.md` and `~/.agents/skills/**/SKILL.md` directly. Verify links and generated rules after sync, then use fresh sessions to load the updated inventory.

## Invocation contract

- Always apply `write-like-shiv` for writing. Select additional skills that resolve a current need. Avoid overlapping guidance and prerequisite chains for routine work.
- Read only references relevant to the chosen workflow. Preserve specialized procedures when correctness or safety depends on their sequence.
- Imported examples and suggested commands follow the kernel and repository conventions. Use existing authorization, actual tool availability, the configured model, and the repository's package manager and checks. Keep skill discovery separate from installing dependencies or executing the discovered workflow.
