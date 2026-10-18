# Source and local changes

Upstream identity is in `.skill-lock.json`; it is not a claim that local files are unmodified.

Local edits on 2026-10-18 (re-apply after `npx skills update`):
- A plain `git push` passes, because `~/.agents/hooks/review-gate.py` gates pushes on a review. Pushes that rewrite or delete remote history stay blocked: `--force`, `--force-with-lease`, `-f`/`-d` alone or bundled, `--delete`, `--mirror`, `--prune`, and `+ref` or `:ref` refspecs.
