---
title: Deduplicate Global Event Listeners
impact: LOW
impactDescription: single listener for N components
tags: client, event-listeners, subscription, useSyncExternalStore
---

## Deduplicate Global Event Listeners

Register one module-level listener and fan out to subscribers, so N component instances share one global listener.

**Incorrect (N instances = N listeners):**

```tsx
function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && e.key === key) {
        callback()
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [key, callback])
}
```

When using the `useKeyboardShortcut` hook multiple times, each instance will register a new listener.

**Correct (N instances = 1 listener):**

```tsx
// Module-level Map to track callbacks per key
const keyCallbacks = new Map<string, Set<() => void>>()

function onKeyDown(e: KeyboardEvent) {
  if (e.metaKey) keyCallbacks.get(e.key)?.forEach(cb => cb())
}

function subscribe(key: string, callback: () => void) {
  if (keyCallbacks.size === 0) window.addEventListener('keydown', onKeyDown)
  const set = keyCallbacks.get(key) ?? new Set()
  set.add(callback)
  keyCallbacks.set(key, set)

  return () => {
    set.delete(callback)
    if (set.size === 0) keyCallbacks.delete(key)
    if (keyCallbacks.size === 0) window.removeEventListener('keydown', onKeyDown)
  }
}

function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => subscribe(key, callback), [key, callback])
}

function Profile() {
  // Multiple shortcuts share the same listener
  useKeyboardShortcut('p', () => { /* ... */ })
  useKeyboardShortcut('k', () => { /* ... */ })
  // ...
}
```

The first subscriber attaches the listener and the last one removes it. Pair with [Store Event Handlers in Refs](./advanced-event-handler-refs.md) if callers pass unstable callbacks.
