---
name: smartac-ambient-ui
description: >
  Enforces the SmartAC Ambient UI design system (@smartacteam/ambient-web + Terrazzo
  tokens) for every UI artifact — HTML artifacts, React components, Claude.ai JSX,
  dashboards, mockups, internal tools. Use whenever ANY visual interface is being
  created or modified for SmartAC, regardless of how the request is phrased: "build a
  component", "make a screen", "mock up a page", "design a dashboard", "prototype a
  flow", "create a UI". This skill is strict — it uses a primitive-emulation CSS
  layer and real React component imports; freeform CSS classes and inline styling of
  colors/borders/shadows/typography are forbidden. Must be consulted BEFORE writing
  any markup.
---

# SmartAC Ambient UI Skill

**Read this entire file before writing any markup.** This skill exists because
earlier outputs reinvented the design system instead of using it. That stops
here.

There is exactly one vocabulary for SmartAC UI. It has two modes:

| Mode | Context | Vocabulary |
|------|---------|-----------|
| **React / TSX** | Next.js app, Claude.ai JSX artifact | Import from `@smartacteam/ambient-web/<primitive>` |
| **HTML artifact** | Single-file HTML artifact, standalone preview | Use `.ui-*` emulation classes from `references/primitives.css` |

**Pick mode first.** If the user wants a `.html` file, a Claude.ai HTML
artifact, or anything standalone with no package manager, use HTML mode. If
the user is in a repo with `@smartacteam/ambient-web` available, or asks for
React/JSX/TSX, use React mode. Never mix the two.

---

## The Iron Rules

**Violations of any of these mean: delete and start over. Not "adjust" — delete.**

1. **No custom CSS classes.** Every visible element uses a primitive class
   (`.ui-card`, `.ui-button-primary`, `.ui-badge-success`, `.ui-stat`,
   `.ui-table`, `.ui-sidebar-item`, `.ui-text-sm`, etc.) or a real React
   primitive. If you catch yourself writing `.stat-val`, `.wtd-grid`,
   `.card-dark`, `.warn-box`, `.prog-track`, or any other bespoke class:
   stop, delete, use a primitive.

2. **No inline styles for colors, borders, shadows, radii, or typography.**
   These must come from a primitive class or a token-backed Tailwind class
   (`bg-surface-default`, `text-text-primary`, `border-stroke-default`,
   `rounded-lg`). Inline `style=` is permitted **only** for layout —
   `display`, `grid-template-columns`, `gap`, `flex`, `min-height`, positional
   properties when a real SVG needs it.

3. **No hardcoded hex / rgb / named colors. Ever.** Not for accents, not for
   "just this one border", not for chart colors. Chart colors come from
   `--primitives-color-dataviz-series-*` and `--primitives-color-dataviz-qualitative-*`.

4. **No emoji / HTML-entity icons.** `▶`, `✕`, `✓`, `⚠`, `&#9654;`, `&#10005;`,
   `➔`, `●`, `◆` are banned. Icons are either `<CentralIcon name="..." />`
   (React) or inline SVG inside `<span class="ui-icon ui-icon-4">` (HTML).

5. **Font weights are 300 / 400 / 500 only.** `font-weight: 700`, `600`,
   `800`, `bold` (as numeric 700) are banned. The typography scale has three
   weights: `.ui-font-normal` (300), `.ui-font-medium` (400), `.ui-font-bold`
   (500).

6. **Minimum font size is 12px (`.ui-text-xs`).** No `font-size: 10px`,
   `11px`, or anything below `12px`. Not for axis labels, not for footnotes.

7. **Cards are `.ui-card` or `Card.Root`. Full stop.** A grouped content
   panel is a card. A card has `.ui-card-header` with `.ui-card-title`, then
   `.ui-card-content`. No freestyling.

8. **Status is a Badge.** If something is "on pace" / "behind" / "stalled" /
   "error" / "success" / "warning", it is rendered as `<Badge color="...">`
   or `<span class="ui-badge ui-badge-...">`. Never as colored raw text,
   never as a custom pill div.

9. **Use the page rhythm.** Main area has `24px` padding, cards stack with a
   `16px` gap, section headings use `.ui-text-lg` with an `8px` top margin.
   See `composition-patterns.md` §8.

10. **Support both themes automatically.** Semantic `--app-color-*` tokens
    flip with `.dark` / `[data-theme="dark"]` on a root element. Never use
    `--primitives-color-*` directly for color — they are not theme-aware.
    The only exception is `--primitives-color-dataviz-*`, which is used
    only via `.ui-swatch-*` classes (see §11).

11. **Never invent a new CSS variable namespace.** No `--gtm-*`, `--dash-*`,
    `--chart-*`, or any project-level variable layer on top of tokens. If
    you need a named color for "paid social" vs "organic", use the
    `.ui-swatch-series-N` classes directly; attach meaning in a legend row,
    not in the variable name.

12. **Only reference tokens that exist.** See "Valid token names" below.
    Do not guess. `--app-color-text-primary`, `--app-color-text-secondary`,
    `--primitives-typography-family-sans` do **not exist** — common
    mistakes. The correct names are `--app-color-foreground-primary`,
    `--app-color-foreground-secondary`, and (for fonts) inherit from
    `font-family` on `body` / `.ui-text-*` classes.

**If you cannot satisfy the requirement using these primitives, say so
explicitly before writing markup. Do not invent.**

---

## Valid token names (the complete list — anything else does not exist)

Copy-paste from this list. If a name is not here, it is not a token.

**Surfaces:** `--app-color-surface-default`, `--app-color-surface-default-offset`,
`--app-color-surface-elevated`, `--app-color-surface-elevated-offset`,
`--app-color-surface-inset`, `--app-color-surface-inset-offset`.

**Foreground (text & icons):** `--app-color-foreground-primary`,
`--app-color-foreground-secondary`, `--app-color-foreground-inverse`,
`--app-color-foreground-on-color`, `--app-color-icon-primary`,
`--app-color-icon-secondary`, `--app-color-icon-inverse`.

(There is **no** `--app-color-text-primary` / `--app-color-text-secondary`.
Those names sound right but do not exist.)

**Strokes:** `--app-color-stroke-default`, `--app-color-stroke-strong`,
`--app-color-stroke-inverse`, `--app-color-ring-default`.

**Interactive:** `--app-color-interactive-primary`,
`--app-color-interactive-primary-hover`, `--app-color-interactive-secondary`,
`--app-color-interactive-secondary-hover`.

**Status** — pattern `--app-color-status-{level}-{role}`:
- levels: `success`, `warning`, `error`, `info`
- roles: `default`, `subtle`, `border`, `icon`

**Radius:** `--app-radius-sm`, `--app-radius-md`, `--app-radius-lg`, `--app-radius-full`.

**Shadow:** `--app-shadow-xs`, `--app-shadow-sm`, `--app-shadow-md`, `--app-shadow-lg`.

**Chart grid:** `--app-color-chart-grid`.

**Spacing (for use inside the emulation CSS only, not typically in markup):**
`--app-spacing-component-{xs,sm,md,lg,xl}`, `--app-spacing-layout-{xs,sm,md,lg,xl}`.

**Dataviz (only via `.ui-swatch-*` classes — never inline in `style=`):**
`--primitives-color-dataviz-series-{1..8}`,
`--primitives-color-dataviz-qualitative-{0,10,20,…,100}`.

**There is no `--primitives-typography-family-*` token.** Fonts are set
once on `body` in `primitives.css` and inherited — do not attempt to
reference a font-family token.

---

## Setup for an HTML artifact

The head must contain, **in order**, three blocks inlined verbatim from the
`references/` folder:

```html
<style>
  /* 1) Light tokens (required) */
  /* paste references/tokens-light.css */

  /* 2) Dark tokens (required) */
  /* paste references/tokens-dark.css */

  /* 3) Primitive emulation layer (required) */
  /* paste references/primitives.css */
</style>
```

Activate dark mode by adding `class="dark"` or `data-theme="dark"` on the
`<html>` or top-level wrapper.

Working skeleton: `references/html-template.html`. Copy it and fill in.

## Setup for a React / TSX artifact

Import only from `@smartacteam/ambient-web/<primitive>` subpaths. Use token
classes (`bg-surface-default`, `text-text-primary`, etc.) in `className`.
Never inline CSS variables via `style={{ background: 'var(--app-...)' }}` when
a token class exists.

Working skeleton: `references/react-template.tsx`.

For Claude.ai JSX artifacts where `@smartacteam/ambient-web` is not
available, fall back to HTML mode with the `.ui-*` primitives — do not
simulate the components with raw `<div>`s.

---

## Component quick map

Full catalog with import paths and HTML equivalents:
`references/components-catalog.md`.

| Need | React | HTML |
|------|-------|------|
| Grouped panel | `Card.Root` + parts | `.ui-card` + `.ui-card-header` etc. |
| Big number + label | flex col with token classes | `.ui-stat` + `.ui-stat-value` + `.ui-stat-label` |
| Status pill | `<Badge color="success">` | `.ui-badge .ui-badge-success` |
| Action | `<Button variant="primary">` | `.ui-button .ui-button-primary` |
| Icon button | `<Button variant="ghost" size="icon">` | `.ui-button .ui-button-ghost .ui-button-icon` |
| Text input | `<Input />` | `.ui-input` |
| Label | `<Label>` | `.ui-label` |
| Divider | `<Separator />` | `.ui-separator` |
| Rows of data | `Table.Root` / `DataTable` | `.ui-table` |
| Nav rail | `Sidebar.Root` + parts | `.ui-sidebar` + `.ui-sidebar-item` |
| Icon | `<CentralIcon name="..." />` | inline SVG inside `.ui-icon .ui-icon-4` |
| Progress bar | `<Progress value={…} />` | `.ui-progress-track` + `.ui-progress-fill` |
| Stacked bar chart row | compose with `<Chart>` | `.ui-bar-stack` + `.ui-bar-segment.ui-swatch-series-N` |
| Chart legend | — | `.ui-chart-legend` + `.ui-chart-legend-item` + `.ui-swatch-dot.ui-swatch-series-N` |
| Chart swatch / series color | tailwind `bg-dataviz-series-N` (in real app) | `.ui-swatch-series-{1..8}`, `.ui-swatch-qual-{0,10,…,100}` |

---

## Composition patterns

Copy from `references/composition-patterns.md` for:

1. KPI / stat card
2. Stat grid (multiple KPIs in one card)
3. Status badges
4. Progress bar
5. Data table
6. App shell (sidebar + header + main)
7. Empty state / callout
8. Page layout rhythm

These are the only approved shapes. If the user asks for something that
doesn't fit, compose from these — don't invent a new shape.

---

## Red flags (stop immediately if you're doing any of these)

| You're writing… | Stop. Do this instead. |
|-----------------|------------------------|
| `<style>.stat-strip { ... }</style>` | Use `.ui-stat` inside a grid with `.ui-card`. |
| `style="font-size:10px"` / `11px` | Minimum is `.ui-text-xs` = 12px. |
| `style="font-weight:700"` | Use `.ui-font-bold` (500). 600/700/800 don't exist. |
| `style="color:#ff3b3b"` | Use `.ui-text-error` or `.ui-badge-error`. |
| `&#9654; Actual` / `▶ Actual` | Inline SVG inside `.ui-icon .ui-icon-4`. |
| `<div class="warn-box">` | `.ui-card` + `.ui-badge-warning` (see pattern §7). |
| `style="position:absolute; top:…; left:14%"` for label overlays | Use a grid/flex row under the bar. |
| Custom `.prog-track` / `.prog-fill` | Pattern §4 — 6px track, `var(--app-color-interactive-primary)` fill. |
| Uppercased `.sec-hdr { text-transform: uppercase }` | Plain `.ui-text-lg` heading. No section dividers. |
| Raw `<button style="...">` | `.ui-button .ui-button-{default,primary,ghost}`. |
| `<span style="background:#...; color:#...">` for a status chip | `.ui-badge .ui-badge-<level>`. |
| Inline hex in SVG `stroke="#1e90ff"` | `stroke="currentColor"` + set color via class. |
| `:root { --gtm-src-paid-social: var(--primitives-color-dataviz-series-1); }` | Don't create a project-level variable layer. Use `.ui-swatch-series-1` directly and label it in a `.ui-chart-legend`. |
| `style="background: var(--primitives-color-dataviz-series-5)"` on a chart segment | `<div class="ui-bar-segment ui-swatch-series-5" style="width:42%;">` — width is layout (inline ok), color is a swatch class. |
| `var(--app-color-text-primary)` / `var(--app-color-text-secondary)` | Those tokens **do not exist**. Use `--app-color-foreground-primary` / `--app-color-foreground-secondary` (or just `.ui-text-primary` / `.ui-text-secondary`). |
| `var(--primitives-typography-family-sans, …)` | That token does not exist. `body` in `primitives.css` already sets the font family — inherit it. |
| Custom `.prog-track` or inline `style="height:8px;background:var(--app-color-surface-inset)…"` for progress | `.ui-progress-track` + `.ui-progress-fill`, optional `.ui-progress-marker` for expected-pace tick. |
| Inline-styled legend dots `<span style="width:10px;height:10px;background:var(--gtm-src-…)">` | `<span class="ui-swatch-dot ui-swatch-series-N"></span>` inside `.ui-chart-legend`. |

---

## Pre-flight checklist

Run through this **every time** before returning markup. Any `no` → fix
before delivering.

- [ ] Mode picked explicitly (HTML vs React)?
- [ ] All three CSS blocks inlined (tokens-light + tokens-dark + primitives) — HTML mode?
- [ ] All imports from `@smartacteam/ambient-web/<primitive>` — React mode?
- [ ] Zero custom CSS classes beyond `.ui-*`?
- [ ] Zero inline `style=` for `color`, `background`, `border-color`, `box-shadow`, `border-radius`, `font-size`, `font-weight`?
- [ ] Zero hardcoded hex/rgb values anywhere (CSS, inline, SVG)?
- [ ] Every status indicator is a Badge primitive?
- [ ] Every grouped panel is a Card primitive?
- [ ] Every icon is `<CentralIcon>` or inline SVG inside `.ui-icon` — no emoji/entities?
- [ ] Every font size is ≥ 12px (`.ui-text-xs`)?
- [ ] Every font weight is 300 / 400 / 500?
- [ ] Page rhythm: 24px main padding, 16px gap between cards?
- [ ] Dark mode verified — swap `class="dark"` on root and nothing breaks?

If you scanned the checklist in your head instead of actually checking each
item against the markup: go back. Check the markup.

---

## What to do when the user says "it's still ugly"

That means a visual-quality problem inside the vocabulary, not a reason to
escape the vocabulary. Tighten:

- Hierarchy — are headings using `.ui-text-2xl` → `.ui-text-lg` → `.ui-text-sm` in order?
- Density — is card padding exactly 20px vertical / 24px horizontal?
- Numbers — are all numeric cells `.ui-tabular`?
- Whitespace — is there a 16px gap between cards, 8px above section headings?
- Color restraint — status color **only** for status. Primary color **only** for the primary action or the progress fill. Everything else is primary/secondary text on default/inset surfaces.
- No more than one Badge per card header.
- No more than one primary Button per card.

If a visual still feels wrong, it's composition, not the system. Look at
`composition-patterns.md` and pick a closer pattern.
