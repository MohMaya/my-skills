---
title: Avoid Barrel File Imports
impact: CRITICAL
impactDescription: slow dev server and larger bundles
tags: bundle, imports, tree-shaking, barrel-files, vite
---

## Avoid Barrel File Imports

Import directly from source files instead of barrel files. **Barrel files** are entry points that re-export many modules (e.g., an `index.ts` that does `export * from './module'`).

Two costs:

- **Dev server:** Vite serves source modules one by one, so importing one name from your own `index.ts` barrel loads every module it re-exports. A dependency barrel with thousands of re-exports (icon libraries, `@mui/icons-material`) slows Vite's dependency pre-bundling and the first page load.
- **Production bundle:** Rollup tree-shakes ESM barrels only when the package declares `"sideEffects": false` (or the barrel's modules are side-effect free). CJS packages and barrels with side effects keep unused modules.

Measure before rewriting: build with `rollup-plugin-visualizer` and check whether the unused modules ship.

**Incorrect (pulls the whole barrel):**

```tsx
import { Check, X, Menu } from 'lucide-react'
import { Button, TextField } from '@mui/material'
import { formatDate } from '@/utils'
```

**Correct (direct imports):**

```tsx
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import { formatDate } from '@/utils/format-date'
```

> **TypeScript warning:** Some libraries (notably `lucide-react`) don't ship `.d.ts` files for their deep import paths. Importing from `lucide-react/dist/esm/icons/check` resolves to an implicit `any` type, causing errors under `strict` or `noImplicitAny`. Verify the library exports types for its subpaths before using direct imports; otherwise keep the barrel import and confirm tree-shaking with the visualizer.

Libraries commonly affected: `@mui/material`, `@mui/icons-material`, `@tabler/icons-react`, `react-icons`, `@headlessui/react`, `lodash`, `ramda`, `date-fns`, `rxjs`, `react-use`. Avoid barrels in your own `src/` too.
