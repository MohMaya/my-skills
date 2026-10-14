---
name: lesson-log
description: Lesson capture for the shared bot loop. Use at the end of a substantive task, when Shivanshu corrects or pushes back, and before output, to read promoted lessons and append one critique.
---

# Lesson log

Lessons travel as files. One Reflexion critique closes a task. The nightly distill promotes only what clears the bar. A check enforces what a prose rule would only repeat.

## Capture

End every substantive task by appending one lesson to today's inbox, or the line `none`. A correction or pushback from Shivanshu is that lesson.

Before output, read the promoted lessons for this task type and apply each one that fits. A missing `promoted.md` means there are none yet.

When something is wrong, name it, including a pattern of Shivanshu's, with the evidence, kindly and directly. The subject is the pattern.

_Done when_ the artifact shows every fitting lesson, and today's inbox holds this task's one entry, written after the artifact exists.

## Where

Paths are relative to the home directory of the user `box`.

- Inbox: `agent-data/lessons/inbox/<bot-slug>/<YYYY-MM-DD>.md`
- Promoted: `agent-data/lessons/promoted.md`
- Ledger: `agent-data/lessons/ledger/<YYYY-MM-DD>.md`
- Audits: `agent-data/lessons/audits/<YYYY-MM-DD>.md`

`<bot-slug>` is the slug the bot already uses. The date is the day the task ends. Create a missing directory.

Read today's inbox first. If this trigger is already there, leave the file. A second `none` in a row is not written.

## Entry

A critique of the bot's own action. The miss, the rule, the evidence. Not a transcript.

```
- trigger:
  happened:
  rule:
  evidence:
  scope: self | all-bots | shiv
```

`trigger` names what fired it. A correction from Shivanshu starts with `correction:`.

`happened` is one sentence, the miss or the surprise.

`rule` is what the bot does next time.

`evidence` is the shortest quote or diff that shows the miss.

`scope` is `self` for this bot, `all-bots`, or `shiv` for a fact or pattern of Shivanshu's.

`none` is the whole entry when the task taught nothing.

Write the general rule. Where the episode is private, the evidence names the miss. Health lessons (Tara) and finance lessons (Lakshmi) take scope `self` and keep no personal data.

## Enforce

A lesson that can be a lint, a gate, or an eval case becomes that. A prose rule is for what no check can hold.

Nightly: [references/distill.md](references/distill.md). Weekly: [references/audit.md](references/audit.md).
