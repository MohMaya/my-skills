# Sources

Rules rewritten 2026-10-18 from the skills imported in commit 40c5f7c; no text is copied. Each rule was checked against the primary document in the table, and anything unverifiable was left out.

## Upstream skills

| Skill | Repository | License as found on disk |
| --- | --- | --- |
| api-designer, graphql-architect, websocket-engineer, mcp-developer, cli-developer, code-documenter | [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) | `license: MIT` in each SKILL.md frontmatter; no LICENSE file in the import |
| api-design-principles | [wshobson/agents](https://github.com/wshobson/agents) | Unknown in the import: no frontmatter license and no LICENSE file |

Ideas adopted: OpenAPI linting with Redocly, `application/problem+json` errors with documented `type` URIs, the CLI stream, colour, and exit-code split, the MCP `isError` split, running documentation examples in CI. Patterns not adopted: offset cursors, offset-and-count templates, a version from day one, two live versions, RFC 7807 (obsoleted), socket-supplied identity, `startswith` path checks, SSE as the remote MCP transport, `any` and `as` casts, swallowed exceptions, setuptools and pip.

## Rule verification

| Rule | Primary source |
| --- | --- |
| `application/problem+json`; RFC 9457 obsoletes 7807; `type` URI; `status` equals the HTTP status; avoid exposing implementation detail; clients ignore unknown extensions | [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) |
| `Retry-After` with `429`; `428` Precondition Required | [RFC 6585](https://www.rfc-editor.org/rfc/rfc6585.html) |
| `PUT` and `DELETE` idempotent, `POST` not (§9.2.2); `If-Match` uses strong comparison (§13.1.1); `412` on a failed precondition (§15.5.13) | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) |
| `Idempotency-Key` semantics: stored result on retry, `409` in flight, `422` payload mismatch, `400` missing. An expired Internet-Draft (rev 07, expired 2026-04-18), not an RFC | [draft-ietf-httpapi-idempotency-key-header](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/) |
| `Deprecation` as a Structured Fields date; `Link rel="deprecation"`; Sunset not earlier than Deprecation | [RFC 9745](https://www.rfc-editor.org/rfc/rfc9745.html) |
| `Sunset` as an HTTP-date | [RFC 8594](https://www.rfc-editor.org/rfc/rfc8594.html) |
| `Link rel="successor-version"` | [RFC 5829](https://www.rfc-editor.org/rfc/rfc5829.html) |
| Cursors opaque; offset pagination has downsides; every list paginated with a bound | [graphql.org pagination](https://graphql.org/learn/pagination/), [graphql.org security](https://graphql.org/learn/security/) |
| GraphQL depth and cost limits, trusted documents (first-party only), hidden error detail outside development | [graphql.org security](https://graphql.org/learn/security/) |
| SSE `id` and `Last-Event-ID` resume, `retry`, a comment line about every 15 seconds, `204` stops reconnect, `text/event-stream` | [WHATWG HTML, server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html) |
| WebSocket `Origin` check with `403` (§10.2); no authentication of its own (§10.5); ping and pong (§5.5.2, §5.5.3); close codes `1008` and `1009` (§7.4.1) | [RFC 6455](https://www.rfc-editor.org/rfc/rfc6455.html) |
| MCP: stdio and Streamable HTTP are the standard transports; HTTP+SSE deprecated; stdio stdout carries only MCP messages and logs go to stderr; `Origin` validation with `403`, localhost binding; `isError: true` for execution and validation failures, JSON-RPC errors for unknown tool and malformed requests; tool name characters and length; `outputSchema`. Verified against revision 2026-07-28 | [Transports](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports), [stdio](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio), [Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http), [Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) |
| Path confinement: resolve symlinks and `..` first, then check containment; a raw prefix check is bypassable (Example 4); `os.Root` from Go 1.24; `is_relative_to` is string-based, so resolve first | [CWE-22](https://cwe.mitre.org/data/definitions/22.html), [Go blog: os.Root](https://go.dev/blog/osroot), [Python pathlib](https://docs.python.org/3/library/pathlib.html) |
| CLI: stdout for data and stderr for diagnostics; `--json`; colour off for non-TTY, `NO_COLOR`, `TERM=dumb`, `--no-color`; prompts only on a TTY and `--no-input`; confirmation and `--force` and `--confirm`; examples in help; Ctrl-C handling; exit zero or non-zero | [clig.dev](https://clig.dev/) |
| `NO_COLOR` when present and non-empty | [no-color.org](https://no-color.org/) |
| Exit code 2 for usage: `flag.ExitOnError` calls `os.Exit(2)` | [Go flag package](https://pkg.go.dev/flag) |
| Exit code 130: a fatal signal N yields 128+N | [Bash manual, exit status](https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html) |
| OpenAPI 3.1 and 3.2 are supersets of JSON Schema 2020-12; Redocly lint handles 3.0, 3.1, and 3.2 | [OpenAPI 3.1.1](https://spec.openapis.org/oas/v3.1.1.html), [OpenAPI 3.2.1](https://spec.openapis.org/oas/latest.html), [Redocly CLI](https://github.com/redocly/redocly-cli) |

## Deliberate departures and omissions

- `next_cursor` alone ends a list; a separate `has_more` is dropped because it can contradict the cursor.
- Destructive CLI commands use `--force` and `--confirm=<name>`, the forms clig.dev documents, rather than `--yes`.
- "CI" as a trigger for non-interactive mode is dropped; no TTY is the verified signal.
- Not verified, so omitted: that `EventSource` is GET-only without custom headers; argparse and Node exit-code parity; Spectral as an alternative linter; shell-completion and startup-time targets; the cost of a `total` count.
- The rules that an idempotency record commits in the effect's transaction, that a cursor never encodes an offset, and that one tie-breaker-terminated sort order is contractual are this repository's own design rules, not cited.
