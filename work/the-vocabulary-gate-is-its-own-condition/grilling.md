surfaced: 2

[Q] Does vocabulary.py own only the gate, or also the glossary-corpus assembly it reads (the intent.md/spec traversal)?
lean: Own the corpus reader too, so no second corpus reader appears.
flip: A second consumer of the same corpus assembly already lived elsewhere — then the reader would belong in a shared lower leaf, not in vocabulary.py.
answer: Resolved by the architect — a depth/locality call with no operator stake: vocabulary.py owns the WHOLE check, the glossary/intent/spec corpus assembly included. One module, one reader; nothing outside it learns how the corpus is assembled.

[Q] Is the new module a folding condition only, or does it also feed a standing scan (mirroring the architecture review's shape)?
lean: Folding-condition only this pass; leave the standing-scan mirror to its own ask.
flip: A standing vocabulary read were already specced and waiting — then mirror it now to avoid a second extraction.
answer: Resolved by the architect — a scope call with no operator stake: folding-condition only. The watched semantic half stays held-not-yet exactly as today, and any standing vocabulary scan is left to its own ask, so this crossing is a behavior-preserving extraction and nothing more.

[CONTRACT]
The vocabulary / glossary-consistency gate, today inlined in `conditions.py` against the codebase's own one-module-per-condition pattern, becomes its own module `vocabulary.py`. The new module owns the WHOLE check — its glossary-corpus assembly (the glossary, intent.md, and spec traversal) included — so no second corpus reader appears, and it takes only the live corpus root it needs, with the dead `result`/`node` parameters a shared sibling-gate signature forced onto it dropped. `material_unmet` composes the vocabulary condition by CALLING it, exactly as it already calls `provenance` and `delta.check`, and its own public signature is unchanged. The vocabulary check stays a folding condition only this pass — its watched semantic half remains held-not-yet, and no standing scan is added. `conditions.py` is left cohering around one thing — the length/depth signal and its accepted-length ledger — matching the docstring its authors already wrote. The extraction is behavior-preserving and proven red→green: a new folding-conditions requirement adds a scenario whose check is red at the fork base (the dedicated module is absent) and green at the tip (the gate's vocabulary verdict is produced by the module it now calls), so the one-module-per-condition pattern holds with no inlined exception.

[DELTA]
# delta — the vocabulary gate is its own condition

## ADDED — folding-conditions
### Requirement: the vocabulary check is its own condition module
The vocabulary / glossary-consistency check MUST live in its **own module** and be **called** by the
folding gate exactly as the depth, provenance, and delta conditions are — one module per condition, with
no inlined exception. The gate module composes the vocabulary condition by calling it the same way
`material_unmet` already calls `provenance` and `delta.check`; the gate module MUST NOT carry the check's
body. The extracted module owns the **whole** check — the glossary-corpus assembly it reads (the
glossary, intent.md, and the spec traversal) included — so no second corpus reader appears, and the
check takes only the live **corpus root** it needs, never the dead sibling-gate parameters a shared
signature forced onto a check that reads only the corpus. The vocabulary condition is a **folding
condition only**: its watched semantic half stays held-not-yet and no standing scan is added this pass.
The gate module then coheres around the length/depth signal and its accepted-length ledger alone,
matching its own docstring.

#### Scenario: the vocabulary guard is reached as its own module
- WHEN a fold runs the folding conditions over a corpus whose glossary defines a term the corpus no
  longer uses
- THEN the vocabulary guard's verdict is produced by the dedicated vocabulary module the gate **calls** —
  a sibling of the depth and provenance conditions, absent from the gate module's own body — and that
  verdict still holds the fold naming the orphaned term, so the one-module-per-condition pattern holds
  with no inlined exception

  ```check
  orphan glossary-term widget
  vocabulary is-its-own-module
  gate held because vocabulary names widget
  ```
