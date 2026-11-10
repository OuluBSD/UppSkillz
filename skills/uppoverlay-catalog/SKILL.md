---
name: uppoverlay-catalog
description: Cataloging, registering, and resolving decoupled U++ packages in the OuluBSD/UppOverlay catalog using CapitalCase categories, U++ Esc-syntax .escbuild specifications, Portage target profiles, and virtual capability mappings.
---

# UppOverlay Package Catalog & Portage Integration

## Rules

- **Central Package Catalog**: All decoupled U++ repositories and modern packages are indexed centrally in [`OuluBSD/UppOverlay`](https://github.com/OuluBSD/UppOverlay). Agents must query and register packages in this repository.
- **CapitalCase Taxonomy**: Categories and package names strictly follow `CapitalCase` (e.g. `DevCpp/BazaarCore`, `DevUtil/UppBuilder`, `Virtual/Sqlite`, `MediaSound/SoftAudio`), replacing legacy lower-case-with-hyphens.
- **Esc Language Specifications (`.escbuild`)**: Ebuild specifications use U++'s native Esc language syntax and the `.escbuild` file extension (never Unix shell `.ebuild`).
- **Standard Metadata Fields**: Every `.escbuild` must define:
  - `DESCRIPTION = "..."`
  - `HOMEPAGE = "..."`
  - `GIT_REPO = "..."`
  - `GIT_BRANCH = "main"`
  - `IUSE = [ "..." ]`
  - `ACCEPTFLAGS = [ "..." ]`
- **Virtual Capability Providers (`Virtual/*`)**: External dependencies are specified via virtual capability packages mapping to host providers:
  - Windows: `windows-vcpkg` (e.g. `"sqlite3:x64-windows"`)
  - Ubuntu/Debian: `posix-apt` (e.g. `"libsqlite3-dev"`)
  - macOS: `posix-brew` (e.g. `"sqlite"`)
  - Internal fallback: `upp-plugin` (e.g. `"plugin/sqlite"`)
- **Simultaneous Target Profiles**: Multiple target profiles (`NativeClang`, `NativeGcc`, `MsvcX64`, `WasmBrowser`) are supported with inheritance from `profiles/base/make.conf` and target overrides in `profiles/targets/<target>/make.conf`.
- **Shared Global Build Cache**: Compilation caches intermediate objects globally at `~/.cache/upp.out` on POSIX and `%LOCALAPPDATA%/u++/out` on Windows, matching TheIDE's canonical `GetDefaultUppOut()`.

## CLI Workflow with UppBuilder

Agents interact with the overlay through `UppBuilder`:

```bash
# List all registered packages across categories:
uppbuilder overlay list

# Inspect detailed package metadata from .escbuild:
uppbuilder overlay info DevCpp/BazaarCore
uppbuilder overlay info Virtual/Sqlite

# Synchronize local overlay copy with remote git:
uppbuilder overlay sync

# List available target profiles:
uppbuilder profile list

# Show profile configuration details:
uppbuilder profile show NativeClang

# Resolve virtual package to host platform install command:
uppbuilder virtual resolve Virtual/Sqlite

# Build with active target profile:
uppbuilder TargetPackage --profile NativeClang
```

## Creating a New Package Specification

Place new `.escbuild` files at `UppOverlay/<Category>/<Package>/<Package>-<Version>.escbuild`:

```esc
DESCRIPTION = "Example decoupled U++ library";
HOMEPAGE = "https://github.com/OuluBSD/ExampleLib";
GIT_REPO = "https://github.com/OuluBSD/ExampleLib.git";
GIT_BRANCH = "main";
UPP_ASSEMBLY = "uppsrc";
DEFAULT_PKG = "ExampleLib";

IUSE = [ "blitz", "debug", "gui", "posix", "win32" ];
ACCEPTFLAGS = [ "GUI", "POSIX", "WIN32", "DEBUG" ];
RDEPEND = [ "DevCpp/BazaarCore", "Virtual/Sqlite" ];

src_unpack() {
    git_clone(GIT_REPO, GIT_BRANCH);
}

src_compile() {
    uppbuilder(DEFAULT_PKG);
}

src_install() {
    install_binaries();
}
```

## Adding a Virtual Capability Provider

Virtual packages live under `UppOverlay/Virtual/<Name>/<Name>-<Version>.escbuild`:

```esc
DESCRIPTION = "Virtual capability provider for SQLite3";
HOMEPAGE = "https://www.sqlite.org/";

PROVIDERS = {
    "windows-vcpkg": "sqlite3:x64-windows",
    "posix-apt":     "libsqlite3-dev",
    "posix-brew":    "sqlite",
    "upp-plugin":    "plugin/sqlite"
};
```
