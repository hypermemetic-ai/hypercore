# architecture-review

The standing scan that keeps the system deep (rebuild-spec §7.4). It reads the source
tree live for deepening opportunities and renders two things from one scan: the
**deepening backlog** — the engine that surfaces god-files-in-the-making before they
set — and the operator view's **"what the system is" upper levels** — the structural
map of as-built reality, debt marked, read without reading code. The review is not a
separate artifact; its output *is* the operator view's as-built and gap, kept honest
between folds. It consults the same line-count budget `folding-conditions` gates with —
one budget at two scopes: the per-graph gate at the fold, this standing whole-tree scan.

### Requirement: the architecture review is a standing scan, read live
The architecture review MUST scan the source tree live every time it is asked for, never
a stored report, and yield a finding for each module over or nearing the line-count budget
— each carrying its subject, its measure, and a recommendation strength. It is a standing
process, not a one-off, so the picture is current by construction like every other view.

#### Scenario: the scan runs
- WHEN the review is read
- THEN it measures every source module fresh and yields, for each over or nearing the
  budget, a finding with its line count and a recommendation strength, computed live

### Requirement: the review surfaces a god-file-in-the-making before it sets
A module over the budget without a decision record justifying it MUST surface as a strong
deepening opportunity; a module nearing the budget surfaces as a lighter one; a module over
the budget but named in a decision record is not debt. The measure is length — what a module
costs a worker's window — the same budget and escape hatch `folding-conditions` enforces at
the fold, applied here to the whole standing tree. The deeper structural judgments the review
is meant to grow — the deletion test, seam analysis, testable-through-the-interface — are not
yet built; that shallowness is recorded here rather than fabricated into the operator's gap.

#### Scenario: a god-file in the making
- WHEN a source file crosses the budget with no decision naming it
- THEN the review flags it as a strong deepening opportunity, and a file merely nearing the
  budget as a lighter one

#### Scenario: a justified module
- WHEN a source file over the budget is named in a decision record justifying its size
- THEN it is not in the deepening backlog, though the structural map still shows it, marked

### Requirement: the review's output is the operator view's upper levels and the backlog
The review's output MUST be the operator view's "what the system is" upper levels — the
structural map of the modules against the budget, debt marked, rendered visually where a
picture carries it — and its findings MUST be the deepening backlog the operator reads as the
gap. Both are derived from the scan, never hand-authored, so the operator reads the current,
honest shape of the system at a glance without reading code.

#### Scenario: the operator reads the map
- WHEN the operator opens the operator view
- THEN the root renders the visual structural map of as-built reality (debt marked) and the
  deepening backlog, both derived from the review, with no source code read
