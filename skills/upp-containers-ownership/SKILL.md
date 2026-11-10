---
name: upp-containers-ownership
description: U++ container ownership rules. Vector is move-only; copy it with the tagged deep-copy constructor or clone(); records with Vector members need explicit copy operations.
---

# U++ containers and ownership

## Rules

- `Vector<T>` is move-only. A plain copy does not compile. Make a deep copy with
  `Vector<T>(v, 1)` or copy elements explicitly with `clone(...)`.
- Moving: `Vector(Vector&&)` and `operator=(Vector&&)` pick the source. A picked
  source may only be cleared, destroyed, assigned to, or appended from with `<<=`.
- A record with a `Vector` member needs explicit copy and assignment that clone the
  vector members. Without them, the record copy fails or aliases.

## Pattern

```cpp
struct Account {
	Vector<String> roles;

	Account() {}
	Account(const Account& o, int) : roles(clone(o.roles)) {}   // explicit deep copy
	Account(Account&& o) : roles(pick(o.roles)) {}
};
```

Use `clone(...)` for the members you want duplicated. Do not rely on an implicit copy.

## Sources

- Upstream `ultimatepp/uppsrc/Core/Vcont.h`: `Vector(Vector&&)`, `Vector(const Vector&, int)`.
- Project record pattern: `SkylarkManager/uppsrc/WebAccounts/WebAccounts.h` (copy
  constructor and `operator=` with `clone(...)`).

## Verified

- Read in upstream `Vcont.h`: the move constructor and move assignment are declared,
  and the tagged deep-copy constructor is declared. No plain copy constructor is declared.
- The pattern exists in `WebAccounts.h` (`clone` used for `roles` and `recovery_hashes`).
