# 8. Realtime specifics

Consult from `api-design` step 8.

Authentication happens at connect; authorization happens on every message or event against current permissions (`security` owns the checks). Identity comes from the authenticated session, never from a field the socket client sends.

- **SSE**: `text/event-stream`; every event carries an `id` so a reconnecting client sends `Last-Event-ID` and the server replays from it; set `retry`; send a comment line about every 15 seconds as a keepalive; `204` tells the client to stop reconnecting (WHATWG HTML, server-sent events).
- **WebSocket**: verify `Origin` and answer `403` for an unexpected one (RFC 6455 §10.2). Define the resume token yourself: the server issues a sequence number, and the client returns the last one it saw on reconnect.
- **Heartbeat**: ping at a stated interval, close the connection after a stated silence (RFC 6455 §5.5.2).
- **Buffers**: every connection has a bounded send buffer and a message-size cap. Overflow has one named action, for example close with `1008` and let resume replay; an oversize inbound message closes with `1009` (RFC 6455 §7.4.1).
- Capacity targets and alerts belong to `operability`.
