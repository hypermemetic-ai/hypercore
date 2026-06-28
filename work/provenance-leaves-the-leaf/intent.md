---
kind: ask
state: in flight
owner: operator
created: 1782576911
---
Provenance leaves the leaf — extract the ledger primitive that `conditions` and `provenance` share into a lower module, so the provenance gate declares its layer at module scope instead of hiding it behind lazy imports.

`provenance` reads as an L0 leaf in the static import graph (out-degree 0), but it is genuinely a top-of-stack folding gate. All four of its engine imports are deferred inside functions (provenance.py:110,175,198,210) to dodge a real bidirectional dependency with `conditions`, whose own `import provenance` is likewise deferred (conditions.py:77,88). The system's no-static-cycles property holds only because of these import-timing band-aids: promote any one of the five deferred imports to module scope and `conditions ↔ provenance` closes into a cycle. The cost is architectural legibility — provenance's true layer (above `conditions`) is invisible to any static reading of the dependency graph, the one place in the whole engine where a module's layer is hidden from the graph rather than shown by it. (A lighter second instance rides nearby: `scenario → delta` is static and correct, while `delta → scenario` is a single deferred back-edge at delta.py:226.)

Build it so the seam is real and visible. Extract the one primitive both modules share — the accepted-length ledger that `conditions.accept` writes and `provenance` re-derives — into a small lower leaf module (`ledger`) that both import downward. Then `provenance` imports `conditions`/`scenario`/`tree` at module scope and lands at its true layer; `conditions → provenance` disappears; and the five deferred `import provenance` sites across `conditions` and the worlds become a real, statically visible dependency.

To surface in grilling: the exact cut of the `ledger` leaf — does it own both the accepted-length record's read and the commit-attest, or only the read with the write staying on `conditions.accept`; whether the `delta ↔ scenario` deferred back-edge (delta.py:226) is dissolved in the same pass or left as one acceptably-localized edge; and that the cycle scan (`review.red_flags`) stays green by construction on the result — the graph is acyclic because the seam points one way, never because an import is deferred.
