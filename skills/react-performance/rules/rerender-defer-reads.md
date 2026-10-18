---
title: Defer State Reads to Usage Point
impact: MEDIUM
impactDescription: avoids unnecessary subscriptions
tags: rerender, search-params, localStorage, optimization
---

## Defer State Reads to Usage Point

Don't subscribe to dynamic state (search params, localStorage) if you only read it inside callbacks.

**Incorrect (subscribes to all search param changes):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const search = useSearch({ strict: false })

  const handleShare = () => {
    shareChat(chatId, { ref: search.ref })
  }

  return <button onClick={handleShare}>Share</button>
}
```

**Correct (reads on demand, no subscription):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const router = useRouter()
  const handleShare = () => {
    const { ref } = router.state.location.search
    shareChat(chatId, { ref })
  }

  return <button onClick={handleShare}>Share</button>
}
```
