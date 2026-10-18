---
title: Preload Based on User Intent
impact: MEDIUM
impactDescription: reduces perceived latency
tags: bundle, preload, user-intent, hover, tanstack-router
---

## Preload Based on User Intent

Preload heavy bundles before they're needed to reduce perceived latency.

**Routes:** set `defaultPreload: 'intent'` on the router. Hovering or focusing a `<Link>` then loads the route's code and loader data before the click.

```tsx
const router = createRouter({ routeTree, defaultPreload: 'intent' })
```

**Example (preload a non-route module on hover/focus):**

```tsx
function EditorButton({ onClick }: { onClick: () => void }) {
  const preload = () => {
    void import('./monaco-editor')
  }

  return (
    <button
      onMouseEnter={preload}
      onFocus={preload}
      onClick={onClick}
    >
      Open Editor
    </button>
  )
}
```

**Example (preload when feature flag is enabled):**

```tsx
function FlagsProvider({ children, flags }: Props) {
  useEffect(() => {
    if (flags.editorEnabled) {
      void import('./monaco-editor').then(mod => mod.init())
    }
  }, [flags.editorEnabled])

  return <FlagsContext.Provider value={flags}>
    {children}
  </FlagsContext.Provider>
}
```

The browser caches the module, so a later `React.lazy(() => import('./monaco-editor'))` resolves without another network request.
