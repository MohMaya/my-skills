# pstack model configuration

Single-model roles inherit the model selected in the Codex session. The strongest judgment role uses Astra. Panels use distinct available GPT models. These are one model family, so report reduced diversity when a workflow calls for cross-family review.

feature, refactoring: inherit-parent
bug-fix: gpt-6-astra
perf-issue: gpt-6-astra
hillclimb: gpt-6-astra
judgment and prose: inherit-parent
strongest judgment: gpt-6-astra
how explorer: inherit-parent
how explainer: inherit-parent
why investigators: inherit-parent
why synthesizer: inherit-parent
reflect tooling: inherit-parent
reflect judgment, divergent, synthesizer: inherit-parent
arena runners: gpt-6.1-sol, gpt-6-astra, gpt-6-luna
arena cross-judge pool: gpt-6.1-sol, gpt-6-astra, gpt-6-luna
swarm workers: inherit-parent
architect runners: gpt-6.1-sol, gpt-6-astra, gpt-6-luna
interrogate reviewers: gpt-6.1-sol, gpt-6-astra, gpt-6-luna

default effort: session
session hook: off
