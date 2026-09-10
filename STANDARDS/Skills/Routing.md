# Skills/Routing.md

Apply `write-like-shiv` whenever writing or revising anything. Read `~/.agents/skills/write-like-shiv/SKILL.md` and its relevant surface reference before drafting, including short replies and progress updates. Use this router for additional specialist guidance. The active runtime provides the installed inventory. Load the matching entry, not the entire tree.

The runtime's available-skills list is the source of truth for what is loadable right now. Never route to a skill you cannot see in the runtime or verify on disk; use `find-skills` only when available.

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
| GitHub issues and `gh` flow | `Workflow/GitHub.md` |
| Stacked branches and dependent PRs | `gh-stack`, then `Workflow/GitHub.md` |
| CI, deploys, rollback, flags, runtime safety | `Workflow/Delivery.md` |
| Linear workflow | `Workflow/Linear.md` |
| Notion knowledge base | `Workflow/Notion.md` |
| Auth-touching code or pre-launch | `security-review` |
| E2E or browser testing | `playwright-cli` |
| Test-first loop on new behavior | `tdd` |
| Stack-specific work | matching file under `STANDARDS/Stack/` |
| Postgres schema, queries, migrations | `supabase-postgres-best-practices` |
| FastAPI / Python API work | `fastapi` |
| Go | `golang-code-style`, `golang-error-handling` |
| Backend on Railway | `use-railway` |
| Vercel cost or perf | `vercel-optimize` |
| Mobile (Expo / React Native) | `expo-native-ui`, `expo-router`; ship via `eas-workflows`, `eas-app-stores` |
| LLM features | `ai-sdk` (TS), `claude-api` (Anthropic specifics) |
| New UI, screens, or design direction | `design-taste-frontend`; `high-end-visual-design` for premium surfaces |
| Figma design → code | `figma:figma-design-to-code`; `extract-design-system` to formalize tokens first |
| Code or description → Figma | `figma:figma-generate-design` (screens), `figma:figma-generate-library` (design system); `figma:figma-use` before any `use_figma` call |
| UI polish and motion | `emil-design-eng`, `apple-design`, `web-design-guidelines` |
| Animation work | `improve-animations` to plan, `review-animations` to review, `animation-vocabulary` to name the effect |
| Marketing copy, GTM, pricing | `product-marketing` context first, then `copywriting` / `positioning` / `pricing` |
| Product architecture | `Product/Architecture.md` |
| Office file in or out | `docx`, `pptx`, `xlsx` |
| Can't find the right skill | `find-skills` |

## Availability

Routes name preferred skills, not guaranteed installations. The active runtime and readable `~/.agents/skills/*/SKILL.md` files determine availability. Verify provider-specific tools in the current session. For `simplify`, re-climb the code gate if the skill is absent. For unavailable document or domain skills, apply the relevant standards directly and state the gap. Figma capabilities depend on the installed integration, not the harness name.

## Invocation contract

- Always apply `write-like-shiv` for writing. Select additional skills that resolve a current need. Avoid overlapping guidance and prerequisite chains for routine work.
- Read only references relevant to the chosen workflow. Preserve specialized procedures when correctness or safety depends on their sequence.
