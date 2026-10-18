---
name: api-design
description: Contract-first design of an external interface before any code, whether an HTTP endpoint, a realtime stream (SSE or WebSocket), a CLI command, an MCP tool, or a GraphQL schema. Use before adding or changing a route, error shape, list pagination, write retry, or version, and before deprecating any of them.
---

# API design

An interface is a promise to a caller you cannot see. Write the promise (the contract document) first, then the code that keeps it; a public contract is hard to reverse, so the mandate comes before the shape.

**Dvandva.** Run `dvandva` before you produce a contract.

Steps run in order; a later step that breaks an earlier answer sends you back to it. Steps 8 to 10 apply only to the matching transport.

| Concern | Owner |
| --- | --- |
| SQL, keyset query shape, indexes | `postgres` |
| Authn, authz, tokens, injection, CORS, CSRF | `security` |
| SLOs, alerts, capacity | `operability` |
| Choosing topology or datastore | `system-design` |
| FastAPI handler code | `fastapi` |
| In-process module interfaces | `codebase-design` |

## 1. Mandate

Write the card before any shape:

- **Caller**: the named client, team, script, or agent, and the job it does through this interface.
- **Consumption**: every response field the caller reads, traced into the client's code when it is reachable.
- **Success signal**: how we will know it worked.
- **Out of scope**: what this interface will not do.

When any line is missing, run `grilling` with one question and a recommended answer.

**Done when** the card is complete and every response field maps to a named consumer or is dropped.

## 2. Transport

Pick the first row that fits the caller's need:

| Need | Transport |
| --- | --- |
| Request and response over HTTP | **REST with JSON** (default), described by OpenAPI |
| Server pushes, the client sends nothing on the stream | **SSE** |
| Both sides send on one long-lived connection | **WebSocket** |
| Two or more named clients each need a different shape of one graph | **GraphQL** |
| A person or script at a shell | **CLI**, [references/cli.md](references/cli.md) |
| A model or agent calls tools | **MCP tool server** |

GraphQL needs its named clients written on the card; otherwise the row is REST. Three rules when it ships:

- Execute only trusted (persisted) documents when every client is first-party, and bound every operation with depth and cost limits.
- Paginate every list as a connection with a hard maximum `first`.
- Hide error detail outside development.

**Done when** one row is chosen and the card names the caller that justifies it.

## 3. Resource and operation shape

- URLs name resources; the method carries the verb. `GET` reads, `PUT` and `DELETE` are idempotent, `POST` creates or acts (RFC 9110 §9.2.2).
- Parse every request into a domain type at the boundary, then trust the type inside. A body that fails to parse never reaches a service.
- Declare an explicit response schema as its own type, separate from the storage model, holding only the fields step 1 mapped to a consumer. Internal ids, audit columns, and flags stay inside.
- Use one naming convention for every field.

**Done when** every operation in the OpenAPI document lists its request type, response type, and failure types, and its response fields are a subset of the card's consumed fields.

## 4. Errors

- A failure carries its status code; `200` carries success only.
- The body is `application/problem+json` (RFC 9457, which obsoletes RFC 7807): `type`, `title`, `status` (equal to the HTTP status), and `detail`, plus extension members where a caller needs them.
- `type` is a stable URI with a documented entry. Each failure class has exactly one `type`, and each entry names what the caller does next.
- `detail` says what the caller can fix. Stack traces, SQL, internal identifiers, and the permissions a caller lacked go to logs (RFC 9457 Security Considerations; the `security` skill decides what a `403` or `404` reveals).
- A rate limit returns `429` with `Retry-After` (RFC 6585).

**Done when** every failure class in the document has one `type` and a documented entry, and a test per class asserts status, content type, and `type`.

## 5. Lists

The wire contract; the query behind it belongs to `postgres`.

```json
{ "items": [], "next_cursor": "opaque-or-null" }
```

- Request: `limit` and `cursor`. The cursor is opaque to the caller: sort-column values plus a unique tie-breaker, encoded, and never a position or an offset. Callers treat it as a token; its format changes without notice.
- `next_cursor` is `null` on the last page. One field carries the end of the list, so no response can say "more" and "done" at once.
- `limit` has a documented default and a hard maximum. A request above the maximum returns `400` naming the maximum.
- A malformed or expired cursor returns `400` with its own `type`.
- A `total` field ships only when a named consumer reads it; its count query goes through `postgres`.
- The sort order is part of the contract and ends in the tie-breaker.

**Done when** the OpenAPI document declares `limit` with `default` and `maximum`, and a test walks every page of a fixture with ties on the sort column and sees each row exactly once.

## 6. Writes

- A `POST` that creates or charges accepts `Idempotency-Key`. The server stores the first result under (caller, key, request fingerprint), commits that record in the same transaction as the effect, and returns the stored result, success or error, on every retry. Name the retention window in the document.
- A key whose first request is still running returns `409`; a key reused with a different payload returns `422`; a required key that is absent returns `400`. The header is an expired IETF draft (`draft-ietf-httpapi-idempotency-key-header-07`), so the document carries the semantics.
- Read-modify-write resources return a strong `ETag`. An update sends `If-Match`; a mismatch returns `412`, and an absent `If-Match` on a resource that requires one returns `428` (RFC 9110 §13.1.1 requires strong comparison; RFC 6585 defines `428`).

**Done when** a test replays each keyed `POST` twice and asserts one effect and an identical response, and a test asserts `412` on a stale `If-Match`.

## 7. Evolution

- Change by addition: new optional fields and new operations. Removing, renaming, retyping, or tightening a field is a break.
- Add a version marker only when a break exists today, and only for the operations it breaks. Until then the path carries none, and one version is live.
- A forced break puts these on the old operation:
  - `Deprecation: @<unix-seconds>` (RFC 9745, a Structured Fields date);
  - `Sunset: <HTTP-date>` (RFC 8594), never earlier than the `Deprecation` date;
  - `Link: <migration-guide>; rel="deprecation"` (RFC 9745);
  - `Link: <new-operation>; rel="successor-version"` (RFC 5829).
- Migrate every caller, then delete the old operation on the Sunset date.

**Done when** the OpenAPI diff against the released document shows only additions, or the break carries a Sunset date, a caller-migration list, and a dated deletion.

## 8. Realtime specifics

Follow [references/realtime.md](references/realtime.md): authorization per message, SSE resume, WebSocket origin and resume token, heartbeat, bounded buffers.

**Done when** the contract states the event schema, ordering, resume token, buffer bound with its overflow action, and heartbeat interval with timeout, and a test reconnects with the last id and receives the missed events once.

## 9. CLI contract

Follow [references/cli.md](references/cli.md): stdout data, stderr diagnostics, a `--json` mode, colour rules, non-interactive failure, exit codes, confirmation for destructive commands, examples in `--help`.

**Done when** the reference's checks pass against the built binary.

## 10. MCP tools

Follow [references/mcp.md](references/mcp.md): one tool per intent, `isError` for tool failures, stdio logging to stderr, Streamable HTTP, path confinement.

**Done when** a test per failure class asserts `isError`, and `../` and symlink path arguments are refused.

## 11. Proof

- The OpenAPI 3.1-or-later document is committed beside the code and `redocly lint openapi.yaml` runs in CI.
- Contract tests assert responses (status, headers, body) for every error path from step 4 and for steps 5 to 7, never which functions ran.
- Examples in the docs run in CI against the real server.

**Done when** lint is green, each contract test named above passes, and a doc example fails the build when the server changes under it.
