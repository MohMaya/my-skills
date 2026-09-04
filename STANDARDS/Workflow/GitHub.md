# Workflow/GitHub.md

Load when the task touches GitHub issues, labels, milestones, projects, or `gh`. Commits, branches, and PR bar: `Workflow/Git.md`.

## Issues

Good issues contain:
- a precise title in the tracker format from `Workflow/Git.md`
- enough context to reproduce or understand the problem
- concrete acceptance criteria when it is implementation work

Keep labels useful:
- one type label
- one priority label when needed
- area labels only if the repo uses them consistently

## Issue to code flow

Preferred sequence:

1. issue or ticket exists
2. branch references the issue or tracker key
3. commits stay linked
4. PR references the issue
5. issue closes from the merged PR

## `gh` usage

Prefer `gh` over the web UI for repeatable operations.

Typical use:
- inspect issues and PRs
- open or update PRs
- inspect checks
- manage labels and assignees

## Projects and milestones

Use milestones or project state only if the repo actually relies on them.
Do not create a second planning system inside GitHub if Linear or Jira is already primary.

## Stacked branches and PRs

Use the `gh-stack` skill (backed by the `gh stack` CLI extension) when work ships as a chain of dependent PRs: creating, pushing, rebasing, syncing, or navigating a stack. One branch per layer, each PR based on the branch below it, reviewers see only that layer's diff.
