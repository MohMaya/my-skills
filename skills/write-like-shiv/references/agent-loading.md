# Loading and enforcement

Keep one maintained skill directory. On a machine where the skill files are present, expose that directory at `~/.agents/skills/write-like-shiv/`; a symlink is sufficient for Codex. Keep `assets/AGENTS.md` available as `~/.agents/AGENTS.md`. These files must exist on each host that needs them. A path created inside a remote session does not install anything on Shiv's Mac.

## Host routing

| Host | How it loads the contract | What remains to verify |
| --- | --- | --- |
| ChatGPT Work | Install this personal skill; select Write Like Shiv with @ or allow task matching | Installation makes the skill available. Automatic selection is not a guarantee it is invoked for every response. |
| Codex CLI / IDE | Discover `~/.agents/skills/write-like-shiv/`; add a short instruction in the actual Codex home `AGENTS.md` to read `~/.agents/AGENTS.md` for prose work | Check for an existing `AGENTS.override.md`, which takes precedence at that level. Verify loading in a fresh task. |
| Claude Code | Add the import `@~/.agents/AGENTS.md` to `~/.claude/CLAUDE.md`, preserving existing instructions | Verify with `/context`. Claude Code does not automatically read AGENTS.md. Cowork has different file-import restrictions. |
| Gemini CLI | Import the shared contract from `~/.gemini/GEMINI.md` using an actual absolute path, for example `@/Users/your-user/.agents/AGENTS.md` | Verify with `/memory show`; use `/memory reload` after a change. Do not assume tilde expansion in imports. |
| Other agent / API application | Inject the contract and SKILL.md through that host's supported instruction or context mechanism | Confirm access to references and test one real output; a directory name alone has no effect. |

Official references, checked September 8, 2026: [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills), [Codex instruction loading](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude Code memory](https://code.claude.com/docs/en/memory), [Gemini CLI context](https://geminicli.com/docs/cli/gemini-md/).

## The enforcement boundary

A prompt can condition word choices and require a review pass. It cannot replace the model's probability distribution, directly set sampling in an unavailable runtime, or guarantee that another host loads the skill. Keep provider sampling defaults unless the application exposes them and a controlled comparison supports a change. Higher temperature is not a voice model.

The checker offers repeatable pattern detection. Its optional strict exit status can require editorial review in an application controlled by Shiv, but it cannot judge factual support or authentic personal tone. No publication pipeline or hook has been configured by this package. True application-level enforcement requires that pipeline to run the check and reject or hold a draft before releasing it.

Pangram's own [technical report](https://arxiv.org/html/2402.14873v3) describes a trained transformer classifier and a data-selection procedure using synthetic examples. Its [explanation of detection](https://www.pangram.com/blog/how-does-ai-detection-work) distinguishes its approach from simple perplexity and burstiness measures. Neither provides a measurement of Shiv's preferred voice. Use accepted revisions as the calibration target.

## File responsibilities

| File | Purpose, caller, and consequence if absent |
| --- | --- |
| SKILL.md | A writing agent reads the shared voice contract; without it the package has no usable skill entrypoint. |
| agents/openai.yaml | The skill selector reads its name, summary, and invocation prompt; without it this package lacks its intended UI presentation. |
| references/surfaces.md | The drafting agent selects form-specific guidance; without it a message, journal, and design doc tend to inherit one inappropriate template. |
| references/corpus.md | An agent researching or updating the voice reads source links, evidence status, and annotations; without it inferred taste loses provenance. |
| references/calibration.md | The editor reads examples and diagnostic limits; without it generated examples or rhythm statistics can be mistaken for personal evidence. |
| references/agent-loading.md | An installer or host maintainer reads the loading boundaries; without it ~/.agents/ can be mistaken for universal enforcement. |
| assets/AGENTS.md | A configured host loads the compact default contract; without it implicit skill selection remains the only default trigger. |
| scripts/voice_check.py | The writing agent or an explicitly configured publication pipeline runs repeatable checks; without it review depends entirely on model attention. |

For portability, copy the complete skill folder, including references, script, and contract. Preserve existing host configuration and its unrelated instructions. The Notion reading profile is the browsing and feedback surface; this package is the executable instruction surface. A change to one does not automatically update the other.
