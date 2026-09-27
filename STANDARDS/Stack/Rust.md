# Stack/Rust.md

Load before writing or reviewing Rust code.

## Skills

Use `rust-best-practices` for ownership, errors, traits, concurrency, tests, linting, and documentation.
Read its relevant chapters; existing repository conventions and shared standards govern when examples differ.
`codebase-design` owns module boundaries. [Desktop.md](Desktop.md) owns desktop stack choice and GPUI behavior.

## Toolchain and conventions

Use Cargo and the repository's declared toolchain, edition, minimum supported Rust version, and feature matrix.
Keep application lockfiles committed. Verify new APIs against the declared minimum version.
Prefer explicit ownership, borrowing, and domain types. Add shared ownership or trait indirection when the use case requires it.
Return recoverable failures through `Result`; preserve actionable context at IO boundaries.
Use the existing runtime and error libraries. A skill example alone does not justify another dependency.
Document unsafe invariants and verify them at their boundary. Keep unsafe code narrowly scoped.

## Checks

Follow repository-required checks and `Workflow/Delivery.md`. For a new Rust application, establish these baseline commands:

```sh
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --locked -- -D warnings
cargo test --workspace --locked
```

Exercise supported feature combinations and target platforms in addition to the default configuration when behavior depends on them.
Use the repository's existing runner when it replaces these commands. Preserve or strengthen its check coverage.
Run these checks explicitly: the shared turn-end gate currently covers Python and TypeScript, not Rust.
