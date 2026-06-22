---
name: coherence
description: hypercore's coherence methodology — the archive-gate judgment over a worker's hand-off: check it against the contract at the operator's altitude (not a code review) and against the depth bar, folding on a pass and raising a decision otherwise. Load when integrating or archiving a worker's result.
---

# coherence

The architect's judgment at the archive gate — how it integrates a worker's hand-off without
the worker's raw output ever reaching the operator. *(ADR 0013, carved from `conversation`.)* When a
worker hands a result back, the architect holds it against the contract at the **operator's
altitude** — a coherence check, not a code review — and against the **depth** bar. The raw report
is *input* to that judgment, never output: every operator-facing word is authored fresh, so the
report crosses to the operator through no path. A result that honors the contract folds its
refined delta into the spec — the work leaving the work view in the same act; a result that
does not, or whose material is past the length signal with no depth-decision accepting it, surfaces
as exactly one of two outcomes — a fold, or a **decision** (re-cut / deepen / accept-with-reason /
abandon / change the ask) on the operator's queue. *(ADR 0006.)* The architect's
structural opposition to the worker's investment in its own product is the defense against
self-judging.

## The disciplines — what good looks like

- **the architect integrates the worker's hand-off** — The architect MUST archive a worker's result: coherence-check it against the contract at the operator's altitude — not a code review — and on a pass fold the refined delta into the spec, the work leaving the work view in the same act. The raw report is input to that judgment, never output.
- **the architect judges depth at the archive gate** — The architect MUST hold the design judgment the worker cannot hold over its own product: at the archive gate, a result whose material is past the length signal with no depth-decision accepting it surfaces as exactly one of two outcomes — a fold, or a **depth decision** (re-cut / deepen / accept-with-reason) on the operator's queue. *(ADR 0006.)* Depth surfaces to the operator as a decision rather than hiding in a number, so the operator reads the system's depth; the architect's structural opposition to the worker's investment in its own product is the defense against self-judging.

## Going deeper

The full requirements and their scenarios are `spec/coherence.md`, this skill's single source.
