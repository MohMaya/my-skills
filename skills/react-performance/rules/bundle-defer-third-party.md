---
title: Defer Non-Critical Third-Party Libraries
impact: MEDIUM
impactDescription: loads after first render
tags: bundle, third-party, analytics, defer
---

## Defer Non-Critical Third-Party Libraries

Analytics, logging, and error tracking don't block user interaction. Load them after the first render.

**Incorrect (blocks initial bundle):**

```tsx
import { Analytics } from './analytics'

export function App() {
  return (
    <>
      <Routes />
      <Analytics />
    </>
  )
}
```

**Correct (separate chunk, fetched after the app renders):**

```tsx
import { lazy, Suspense } from 'react'

const Analytics = lazy(() =>
  import('./analytics').then(m => ({ default: m.Analytics }))
)

export function App() {
  return (
    <>
      <Routes />
      <Suspense fallback={null}>
        <Analytics />
      </Suspense>
    </>
  )
}
```

For an SDK with no component, call `requestIdleCallback(() => import('./sdk').then(m => m.init()))` from the entry module after `createRoot(...).render(...)`.
