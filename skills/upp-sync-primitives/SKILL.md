---
name: upp-sync-primitives
description: Synchronization primitives in U++ code. Do not make StaticMutex a non-static member; use a plain Mutex member, and keep static StaticMutex for file-scope guards.
---

# U++ synchronization primitives

## Rules

- `StaticMutex` as a non-static class member is uninitialized before C++20
  (`StaticPrimitive_::once`). Use `Mutex` for members.
- `StaticMutex` belongs at file or function scope, where static initialization makes
  it usable.
- Lock with a scoped guard: `Mutex::Lock hold(lock);`.
- Multithreading is always compiled in. Do not write `#ifdef MT` guards for it.

## Sources

- Project trap record: `SkylarkManager/tasks/takeover/T00-context-and-rules.md`.
- Project use: `SkylarkManager/uppsrc/ManagerSkylark/PrivateHubService.h` (a `Mutex
  lock` member).

## Verified

- Upstream `ultimatepp/uppsrc/Core/Core.h` defines `_MULTITHREADED` and `MULTITHREADED`
  unconditionally (lines 6-7).
- The `StaticMutex` member trap is recorded from a project defect (T00). Not re-derived here.
