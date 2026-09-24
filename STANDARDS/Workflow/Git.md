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

Use `create-pr` for preparation and publication, and `follow-up-on-pr` for requested updates to an open PR. This file owns title, ticket, verification, and merge conventions when imported examples differ. Standalone maintenance needs no ticket. Inspect PR state before updating it; a merged PR requires a linked follow-up PR. Apply review comments after checking their claims against the current diff. Merge and deploy remain governed by the user's authorized scope.

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

## Cubic review comments

Cubic is an automated reviewer on our PRs. When Shiv hands over a Cubic review, test every comment instead of applying it. Some comments catch real defects; others misread the system or ask for changes outside the PR's scope. Both outcomes need a reply so Cubic's next review is sharper.

For each comment:

1. Read the affected code and the current diff, then decide whether the change it asks for is correct and in scope for this PR.
2. If the change holds, make it, commit it on the PR's branch, and reply with the short commit SHA.
3. If the change does not hold, leave the code as is and reply with the reason: the behavior is intentional, the claim is wrong about this system, or the work belongs outside this PR.
4. If the comment is valid but wider than this PR, say so and open a follow-up ticket or note it in the PR.

Reply on Cubic's own review thread, not a new top-level comment. Keep it two or three plain-English lines: the decision, the reason, and the commit when one exists. Write for Cubic as the reader; name what matters to this system and correct any misreading of it. Do not reply "done" by itself, and do not argue for its own sake. Leave the thread open for Cubic's response.

List the review comments, then reply to one:

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/comments
gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies -f body='...'
```


## Merge policy

Default:
- squash merge to protected branch
- delete branch after merge

Do not carry long-lived branches unless the product workflow explicitly requires them.
