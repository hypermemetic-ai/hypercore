# architecture-review

The standing scan that keeps the system deep. It reads the source
tree live for complexity debt and renders two things from one scan: the
**complexity debt** — the engine that surfaces god-files-in-the-making before they
set — and the operator view's **"what the system is" upper levels** — the structural
map of as-built reality, debt marked, read without reading code. The review is not a
separate artifact; its output *is* the operator view's structure and complexity debt, kept honest between
folds. It consults the same accepted-length record `folding-conditions`
gates with — one criterion (depth, signalled by length) at two scopes: the per-tree gate at
the fold, this standing whole-tree scan.

Depth is **judgment, not a threshold the scan enforces**. The review raises a decision off the length
signal and the mechanical red flags; it never scores or certifies depth, and a green scan means
"length-clean, no dead symbols, no cycles," never "deep." The model-driven module depth judgment — the real
shallow/leakage/deletion-test assessment — is the standing job this review exists to grow and is **not
yet built**; until it is, the review names that absence rather than passing length off as
depth. This honesty is the point: a regenerating author told the truth will not lean on a depth gate
that does not exist.

### Requirement: the architecture review is a standing scan, read live
The architecture review MUST scan the source tree live every time it is asked for, never
a stored report, and yield a finding for each module past or nearing the length signal
— each carrying its subject, its measure, and a recommendation strength. It is a standing
process, not a one-off, so the picture is current by construction like every other view.

#### Scenario: the scan runs
- WHEN the review is read
- THEN it measures every source module fresh and yields, for each past or nearing the
  length signal, a finding with its line count and a recommendation strength, computed live

  ```check
  module helper.py within-signal
  module facade.py past-signal
  scan measures helper.py
  scan measures facade.py
  debt facade.py strong
  ```

### Requirement: the review surfaces a god-file-in-the-making before it sets
A module past the length signal with no accepted-length record accepting it MUST surface as strong
complexity debt, marked *assess its depth*. A module merely nearing the signal MUST surface as
a lighter one. A module past the signal but **within** an accepted-length record's accepted length
is not debt. A module that has grown **materially past** the length an accepted-length record once accepted it
at (a *stale* acceptance) MUST return to the backlog, marked as having outgrown its bar.
That stale-acceptance finding is distinct from a never-decided over-signal file, so the operator reads
the two differently. The measure shipped here is **length** — what a module costs a worker's window,
one signal of depth — the same record `folding-conditions` consults at the fold, applied to the whole
standing tree. Length raises the finding; it never renders a module depth judgment. Depth is the criterion,
not length, and depth is **judgment**: the review surfaces the signal for a judge to weigh, it does
not score depth. The mechanical structural red flags a tool can read — dead module-level symbols and
circular dependencies — are the only depth-adjacent facts the scan computes, and they are a
narrow subset, not the judgment. The model-driven **red-flag module depth judgment** — the deletion test, the
shallow-module and information-leakage judgments, testable-through-the-interface — is **not yet built**.
The review records that absence honestly, as wanted-but-not-built gap rather than complexity debt, and
never fabricates a module depth judgment from length or from the mechanical subset.

#### Scenario: a god-file in the making
- WHEN a source file crosses the length signal with no accepted-length record accepting it
- THEN the review flags it as a strong complexity-debt finding (assess its depth), and a file
  merely nearing the signal as a lighter one

  ```check
  module giant.py past-signal
  module rising.py near-signal
  module small.py within-signal
  debt giant.py strong
  debt rising.py consider
  debt small.py none
  ```

#### Scenario: an accepted-length module
- WHEN a source file past the signal is named in an accepted-length record accepting it, and is
  still within that accepted length
- THEN it is not in the complexity debt, though the structural map still shows it, marked

  ```check
  module deep.py past-signal
  accept deep.py @460
  debt deep.py none
  map deep.py accepted
  mark deep.py accepted
  ```

#### Scenario: a module that has outgrown its accepted bar
- WHEN a source file has grown materially past the length an accepted-length record accepted it at
- THEN it returns to the complexity debt as a strong opportunity, the map marks it as having
  outgrown its bar (the decision re-opened), distinct from a never-decided over-signal file

  ```check
  module sprawl.py 800
  accept sprawl.py @460
  debt sprawl.py strong stale 460
  map sprawl.py exceeded
  mark sprawl.py grew re-opened
  ```

### Requirement: the review reads the mechanical structural red flags
The architecture review MUST scan the source tree for the structural red flags a tool can read
without judgment: a module-level name used nowhere in the package (dead code), and a pair of
modules that depend on each other (a circular dependency, the structural signature of information
leakage). The cycle scan reads the dependency *graph*: the edge of a relative `from .x` clause is the
module `x` it names, never the symbols it binds — depending on a name binds you to that name's module,
not to a sibling that merely shares the name — so a name clash never forges a cycle that is not there.
It surfaces each in the complexity debt beside the length findings, computed live.
These are the **mechanical subset** of the red flags; the model-driven *judgment* —
shallow module, information leakage, the deletion test — stays judgment and is recorded as
not-yet-built, never fabricated. A newly introduced instance of either rule returns the scan to
red, so the standard bites by construction rather than by a reviewer remembering it.

#### Scenario: a dead module-level symbol
- WHEN a module-level name is defined but used nowhere in the package
- THEN the scan surfaces it as a dead-symbol red flag in the complexity debt

  ```check
  dead-symbol consumer ORPHAN
  used api value
  flag dead consumer.ORPHAN
  no-flag dead api.value
  ```

#### Scenario: a circular dependency
- WHEN two modules depend on each other
- THEN the scan surfaces the pair as a circular-dependency red flag; a tree with no dead symbols
  and no cycles reports a clean structural scan, not a fabricated judgment

  ```check
  cycle ring_a ring_b
  flag cycle ring_a ring_b
  clean
  ```

#### Scenario: a symbol sharing a module's name is not a false cycle
- WHEN a module binds a symbol by name from a sibling (a `from .x` clause naming `y`), and another
  module sharing that name `y` depends back on it, while no two modules actually depend on each other
- THEN the scan raises no circular-dependency flag — the edge is the clause's module `x`, not the
  symbol's namesake, so a preventable false positive is prevented by construction

  ```check
  symbol-clash
  ```

### Requirement: the review's output is the operator view's upper levels and complexity debt
The review's output MUST be the operator view's "what the system is" upper levels — the
structural map of the modules by length against the signal, debt marked, rendered visually
where a picture carries it — and its findings MUST be the complexity debt the operator reads, distinct
from the wanted-but-not-built gap. Both are derived from the scan, never hand-authored, so the operator
reads the current, honest shape of the system at a glance without reading code.

#### Scenario: the operator reads the map
- WHEN the operator opens the operator view
- THEN the root renders the visual structural map of as-built reality (debt marked) and the
  complexity debt, both derived from the review, with no source code read

  ```check
  view renders-map
  view complexity-debt-derived
  view no-source
  ```

### Requirement: a module declares its layer in the static graph, never behind a deferred import
A module MUST declare its dependencies at module scope so the static import graph shows its true
layer, and MUST NOT defer an import inside a function to dodge a circular dependency. A deferred
import that hides a latent cycle hides the module's real layer from the graph, the one place a layer
should be visible. Shared knowledge two modules both rest on MUST live in a lower leaf they each
import downward, never duplicated and never reached by a back-edge a deferred import conceals, so the
cycle scan is green **by construction** — the graph is acyclic because the seam points one way —
and never by import timing. The accepted-length ledger the depth gate and the provenance gate both
read is such a leaf: each imports it downward, neither defers an import to reach the other, and the
provenance gate's real dependencies are visible at module scope rather than disguising it as a leaf.

#### Scenario: the shared ledger is a lower leaf, each gate's layer visible
- WHEN the engine's static import graph is read over its own source
- THEN the accepted-length ledger is a lower leaf that imports neither the depth gate nor the
  provenance gate
- AND the depth gate and the provenance gate each import that ledger at module scope, downward
- AND the provenance gate is not a static leaf — its real dependencies show at module scope, not
  behind a deferred import
- AND the cycle scan reports no dependency cycle between the depth gate and the provenance gate

  ```check
  layer ledger leaf
  layer depth-gate rests-on-ledger
  layer provenance-gate rests-on-ledger
  layer provenance-gate declares-layer
  layer no-cycle depth-gate provenance-gate
  ```

### Requirement: the model-driven depth scan is a built, watched assessment over the standing map
The model-driven red-flag depth assessment MUST be **built** — no longer recorded as not-yet-built —
as a **watched** mechanism: a model judgment no deterministic fixture can certify, so it leaves a
verdict trace whose presence is its only honest trail, never a fabricated depth score and never a
gameable metric. It is the single place the depth judgment is computed — the **shared
depth-assessment seam** (`engine/depth_scan.py`) — consulted by this standing whole-tree scan and fed,
at the fold, the one flagged file (`a depth-gate trip raises a neighborhood-aware assessment`). The
seam MUST **consult** the standing architecture review's already-computed structural map and complexity
debt rather than walking the source tree a second time: the assessment reads the `Review` it is handed,
so there is no second whole-tree scan and no second copy of the depth standard to drift. Its output is
a model-judged assessment — the depth red flags a tool cannot read but a model can (a shallow module, a
design decision smeared across modules past the mechanical cycle, a module that fails the deletion
test) — each carrying a **lean** (the recommendation) and a **flip** (the one thing that would change
it), returned for the dedicated watched run to trace and for the later committed-trace view path to
surface beside the length and mechanical findings. The review's standing gap MUST no longer carry the
unconditional *not-yet-built* line: the scan is built, its verdict watched. The model verdict itself
stays **watched** — no `#### Scenario:` certifies whether a module is actually shallow — while the seam's
*structure* (it is built, it consults the handed map and never re-scans, it yields a finding carrying a
lean and a flip) is gated below.

#### Scenario: the depth scan is built, watched, and consults the standing map
- WHEN the model-driven depth scan assesses the tree
- THEN the seam reads the structural map the standing review already computed rather than walking the
  tree a second time, returns a model-judged assessment carrying a finding, a lean, and a flip, and the
  review's standing gap no longer reads the unconditional not-yet-built line — the scan is built, its
  verdict watched, never a fabricated score

  ```check
  depth-scan built
  depth-scan consults-map
  depth-scan finding-has-lean-flip
  ```
