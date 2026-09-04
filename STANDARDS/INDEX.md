# STANDARDS/INDEX.md

This folder is the operating system. `AGENTS.md` is only the kernel.

## Structure

| Area | Owns |
| ---- | ---- |
| `Core/` | How the agent codes, executes, plans, writes, and structures documents |
| `Skills/` | The single router: situation → skill or file, plus the installed inventory |
| `Workflow/` | Git, CI/CD, tracker workflow, knowledge base, runtime rules |
| `Stack/` | Language and framework rules |
| `Product/` | Product-specific architecture doctrine |

## Load order

1. `Skills/Routing.md` -- the router for everything below.
2. The matching `Core/` file.
3. The relevant `Workflow/` file if the task touches process or delivery.
4. The relevant `Stack/` file if the task touches a language or framework.
5. `Product/` only if the task is product-architecture specific.

## Ownership rule

One concern, one owner. If two files start teaching the same thing, the tree is drifting; collapse it to the owner below.

- Situation→skill routing and the skill inventory -- `Skills/Routing.md`. `Skills/Catalog.md` was folded into it and deleted.
- Code quality, layering, tests, comment policy, mocks only at IO edges, N+1 -- `Core/Code.md`.
- Execution behavior: discovery order, the interrogate-before-write checklist, verification, stop conditions -- `Core/Execution.md`.
- Planning quality and ADR triggers -- `Core/Planning.md`.
- Default tone -- `Core/Prose.md`.
- Document shapes, including the ADR template -- `Core/Documents.md`.
- Reading list behind the kernel's discipline -- `Core/Craft.md`.
- Commit format, branch naming, PR bar, merge policy -- `Workflow/Git.md`.
- GitHub issues, labels, and `gh` flow -- `Workflow/GitHub.md`. Git.md owns commits, branches, and PRs; GitHub.md does not restate those patterns.
- Delivery operations: pipeline, pre-commit minimum, observability, secrets in logs, rollback, feature flags, caching, schema compatibility -- `Workflow/Delivery.md`.
- Linear as the work tracker -- `Workflow/Linear.md`. Notion as the durable knowledge base -- `Workflow/Notion.md`. Linear tracks work; Notion holds why.
- Stack rules -- the matching file under `Stack/`. Each defers to `Workflow/Delivery.md` for the pre-commit minimum and adds only stack-specific checks.
- Product architecture -- `Product/Architecture.md`. Architecture-level statements only; operational rules defer to `Workflow/Delivery.md`.

Mandates -- always-on skills, the grilling gate, the subtractive pass, the prose pipeline, one package manager per repo -- are owned by the kernel and are not restated in this tree.

## Rewrite rule

Do not add a new standards file until you can explain why the concern cannot live cleanly inside an existing owner. Flat sprawl is just as bad as one giant constitution.
