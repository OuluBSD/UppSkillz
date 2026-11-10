---
name: upp-build-packaging
description: Building U++ packages with uppbuilder. Multithreading is always on, so do not add MT mainconfigs; keep mainconfig only for packages that build a standalone main behind flagMAIN; use INITBLOCK_(Name) for module init; build across repos with -a.
---

# U++ build and packaging

## Rules

- Multithreading is always compiled in. Do not add `MT` to a mainconfig and do not
  guard code with an MT flag. A mainconfig that only sets `MT` is stale.
- Keep a `mainconfig` only for a package that also builds a standalone executable.
  Guard the entry point with `#ifdef flagMAIN`, so the library build does not get it.
  The package's mainconfig then applies to both builds.
- Module initialization uses `INITBLOCK` in the package's own unit, or `INITBLOCK_(Name)`
  when the name must be stable (a named descriptor for a host to find).
- Keep `.upp` file lists grouped with separators. A `readonly separator` marks a group
  of files that are not built into the package.
- Build a package that depends on sibling repos with `-a` assembly roots:

  ```sh
  uppbuilder CompanySkylark -a ../SkylarkManager/uppsrc -v
  uppbuilder -m CLANG -a ../CompanySkylark/uppsrc ManagerSkylark -v
  ```

- Build and run from the assembly, not from a monorepo `bin/build` wrapper.

## Sources

- Upstream `ultimatepp/uppsrc/Core/Defs.h`: `INITBLOCK` and `INITBLOCK_(x)`.
- Project examples: `CompanySkylark/uppsrc/CompanySkylark/main.cpp` (flagMAIN entry),
  `CompanySkylark/uppsrc/CompanySkylark/CompanyModule.cpp` (`INITBLOCK_(CompanySkylark)`),
  `CompanySkylark/AGENTS.md` (build commands).
- Historical, superseded: `ai-upp/ai/skills/build-upp-package.md` describes a `bin/build`
  wrapper and `stdsrc/` bootstrap. Not migrated.

## Stale guidance dropped

- "MT required" in package guidance (multithreading is unconditional now).
- `bin/build` and `stdsrc/**` monorepo paths (replaced by the uppbuilder assembly model).

## Verified

- `INITBLOCK` and `INITBLOCK_(x)` exist in upstream `Defs.h` (lines 100-104).
- `main.cpp` in CompanySkylark is guarded by `#ifdef flagMAIN`, and its package keeps
  a mainconfig, as the comment there states.
- `INITBLOCK_(CompanySkylark)` is used in `CompanyModule.cpp`.
- The `-a` commands match CompanySkylark `AGENTS.md`.
- Known project issue, not changed here: `CompanySkylark.upp` still declares
  `mainconfig "" = "MT";`. Planner decision needed (recorded in the step-0 backlog work).
