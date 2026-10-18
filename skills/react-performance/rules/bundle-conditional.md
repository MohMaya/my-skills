---
title: Conditional Module Loading
impact: HIGH
impactDescription: loads large data only when needed
tags: bundle, conditional-loading, lazy-loading
---

## Conditional Module Loading

Load large data or modules only when a feature is activated.

**Example (lazy-load animation frames):**

```tsx
function AnimationPlayer({ enabled }: { enabled: boolean }) {
  const [frames, setFrames] = useState<Frame[] | null>(null)
  const [loadError, setLoadError] = useState<unknown>(null)

  useEffect(() => {
    if (enabled && !frames) {
      import('./animation-frames.js')
        .then(mod => setFrames(mod.frames))
        .catch(setLoadError)
    }
  }, [enabled, frames])

  if (loadError) throw loadError
  if (!frames) return <Skeleton />
  return <Canvas frames={frames} />
}
```

The dynamic `import()` makes the bundler emit `animation-frames` as its own chunk, fetched only when `enabled` first turns true.
