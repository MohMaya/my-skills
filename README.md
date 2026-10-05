# Shiv's agent setup

Claude Code and Codex use pstack for engineering execution and verification, Matt Pocock Skills for requirements and test-first workflows, and `write-like-shiv` for voice. Supermemory remains the shared memory service. `AGENTS.md` connects the systems without copying their playbooks.

Lauren's [Complete Guide to pstack, Part 1](https://x.com/poteto/status/2094457600259842065) makes verification the foundation. Each product repository needs a working driver and Feature Map. The global instructions make agents create or maintain those when needed. This repository does not claim to have configured every product or scheduled daily maintenance.

The [claude.ai performance report](https://claude.dev/blog/how-we-made-claude-ai-faster/) adds the production feedback loop: choose important journeys, validate lab proxies, preserve wins in CI, and check field telemetry. pstack already supplies the measurement and iterative optimization workflows. Project repositories own the actual instruments and budgets.

## Set up a machine

Install [Matt Pocock Skills](https://github.com/mattpocock/skills) in both harnesses. Install the full [pstack port for Claude Code and Codex](https://github.com/michael-denyer/pstack-claude), which adapts [Lauren's upstream pstack](https://github.com/cursor/plugins/tree/main/pstack). Keep the [Supermemory Claude plugin](https://github.com/supermemoryai/claude-supermemory) and Codex connector installed and authenticated. The curated Codex `pstack-plugin` is a ChatGPT subset and lacks `poteto-mode` and the verification generators.

The tested pstack port is `0.9.70`, from commit `72270b73211a4b9baa673a33728bb18b05684f91`. Matt Pocock Skills is `1.2.3`.

```sh
claude plugin marketplace add michael-denyer/pstack-claude
claude plugin install pstack@pstack-claude
codex plugin marketplace add michael-denyer/pstack-claude --ref 72270b73211a4b9baa673a33728bb18b05684f91
codex plugin add pstack@pstack-claude
codex plugin add mattpocock-skills@openai-curated-remote
bash ~/.agents/sync.sh
```

Enable Codex subagents in `~/.codex/config.toml` if they are disabled:

```toml
[features]
multi_agent = true
```

Start fresh Claude and Codex sessions after setup. Rerun `sync.sh` after changing the shared instructions or model sheets. It rewrites the two global instruction files, links the voice skill and model sheets, and preserves unrelated runtime settings. Back up any independent global instructions before adopting this setup.

The sync also disables Claude's cloud skill and plugin sync so archived skills and disabled workflow plugins stay out of the active catalog. It links the installed Matt `1.2.3` skill tree into Codex's local discovery directory because the CLI does not load the remote plugin catalog. This is a link to the plugin's files, not another copy. Update that version in `sync.py` when upgrading Matt and repeat the discovery check.

Claude loads pstack's native session hook. Codex uses the standing instruction in its generated `AGENTS.md`; its optional plugin hook is off, so routing does not depend on hook trust. Codex's model rows are included in that file because Codex does not support Claude's `@` imports.

## Use the systems

Describe the outcome. pstack selects the engineering playbook for substantial work. Ask for Matt's planning or implementation workflow when you want that flow. His explicit-entry skills remain explicit-entry. The shared instructions compose the two without starting competing execution loops.

Use `write-like-shiv` for authored prose. It is the only personal skill in `skills/`. Browser and computer tools, language servers, document tools, and service connectors remain available to execute the work.

Supermemory calls use `user_shiv` across surfaces. Sync preserves its enabled Claude plugin and sets `SUPERMEMORY_REPO_TAG` to the same value while preserving unrelated environment and plugin settings. Cloud plugin sync stays off so disabled workflow plugins do not return. Ponytail stays disabled.

The model sheets live in `claude/` and `codex/`. Ordinary roles inherit the selected session model. Claude's review panels use its supported model families. Codex uses available GPT models and reports the reduced diversity compared with a cross-family panel. These settings do not create cloud workers or raise agent limits.

## Check the wiring

```sh
./check.sh
bash -n sync.sh check.sh
python3 -m unittest -v test_sync.py
claude plugin details pstack@pstack-claude
codex plugin list --json
```

The tests exercise instruction generation, repeat runs, existing shared skill links, conflicting skill preservation, and missing-source failures. Fresh-session probes additionally check skill discovery and workflow routing. Neither check proves quality on an application that has not been exercised.

## Recover the old system

`alt-main` preserves the previous setup, including its formerly untracked cloud-synced skills. The migration also saved a private archive under `backups/`, including the previous Claude and Codex configuration. That directory is ignored by Git and should stay private.

To inspect the tracked old system without changing the active harness:

```sh
git show alt-main:AGENTS.md
git ls-tree -r --name-only alt-main
```

Restoring the old setup requires both its repository files and its runtime settings. Switching branches alone does not re-enable disabled plugins or restore configuration. The archive and plugin inventory in `backups/` preserve that state.
