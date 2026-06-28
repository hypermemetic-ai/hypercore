# design decision — the cut of the accepted-length `ledger` leaf [machine]

The load-bearing seam: the new lower leaf both `conditions` (the depth gate) and `provenance` (the
fold-trail gate) import **downward**, so the `conditions ↔ provenance` cycle is acyclic by
construction — the graph points one way — never because an import is deferred. The contest is over
*the cut*: what the leaf owns, where the seam falls, and what stays above it.

The shared primitive is the accepted-length record: `conditions._depth` reads it (`accepted` /
`accepted_at`) to raise the length decision, and `provenance._accepted_length` reads it
(`working_accepted` / `committed_accepted`) to catch a forged, uncommitted acceptance. Today the
record's location, format, git-committed-vs-working semantics, parsing, and the single-writer commit
all live in `conditions.py`, and `provenance` reaches up into `conditions` for the read — the one
back-edge whose deferral disguises provenance as a static L0 leaf.

## the briefed candidates (the contest)

- **minimize the interface — read-only leaf, the write stays on the accept seam**: `ledger` owns
  the durable **read** and nothing else — the record's location (`_ledger`), the parse helpers
  (`_depth_record`, `_accepted_length`, `_ledger_records`, `_committed_ledger`), and the four
  readers (`accepted_at`, `accepted`, `working_accepted`, `committed_accepted`). The
  single-writer commit (`accept` / `accept_length` / `length_decision`) **stays on
  `conditions`**, calling down into the leaf for the path and the ratchet bar. `provenance` and
  `conditions._depth` each read from the leaf; provenance stops importing conditions. Smallest
  read-only interface, write-locality preserved next to the depth gate that raises the decision the
  write settles.
- **maximize cohesion — a full ledger object, read AND write in the leaf**: `ledger` owns both the
  read and the accept-commit; `conditions.accept` becomes a thin forward to `ledger.accept`. One
  module fully owns the record. But it pulls the single-writer commit and the
  card-template producer (`length_decision`, which mirrors the exact template `_depth_decision`
  emits) **away** from the depth gate that raises and settles the length decision, and widens the
  leaf's interface with three write verbs for marginal cohesion gain. The depth-decision ↔ accept
  coupling is real and local today; moving the write down severs it across a seam.
- **optimize the provenance caller — extract only the forge-detection pair**: lift just
  `working_accepted` / `committed_accepted` into a tiny leaf for `provenance`, leave
  `accepted_at` / `accepted` on `conditions`. The leaf and `conditions` would then **both** parse
  the same ledger file and **both** know its location — the record's format and home duplicated
  across two readers. That is information leakage (depth.md's gravest red flag after shallowness):
  the location must change in two places at once. Rejected on depth.

## the pick

design-decision: the cut of the accepted-length ledger leaf → minimize the interface — read-only
leaf, the accept writer stays on the depth gate calling down — because it is the deepest cut (the
leaf hides the record's location, format, git-committed-vs-working semantics, and ratchet parsing
behind a small **read** interface both gates rest on), keeps the single-writer commit local to the
depth gate that raises and settles the length decision (write-locality), and points the seam
strictly downward so the cycle scan is green by construction. Candidate 2 trades that write-locality
and a wider interface for cohesion the read-only cut already has; candidate 3 leaks the record's
location and parse into two readers. This realizes ⚑1's lean.

## build notes (machine-side, for the fenced worker)

- **`engine/ledger.py` (the new leaf)** — owns the durable read only: `_ledger` (the location),
  `_depth_record` / `_accepted_length` (parsing), `_ledger_records` / `_committed_ledger`,
  `accepted_at`, `accepted`, `working_accepted`, `committed_accepted`. Imports only `os` / `re` /
  `subprocess` / `spec` (and `record` is **not** needed — it does not write). It imports **neither**
  `conditions` nor `provenance`: a true lower leaf.
- **`engine/conditions.py`** — `_depth` calls `ledger.accepted` / `ledger.accepted_at`. The writer
  `accept` (and `accept_length`, `length_decision`) **stays here**, calling down to `ledger`
  (`accepted_at` for the ratchet, the leaf's path for the append) under its existing
  `record.transact` single-writer commit. Promote the deferred `from . import provenance` in `unmet`
  / `material_unmet` to **module scope** — provenance no longer imports conditions, so this static
  edge is honest and the cycle scan stays green. `SIGNAL` / `SLACK` stay here (depth-signal, not
  ledger).
- **`engine/provenance.py`** — `_accepted_length` reads `ledger.working_accepted` /
  `ledger.committed_accepted` (was `conditions.*`). Promote the deferred imports of `scenario`
  (in `derived`), `tree` (in `commit_verdict`), and the new `ledger` to **module scope**; **drop**
  the `from . import conditions` import entirely. Provenance now has a real static out-degree — its
  layer is visible.
- **the worlds** — promote the deferred `from .. import provenance` in
  `folding_conditions_world.py` (the `unmet` / `material_unmet` call sites) and `worker_world.py` /
  `design_it_twice_world.py` to module scope where doing so introduces no new module-level cycle (run
  `review.red_flags` to confirm). The sites commented "the brand-new seam — absent at the base" are
  deferred for the scenario gate's base-run reason, **not** the cycle; leave those as they are.
- **the new `layer` verb (`architecture_review_world.py`)** — reads hypercore's own engine source
  under the review's real root (`_REAL`) **by file path**, reusing `review._sibling_imports` and
  `review.red_flags`; the world module must **not** `import ledger` at top level, so at the fork base
  (no `ledger.py`) the verb reports the property **absent** (red) rather than crashing on import. Map
  the domain words inside the verb: `ledger` → `engine/ledger.py`, `depth-gate` →
  `engine/conditions.py`, `provenance-gate` → `engine/provenance.py`. Assertions:
  `leaf` (the module exists and its sibling-imports include neither the depth gate nor the
  provenance gate); `rests-on-ledger` (the named gate's module-scope sibling-imports include
  `ledger`); `declares-layer` (provenance's module-scope sibling-imports are non-empty — not a static
  leaf); `no-cycle <a> <b>` (no `import cycle` red flag pairs the two named modules).
- **left for its own ask (⚑2)** — the `delta ↔ scenario` deferred back-edge (`delta.py`'s
  function-local `from . import scenario` inside `fold`) is **not** touched: it is a separate,
  localized, correct back-edge that does not fall out of this extraction, and the lean is to dissolve
  only the `conditions ↔ provenance` cycle this pass.
