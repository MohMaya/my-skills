# Sources

Rewritten for this repository on 2026-10-18 from `rust-engineer` in [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) (MIT, per the upstream skill's frontmatter), imported in commit `40c5f7c`. Rules are rewritten, and upstream defects are not carried over: edition 2021 as the default, `async-trait` recommended by default, `tokio::spawn` for CPU-bound work, mockall-first testing, `&s[..50]` byte slicing of strings, `&String` parameters, and `expect()`-in-production advice that contradicts `?` propagation.

Checked on 2026-10-18 against Rust 1.98.1 installed (1.99.1 current stable), tokio 1.53.3, tokio-util 0.7.20, thiserror 2.0.21, and anyhow 1.0.104:

- [Edition 2024](https://doc.rust-lang.org/edition-guide/rust-2024/index.html) (Rust 1.85.0); `cargo new` wrote `edition = "2024"` on 1.98.1.
- [Cargo workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html) (`[workspace.dependencies]`, `[workspace.lints]`, member `workspace = true`)
- [Lint levels](https://doc.rust-lang.org/rustc/lints/levels.html) (`forbid` cannot be lowered)
- [thiserror](https://docs.rs/thiserror/latest/thiserror/) and [anyhow](https://docs.rs/anyhow/latest/anyhow/) (`Context`, `with_context`)
- [The Book: to panic or not to panic](https://doc.rust-lang.org/book/ch09-03-to-panic-or-not-to-panic.html) and [API guidelines C-GOOD-ERR](https://rust-lang.github.io/api-guidelines/interoperability.html)
- [Blocking and CPU-bound work in tokio](https://docs.rs/tokio/latest/tokio/index.html) and [`spawn_blocking`](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html) (cannot abort a started task; shutdown waits)
- [`time::timeout`](https://docs.rs/tokio/latest/tokio/time/fn.timeout.html)
- [`JoinSet`](https://docs.rs/tokio/latest/tokio/task/struct.JoinSet.html) (drop aborts), [`TaskTracker`](https://docs.rs/tokio-util/latest/tokio_util/task/task_tracker/struct.TaskTracker.html) (drop does not abort), [`CancellationToken`](https://docs.rs/tokio-util/latest/tokio_util/sync/struct.CancellationToken.html), [graceful shutdown](https://tokio.rs/tokio/topics/shutdown)
- [`mpsc`](https://docs.rs/tokio/latest/tokio/sync/mpsc/index.html) (bounded send waits) and [`Receiver::recv`](https://docs.rs/tokio/latest/tokio/sync/mpsc/struct.Receiver.html) (cancel safe)
- [`select!` cancel safety](https://docs.rs/tokio/latest/tokio/macro.select.html)
- [Shared state: std vs tokio mutex](https://tokio.rs/tokio/tutorial/shared-state)
- [async fn in traits (1.75)](https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/)
- [API guidelines: C-CALLER-CONTROL, C-GENERIC](https://rust-lang.github.io/api-guidelines/flexibility.html), [C-NEWTYPE, C-CUSTOM-TYPE](https://rust-lang.github.io/api-guidelines/type-safety.html)
- [The Book: test organization](https://doc.rust-lang.org/book/ch11-03-test-organization.html), [`#[tokio::test]`](https://docs.rs/tokio/latest/tokio/attr.test.html), [`time::pause`](https://docs.rs/tokio/latest/tokio/time/fn.pause.html), [nextest](https://nexte.st/) (no doctests)

Run on rustc 1.98.1: a trait with `async fn` fails `Box<dyn Trait>` with E0038 (not dyn compatible); a `pub` trait with `async fn` warns `async_fn_in_trait` and suggests `-> impl Future<Output = T> + Send`; `String` fails an `E: std::error::Error` bound. The shutdown example in `SKILL.md` passes `cargo clippy --all-targets -- -D warnings` with tokio 1.53.3 and tokio-util 0.7.20 under `unwrap_used`, `expect_used`, and `await_holding_lock` denied.
