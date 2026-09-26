---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
disable-model-invocation: true
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

## When to invoke

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## Process

### 1. Locate the active transcript

The parent finds its own transcript file before fanning out. Use only the active workspace's transcript directory. Never glob across every project's directory. That crosses workspace boundaries and reads private chats from unrelated projects.

Where the transcript lives depends on your harness:

- **Cursor:** the system prompt names the active workspace's `agent-transcripts/` directory. Use that path.

  ```bash
  ls -t <agent-transcripts>/*.jsonl <agent-transcripts>/*/*.jsonl <agent-transcripts>/*/subagents/*.jsonl 2>/dev/null | head -10
  ```

  Three transcript layouts: legacy flat (`<id>.jsonl`), current nested (`<id>/<id>.jsonl`), and subagent (`<parent>/subagents/<child>.jsonl`).
- **Claude Code:** `~/.claude/projects/<slug>/<session-id>.jsonl`, where `<slug>` is the workspace path with every character that isn't a letter or digit turned into "-".
- **Pi:** `~/.pi/agent/sessions/--<slug>--/*.jsonl`, where `<slug>` is the workspace path with the leading slash dropped and each "/" turned into "-".
- **Codex:** `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`. Keep only files whose first line has `payload.cwd` equal to the workspace path.
- **Other harnesses:** check the harness's session directory for this workspace.

Take the newest candidates first. Confirm a candidate by finding the conversation's opening user prompt in its first user message. Take the matching path. If no path resolves, write a tight digest of the session and pass that instead.

### 2. Spawn three reviewers in parallel

One message, three fresh-context subagents on the configured model, spawned with the current harness's subagent tool (in Claude Code: the Agent tool). Reviewers need MCP access for context lookups (tickets, chat threads, observability traces referenced in the transcript), so use a subagent type that keeps MCPs. If the harness has no subagent tool, run each role yourself, one after another.

| Lens | Prompt template |
|---|---|
| Judgment | `references/judgment-reviewer.md` |
| Tooling | `references/tooling-reviewer.md` |
| Divergent | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in the subagent's response body.

### 3. Synthesize

One fresh-context subagent on the configured model, with MCP access kept: the synthesizer's quality check includes spot-verifying citations, which can require MCPs. Use `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. The synthesizer returns a structured Accepted / Rejected / Backlog list.

### 4. Climb the trust ladder

For each Accepted learning, choose the most enforceable fix that holds, in this order:

1. **Structure.** Change code or data structures so the mistake is impossible.
2. **Check.** A lint rule, type, compiler check, or CI check. The repo's stop-gate hook enforces these at turn end.
3. **Skill or rule edit.**
4. **Human review.**

Propose rungs 1 and 2 before a skill edit. Rewrite any Accepted row that lands on rung 3 or 4 when a higher rung would hold, and say which rung each row sits on.

### 5. Apply

Before applying any Accepted edit, present the synthesizer's full Accepted/Rejected/Backlog output to the user and wait for explicit approval. The user picks which subset to apply and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

Backlog items stay in the summary. Filing one to a tracker is an external action: file only the items Shiv explicitly approves.

For each approved Accepted item, follow the Routing field exactly:

- `structure:` or `check:` rows (rungs 1 and 2): make the code, type, lint, or CI change as an ordinary code change under `shiv-code-gate`.
- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): parent does directly, following `writing-for-agents`.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): route through `writing-for-agents` and `skill-creation`.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): route through `skill-creation` and `writing-for-agents`.
- `new skill via skill-creation: <kebab-name>`: hand creation to `skill-creation`, written per `writing-for-agents`.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done. Skip this step if it doesn't.

### 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog: `<title>`, with whether Shiv approved filing it. One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
