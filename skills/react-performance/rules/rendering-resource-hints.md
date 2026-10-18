---
title: Use Resource Hints
impact: HIGH
impactDescription: reduces load time for critical resources
tags: rendering, preload, preconnect, prefetch, resource-hints
---

## Use Resource Hints

Hint the browser about resources it will need. Which tool to use depends on when you know about the resource:

- **Known at build time (first paint):** put `<link>` tags in `index.html`. Render-time calls run only after the JS bundle has loaded, so they cannot help the first request. Vite already emits `modulepreload` for entry chunks.
- **Known only at runtime:** call React DOM's resource APIs from components or handlers. React 19 adds the matching `<link>` to the document head.

**Example (`index.html`: preconnect and preload a critical font):**

```html
<link rel="preconnect" href="https://api.example.com" crossorigin />
<link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin />
```

**Example (runtime: preconnect to a third-party origin once a feature needs it):**

```tsx
import { preconnect, prefetchDNS } from 'react-dom'

function CheckoutButton({ onClick }: { onClick: () => void }) {
  const warm = () => {
    prefetchDNS('https://payments.example.com')
    preconnect('https://payments.example.com')
  }

  return <button onMouseEnter={warm} onFocus={warm} onClick={onClick}>Pay</button>
}
```

**Example (runtime: preload a module for a likely next navigation):**

```tsx
import { preloadModule } from 'react-dom'

preloadModule('/assets/dashboard.js', { as: 'script' })
```

Vite hashes chunk file names, so for route code prefer [router preloading](./bundle-preload.md) over hand-written URLs.

**When to use each:**

| API | Use case |
|-----|----------|
| `prefetchDNS` | Third-party domains you'll connect to later |
| `preconnect` | APIs or CDNs you'll fetch from immediately |
| `preload` | Critical resources needed for current page |
| `preloadModule` | JS modules for likely next navigation |
| `preinit` | Stylesheets/scripts that must execute early |
| `preinitModule` | ES modules that must execute early |

Reference: [React DOM Resource Preloading APIs](https://react.dev/reference/react-dom#resource-preloading-apis)
