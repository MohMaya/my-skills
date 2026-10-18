---
name: rust
description: "Rust: writing or reviewing Rust services, CLIs, libraries, or non-UI crates; async/tokio work; error type design. Use before adding a crate, error type, spawned task, channel, lock, or async trait."
---

# Rust

Scope: services, CLIs, libraries, and the non-UI crates of a desktop workspace. Inside a GPUI app, async work follows `gpui` and its executors; this skill's tokio rules apply to code that runs on a tokio runtime, and the SIGTERM handling below is Unix-only (`#[cfg(unix)]` on other targets). Neighbouring owners: SQL and migrations are `postgres`; wire contracts are `api-design`; secrets and untrusted input are `security`; logs, metrics, and SLOs are `operability`; test discipline is `tdd`.

New workspaces adopt [lint/cargo-workspace-lints.toml](../../lint/cargo-workspace-lints.toml) and [lint/clippy.toml](../../lint/clippy.toml); this skill holds what lint cannot check. Run `cargo fmt --all -- --check`, `cargo clippy --workspace --all-targets --locked -- -D warnings`, and `cargo test --workspace --locked`. Check crate APIs against the versions in `Cargo.lock`.

## Workspace

- New crates use `edition = "2024"` (stable since Rust 1.85; `cargo new` writes it).
- Share versions through `[workspace.dependencies]` (members write `tokio.workspace = true`) and lints through `[workspace.lints]` (each member sets `[lints] workspace = true`).
- A crate that needs `unsafe` lives in its own small crate that does not inherit `unsafe_code = "forbid"`: `forbid` cannot be lowered, so a local `allow` is a compile error. Every `unsafe` block carries a `// SAFETY:` comment stating the invariant.

## Errors

- A library exposes one `thiserror` enum per failure set a caller can act on, one variant per distinct reaction, `#[from]` or `#[source]` keeping the cause chain.
- A binary or application layer returns `anyhow::Result` and adds `.context("doing X")` (`.with_context(|| ...)` when the message allocates) at every IO boundary.
- `String` and `()` are not error types: neither implements `std::error::Error`, so callers cannot match, chain, or box them.
- Propagate with `?`; `match` an error only to handle it, never to rewrap it by hand.
- Panic only when an invariant the types cannot express is broken (a caller bug). Malformed input, a missing file, and a rate limit are `Err`.

## Async (tokio)

- Blocking calls (sync IO, `std::fs`, `std::thread::sleep`) and CPU-heavy work stay off runtime threads: bounded blocking goes to `spawn_blocking`; sustained CPU work goes to a dedicated pool (rayon) or thread. A started `spawn_blocking` task cannot be aborted, and runtime shutdown waits for it.
- Every external call runs under `tokio::time::timeout`, with the duration taken from the caller's deadline. On expiry the future is dropped and `Elapsed` is returned; map it to a typed variant or add `.context(..)`.
- Every spawned task has an owner. A request-scoped group uses `JoinSet` (dropping it aborts its tasks). Long-lived tasks use `TaskTracker` from `tokio-util` (dropping it leaves them running). Nothing is spawned and forgotten.
- Shutdown has three parts: a trigger (SIGTERM, which containers and Railway send, or Ctrl-C), a `CancellationToken` that tasks select on (`child_token()` per subsystem), and a `TaskTracker` awaited under a timeout:

```rust
let (token, tracker) = (CancellationToken::new(), TaskTracker::new());
tracker.spawn(worker(token.child_token()));

let mut sigterm = signal::unix::signal(signal::unix::SignalKind::terminate()).context("listening for SIGTERM")?;
tokio::select! {
    _ = sigterm.recv() => {}
    r = signal::ctrl_c() => r.context("listening for ctrl-c")?,
}
tracker.close();
token.cancel();
timeout(SHUTDOWN_GRACE, tracker.wait()).await.context("workers outlived the shutdown grace")?;
```

- Channels are bounded: `mpsc::channel(n)` with `n` chosen from the memory you can afford, so a full queue makes `send(..).await` wait, and that wait is the backpressure. Decide at each producer whether to wait, shed, or fail.
- A `std::sync::Mutex` guard never lives across an `.await`. Keep the critical section synchronous and short, wrapped in a struct whose methods are not `async`. For state that needs IO, give one task ownership and talk to it over a channel. `tokio::sync::Mutex` only when the guard must be held across an `.await`; it costs more.
- A future inside `select!` in a loop must be cancel-safe (`mpsc::Receiver::recv` and `CancellationToken::cancelled` are; `read_exact` and `write_all` are not).
- Write `async fn` directly in traits (stable since 1.75). Add `async-trait` only to build a `dyn Trait` of async methods: a trait with `async fn` is not dyn compatible. A public library trait spells the method `fn get(&self) -> impl Future<Output = T> + Send`, because `async fn` there leaves callers unable to require `Send` (rustc's `async_fn_in_trait` warning).

## API shape

- Parameters borrow: `&str`, `&[T]`, `&Path`, or `impl AsRef<Path>`; take ownership only when the function stores or consumes the value.
- A domain id, unit, or validated string is a newtype with a private field and one fallible constructor (`TryFrom<&str>` or `FromStr`); parse at the boundary and pass the type inward.
- A state is an enum, and each transition is one function over it. Match without a `_` arm so adding a variant fails to compile in every place that must handle it.
- A parameter that would be `bool` or `Option` to select a mode becomes an enum.

## Tests

- Unit tests sit beside the code in `#[cfg(test)] mod tests`; integration tests go in `tests/` and reach only the public API. A binary keeps its logic in `src/lib.rs` so `tests/` can import it.
- Async tests use `#[tokio::test]` (current-thread by default; `flavor = "multi_thread"` when the test needs it). `start_paused = true` (feature `test-util`) pauses the clock, which jumps to the next timer whenever the runtime is idle, so timeout and retry tests run instantly.
- Run against real dependencies (a real Postgres, a temp directory). `mockall` or a hand-written fake replaces a true IO edge only: a payment client, an email sender, the clock.
- `cargo nextest run` is optional and skips doctests; keep `cargo test --doc` in CI beside it.

**Done when** `fmt`, `clippy -D warnings`, and `cargo test` pass, a service drains and exits on SIGTERM within its grace period, no task is spawned without an owner, every external call has a timeout, and each `Result` error type is an enum or `anyhow::Error`.
