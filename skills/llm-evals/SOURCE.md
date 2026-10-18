# Source and local changes

Adapted from [Seth Hobson's `eval-harness-first` skill](https://github.com/wshobson/agents/tree/9b15b34b0bfc13a815cbfc2366e14ea549e09422/plugins/llm-finetuning/skills/eval-harness-first).
Upstream revision: `9b15b34b0bfc13a815cbfc2366e14ea549e09422`. License: MIT.

Local changes on 2026-09-26:

- Renamed to `llm-evals` and reframed around prompt, model, retrieval, and tool changes in an LLM feature. Upstream gates fine-tuning runs.
- Removed the fine-tuning coupling: training-data holdout, drift suite, MMLU logprob scoring, base-model baseline, and links to sibling fine-tuning skills.
- Added deference to a repository's existing evaluation contract and runner.
- `references/grader-templates.md` drops the drift-suite sections; `references/judge-calibration.md` replaces checkpoint-promotion wording with ship decisions.

`.skill-lock.json` records upstream identity, not a claim that local files are unmodified.

Additions on 2026-10-18, rewritten from [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) `prompt-engineer`, `rag-architect`, and `ml-pipeline` (imported in commit 40c5f7c):

- `SKILL.md` Goldens: an injection test set for every prompt that ingests untrusted input (from `prompt-engineer/references/system-prompts.md`).
- `SKILL.md` Loop: a per-change record of version, hypothesis, result, and rollback (`prompt-engineer/references/prompt-optimization.md`), and dataset version, seed, and git commit per run (`ml-pipeline/references/experiment-tracking.md`).
- `SKILL.md` Graders and `references/grader-templates.md`: pairwise judging in both orders, counting only agreement (`prompt-engineer/references/evaluation-frameworks.md`).
- `SKILL.md` Judge calibration and `references/judge-calibration.md`: Cohen's kappa on human labels before they serve as ground truth (`prompt-engineer/references/evaluation-frameworks.md`).
- `SKILL.md` Retrieval: recall@k and MRR or nDCG on a fixed query set, index parameters versioned, deterministic chunk ids, in-layer tenant filter, abstain path, and embedding input types (`rag-architect/SKILL.md` and its `rag-evaluation.md`, `embedding-models.md`, `vector-databases.md`).
- Not adopted: 1-5 judge scores, uncalibrated judges, the "think step by step" prompt, JSON mode through the system prompt, stale model ids, the RRF snippet, `recreate_collection`, and md5 chunk ids.
