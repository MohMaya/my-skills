# Source and local changes

Adapted from [Seth Hobson's `eval-harness-first` skill](https://github.com/wshobson/agents/tree/9b15b34b0bfc13a815cbfc2366e14ea549e09422/plugins/llm-finetuning/skills/eval-harness-first).
Upstream revision: `9b15b34b0bfc13a815cbfc2366e14ea549e09422`. License: MIT.

Local changes on 2026-09-26:

- Renamed to `llm-evals` and reframed around prompt, model, retrieval, and tool changes in an LLM feature. Upstream gates fine-tuning runs.
- Removed the fine-tuning coupling: training-data holdout, drift suite, MMLU logprob scoring, base-model baseline, and links to sibling fine-tuning skills.
- Added deference to a repository's existing evaluation contract and runner.
- `references/grader-templates.md` drops the drift-suite sections; `references/judge-calibration.md` replaces checkpoint-promotion wording with ship decisions.

`.skill-lock.json` records upstream identity, not a claim that local files are unmodified.
