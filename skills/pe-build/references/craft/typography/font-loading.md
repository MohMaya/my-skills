# Font loading

The face used on the first screen is requested before first paint. Text draws immediately in a fallback, and the swap does not move the line.

## Preload one file

Preload that one file. A preload of every weight competes with the document. Fonts are fetched in anonymous CORS mode, so `crossorigin` is required even on the same origin. Without it the browser downloads the file twice and the preload is wasted.

```html
<link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
```

## Draw now, then swap

`font-display: swap` gives the face an extremely small block period and an infinite swap period. The reader sees the fallback instead of invisible text. `block` holds the glyphs invisible. `optional` never swaps if the face misses that first moment, which is right only when the face may stay absent for the whole view.

The fallback's own `@font-face` carries the metric overrides, and the stack names that family. Overrides on a family nothing uses do nothing. `local()` must name a face the platform has, or the overrides never apply. `size-adjust` scales the fallback's glyphs and advances, and it is the widely available lever. `ascent-override`, `descent-override`, and `line-gap-override` match the line box where the browser supports them; support for those three is still partial.

The block below is the shape. `100%` and `normal` match nothing. Replace them with the percentages measured for this face against this fallback. A number borrowed from another pair moves the line.

```css
@font-face {
  font-family: Inter;
  src: url("/fonts/inter-latin.woff2") format("woff2");
  font-weight: 400;
  font-display: swap;
}

@font-face {
  font-family: "Inter Fallback";
  src: local("Arial");
  size-adjust: 100%;
  ascent-override: normal;
  descent-override: normal;
  line-gap-override: normal;
}

body { font-family: Inter, "Inter Fallback", sans-serif; }
```

Do: one critical preload, `swap`, and overrides measured for this pair. Subset to the scripts the page uses.

Don't: preload the whole family, use `font-display: block`, or ship the initial values above.

Which faces to load at all stays with [typography](index.md). The file format is `.woff2`.

## Verify

Throttle the network. Text is visible on the first frame, and the line does not jump when the web font arrives. The font request happens once: the preload and the `@font-face` request are the same URL.
