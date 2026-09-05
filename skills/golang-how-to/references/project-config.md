# Configure task-specific Go skill routing

Use this workflow only when the user explicitly requests project instruction configuration, including `/golang-how-to configure`.
Existing user authorization covers the requested edits; ask only when the destination or required behavior remains materially ambiguous.

## Find the instruction owner

Read the project's root instruction files and follow their ownership rules and links.
Common owners include `AGENTS.md`, `CLAUDE.md`, Cursor rules, and `.github/copilot-instructions.md`.
Update the active owner named by the user or repository.
When several files serve different runtimes, change only those covered by the request.
If no owner exists and the target runtime is unclear, ask which instruction file to create.

## Select routes from project evidence

1. Read existing Go guidance, including any `Required Go skills` section.
2. Identify the requested workflow and relevant imports or tools.
3. Verify that each proposed skill is available in the runtime or has a readable local `SKILL.md`.
4. Choose a concrete task condition for each route.
5. Use an applicable company skill instead of its superseded community skill.

Use [by-category.md](by-category.md) for skill coverage and [disambiguation.md](disambiguation.md) for overlapping specialties.
Recommended catalog entries are candidates, not a default load list.
A repository's dependencies can justify a route for relevant work; they do not require loading that skill for every Go task.

## Write the smallest useful change

Preserve unrelated instructions and existing project requirements.
Update an existing routing section in place when it owns the concern.
Replace old unconditional directives only when that replacement falls within the user's configuration request.
Keep each skill's trigger specific to the work it supports.

For example, a project that uses Cobra and Viper could use these routes:

```markdown
## Go skill routing

- Load `golang-spf13-cobra` when changing Cobra command trees, flags, or completions.
- Load `golang-spf13-viper` when changing layered configuration or environment binding.
- Use `golang-how-to` when the task's skill choice remains unclear.
```

Adapt this example to verified project needs; omit irrelevant routes.
Use identifiers that the active runtime can resolve.
A company override applies only within the scope that its skill declares.

## Verify and report

1. Re-read the edited section and check that each route appears once.
2. Verify skill identifiers and instruction-file links.
3. Check that repeated configuration would preserve the same content.
4. Review the diff for changes outside the requested scope.
5. Report the files changed and the task conditions added or updated.

Describe metadata and body loading costs separately if the user asks about context usage.
Use measured lengths or clearly labeled estimates; loading a skill body costs more than discovering its description.
