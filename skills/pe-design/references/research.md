# Reference research

How the pe-design skill grounds a proposal in shipped products through the Mobbin MCP.
Mobbin is evidence for a proposal. The kernel design source governs the surface, and the
project's design system governs styling.

## Steps

1. **Name the job.** Write down the one screen, flow, or website section the proposal
   covers, plus the platform: `ios` for mobile (Mobbin has no Android set; iOS is the
   nearest evidence for Expo work) and `web` for everything else.
2. **Pick the tool.**
   - `search_flows` for a multi-step journey: onboarding, checkout, invite, upgrade.
   - `search_screens` for one screen or state: empty, error, loading, settings, detail.
   - `search_sections` for a marketing-site section: hero, pricing, footer.
3. **Write the query.** Describe one job in concrete elements, such as "checkout page
   with promo code field and saved cards". Name an app to filter to it. Search each flow
   or screen separately. Style adjectives and negations weaken results. Keep
   `task_intent` and `output_destination` identical across calls for the task: `code`
   in a repository, `doc` for a brief or PRD, `design_tool` when the output goes to Figma.
4. **Read the images.** Judge each result from its preview images, not its metadata.
   Collect three to six references that span distinct approaches: the convention most
   apps share, and any standout that solves the job better.
5. **Extract structure.** Take information order, states covered, primary-action
   placement, copy patterns, and edge cases the PRD missed. Leave color, type,
   illustration, and brand to the project's design system.
6. **Record references.** Add a References list to the deliverable: app, what the screen
   shows, what the proposal took from it, and the `mobbin_url` link. To embed an image,
   download it from `image_url`, because those links expire after 30 days.

## Done

Every proposed pattern traces to a cited reference, or to a stated reason for departing
from the convention the references show.

## Mobbin absent

Proceed from the design system and judgment, and label the proposal "unresearched: no
Mobbin access" so Shiv can weigh it.
