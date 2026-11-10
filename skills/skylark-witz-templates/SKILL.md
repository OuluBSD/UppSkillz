---
name: skylark-witz-templates
description: Writing Skylark witz templates. Escaping is on by default; $raw is for trusted static markup only; loop and directive lines add newlines; $var directly before $else, $endif, $ or . needs care; a template ending in a bare $endif adds a blank line.
---

# Skylark witz templates

## Rules

- Witz escapes values by default. Use `$raw(...)` only for trusted, static markup. Never
  wrap user input in `$raw`.
- `$for(x in list) ... $else ... $endfor` iterates a `ValueArray` or `ValueMap`. The
  `$else` branch runs when nothing iterates. `$/` closes a block as an alternative to
  `$endfor` and `$endif`.
- A `$for(...)` or other directive on its own line emits the line terminator. Put a
  loop body on lines that are meant to produce output, or accept an extra newline per row.
- `$var` directly before `$else`, `$endif`, `$`, or `.` does not evaluate as expected.
  Put a space or a separate expression between them, and check the rendered output.
- A template ending in a bare `$endif` adds a blank line at the end of the output.
- Member access such as `$c.msg` works.
- Set `use_caching = false` during development, or template edits do not show.

## Example

```witz
$for(c in candidates)
  <li>$c.title</li>
$else
  <li>No candidates.</li>
$endfor
```

## Sources

- Upstream `BazaarCore/uppsrc/Skylark/src.tpp/Witz_en-us.tpp`: `$for`, `$else`,
  `$endif`, `$/`, and `raw(text)` (documented as text that is not escaped).
- Project findings, recorded by the worker when the templates were built:
  `SkylarkManager/tasks/takeover/WORKER-LOG.md` ("Witz findings", brief 09B, and
  "Witz findings added this brief"). The same findings are in the ManagerSkylark AGENTS guidance.

## Verified

- The `$for`/`$else`/`$endif`/`$/` syntax and `raw(text)` are read in the upstream witz
  reference.
- The line-join, `$var`-before-delimiter, and trailing-`$endif` findings are the
  project's recorded test results. They are not re-derived here. Re-check them against a
  rendered output before relying on the exact whitespace.
