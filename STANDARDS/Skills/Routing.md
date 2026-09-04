# Skills/Routing.md

The single router: situation → what to load, plus the installed inventory. The kernel owns the mandates (always-on skills, the grilling gate, the subtractive pass, the prose pipeline); this file does not restate them.

The runtime's available-skills list is the source of truth for what is loadable right now. Never route to a skill you cannot see in the runtime or verify on disk; use `find-skills` only when available.

## Routes

| Task | Load |
| ---- | ---- |
| Any non-trivial task | `STANDARDS/INDEX.md` |
| Writing or changing code | `shiv-code-gate`, then `Core/Code.md` + `Core/Execution.md` |
| Closing out a diff (pre-commit/PR) | `simplify` |
| Writing anything that is not code | `caveman` |
| Knowledge-base doc (Notion, TDD, spec, `docs/`) | Concise draft; clarity pass per the kernel |
| Chat replies, PR text, README edits | `Core/Prose.md`, `Core/Documents.md` |
| Any composed piece (essay, article, memo) | `writing-fragments` → `writing-shape` → `edit-article` |
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
| New UI, screens, or design direction | `design-taste-frontend` (mandatory taste pass); `high-end-visual-design` for premium surfaces |
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

- Prefer the smallest useful set: one process skill, one domain skill, one polish skill if needed. No overlapping loads.
- Apply the kernel's availability fallback when a routed skill is missing. Load only skills that improve the current task.
