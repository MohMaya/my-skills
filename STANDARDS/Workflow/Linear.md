# Workflow/Linear.md

Load when Linear is the system of record for work tracking.

## When Linear is primary

The Linear issue key is the tracker key in branch names, commit subjects, and PR titles. Patterns live in `Workflow/Git.md`.

## Issue hygiene

Apply `i-have-adhd` to ticket titles and bodies by default. Use plain English for the problem, expected behavior, and acceptance criteria. Keep necessary implementation details and exact identifiers; explain unfamiliar terms. Tickets follow the everyday communication rules in `Core/Prose.md`.

A usable issue has:
- clear summary in the tracker format
- context or problem statement
- concrete requirements or acceptance criteria
- owner when active
- links to related PRs or docs

## Branch and PR linkage

Close the loop by linking the PR back to the Linear issue and using the closing syntax your repo expects.

## Workflow expectations

- do not start vague tickets blind
- tighten the ticket before coding if the ambiguity would cause rework
- keep large efforts broken into smaller issues
- treat cleanup for feature flags and follow-ups as tracked work, not oral tradition

## Tooling

Use the Linear MCP tools (linear plugin) for reading, creating, and updating issues or projects -- issue state lives in the tracker, not in prose.
