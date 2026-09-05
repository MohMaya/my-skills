---
name: golang-how-to
description: "Select Go skills when routing is unclear, distinguish overlapping specialties, or configure task-specific project guidance on explicit request."
user-invocable: true
license: MIT
compatibility: Designed for Claude Code or similar AI coding agents. Requires git.
metadata:
  author: samber
  version: "1.3.0"
  openclaw:
    emoji: "🧭"
    homepage: https://github.com/samber/cc-skills-golang
    requires:
      bins:
        - go
        - gopls
    install:
      - kind: go
        package: golang.org/x/tools/gopls@latest
        bins: [gopls]
allowed-tools: Read Edit Write Glob Grep Bash(go:*) Bash(git:*) Agent AskUserQuestion LSP Bash(gopls:*) mcp__gopls__*
---

# Go skill router

Use this router when the task does not clearly match an available Go skill.
When a skill already matches, load it directly.

## Select the next skill

1. Identify the task's immediate concern and the repository's existing conventions.
2. Check the active skill inventory before choosing a skill.
3. Read the matching category in [by-category.md](references/by-category.md) when discovery needs more detail.
4. Read the relevant boundary in [disambiguation.md](references/disambiguation.md) when specialties overlap.
5. Load the smallest set that supplies missing task-specific guidance.
6. Add another skill when a distinct concern arises during the work.

The catalog's recommendations describe useful coverage; they do not require loading every recommended skill.
Library-specific skills apply when the task uses or evaluates that library.
A missing optional skill does not block work that available tools and repository guidance support.

Short names in the references identify `samber/cc-skills-golang@<name>` skills.
Resolve them through the active runtime or a readable local `SKILL.md`.

## Code navigation with gopls

Use `golang-gopls` for semantic navigation, diagnostics, or refactoring within the locally resolved Go build.
That skill owns tool setup and the choice between MCP, native LSP, and CLI access.
Routing itself needs no language-server installation.

## `godig` vs gopls vs Context7 vs govulncheck

| Task | Tool and skill |
| --- | --- |
| Published Go documentation, versions, licenses, importers, or package vulnerabilities | `godig`, through `golang-pkg-go-dev` |
| Local definitions, call sites, diagnostics, and refactoring, including resolved dependencies and `replace` directives | `gopls`, through `golang-gopls` |
| An on-demand vulnerability reachability check of the current build | `gopls` vulnerability check, through `golang-gopls` |
| A whole-module vulnerability audit or CI gate | `govulncheck`, through `golang-security` |
| Non-Go documentation or Go documentation unavailable through pkg.go.dev | Context7, when available |

Published vulnerability records describe a package version; build reachability checks determine whether the current code can reach vulnerable functions.
Library selection belongs to `golang-popular-libraries`; dependency changes belong to `golang-dependency-management`.
Read the selected skill for commands and detailed workflows.

## Configure mode

Configure project guidance only when the user explicitly requests configuration, including `/golang-how-to configure`.
Follow [project-config.md](references/project-config.md) to add task-specific routes to the project's existing instruction owner.
Ordinary Go work and project creation do not authorize configuration changes through this skill.
