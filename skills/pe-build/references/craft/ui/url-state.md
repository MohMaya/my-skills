# URL state

Filters, tabs, pagination, and an open modal live in the query string. Refresh, share, and the back button reproduce the view. Scroll position belongs to that history entry.

## The URL is the view

A discrete change pushes a history entry. `?status=open&tab=activity&item=42` is the orders list, the activity tab, and the modal for item 42. That URL is the view.

Do: write those in the router's search params, and validate them. A malformed shared link falls back to a safe default; it does not blank the page.

Don't: keep them in component state. Back returns to the route and forgets the filter, and the view cannot be pasted into a new tab.

Typing replaces the current entry. One search box does not stack a history entry per keystroke. Pass `replace: true` on the router's search update. Without a router, `history.replaceState` the query string and keep `history.state`. Use one. `replaceState` beside the router desyncs the search it parsed.

```tsx
navigate({
  to: "/orders",
  search: (prev) => ({ ...prev, q }),
  replace: true,
});
```

Navigation that opens another view is a real link, so command-click and middle-click work. Intent prefetch goes on this same router: [finishing](finishing.md).

```tsx
export const Route = createFileRoute("/orders")({
  validateSearch: (search: Record<string, unknown>) => ({
    status: search.status === "closed" ? "closed" : "open",
    tab: search.tab === "activity" ? "activity" : "details",
    q: typeof search.q === "string" ? search.q : undefined,
    item: typeof search.item === "string" ? search.item : undefined,
  }),
});
```

## Scroll

On a multi-page site, leave `history.scrollRestoration` at `"auto"`. The browser restores the offset.

A client router paints the next view after the history event, so the browser restores against a short page and the reader lands at the top. Turn on the router's restoration. It caches each history entry's scroll and restores it before paint. A new navigation starts at the top.

Do: one owner. The router below.

Don't: set `history.scrollRestoration = "manual"` next to that router, or keep a second scroll map. Two owners fight, and back lands at the top.

```tsx
const router = createRouter({
  routeTree,
  scrollRestoration: true,
});
```

Focus and the document title on a route change stay with [keyboard focus](../../a11y/focus-and-keyboard.md).

## Verify

Paste the URL into a new tab: the same filters, tab, and modal are open. Back returns the previous offset, and forward does too. Command-click the link and the new tab matches.
