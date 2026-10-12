# Touch

A tap fires on the first contact. The pressed state is one you designed. The target is large enough to hit. Hover styling exists only on a device that can hover.

```css
:where(a, button, summary, label, input, select, textarea) {
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}

@media (hover: hover) {
  button:hover { background-color: var(--color-bg-hover); }
}
```

`touch-action: manipulation` tells the browser the control never double-tap zooms, so the click is not held for a second tap. The platform tap flash is transparent because the press is `:active`. That press is `scale(0.96)`, in [animations](animations.md#scale-on-press). A gray flash on top of it reads as a glitch.

Primary touch targets are at least 44px on each side. The 24px floor, its exceptions, and how to grow a smaller visible control without inflating the graphic are in [hit areas](../../a11y/hit-areas.md). A surface that owns its own pan or drag uses `touch-action: none` on that surface only, also there. Page-level `none` removes scrolling.

Hover goes inside `@media (hover: hover)`. On a touch screen `:hover` latches after the tap until the next tap elsewhere, so the control looks selected. `:active` still runs on those devices. Hover is not the pressed state. Tailwind 4's `hover:` variant already compiles under this query, so don't wrap it a second time.

Do: manipulation, a transparent tap highlight, a real `:active`, a 44px touch target, and hover behind the media query.

Don't: the default gray flash, hover rules outside the query, or `touch-action: none` on the page.

## Verify

On a phone, the first tap activates, the pressed state shows, and no gray overlay flashes. Lifting the finger does not leave the hover color stuck. The target's box is at least 44px on each side. On a mouse, hover still shows.
