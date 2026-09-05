# Core/Execution.md

Use this guidance when execution scope, verification, or completion is unclear.

## Discovery

Read the instructions and implementation that govern the requested change. Inspect callers, configuration, and dependencies when they affect the decision.

Use targeted searches before broad repository exploration. Load additional standards or skill references only when they answer a live question.

## Before adding an artifact

For a new function, type, table, role, helper, or document, establish its current purpose and caller. Check whether existing code can absorb the need.

For a trust boundary, establish the legitimate entry path and required validation. Keep separate responsibilities under clear ownership.

Omit artifacts whose removal would not affect the requested outcome. Keep routine reasoning local; explain material choices to the user.

## Execution and verification

Follow the kernel's scope and authorization contract. Resolve ordinary implementation choices and continue through fixes within that scope.

Choose verification from the changed behavior and repository requirements. Use a reproducing test for a bug when practical. Use inspection or a focused manual check when that better fits the change.

Check test configuration before assuming fixtures are disposable or services are isolated. A label such as local does not establish production safety.

Run affected checks after relevant edits. Broaden or repeat them when new evidence warrants it. Fix failures caused by the change and report unrelated failures.

## Completion

Compare the result with the user's requested artifacts and delivery actions. Check changed references, observable behavior, and material failure modes.

An implementation awaiting requested validation or delivery is unfinished. Continue until the authorized outcome is complete or a concrete blocker requires input.

Report what changed, the relevant verification, and any remaining limitation. Do not present static instruction checks as measured improvements in agent performance.
