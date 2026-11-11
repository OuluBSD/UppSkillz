# HISTORY

Provenance for each UppSkillz item. Source paths are under `~/Dev/ai-upp/ai/` unless
stated otherwise. Verdicts: **adapted** (rewritten, stale parts fixed), **new**
(no direct historical source; written from project traps and checked code).

| Skill | Source | Verdict | Date | Notes |
|---|---|---|---|---|
| upp-containers-ownership | `rules/movable-and-ownership.md`, `skills/memory-safe-containers.md`; T00 traps | adapted | 2026-11-10 | Vector move-only rule checked in upstream Vcont.h |
| upp-value-json | `skills/upp-value.md`; T00 traps | adapted | 2026-11-10 | JSON helpers checked in upstream JSON.h |
| upp-sync-primitives | T00 traps; `Core.h` | new | 2026-11-10 | MT-always rule (stale "MT required" text dropped) |
| upp-build-packaging | `skills/build-with-uppbuilder.md`, `skills/build-upp-package.md` (superseded `bin/build` section), `rules/upp-flags.md` | adapted | 2026-11-10 | MT-required and bin/build paths dropped; INITBLOCK and -a checked against project code |
| skylark-witz-templates | `ai-upp/ai/skills/skylark-web-ui.md` (witz section); project witz findings (WORKER-LOG) | adapted | 2026-11-10 | Witz reference checked upstream; whitespace findings are recorded test results |
| skylark-engine-fence | `ai-upp/ai/skills/skylark-web-ui.md`; `BazaarCore` Dispatch.cpp | adapted | 2026-11-10 | Origin and CSRF conditions corrected to what the gateway does; POST_RAW caveat stated |
| socket-and-console-hygiene | T00 traps | new | 2026-11-10 | EINPROGRESS and accepted-socket behavior checked in upstream Socket.cpp and Host.cpp |
| uppoverlay-catalog | `OuluBSD/UppOverlay`, `OuluBSD/UppBuilder` Task 09 | new | 2026-11-10 | CapitalCase taxonomy, .escbuild Esc language specs, target profiles, and virtual providers |
| agentipc-channels | `OuluLinux/AgentIPC` `docs/scenarios/skylark-manager.md` (role messages copied verbatim), `agentipc/cli.py`, `daemon.py`, `node.py`, `vserver.py` at `c9c8b3c` | new | 2026-11-11 | Commands checked against `--help` and a two-session run on an encrypted server; control secret and feature gate checked in AgentIPC tests and live |
