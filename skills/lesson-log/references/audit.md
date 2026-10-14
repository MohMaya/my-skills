# Audit

Weekly. Write `audits/<YYYY-MM-DD>.md` under the lessons root in `../SKILL.md`. Count the seven days ending today. Every number cites the inbox. Every observation cites a quote or a count.

## Repeat-correction rate

The core metric. A correction is an entry whose trigger starts with `correction:`. A repeat restates a rule already in `promoted.md` or in an earlier correction. The rate is repeats divided by corrections in the window. List each repeat beside the rule it restates. When the window has no corrections, write `no corrections`.

## Counts

- Lessons per bot, entries other than `none`. A bot with no inbox file in the window is silent. A bot whose files are only `none` ran and captured nothing.
- Capture-to-merge latency, in days, from the inbox date of an entry marked `promoted` to the day the destination change landed, the merge or the edit when there is no PR. Report the median and the slowest. List entries with no `mark:` line that already clear the bar in [distill.md](distill.md).
- Promotion PRs open more than 3 days.
- Kernel size, in lines, of the shiv-kernel core-rules file. Note a week that added a line and deleted none. When the file is absent, write `kernel missing`.

## Unfollowed

List each promoted rule that nothing follows: a later repeat correction, or a prose rule with no check whose miss shows up again. The next nightly deletion pass takes this list.

## Mirror

Three blunt observations about Shivanshu's patterns. One sentence each, with the evidence, from scope `shiv` and from corrections. Kind and direct. The pattern, with private, health, and finance detail left out. When the evidence supports fewer than three, write those and name the shortfall.
