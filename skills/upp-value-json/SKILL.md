---
name: upp-value-json
description: U++ Value and JSON pitfalls. Use AsJSON for maps and typed values, not StoreAsJson on a ValueMap; indexing a ValueMap by integer is a key lookup, so use GetValue(i) for position.
---

# U++ Value and JSON

## Rules

- `StoreAsJson(x)` on a `Jsonize` struct gives plain JSON. Wrapping a `ValueMap` or
  using `StoreAsJsonValue` and then `StoreAsJson` gives U++ typed debug JSON
  (`{"key":{"type":...}}`), which parses back as an array. For maps use
  `AsJSON(Value(map))`.
- `ValueMap::operator[](int)` looks up a key. Integer 0 becomes key `"0"`. Positional
  access is `GetValue(i)` and `GetKey(i)`.
- `LoadFromJson` returns false on parse or type errors. Check the result.

## Example

```cpp
ValueMap rec;
rec.Add("payload", payload);
String json = AsJSON(Value(rec));          // plain JSON for a map
Value v = ParseJSON(json);
ValueMap back = v;
Value first = back.GetValue(0);             // positional, not back[0]
```

## Sources

- Upstream `ultimatepp/uppsrc/Core/JSON.h`: `StoreAsJsonValue`, `StoreAsJson`,
  `LoadFromJsonValue`, `LoadFromJson`, `AsJSON` overloads.
- Project trap record: `SkylarkManager/tasks/takeover/T00-context-and-rules.md`
  ("U++ traps"). The `operator[](int)` trap broke schema validation in CompanySkylark.

## Verified

- Read in upstream `JSON.h`: `StoreAsJson` calls `AsJSON(StoreAsJsonValue(var))`,
  and `LoadFromJson` returns false on `ValueTypeError` and `JsonizeError`.
- The `operator[](int)` key behavior is recorded from a project defect (T00), not
  re-derived here.

Provenance: [HISTORY.md](../../HISTORY.md).
