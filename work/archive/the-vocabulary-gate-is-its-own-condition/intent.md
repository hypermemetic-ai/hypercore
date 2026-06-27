---
kind: ask
state: done
owner: operator
created: 1782576911
---
The vocabulary gate is its own condition — extract the glossary-consistency check out of folding-conditions into its own module, called the way every other condition already is.

`conditions.py` is "the folding conditions," but a ~77-line glossary-consistency gate is inlined inside it (conditions.py:149-225) — a different body of knowledge entirely: glossary headword format, term-usage set-difference, corpus assembly from `intent.md` and `spec/`. Three tells mark it a bolt-on, not a member. The module's own opening docstring enumerates the conditions and never mentions vocabulary (conditions.py:1-42). `material_unmet`'s docstring lists three things while its body returns a fourth (conditions.py:81-91). And `_vocabulary(result, root, node)` uses neither `result` nor `node` (conditions.py:159) — dead parameters carried only to mimic the sibling-gate signature, when the check needs only `root`. Every other condition lives in its own module and is *called* — the scenario gate in `scenario.py`, provenance in `provenance.py` (conditions.py:78,92), the delta check in `delta.py` (conditions.py:96) — vocabulary alone is inlined, breaking the codebase's own one-module-per-condition pattern. This is `spec/depth.md`'s special-general mixture verbatim: a special concern embedded in the general gate where its peers each got a module.

Build it so the pattern holds with no exception. Extract the vocabulary/glossary-consistency gate (conditions.py:149-225) into `vocabulary.py`, and have `material_unmet` call it the way it already calls `provenance` and `delta.check`. Drop the dead `result`/`node` parameters the gate-shape forced onto a check that needs only `root`. `conditions.py` then coheres around one thing — the length/depth signal and its accepted-length ledger — matching the docstring the authors already wrote.

To surface in grilling: whether `vocabulary.py` owns only the gate or also the glossary-corpus assembly it reads (the `intent.md`/`spec/` traversal), so no second corpus reader appears; whether the new module is a folding condition only or also feeds a standing scan (the vocabulary watched-half is "held not-yet" at conditions.py:159-178, and a standing vocabulary read would mirror the architecture review's shape); and that the extraction ADDs a requirement to the touched capability rather than co-modifying the folding-conditions requirement, so it composes with any concurrent fence on `conditions`.
