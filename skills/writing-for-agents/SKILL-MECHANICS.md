# Skill mechanics

The skill-specific branch of [`writing-for-agents`](SKILL.md): what changes when the document is a skill (frontmatter, invocation, and router skills). Everything else about writing it is the universal reference in `SKILL.md`.

## Invocation

Every skill is model-invoked: the agent fires it when its own judgement says the skill fits, other skills can reach it, and the human can still type its name. The description is the skill's top-level context pointer, always loaded, so write it model-facing with the trigger branches (the pointer-writing rules in `SKILL.md` apply in full). A skill whose content is all reference is one home for shared reference: any skill that needs it invokes it. `check_skills.py` rejects `disable-model-invocation`, so a reinstalled upstream skill that sets it fails the check until the line is deleted.

## Splitting by invocation

The invocation cut of splitting (the sequence cut lives in `SKILL.md`): split off a skill when you have a distinct leading word that should trigger it on its own (a trigger word you actually use in your prompts), or another skill must reach it. You pay context load for the new always-loaded description, so that independent reach has to be worth it.

## Router skills

When skills multiply past what the agent picks reliably from descriptions alone, a **router skill** names the others and when to reach for each, and invokes the one that fits.
