# HISTORY

Provenance for each UppSkillz item. Source paths are under `~/Dev/ai-upp/ai/` unless
stated otherwise. Verdicts: **adapted** (rewritten, stale parts fixed), **new**
(no direct historical source; written from project traps and checked code).

| Skill | Source | Verdict | Date | Notes |
|---|---|---|---|---|
| upp-containers-ownership | `rules/movable-and-ownership.md`, `skills/memory-safe-containers.md`; T00 traps | adapted | 2026-11-10 | Vector move-only rule checked in upstream Vcont.h |
| upp-value-json | `skills/upp-value.md`; T00 traps | adapted | 2026-11-10 | JSON helpers checked in upstream JSON.h |
| upp-sync-primitives | T00 traps; `Core.h` | new | 2026-11-10 | MT-always rule (stale "MT required" text dropped) |
