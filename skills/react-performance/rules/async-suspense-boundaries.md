---
title: Strategic Suspense Boundaries
impact: HIGH
impactDescription: faster initial paint
tags: async, suspense, useSuspenseQuery, tanstack-query, layout-shift
---

## Strategic Suspense Boundaries

Fetching in a component that wraps the whole page blocks the whole page. Push `useSuspenseQuery` down into the component that needs the data and wrap that component in `<Suspense>`, so the shell paints immediately.

**Incorrect (page shell waits for data):**

```tsx
function Page() {
  const { data } = useSuspenseQuery(dataOptions())

  return (
    <div>
      <Sidebar />
      <Header />
      <DataDisplay data={data} />
      <Footer />
    </div>
  )
}
```

**Correct (shell renders immediately, data fills in):**

```tsx
function Page() {
  return (
    <div>
      <Sidebar />
      <Header />
      <Suspense fallback={<Skeleton />}>
        <DataDisplay />
      </Suspense>
      <Footer />
    </div>
  )
}

function DataDisplay() {
  const { data } = useSuspenseQuery(dataOptions())
  return <div>{data.content}</div>
}
```

Two `useSuspenseQuery` calls in one component run in series, because the first suspends before the second starts. Use `useSuspenseQueries` for several queries in one component, or one component per query under sibling boundaries (see [Promise.all() for Independent Operations](./async-parallel.md)).

```tsx
const [{ data: users }, { data: teams }] = useSuspenseQueries({
  queries: [usersOptions(), teamsOptions()],
})
```

**When NOT to use this pattern:**

- Critical data needed for layout decisions (affects positioning)
- Small, fast queries where suspense overhead isn't worth it
- When you want to avoid layout shift (loading → content jump)

**Trade-off:** Faster initial paint vs potential layout shift. Choose based on your UX priorities.
