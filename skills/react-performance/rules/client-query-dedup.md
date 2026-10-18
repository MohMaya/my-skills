---
title: Use TanStack Query for Request Deduplication
impact: MEDIUM-HIGH
impactDescription: automatic deduplication and caching
tags: client, tanstack-query, deduplication, caching, data-fetching
---

## Use TanStack Query for Request Deduplication

One `QueryClient` deduplicates in-flight requests and caches results by `queryKey`, so every component that calls `useQuery` with the same key shares one request. Define each query once with `queryOptions` and reuse it everywhere.

**Incorrect (no deduplication, each instance fetches):**

```tsx
function UserList() {
  const [users, setUsers] = useState([])
  useEffect(() => {
    fetch('/api/users')
      .then(r => r.json())
      .then(setUsers)
  }, [])
}
```

**Correct (multiple instances share one request):**

```tsx
import { queryOptions, useQuery } from '@tanstack/react-query'

export const usersOptions = () =>
  queryOptions({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(r => r.json()).then(parseUsers),
    staleTime: 60_000,
  })

function UserList() {
  const { data: users } = useQuery(usersOptions())
}

function UserCount() {
  const { data } = useQuery(usersOptions()) // same key: no second request
}
```

`parseUsers` turns the untrusted JSON into `User[]` at the boundary (a schema parser such as `z.array(User).parse`), so no cast is needed.

Reuse the same options object for `useSuspenseQuery`, `queryClient.ensureQueryData` in route loaders, `prefetchQuery` on hover, and `setQueryData(usersOptions().queryKey, ...)`.

**Tune freshness:**

- `staleTime` (default `0`): how long data counts as fresh. At `0`, every new mount and window focus refetches in the background. Set a real value per query, or `Infinity` for immutable data such as `/api/config`.
- `gcTime` (default 5 minutes; named `cacheTime` before v5): how long unused data stays in cache.
- Create one `QueryClient` at module level and share it through `QueryClientProvider`; a second client has its own cache and its own requests.

**For mutations:**

```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query'

function UpdateButton() {
  const queryClient = useQueryClient()
  const { mutate } = useMutation({
    mutationFn: updateUser,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
  })
  return <button onClick={() => mutate()}>Update</button>
}
```

Reference: [TanStack Query](https://tanstack.com/query/latest)
