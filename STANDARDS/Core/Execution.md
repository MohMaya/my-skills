# Core/Execution.md

Load for day-to-day execution, especially when stack, process, or verification is unclear.

## Discovery order

Before changing anything:

1. Read the user request closely.
2. Read the local code or docs that already own the concern.
3. Check repo truth: lockfiles, CI, config, existing patterns.
4. Load what `Skills/Routing.md` routes for the task.
5. Then edit.

Do not ask the user for facts you can discover locally.

## Interrogate before you write

For each new artifact you are about to add -- function, type, table, column, role, repo, helper, test, migration row, config field -- answer these in one line each. If you cannot, do not write it.

1. Purpose. What real behavior does this enable? Not "supports future X." Today.
2. Caller. Who invokes this? Show the actual call site or the request that triggered the need.
3. Authentication / entry path, if it crosses a trust boundary. How does a caller legitimately reach this? If the answer involves "we will figure out later how it gets called," stop.
4. Conflation check. Is this trying to serve two distinct purposes (system vs human, internal vs external, read vs write)? Split or pick one.
5. Deletion test. If I leave this out, what fails, and how loudly? If nothing fails, leave it out.
6. Smallest shape. Could this be a plain value, a column, or a function instead of a class, table, or subsystem?

This is the same interrogation a strong reviewer will run on the diff. Running it before you write saves the round trip.

## Ask vs proceed

Ask when the architecture could fork in multiple valid ways, the choice crosses more than one layer, a wrong guess costs an hour of rework, or you are about to delete or replace significant existing behavior. Otherwise proceed and state the assumption.

## TDD and execution order

If the repo has tests, use the loop:

1. Write or identify the failing test.
2. Make the smallest change that passes.
3. Refactor with tests still green.

If the repo does not test that layer today, do not bolt on a new framework without cause. Follow the local pattern and pick verification by shape:

- pure function → unit test
- handler or endpoint → one integration test asserting status plus persisted state
- neither → paste the manual command and its output into the PR body

Default build order:
- contract first when the repo is contract-led
- otherwise core inward to outward: model, service, view

## History and checkpoints

Commit discipline is the kernel's. Outside a git repo, hold the same rule: never mix unrelated concerns in one edit pass.

## Verification before "done"

Do not claim completion until you have checked:

- the behavior changed for the intended reason
- tests or equivalent verification passed
- errors are explicit
- no new boundary violations appeared
- no stale references remain in docs you touched

## Stop conditions

Stop and surface it when:
- you hit a real blocker
- the task depends on a missing secret, service, or repo
- an instruction conflict remains material after applying the precedence rules
- repeated verification failures show the plan is wrong

Do not push through by guessing.
