---
name: socket-and-console-hygiene
description: Socket and console details that cost debugging time. TcpSocket::Connect returns true on EINPROGRESS; a freshly accepted socket needs a read timeout before the request is read; set stdout unbuffered for test output before _Exit.
---

# Sockets and console output

## Rules

- `TcpSocket::Connect` returns true on `EINPROGRESS` (and `EWOULDBLOCK`). Success is not
  yet known. Wait for writability and check the socket error before treating the
  connection as made.
- A freshly accepted socket with the default zero-wait timeout can close before the
  request bytes arrive. Set a read timeout right after accept, before reading the request.
  Engine acceptors use `request.Timeout(30000)` before dispatch.
- Console test output can be lost on `_Exit` or a crash, because stdout is buffered. Call
  `setvbuf(stdout, NULL, _IONBF, 0)` at startup, or flush before `_Exit`.

## Sources

- Upstream `ultimatepp/uppsrc/Core/Socket.cpp`: `EINPROGRESS` handling in `Connect`.
- Project: `SkylarkManager/uppsrc/WebEngine/Host.cpp` (`request.Timeout(30000)`).
- Project trap record: `SkylarkManager/tasks/takeover/T00-context-and-rules.md`
  (the `setvbuf` and accepted-socket traps, from debugging sessions).

## Verified

- Read in upstream `Socket.cpp`: `EINPROGRESS` and `EWOULDBLOCK` are treated as pending
  in `Connect` (around lines 462 and 1068).
- Read in `Host.cpp` line 115: the request timeout is set on the accepted request.
- The `setvbuf` and zero-wait traps are recorded from project incidents (T00), not
  re-derived here.

Provenance: [HISTORY.md](../../HISTORY.md).
