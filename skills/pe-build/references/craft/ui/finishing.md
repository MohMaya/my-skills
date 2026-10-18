# Finishing

The last details. One delight, a public log of what shipped, a scrollbar that does not shove the page, the next view fetched on intent, a favicon that follows the theme, and a share card that renders.

## One easter egg, one changelog

One delight that never gates a task: a mark in the footer, one console line, or one key sequence. The action it hints at still has an ordinary control.

A public changelog lives at a stable path, `/changelog`, dated, in the product's voice, linked from the footer. Voice belongs to [writing](../writing/index.md).

Do: one egg, and a page a reader can open without an account on the forge.

Don't: confetti on an ordinary click, a feature that exists only as the egg, or a release list that only the repository shows.

## Scrollbar

```css
html {
  color-scheme: light dark;
  scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track);
  scrollbar-gutter: stable;
}
```

`scrollbar-color` is thumb, then track. Define both tokens with the theme; an undefined variable drops the whole declaration. `color-scheme: light dark` follows the system, so native controls and the scrollbar agree. When the project switches theme with a class, set `color-scheme: dark` on that class instead. One theme switch for the whole project: [colors](../colors/index.md).

A value other than `auto` makes the browser ignore `::-webkit-scrollbar` on that element and its descendants. Pick the standard properties. `scrollbar-gutter: stable` reserves the classic scrollbar's space so content does not jump when the bar appears. Overlay scrollbars ignore it. `scrollbar-width: none` hides the only affordance on a region the reader must scroll.

The thumb is a UI component. Measure it against the track with [contrast](../colors/contrast.md).

Do: `scrollbar-color`, `scrollbar-gutter: stable`, and `color-scheme` on the active theme.

Don't: a hidden scrollbar, or webkit pseudo-elements on an element that also sets `scrollbar-color`.

## Prefetch on intent

In the client router, preload on hover and touch start. Add it to the same router as [URL state](url-state.md). Hover and focus wait 50ms and cancel if the pointer leaves. Touch starts immediately.

```tsx
const router = createRouter({
  routeTree,
  scrollRestoration: true,
  defaultPreload: "intent",
});
```

For a full document navigation, prefetch on intent with the Speculation Rules API. `eagerness: "moderate"` waits about 200ms of hover on desktop. It is not baseline, and it prefetches documents, not a client router's chunks. Skip any URL that mutates, such as logout or add-to-cart: the prefetch is a GET that runs the server's side effects. If the page sets `Content-Security-Policy`, allow `'inline-speculation-rules'` on `script-src`.

```html
<script type="speculationrules">
{
  "prefetch": [{
    "where": {
      "and": [
        { "href_matches": "/*" },
        { "not": { "href_matches": "/logout" } }
      ]
    },
    "eagerness": "moderate"
  }]
}
</script>
```

A route module preloaded by hand, outside a router, is [bundle preload](../../../../react-performance/rules/bundle-preload.md).

Do: `defaultPreload: "intent"` in the app, or a document prefetch at moderate eagerness for multi-page navigations.

Don't: prerender every link, or prefetch a URL that sends a message, signs someone out, or writes on GET.

## Favicon

```html
<link rel="icon" href="/icon.svg" type="image/svg+xml" sizes="any">
```

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <style>
    .mark { fill: #171717; }
    @media (prefers-color-scheme: dark) {
      .mark { fill: #fafafa; }
    }
  </style>
  <rect class="mark" width="32" height="32" rx="8"/>
</svg>
```

The media query lives inside the SVG. The favicon is its own document; a page stylesheet does not paint it. The two fills are the theme's ink and paper, written as literals. Manifest, apple-touch-icon, and `theme-color` stay with [metadata](../../harden/metadata.md).

Do: an SVG icon whose mark follows `prefers-color-scheme`.

Don't: one fill for both themes, or a `prefers-color-scheme` rule that sits in the page CSS and never reaches the icon.

## Share card

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="The page title">
<meta name="twitter:description" content="One sentence a stranger understands.">
<meta name="twitter:image" content="https://example.com/card.png">
<meta name="twitter:image:alt" content="What the image shows.">
<meta property="og:title" content="The page title">
<meta property="og:description" content="One sentence a stranger understands.">
<meta property="og:image" content="https://example.com/card.png">
<meta property="og:image:alt" content="What the image shows.">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="website">
```

`summary_large_image` is the default. The image is an absolute `https` URL. Title, description, canonical, and `og:url` agree, and the page defines them in one place. Those rules are [metadata](../../harden/metadata.md).

Do: the card type, title, description, image, image alt, and the Open Graph twins.

Don't: a relative image URL, a card checked on localhost, or a title that disagrees with `og:title`.

## Verify

The egg is skippable and the changelog opens from the footer. With scrollbars set to always show, the page does not shift when a region starts to overflow, and the thumb is visible against the track in both themes. Hovering a link starts a preload, and it is cancelled if the pointer leaves. The tab icon flips with the color scheme. A public URL, not localhost, renders a large image card with the page's title, description, and alt.
