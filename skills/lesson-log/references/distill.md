# Distill

Nightly. Read inbox entries with no `mark:` line, and entries marked `blocked`. Leave every entry in the inbox; the audit reads them there. Paths are under the lessons root in `../SKILL.md`.

## Bar

Promote when all four hold:

- The same rule already appears in an earlier entry, including one marked `held`, or this entry is a `correction:` from Shivanshu.
- It generalizes past the episode.
- A bot can act on it next time.
- No promoted lesson, skill, or kernel line already says it.

Otherwise append `mark: held: <clause>` as the last line of the entry.

## Destination

When a lint, a gate, or an eval case can hold the rule, prefer it to a prose line. A scope `self` check lives in that bot's workflows. A scope `all-bots` check is shared. Scope `shiv` stays in memory. Otherwise the first match below.

- Scope `self`: that bot's skill, in that bot's workflows. A shared skill would teach every bot a one-bot tactic. Tara and Lakshmi stay `self`.
- Scope `shiv`: the shared user memory the bots already use. If it cannot be found, append `mark: blocked: memory missing`.
- A timeless principle with no next action: Vidur's canon, the one that already exists. If it cannot be found, append `mark: blocked: canon missing`.
- A rule every bot must carry into the next task: the kernel. It is the shiv-kernel core-rules skill, about one page, at `agent-data/workflows/shiv-kernel` under the box user's home. An ADD is paired with a DELETE of one line in the same ledger. Prefer a stale or contradicted line. If every line is live, append `mark: blocked: kernel full` and do not add. If the skill is not in the workspace, append `mark: blocked: kernel missing` and do not create one.

## Ledger

Edit ACE-style. Append to today's ledger. Apply each line in order. A destination is changed only by these lines.

```
- ADD <where> :: <one line>
- EDIT <where> <id> :: <from> → <to>
- DELETE <where> <id> :: <why>
```

`<where>` is the destination file. `<id>` is the line's marker, or its first words when it has none.

Then the deletion pass. DELETE a rule a newer lesson or a correction contradicts. DELETE a rule whose work is gone. DELETE a rule the latest audit listed as followed by nobody. A bad lesson spreads; the pass is how it stops. The DELETE names the evidence.

Record the rule in `promoted.md`. The task type, the skill name or the artifact kind (`code`, `prose`, `ticket`, `decision`), is the heading:

```
- <rule> | <scope> | <enforcement>
```

`<enforcement>` is the check, or the destination file. An EDIT or DELETE updates that line in the same ledger.

Append `mark: promoted: <where>` to every inbox entry that carries the rule, and `mark: blocked: <reason>` when a destination is missing or the kernel is full. A rerun skips `promoted` and `held`. It retries `blocked`; when the block still holds, it leaves the mark and adds no ledger line. A DELETE is written only when the line is still there.
