# lint/

Checkable language rules as config. Copy a file under its own name (the turn-end gate in `hooks/stop-gate.py` finds it by name) or extend it; never restate its rules in prose.

| File | Enforces | Adopt |
| ---- | -------- | ----- |
| `tsconfig.strict.json` | strict, noUncheckedIndexedAccess, exactOptionalPropertyTypes, noImplicitOverride, noFallthroughCasesInSwitch, verbatimModuleSyntax, isolatedModules, erasableSyntaxOnly (TS 5.8+) | `"extends"` it. The bundler/noEmit lines suit Vite app tsconfigs only; libraries override `module`, `moduleResolution`, `noEmit` |
| `eslint.config.js` | typescript-eslint strictTypeChecked (no-explicit-any, no-floating-promises, no-misused-promises) plus assertionStyle never, switch-exhaustiveness-check, complexity 10, no empty catch | Copy. Needs eslint 9.22+, typescript-eslint 8, `"type": "module"` |
| `ruff.toml` | E, F, B, BLE, ASYNC, DTZ, UP, ANN, RUF, C901 at 10, S110/S112, TRY002/004/201/203/400 | Copy. `[format]` opts the gate into auto-format |
| `pyrightconfig.json` | strict mode plus reportExplicitAny; points at uv's `.venv` | Copy. basedpyright is the default because the gate runs it and it reads this file |
| `.golangci.yml` | v2 format: standard set plus errorlint, wrapcheck, contextcheck, noctx, bodyclose, copyloopvar, cyclop 10, revive context-as-argument and use-any | Copy. The gate runs only gofmt and `go vet`; run `golangci-lint run` in CI |
| `cargo-workspace-lints.toml` | forbid unsafe_code; deny unwrap_used, expect_used, undocumented_unsafe_blocks, await_holding_lock | Paste into the root `Cargo.toml`; add `[lints] workspace = true` to each crate |
| `clippy.toml` | Allows unwrap and expect inside tests, so `--all-targets -D warnings` stays green | Copy beside the root `Cargo.toml` |

Rust has no cyclomatic lint: `clippy::cognitive_complexity` measures a different thing and is allow-by-default. The gate's lizard ratchet enforces 10 on Rust.

Together `erasableSyntaxOnly` and `assertionStyle: never` rule out `enum`, so TypeScript state machines use string-literal unions with an exhaustive `switch`.
