# Source

UI review has one owner, this skill. The `userinterface-wiki` skill (raphaelsalaja/userinterface-wiki, MIT, v3.0.0, 152 rules) was folded in on 2026-10-18 and deleted. These of its rules were rewritten into the owners an agent loads at review time (`references/engine.md` loads every `pe-build/references/craft/` area). Its other rules were dropped: library-specific (ForesightJS prefetch, one icon library's morphing system), unverifiable or unsourced numbers (sound-synthesis frequencies and envelopes), numbers that contradict the motion and touch owners (durations, stagger, press scale, 32px targets), CSS basics, or engagement nudges against the kernel's core-job rule.

| Rule (upstream) | Now lives in |
| --- | --- |
| `exit-requires-wrapper`, `exit-prop-required`, `exit-key-required`, `presence-*`, `mode-*`, `nested-propagate-required` | `pe-build/references/craft/ui/enter-exit.md`, AnimatePresence mechanics; review reaches it through `references/engine.md` |
| `container-two-div-pattern`, `container-use-resize-observer`, `container-guard-initial-zero` | `pe-build/references/craft/ui/animations.md`, Height animations (`animate/RECIPES.md` Accordion points there) |
| `type-justify-with-hyphens` | `pe-build/references/craft/typography/wrapping-and-punctuation.md` |
| `ux-doherty-under-400ms`, `ux-doherty-perceived-speed`, `ux-goal-gradient-progress` | `references/experience-rubric.md`, S1 |
| `a11y-visual-equivalent`, `a11y-toggle-setting`, `appropriate-*`, `context-reuse-single`, `context-resume-suspended`, `envelope-no-zero-target`, `impl-reset-current-time`, `impl-preload-audio` | `pe-build/references/craft/ui/ui-sound.md` (sources: Chrome autoplay policy, MDN AudioParam) |
