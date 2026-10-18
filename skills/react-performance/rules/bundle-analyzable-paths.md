---
title: Prefer Statically Analyzable Paths
impact: HIGH
impactDescription: avoids accidental broad bundles
tags: bundle, vite, rollup, esbuild, dynamic-import
---

## Prefer Statically Analyzable Paths

Build tools work best when import paths are obvious at build time. If you hide the real path inside a variable or compose it too dynamically, the tool either has to include a broad set of possible files or warn that it cannot analyze the import.

Prefer an explicit map of literal `import()` calls so the set of reachable chunks stays narrow and predictable.

**Incorrect (the bundler cannot tell what may be imported):**

```ts
const PAGE_MODULES = {
  home: './pages/home',
  settings: './pages/settings',
} as const

const Page = await import(PAGE_MODULES[pageName])
```

**Correct (use an explicit map of allowed modules):**

```ts
const PAGE_MODULES = {
  home: () => import('./pages/home'),
  settings: () => import('./pages/settings'),
} as const

const Page = await PAGE_MODULES[pageName]()
```

When the set of files is a directory, `import.meta.glob('./pages/*.tsx')` is Vite's analyzable form: the pattern is a literal, and each match becomes its own lazy chunk.

Reference: [Vite features](https://vite.dev/guide/features.html), [Rollup dynamic import vars](https://www.npmjs.com/package/@rollup/plugin-dynamic-import-vars)
