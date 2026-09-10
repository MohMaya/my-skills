# Workflow/Git.md

Load for branches, commits, PRs, and merge discipline.

## Protected branches

Do not commit directly to these protected branches unless you have explicit permission. Always use a feature branch and a PR.
- `main`
- `develop`
- `next`

## Branch naming

Default pattern when a tracker is in play:

`sc/TICKET-123-short-description`

Rules:
- include the tracker key
- keep the description short and kebab-case
- use a branch only as long as needed

If the product uses trunk-based development, aim to merge within one to two business days.

Example: Linear ticket `PA-124: Add user authentication` → branch `sc/PA-124-add-user-authentication`.

## Commit format

Canonical for every tracker and harness. Generate the message with `caveman-commit`.

When tracker-linked workflow is active, use:

`TICKET-123: Imperative description`

Rules:
- uppercase ticket key
- no leading zeroes
- colon plus space separator
- imperative subject
- meaningful description, not noise

Optional body:
- explain why
- note follow-up if needed

## Pull requests

Apply `i-have-adhd` to PR bodies by default. Use plain English to describe the problem, what changes for the reader, and how the change was checked. Include technical terms when they help review; explain unfamiliar terms and preserve exact identifiers, required templates, and line counts. PR bodies follow the everyday communication rules in `Core/Prose.md`.

Minimum bar:
- self-contained change
- tests or equivalent verification
- green CI
- reviewed before merge

If the PR body exists, the first line should follow the same tracker format as the title.

Recommended PR shape:
- title: `TICKET-123: Imperative description`
- first line: `TICKET-123: Imperative description`
- summary (what changed and why; use bullet points)

When tracker-linked workflow is active, PR titles and the first line of PR bodies begin with the uppercase
tracker key. Otherwise use the repository's format and a concrete imperative subject. Do not put a conventional-commit type such as `feat:` before
the tracker key. For stacked PRs, use the tracker key belonging to the
individual layer, and reference the parent ticket in the body when needed.

## Review posture

Run `code-review` for correctness, `ponytail-review` when bloat is the question. The review bar itself -- what to look at and in what order -- is `Core/Code.md`.

## Merge policy

Default:
- squash merge to protected branch
- delete branch after merge

Do not carry long-lived branches unless the product workflow explicitly requires them.
