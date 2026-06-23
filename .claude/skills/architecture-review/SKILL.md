---
name: architecture-review
description: hypercore's architecture-review methodology — the standing scan that keeps the system deep, surfacing god-files-in-the-making by the length signal against the accepted-length record. Load when assessing structural depth or reading the complexity debt.
---

# architecture-review

The standing scan that keeps the system deep (ADR 0005). It reads the source
tree live for complexity debt and renders two things from one scan: the
**complexity debt** — the engine that surfaces god-files-in-the-making before they
set — and the operator view's **"what the system is" upper levels** — the structural
map of as-built reality, debt marked, read without reading code. The review is not a
separate artifact; its output *is* the operator view's as-built and gap, kept honest
between folds. It consults the same accepted-length record `folding-conditions`
gates with — one criterion (depth, signalled by length) at two scopes: the per-tree gate at
the fold, this standing whole-tree scan.

Depth is **judgment, not a threshold the scan enforces**. The review raises a decision off the length
signal and the mechanical red flags; it never scores or certifies depth, and a green scan means
"length-clean, no dead symbols, no cycles," never "deep." The model-driven module depth judgment — the real
shallow/leakage/deletion-test assessment — is the standing job this review exists to grow and is **not
yet built** (ADR 0006); until it is, the review names that absence rather than passing length off as
depth. This honesty is the point: a regenerating author told the truth will not lean on a depth gate
that does not exist.

## The disciplines — what good looks like

- **the architecture review is a standing scan, read live** — The architecture review MUST scan the source tree live every time it is asked for, never a stored report, and yield a finding for each module past or nearing the length signal — each carrying its subject, its measure, and a recommendation strength. It is a standing process, not a one-off, so the picture is current by construction like every other view.
- **the review surfaces a god-file-in-the-making before it sets** — A module past the length signal with no accepted-length record accepting it MUST surface as strong complexity debt, marked *assess its depth*. A module merely nearing the signal MUST surface as a lighter one. A module past the signal but **within** an accepted-length record's accepted length is not debt. A module that has grown **materially past** the length an accepted-length record once accepted it at (a *stale* acceptance, ADR 0008) MUST return to the backlog, marked as having outgrown its bar. That stale-acceptance finding is distinct from a never-decided over-signal file, so the operator reads the two differently. The measure shipped here is **length** — what a module costs a worker's window, one signal of depth — the same record `folding-conditions` consults at the fold, applied to the whole standing tree. Length raises the finding; it never renders a module depth judgment. Depth is the criterion, not length, and depth is **judgment**: the review surfaces the signal for a judge to weigh, it does not score depth. The mechanical structural red flags a tool can read — dead module-level symbols and circular dependencies — are the only depth-adjacent facts the scan computes (ADR 0020), and they are a narrow subset, not the judgment. The model-driven **red-flag module depth judgment** — the deletion test, the shallow-module and information-leakage judgments, testable-through-the-interface — is **not yet built** (ADR 0006). The review records that absence honestly, here and in the operator's gap, and never fabricates a module depth judgment from length or from the mechanical subset.
- **the review reads the mechanical structural red flags** — The architecture review MUST scan the source tree for the structural red flags a tool can read without judgment — a module-level name used nowhere in the package (dead code) and a pair of modules that depend on each other (a circular dependency, the structural signature of information leakage) — and surface each in the complexity debt beside the length findings, computed live. These are the **mechanical subset** of the red flags (ADR 0020); the model-driven *judgment* — shallow module, information leakage, the deletion test — stays judgment and is recorded as not-yet-built, never fabricated. A newly introduced instance of either rule returns the scan to red, so the standard bites by construction rather than by a reviewer remembering it.
- **the review's output is the operator view's upper levels and the backlog** — The review's output MUST be the operator view's "what the system is" upper levels — the structural map of the modules by length against the signal, debt marked, rendered visually where a picture carries it — and its findings MUST be the complexity debt the operator reads as the gap. Both are derived from the scan, never hand-authored, so the operator reads the current, honest shape of the system at a glance without reading code.

## Going deeper

The full requirements and their scenarios are `spec/architecture-review.md`, this skill's single source.
