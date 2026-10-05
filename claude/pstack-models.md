# pstack model configuration

Single-model roles inherit the model selected in the Claude session. Panels use the model families supported by the installed Claude pstack port.

feature, refactoring: inherit-parent
bug-fix: inherit-parent
perf-issue: inherit-parent
hillclimb: inherit-parent
judgment and prose: inherit-parent
strongest judgment: inherit-parent
how explorer: inherit-parent
how explainer: inherit-parent
why investigators: inherit-parent
why synthesizer: inherit-parent
reflect tooling: inherit-parent
reflect judgment, divergent, synthesizer: inherit-parent
arena runners: opus, fable, sonnet
arena cross-judge pool: opus, fable, sonnet
swarm workers: inherit-parent
architect runners: opus, fable, sonnet
interrogate reviewers: opus, fable, sonnet

default effort: session
session hook: on
