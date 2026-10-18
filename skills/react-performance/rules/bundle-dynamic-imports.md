---
title: Dynamic Imports for Heavy Components
impact: CRITICAL
impactDescription: directly affects TTI and LCP
tags: bundle, dynamic-import, code-splitting, react-lazy, tanstack-router
---

## Dynamic Imports for Heavy Components

Use `React.lazy` with `Suspense` to load large components not needed on initial render.

**Incorrect (Monaco bundles with main chunk ~300KB):**

```tsx
import { MonacoEditor } from './monaco-editor'

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />
}
```

**Correct (Monaco loads on demand):**

```tsx
import { lazy, Suspense } from 'react'

const MonacoEditor = lazy(() =>
  import('./monaco-editor').then(m => ({ default: m.MonacoEditor }))
)

function CodePanel({ code }: { code: string }) {
  return (
    <Suspense fallback={<EditorSkeleton />}>
      <MonacoEditor value={code} />
    </Suspense>
  )
}
```

**Routes:** split per route with the TanStack Router Vite plugin's `autoCodeSplitting: true`, which lazy-loads each route's component for you. Without the plugin, use `lazyRouteComponent(() => import('./Post'))` or a `.lazy.tsx` file with `createLazyFileRoute`.

```ts
// vite.config.ts - place before @vitejs/plugin-react
tanstackRouter({ target: 'react', autoCodeSplitting: true })
```
