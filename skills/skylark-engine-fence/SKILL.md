---
name: skylark-engine-fence
description: Mutation fence for Skylark engine sites. The engine checks Origin against the site's allowed origins and checks a server-side CSRF token on session mutations; POST_RAW skips stock identity checks, so the engine fence is the protection.
---

# Skylark engine fence

## Model

For every mutation (anything other than GET or HEAD), the engine gateway does two checks
before routing:

1. **Origin.** If an `Origin` header is present, its authority must be allowed for the
   site (`EngineSite::OriginAllowed`). A request with a disallowed origin gets 403.
2. **CSRF.** If the request has a session, the `__wf_csrf__` form field (or the
   `x-wf-csrf` header) must equal the session's CSRF token. A mismatch gets 403.

Sessions are per site: each site has its own accounts store and its own cookie name, so
a session from one site does not resolve on another.

## Caveats

- The origin check runs only when an `Origin` header is present. A request with no
  `Origin` header is not refused by that check. The CSRF check still applies when the
  request has a session.
- A mutation with no session has no token to check. Handlers that mutate state must
  require a session themselves (`RequireUser`-style checks).
- Stock Skylark `POST_RAW` handlers skip the stock identity check
  (`BazaarCore/uppsrc/Skylark/Dispatch.cpp`, where non-raw POST verifies
  `__post_identity__`). Engine sites do not depend on that check: the engine fence above
  runs in front of routing.

## Usage

- Put the token in every mutating form: `<input type="hidden" name="__wf_csrf__" value="...">`
  with `r.CsrfToken()`.
- Tests should post the token from a rendered form, as the composed smoke does.

## Sources

- `SkylarkManager/uppsrc/WebEngine/WebEngine.cpp` (gateway mutation fence, lines 154-172).
- `SkylarkManager/uppsrc/WebEngine/Request.cpp` (`EnsureSession`, `AdoptSession`, `CsrfToken`).
- `SkylarkManager/uppsrc/WebEngine/Site.cpp` (`OriginAllowed`).
- `BazaarCore/uppsrc/Skylark/Dispatch.cpp` (POST identity check, POST_RAW).

## Verified

- Read in the gateway: the origin check and the CSRF check, with their conditions.
- Read in Dispatch.cpp: the identity check is skipped for `post_raw` handlers.
- The composed smoke checks that a mutation without the token is refused (403).

Provenance: [HISTORY.md](../../HISTORY.md).
