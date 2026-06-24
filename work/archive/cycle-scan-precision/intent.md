---
kind: ask
state: done
owner: operator
created: 2026-06-24
---
# cycle-scan-precision — the import-cycle scan must not forge a false cycle from a symbol/module name clash

Surfaced by `handoff-format`: naming a transport function `render` made the architecture-review's
import-cycle scan report two false circular dependencies (`communication ↔ render`,
`grill ↔ render`). The cause is in `review._sibling_imports` — it read **every imported name** as a
graph edge, so `from .transport import render` (importing the *symbol* `render`) forged an edge to the
`render` *module*, which imports those callers back. A safely preventable false positive is just a
bug.

The fix: the dependency edge of `from .x import y` is the module `x` it names, never the symbols it
binds; only `from . import a, b` names sibling modules directly, so only its names are edges. Real
two-module cycles are unaffected — they are always carried by the module edge either form produces.

## folding condition
- `review._sibling_imports` keys a `from .x import y` edge on the module `x`, not on the imported
  symbol names; `from . import …` still names sibling modules;
- `spec/architecture-review.md` carries a gated scenario (`symbol-clash`) proving a symbol whose name
  matches a sibling module raises no circular-dependency flag, beside the unchanged genuine-cycle
  scenario;
- `python3 -m engine --check` green (the real engine tree, which now has the colliding shape via the
  worlds importing `instruction`/`read`/etc. from transport, scans clean).
