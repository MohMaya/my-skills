# Selection color

Every website and app ships a custom text selection color from the brand palette, never the default system blue. Selected text meets WCAG AA (4.5:1) against its highlight; measure it. The highlight tracks the page: it shifts with scroll position or the current section, so selection matches the color the reader is looking at.

## Web

One custom property feeds `::selection`; JS or scroll-driven CSS moves it.

```css
:root { --selection-bg: var(--brand-500); --selection-fg: var(--color-paper); }
::selection { background-color: var(--selection-bg); color: var(--selection-fg); }
```

Section-based, the default: each section declares its color, and the one in view owns the property.

```js
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const io = new IntersectionObserver((entries) => {
  for (const e of entries) if (e.isIntersecting)
    document.documentElement.style.setProperty("--selection-bg", e.target.dataset.selection);
}, { rootMargin: "-50% 0px -50% 0px" });
if (!reduce) document.querySelectorAll("[data-selection]").forEach((s) => io.observe(s));
```

Continuous: interpolate a brand ramp by scroll progress, sampled at the selected text's position, on `selectionchange` and scroll in one rAF. Pull each stop toward ink until it clears AA. Under reduced motion keep one static brand color.

## Native

- React Native / Expo: `selectionColor` on `TextInput` and selectable `Text`; set it from the current section's color.
- iOS: `tintColor` on the text view (SwiftUI `.tint`). Android: `textColorHighlight`.

Scroll-shifting is optional on native; a per-section tint is enough.
