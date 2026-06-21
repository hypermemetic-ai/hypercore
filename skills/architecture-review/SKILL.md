---
name: architecture-review
description: hypercore's architecture-review methodology — the standing scan that keeps the system deep, surfacing god-files-in-the-making by the length signal against the depth-decision record. Load when assessing structural depth or reading the deepening backlog.
---

# architecture-review — an architect methodology

The standing scan that keeps the system deep (ADR 0005). It reads the source
tree live for deepening opportunities and renders two things from one scan: the
**deepening backlog** — the engine that surfaces god-files-in-the-making before they
set — and the operator view's **"what the system is" upper levels** — the structural
map of as-built reality, debt marked, read without reading code. The review is not a
separate artifact; its output *is* the operator view's as-built and gap, kept honest
between folds. It consults the same structured depth-decision record `folding-conditions`
gates with — one criterion (depth, signalled by length) at two scopes: the per-graph gate at
the fold, this standing whole-tree scan.

## The disciplines — what good looks like

- **the architecture review is a standing scan, read live** — The architecture review MUST scan the source tree live every time it is asked for, never a stored report, and yield a finding for each module past or nearing the length signal — each carrying its subject, its measure, and a recommendation strength. It is a standing process, not a one-off, so the picture is current by construction like every other view.
- **the review surfaces a god-file-in-the-making before it sets** — A module past the length signal with no depth-decision accepting it MUST surface as a strong deepening opportunity — assess its depth; a module nearing the signal surfaces as a lighter one; a module past the signal but **within** a structured depth-decision's accepted length is not debt. A module that has grown **materially past** the length a depth-decision once accepted it at (a *stale* acceptance, ADR 0008) MUST return to the backlog, marked as having outgrown its bar — distinct from a never-decided over-signal file, so the operator reads the two differently. The measure shipped here is **length** — what a module costs a worker's window, one signal of depth — the same record `folding-conditions` consults at the fold, applied to the whole standing tree. **Depth is the criterion, not length**: the deeper, model-driven **red-flag depth scan** — the deletion test, the shallow-module and information-leakage flags, testable-through-the-interface — is the assessment this review is meant to grow, and is **not yet built** (ADR 0006). That shallowness is recorded here and in the operator's gap, never fabricated into a depth verdict.
- **the review's output is the operator view's upper levels and the backlog** — The review's output MUST be the operator view's "what the system is" upper levels — the structural map of the modules by length against the signal, debt marked, rendered visually where a picture carries it — and its findings MUST be the deepening backlog the operator reads as the gap. Both are derived from the scan, never hand-authored, so the operator reads the current, honest shape of the system at a glance without reading code.

## Going deeper

The full requirements and their scenarios are `spec/architecture-review/spec.md`, this skill's single source.
