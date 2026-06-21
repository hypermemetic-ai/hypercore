# architecture-review

The standing scan that keeps the system deep (rebuild-spec §7.4). It reads the source
tree live for deepening opportunities and renders two things from one scan: the
**deepening backlog** — the engine that surfaces god-files-in-the-making before they
set — and the operator view's **"what the system is" upper levels** — the structural
map of as-built reality, debt marked, read without reading code. The review is not a
separate artifact; its output *is* the operator view's as-built and gap, kept honest
between folds. It consults the same structured depth-decision record `folding-conditions`
gates with — one criterion (depth, signalled by length) at two scopes: the per-graph gate at
the fold, this standing whole-tree scan.

### Requirement: the architecture review is a standing scan, read live
The architecture review MUST scan the source tree live every time it is asked for, never
a stored report, and yield a finding for each module past or nearing the length signal
— each carrying its subject, its measure, and a recommendation strength. It is a standing
process, not a one-off, so the picture is current by construction like every other view.

#### Scenario: the scan runs
- WHEN the review is read
- THEN it measures every source module fresh and yields, for each past or nearing the
  length signal, a finding with its line count and a recommendation strength, computed live

### Requirement: the review surfaces a god-file-in-the-making before it sets
A module past the length signal with no depth-decision accepting it MUST surface as a strong
deepening opportunity — assess its depth; a module nearing the signal surfaces as a lighter
one; a module past the signal but accepted by a structured depth-decision is not debt. The
measure shipped here is **length** — what a module costs a worker's window, one signal of
depth — the same record `folding-conditions` consults at the fold, applied to the whole
standing tree. **Depth is the criterion, not length**: the deeper, model-driven **red-flag
depth scan** — the deletion test, the shallow-module and information-leakage flags,
testable-through-the-interface — is the assessment this review is meant to grow, and is **not
yet built** (slice 7, F1). That shallowness is recorded here and in the operator's gap, never
fabricated into a depth verdict.

#### Scenario: a god-file in the making
- WHEN a source file crosses the length signal with no depth-decision accepting it
- THEN the review flags it as a strong deepening opportunity (assess its depth), and a file
  merely nearing the signal as a lighter one

#### Scenario: a depth-accepted module
- WHEN a source file past the signal is named in a structured depth-decision accepting it
- THEN it is not in the deepening backlog, though the structural map still shows it, marked

### Requirement: the review's output is the operator view's upper levels and the backlog
The review's output MUST be the operator view's "what the system is" upper levels — the
structural map of the modules by length against the signal, debt marked, rendered visually
where a picture carries it — and its findings MUST be the deepening backlog the operator reads
as the gap. Both are derived from the scan, never hand-authored, so the operator reads the current,
honest shape of the system at a glance without reading code.

#### Scenario: the operator reads the map
- WHEN the operator opens the operator view
- THEN the root renders the visual structural map of as-built reality (debt marked) and the
  deepening backlog, both derived from the review, with no source code read
