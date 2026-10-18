# CLI contract

A CLI is an interface with two callers: a person and a script. Serve the script through stdout, stderr, and exit codes; serve the person through help, colour, and prompts.

## Streams and output

- **stdout** holds data, the thing a pipe wants. **stderr** holds diagnostics, progress, and errors.
- `--json` prints one machine-readable document on stdout. It is the only alternate format.
- Colour is on only when that stream is a TTY, `NO_COLOR` is unset or empty, `TERM` is not `dumb`, and `--no-color` is absent. Check stdout and stderr separately.

## Input

- Prompt only when stdin is a TTY. Without one, or with `--no-input`, a missing value fails fast and the message names the flag that supplies it.
- Every prompt has a flag or argument that answers it.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Success |
| 1 | Failure |
| 2 | Usage error (Go's `flag` with `ExitOnError` exits 2) |
| 130 | Interrupted by SIGINT (128 plus signal 2) |

Add a code only when a caller branches on it, and document it in `--help`.

## Destructive commands

Interactively, ask for `y` or `yes`. Without a TTY, require `--force`. For severe actions, require the resource's name, typed or passed as `--confirm=<name>`.

## Help and interrupts

- `--help` leads with one or two examples. Long recipes go to a web page.
- On SIGINT, say what is happening, run bounded cleanup, and exit 130. A second SIGINT skips cleanup, and the message says what skipping does.

## Stack

- **Go**: standard-library `flag` first, with a `context.Context` from `signal.NotifyContext` passed through every IO call. Take a framework only when a subcommand tree outgrows `flag`, and name the case.
- **Python**: a `uv` project with type hints and a `[project.scripts]` entry point.
- **Node**: strict TypeScript with the kernel's no-`any`, no-`as` rules.

**Done when** a test runs the built binary with piped stdout and no TTY and asserts: stdout parses under `--json`, stderr holds the diagnostics, every exit code in the table, no ANSI bytes, and a missing-input failure that names its flag.
