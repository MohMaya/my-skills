---
name: go
description: Go services, CLIs, and libraries - standard-library choices, goroutine ownership, context and graceful shutdown, error and interface design, shared state, tests, and go.mod. Use when writing or reviewing Go code, or adding a Go dependency.
---

# Go

Go code here reads like the standard library: small concrete packages, every goroutine owned, every error handled once. New repositories adopt [.golangci.yml](../../lint/.golangci.yml), which enforces error handling, context passing, loop variables, and complexity; this skill holds what a linter cannot check. Neighbouring owners: SQL is `postgres`; wire and CLI contracts (including `flag`) are `api-design`; secrets, untrusted input, and `govulncheck` are `security`; what to log and measure is `operability`; test discipline is `tdd`. A version in parentheses is the Go release that introduced the feature; the `go` line in `go.mod` must be at least that.

## Standard library first

- Route with `http.NewServeMux()` and method-plus-wildcard patterns, `"GET /orders/{id}"` read by `r.PathValue("id")` (1.22). A router dependency needs a stated gap in `ServeMux`.
- Log with `log/slog`: build the handler in `main`, pass the `*slog.Logger` to constructors, call `InfoContext(ctx, ...)`.
- Use `slices`, `maps`, `cmp`, the `min`, `max`, and `clear` builtins (1.21), and `errors.Join` (1.20); where `slices` has no function, write the `for` loop. `go fix ./...` (1.26) applies these idioms mechanically.
- Open a path built from a caller-supplied name with `os.OpenRoot(dir)` (1.24), whose methods reject any path that leaves `dir`.
- Write the concrete code first. Add a type parameter when the same body is about to appear for a second type; take an interface when the body only calls methods.

## Goroutines

- Every `go` statement has an owner that waits for it and a `ctx` it watches. Fan out with `errgroup.WithContext`, calling `g.SetLimit(n)` before the first `g.Go`; without errors, use `sync.WaitGroup.Go` (1.25). Both require `f` not to panic.
- Work that outlives its request runs under `context.WithoutCancel(ctx)` and belongs to a group drained at shutdown.
- The sender closes a channel. With several senders, one coordinator waits for them and closes.

## Context and shutdown

- `ctx` is the first parameter and never a struct field; a long-lived type takes `ctx` per method.
- Derive a deadline from the caller, `context.WithTimeout(ctx, d)` then `defer cancel()`. Run cleanup on cancel with `context.AfterFunc(ctx, f)` instead of a watcher goroutine.
- `http.Server` sets `ReadHeaderTimeout` and `IdleTimeout` (zero means none), plus `WriteTimeout` when no handler streams. One `http.Client` with `Timeout` set is created and reused; a zero `Timeout` waits forever.
- `main` builds `ctx` with `signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)` and exits on `run(ctx)`'s error, because `os.Exit` skips deferred functions. `ListenAndServe` returns `ErrServerClosed` as soon as `Shutdown` starts, so `run` waits for `Shutdown` itself:

```go
func run(ctx context.Context) error {
	srv := &http.Server{Addr: ":8080", Handler: routes(), ReadHeaderTimeout: 5 * time.Second, IdleTimeout: time.Minute}
	g, ctx := errgroup.WithContext(ctx)
	g.Go(func() error {
		if err := srv.ListenAndServe(); !errors.Is(err, http.ErrServerClosed) {
			return fmt.Errorf("serve: %w", err)
		}
		return nil
	})
	g.Go(func() error {
		<-ctx.Done()
		shutdownCtx, cancel := context.WithTimeout(context.WithoutCancel(ctx), 20*time.Second)
		defer cancel()
		return srv.Shutdown(shutdownCtx)
	})
	return g.Wait()
}
```

## Errors

- The package that owns a failure exports a sentinel (`var ErrNotFound = errors.New(...)`) or a typed error. Callers branch with `errors.Is` and `errors.AsType[*ValidationError]` (1.26); the transport boundary maps them to a status.
- Wrap with the operation and its identifiers, `fmt.Errorf("load order %s: %w", id, err)`. `%w` makes the cause part of your API, so translate driver and OS errors (`sql.ErrNoRows`, `*fs.PathError`) into the package's sentinel.
- A function returns an error or logs it. The layer that handles the error logs it once.

## Interfaces and layout

- The consumer declares the interface next to its caller, with one to three methods; the producer returns its concrete type. An interface needs a second implementation or a fake of a true IO edge today.
- Binaries live in `cmd/<name>/main.go` and logic in `internal/<domain>/`.

## Shared state

- A struct guards its shared fields with a `sync.Mutex`; types holding a mutex or `atomic` value use pointer receivers, since neither may be copied after first use.
- Counters and flags use `atomic.Int64`, `atomic.Bool`, and `atomic.Pointer[T]`, never `atomic.AddInt64(&field, 1)`.
- CI runs `go test -race ./...`. The detector sees only executed paths, so each concurrent type gets a test that drives it from several goroutines.

## Tests

- Table-driven: `for _, tc := range cases { t.Run(tc.name, ...) }`, with `t.Parallel()` in each subtest that touches no package state; `t.Setenv` cannot run in parallel tests.
- Pass `t.Context()` (1.24) to code under test; it cancels before cleanup, so goroutines exit before the test ends.
- Serve HTTP edges with `httptest.NewServer`, use a real database per `postgres`, and fake only true IO edges with small hand-written types.
- Test timeouts, backoff, and tickers inside `synctest.Test(t, func(t *testing.T) {...})` (1.25), where `time` runs on a fake clock. Network I/O is not durably blocking, so a bubble serves HTTP from `httptest.NewTestServer(t, h)` (1.27).
- Benchmarks loop with `for b.Loop()` (1.24).

## Module

- The `go` line is the minimum version the module needs; add a `toolchain` line only to pin a patch release above it.
- Pin dev tools with `go get -tool <pkg>` and run them with `go tool <name>`, not `tools.go`.

**Done when** `golangci-lint run` and `go test -race ./...` pass, every `go` statement names its owner, and every server sets timeouts and shuts down on SIGTERM.
