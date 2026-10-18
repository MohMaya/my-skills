# 10. MCP tools

Consult from `api-design` step 10.

- One tool per caller intent. `inputSchema` is JSON Schema; add `outputSchema` when the result is structured. Names use letters, digits, `_`, `-`, `.`, at most 128 characters.
- A tool-level failure (API error, input validation, business rule) returns a result with `isError: true` and a message the model can act on. Only a protocol failure (unknown tool, malformed request) is a JSON-RPC error.
- A stdio server writes MCP messages to stdout and logs to stderr only. Remote servers use Streamable HTTP, which replaced HTTP+SSE; validate `Origin` (`403`), bind local servers to `127.0.0.1`, and authenticate.
- A path argument is confined by resolving the real path of the root and the target (symlinks and `..` gone), then checking the target is relative to the root: Python `Path.resolve()` then `is_relative_to()`, Go 1.24 `os.Root`. A string-prefix check accepts `/data-evil` for root `/data`.
- Check the live revision at modelcontextprotocol.io before building; scaffold with `anthropic-skills:mcp-builder` or `cloudflare:build-mcp`.
