surfaced: 0

[CONTRACT]
Provenance leaves the leaf. The accepted-length ledger that the depth gate writes and the provenance gate re-derives is extracted into its own lower leaf module that both import downward, so the engine's import graph finally shows each gate's true layer instead of hiding it behind function-local imports. After the change the provenance gate declares its dependencies at module scope -- it is no longer a phantom L0 leaf -- and the conditions-to-provenance cycle is gone by construction: the graph is acyclic because the shared knowledge sits in a leaf both gates rest on, never because an import is deferred, so the standing cycle scan stays green for a structural reason a reader can see. The accept writer keeps its single-writer commit on the depth gate; the leaf owns only the durable read. No fold verdict changes -- this is a legibility refactor -- and it is gated by a new architecture-review scenario that reads the system's own source and goes red-to-green as the ledger leaf appears. (The lighter delta-to-scenario deferred back-edge nearby is left to its own ask.)

[DELTA]
# delta — provenance leaves the leaf: the shared ledger becomes a lower leaf

## ADDED — architecture-review
### Requirement: a module declares its layer in the static graph, never behind a deferred import that dodges a cycle
A module MUST declare its dependencies at module scope so the static import graph shows its true
layer, and MUST NOT defer an import inside a function to dodge a circular dependency -- a deferred
import that hides a latent cycle hides the module's real layer from the graph, the one place a layer
should be visible. Shared knowledge two modules both rest on MUST live in a lower leaf they each
import downward, never duplicated and never reached by a back-edge a deferred import conceals, so the
cycle scan is green **by construction** -- the graph is acyclic because the seam points one way --
and never by import timing. The accepted-length ledger the depth gate and the provenance gate both
read is such a leaf: each imports it downward, neither defers an import to reach the other, and the
provenance gate's real dependencies are visible at module scope rather than disguising it as a leaf.

#### Scenario: the shared ledger is a lower leaf, each gate's layer visible
- WHEN the engine's static import graph is read over its own source
- THEN the accepted-length ledger is a lower leaf that imports neither the depth gate nor the
  provenance gate
- AND the depth gate and the provenance gate each import that ledger at module scope, downward
- AND the provenance gate is not a static leaf -- its real dependencies show at module scope, not
  behind a deferred import
- AND the cycle scan reports no dependency cycle between the depth gate and the provenance gate

  ```check
  layer ledger leaf
  layer depth-gate rests-on-ledger
  layer provenance-gate rests-on-ledger
  layer provenance-gate declares-layer
  layer no-cycle depth-gate provenance-gate
  ```
