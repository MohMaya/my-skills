---
name: code-review
description: Review a diff or PR against repository standards and the requested behavior. Use for branch, commit, or working-tree reviews.
---

Review the requested change on two axes:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue / spec?

Delegate independent axes when the review is substantial and the runtime supports sub-agents. Review small or tightly coupled changes locally.

Use the project's configured tracker when its delivery workflow requires one. A local review does not require tracker setup.

## Process

### 1. Pin the fixed point

Use the explicit commit, branch, tag, PR base, or working-tree scope. Infer the target from repository context when unambiguous. Ask only when plausible targets produce materially different reviews.

For a branch review, use `git diff <fixed-point>...HEAD` and `git log <fixed-point>..HEAD --oneline`. For working-tree changes, use the requested staged or unstaged diff. Record the scope so every reviewer examines the same change.

Verify references resolve and inspect the diff. If it is empty, report that result. Resolve an invalid reference before reviewing.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. The user's request, supplied document, or PR description.
2. Linked issues, fetched through the configured project workflow when available.
3. A relevant specification under `docs/`, `specs/`, or `.scratch/`.

If none is available, continue correctness and standards review. State that requirement coverage could not be verified. Ask for a specification only when missing intent prevents assessing a material behavior.

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below: a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Review the two axes

For a delegated review, provide the scope and these briefs. Apply the same criteria during local review.

**Standards brief** should include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the smell baseline from step 3** pasted in full (the sub-agent has no other access to it).
- The brief: "Report, per file/hunk where relevant, (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Distinguish hard violations from judgement calls: documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words."

**Spec brief** should include:

- The diff command and commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."

If the spec is missing, omit the requirement-coverage review and state that limit.

### 5. Aggregate

Verify findings against the actual diff and relevant context. Remove duplicates and unsupported claims. Report actionable findings by severity, with file references and concrete consequences. Label each finding's axis when useful. Keep requirement gaps visible alongside standards findings. State review limits and say when no actionable findings remain.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.
