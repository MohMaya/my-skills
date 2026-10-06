---
name: ambient-ui-design
description: >
  Ensures all UI designs — HTML artifacts, React components, and JSX/Claude.ai
  artifacts — use the SmartAC Ambient UI design token system (Terrazzo-generated
  CSS variables) for colors, typography, shadows, and radius, with Tailwind CSS
  handling all spacing, layout, padding, and margins. Supports both light and dark
  themes out of the box. Use this skill whenever you are building, prototyping, or
  styling any UI for SmartAC, regardless of output type — even if the user just
  says "make a component", "build a screen", "design a dashboard", "mock up a
  page", or "create a UI". If any visual interface is being created for SmartAC,
  this skill must be consulted first.
---

# Ambient UI Design Skill

Apply this skill to **every** UI output for SmartAC — HTML artifacts, React
components, and Claude.ai JSX artifacts. It ensures designs use the official
Terrazzo token system for color/type/shadow/radius, and Tailwind CSS for
spacing and layout.

---

## Core Principles

1. **Tokens for visual properties** — All colors, typography sizes/weights/line
   heights, border radii, and shadows must come from `--app-*` or
   `--primitives-*` CSS variables. Never hardcode hex values or arbitrary sizes.

2. **Tailwind for layout and spacing** — Use Tailwind utility classes (`p-4`,
   `gap-3`, `flex`, `grid`, `mt-2`, etc.) for all spacing, layout, padding,
   and margins. Do not write custom spacing CSS.

3. **Both themes always** — Every artifact must work correctly in both light and
   dark mode. Use the semantic `--app-color-*` tokens (they flip automatically)
   rather than raw `--primitives-color-*` values.

4. **Semantic tokens over primitives** — Prefer `--app-color-surface-default`
   over `--primitives-color-gray-0`. Semantic tokens are theme-aware; primitives
   are not.

---

## Token Injection

**Always inline both token blocks** into every artifact. The full token
definitions live in:
- `references/tokens-light.css` — `:root { ... }` (light mode defaults)
- `references/tokens-dark.css` — `.dark, [data-theme="dark"] { ... }` (dark overrides)

Read those files and paste the CSS verbatim into a `<style>` block (HTML) or
a `<style jsx global>` / CSS-in-JS injection (React/JSX).

### HTML artifacts

```html
<style>
  /* paste full contents of tokens-light.css here */
  /* paste full contents of tokens-dark.css here */

  body {
    font-family: system-ui, -apple-system, sans-serif; /* Booton fallback */
    background-color: var(--app-color-surface-inset);
    color: var(--app-color-foreground-primary);
  }
</style>
```

Add `class="dark"` to `<html>` or any root element to activate dark mode.

### React / JSX artifacts (Claude.ai)

Inject tokens via a `<style>` tag rendered inside the component, or at the
top of a `<GlobalStyle>` / `createGlobalStyle` block:

```jsx
// At the top of your component file:
const tokens = `
  /* paste full contents of tokens-light.css */
  /* paste full contents of tokens-dark.css */
`;

export default function MyComponent() {
  return (
    <>
      <style>{tokens}</style>
      <div className="...tailwind classes...">
        {/* content */}
      </div>
    </>
  );
}
```

For dark mode in React, toggle `data-theme="dark"` on the root `<div>` or
`<html>` and the CSS overrides will apply automatically.

---

## Tailwind + Token Hybrid Pattern

Use Tailwind for layout/spacing, CSS variables for visual styling:

```jsx
// ✅ Correct
<div
  className="flex flex-col gap-4 p-6 rounded-lg"
  style={{
    background: 'var(--app-color-surface-default)',
    border: '1px solid var(--app-color-stroke-default)',
    boxShadow: 'var(--app-shadow-md)',
  }}
>
  <h2
    className="text-lg font-semibold tracking-tight"
    style={{ color: 'var(--app-color-foreground-primary)' }}
  >
    Card Title
  </h2>
  <p
    className="text-sm"
    style={{ color: 'var(--app-color-foreground-secondary)' }}
  >
    Secondary content
  </p>
</div>

// ❌ Wrong — hardcoded colors, custom spacing CSS
<div style={{ background: '#fff', padding: '24px', color: '#333' }}>
```

---

## Key Semantic Tokens (Quick Reference)

These are the tokens you'll reach for most often. They work in both themes.

### Surfaces (backgrounds)
| Token | Use for |
|-------|---------|
| `--app-color-surface-inset` | Page background |
| `--app-color-surface-default` | Cards, panels, modals |
| `--app-color-surface-elevated` | Elevated cards, dropdowns |
| `--app-color-surface-default-offset` | Subtle offset within a surface |

### Foreground (text & icons)
| Token | Use for |
|-------|---------|
| `--app-color-foreground-primary` | Primary text |
| `--app-color-foreground-secondary` | Muted/secondary text |
| `--app-color-foreground-on-color` | Text on colored/brand backgrounds |
| `--app-color-icon-primary` | Primary icons |
| `--app-color-icon-secondary` | Secondary/muted icons |

### Strokes (borders)
| Token | Use for |
|-------|---------|
| `--app-color-stroke-default` | Default borders (subtle, transparent) |
| `--app-color-stroke-strong` | Visible/strong borders |
| `--app-color-ring-default` | Focus rings |

### Interactive
| Token | Use for |
|-------|---------|
| `--app-color-interactive-primary` | Primary button background |
| `--app-color-interactive-primary-hover` | Primary button hover |
| `--app-color-interactive-secondary` | Secondary button / inactive state |
| `--app-color-interactive-secondary-hover` | Secondary hover |

### Status
Use the `--app-color-status-{level}-{role}` pattern:
- Levels: `error`, `warning`, `success`, `info`
- Roles: `default` (foreground), `subtle` (background fill), `border`, `icon`

Example: `--app-color-status-error-default`, `--app-color-status-success-subtle`

### Radius (use these, not arbitrary px)
| Token | Tailwind equiv | Use for |
|-------|---------------|---------|
| `--app-radius-sm` | `rounded-sm` | Inner elements, badges |
| `--app-radius-md` | `rounded` | Checkboxes, alerts, chips |
| `--app-radius-lg` | `rounded-lg` | Buttons, inputs, cards |
| `--app-radius-full` | `rounded-full` | Avatars, switches, pills |

### Shadows
| Token | Use for |
|-------|---------|
| `--app-shadow-xs` | Very subtle lift |
| `--app-shadow-sm` | Cards at rest |
| `--app-shadow-md` | Dropdowns, popovers |
| `--app-shadow-lg` | Modals, sheets |

### Typography

**Font families**

| Font | CSS | Usage |
|------|-----|-------|
| **Booton** (primary) | `var(--font-booton), system-ui, sans-serif` | All UI text — body, labels, buttons, inputs |
| **ABC Otto** (display) | `var(--font-otto)` | Marketing/hero/brand moments only — never for UI chrome |

In artifacts where custom fonts aren't loaded, use `system-ui, -apple-system, sans-serif`
as the Booton fallback. Do **not** substitute Otto — omit it entirely.

**Type scale** — use Tailwind classes:

| Tailwind | Size | Use for |
|----------|------|---------|
| `text-2xl` | 24px | Page titles, major headings |
| `text-xl` | 20px | Section headings |
| `text-lg` | 18px | Subheadings, lead paragraphs |
| `text-base` / `text-md` | 16px | Lead body text |
| `text-sm` | 14px | Body text, form labels, UI controls |
| `text-xs` | 12px | Captions, helper text, metadata — **minimum size** |

**Font weights** — Booton is a variable font; use these three semantic values:

| Tailwind | Value | Use for |
|----------|-------|---------|
| `font-normal` | 300 | Body text, default content |
| `font-medium` | 400 | Labels, buttons, emphasis |
| `font-bold` | 500 | Headings, strong emphasis |

> These map to the `--primitives-typography-font-weight-*` tokens. Never use
> weight values outside this set (e.g. `font-semibold` / 600 is out of range).

**Line height** — two values cover all needs:

| Tailwind | Value | Token | Use for |
|----------|-------|-------|---------|
| `leading-normal` | 1.5 | `--primitives-typography-line-height-normal` | Body text, longer passages |
| `leading-tight` | 1.167 | `--primitives-typography-line-height-tight` | Headings, short bursts |

**Letter spacing:**

| Tailwind | Value | Token | Use for |
|----------|-------|-------|---------|
| `tracking-tight` | -0.01em | `--primitives-typography-letter-spacing-tight` | Headings |

**Hierarchy rules:**
- `2xl–xl` → page titles and section headings
- `lg–md` → subheadings and lead paragraphs
- `sm` → body text, form labels, UI controls
- `xs` → captions, helper text, metadata (never go below this)

**Accessibility:**
- Minimum font size: `12px` (`text-xs`) — never smaller
- Color contrast: `4.5:1` for body text, `3:1` for large text
- Never use font weight alone to convey meaning

---

## Dark Mode Toggle (React)

For artifacts that should support a live dark/light toggle:

```jsx
import { useState } from "react";

export default function App() {
  const [dark, setDark] = useState(false);

  return (
    <div data-theme={dark ? "dark" : undefined} className="min-h-screen">
      <style>{tokens}</style>
      <button
        onClick={() => setDark(d => !d)}
        className="px-3 py-1 rounded-lg text-sm"
        style={{
          background: 'var(--app-color-interactive-secondary)',
          color: 'var(--app-color-foreground-primary)',
          border: '1px solid var(--app-color-stroke-default)',
        }}
      >
        {dark ? "Light mode" : "Dark mode"}
      </button>
      {/* rest of UI */}
    </div>
  );
}
```

---

## Pre-flight Checklist

Before delivering any UI output, verify:

- [ ] Both token CSS blocks are inlined (light `:root` + dark `.dark`)
- [ ] No hardcoded hex/rgb color values — all from `--app-color-*` tokens
- [ ] All spacing/layout uses Tailwind classes (no custom `padding`/`margin` CSS)
- [ ] Border radii use `--app-radius-*` tokens or Tailwind equivalents
- [ ] Shadows use `--app-shadow-*` tokens
- [ ] Component is visually tested in both light and dark themes
- [ ] Font family set to `system-ui, -apple-system, sans-serif` (Booton fallback)
- [ ] Interactive states (hover, focus) use the correct `*-hover` and ring tokens

---

## Full Token Reference

The complete Terrazzo-generated token definitions are in:
- `references/tokens-light.css` — all `:root` light-mode values
- `references/tokens-dark.css` — all `.dark` / `[data-theme="dark"]` overrides

Read these files and paste their contents verbatim when building any artifact.
