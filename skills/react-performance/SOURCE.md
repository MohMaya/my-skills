# Source and local changes

Forked from [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) `vercel-react-best-practices` (version 1.0.0). License: MIT. Upstream folder hash at fork, from `.skill-lock.json` (`skills/react-best-practices`): `343db72180d05814949fef7d46be96b5c6ee86b3`.

Forked on 2026-10-18 for a Vite and TanStack (Router, Query) client-rendered stack hosted on Cloudflare Pages. It is no longer tracked in `.skill-lock.json`, so `npx skills update` no longer touches it.

Removed:

- All ten `server-*` rules and `async-api-routes`: React Server Components, server actions, API routes, and `after()` have no place in a client-only app.
- `rendering-hydration-no-flicker` and `rendering-hydration-suppress-warning`: no SSR, so no hydration.
- `client-swr-dedup`: replaced by `client-query-dedup`.
- `AGENTS.md` (compiled copy of the rules), `README.md`, `rules/_sections.md`, and `rules/_template.md` (upstream authoring files). `SKILL.md` carries the index.

Rewritten for Vite and TanStack:

- `async-suspense-boundaries`: `useSuspenseQuery` and `useSuspenseQueries` under Suspense replace async server components and `use(promise)`.
- `bundle-dynamic-imports`: `React.lazy`, TanStack Router `autoCodeSplitting`, and `lazyRouteComponent` replace `next/dynamic`.
- `bundle-preload`: router `defaultPreload: 'intent'` for routes; dropped the `typeof window` SSR guard.
- `bundle-conditional`: dropped the SSR guard; a failed import now reaches the error boundary instead of being swallowed.
- `bundle-defer-third-party`: `React.lazy` replaces `next/dynamic` and `@vercel/analytics`.
- `bundle-barrel-imports`: Vite dev-server and Rollup tree-shaking costs replace Next `optimizePackageImports` and its cold-start numbers.
- `bundle-analyzable-paths`: removed the Next file-tracing and `fs` path section; added `import.meta.glob`.
- `rendering-resource-hints`: `index.html` links for first paint, React DOM APIs for runtime hints.
- `rendering-script-defer-async`: plain HTML; removed `next/script`.
- `client-event-listeners`: a module-level subscriber map replaces `useSWRSubscription`.
- `rerender-defer-reads`: TanStack Router `useSearch` replaces Next `useSearchParams`, and the on-demand read uses `useRouter().state.location.search` (non-reactive by design).
- `async-dependencies`: leads with plain promise chaining; the `better-all` dependency is removed.
- Small edits: `async-cheap-condition-before-await` (dropped `React.cache`), `js-cache-function-results` (dropped the Vercel blog link), `rendering-activity` and `advanced-event-handler-refs` (React 19.2 requirement; handlers typed `(e: Event)`).

Added:

- `client-query-dedup`: TanStack Query v5 `queryOptions`, `staleTime`, `gcTime`, one `QueryClient`.

Currency checked on 2026-10-18 against react.dev (React 19.2 release notes and reference pages): `Activity` and `useEffectEvent` are stable in 19.2, so `rendering-activity`, `advanced-effect-event-deps`, `advanced-event-handler-refs`, and `advanced-use-latest` stay. TanStack Query v5.90 and TanStack Router docs checked through Context7.
