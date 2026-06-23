# coherence
<!-- vision: coherence -->

The architect's judgment at the archive gate — how it integrates a worker's hand-off without
the worker's raw output ever reaching the operator. *(ADR 0013, carved from `communication`.)* When a
worker hands a result back, the architect holds it against the contract at the **operator's
altitude** — a coherence check, not a code review — and against the **depth** bar. The raw report
is *input* to that judgment, never output: every operator-facing word is authored fresh, so the
report crosses to the operator through no path. A result that honors the contract folds its
refined delta into the spec — the work leaving the work view in the same act; a result that
does not, or whose material is past the length signal with no accepted-length record accepting it, surfaces
as exactly one of two outcomes — a fold, or a **decision** (re-cut / deepen / accept-with-reason /
abandon / change the ask) on the operator's queue. *(ADR 0006.)* The architect's
structural opposition to the worker's investment in its own product is the defense against
self-judging.

### Requirement: the architect integrates the worker's hand-off
The architect MUST archive a worker's result: coherence-check it against the
contract at the operator's altitude — not a code review — and on a pass fold the refined
delta into the spec, the work leaving the work view in the same act. The raw report is
input to that judgment, never output.

#### Scenario: coherence decides the fold
- WHEN a worker hands a result back
- THEN a result that honors the contract folds its delta and integrates, and a result that
  does not raises a decision (re-cut, abandon, or change the ask) rather than folding

### Requirement: the architect judges depth at the archive gate
The architect MUST hold the design judgment the worker cannot hold over its own product: at
the archive gate, a result whose material is past the length signal with no accepted-length record
accepting it surfaces as exactly one of two outcomes — a fold, or a **decision** (re-cut /
deepen / accept-with-reason) on the operator's queue. *(ADR 0006.)*
Depth surfaces to the operator as a decision rather than hiding in a number, so the operator
reads the system's depth; the architect's structural opposition to the worker's investment in
its own product is the defense against self-judging.

#### Scenario: a shallow-or-long result reaches the gate
- WHEN a worker hands back material past the length signal with no accepted-length record accepting it
- THEN the architect raises a decision (re-cut / deepen / accept-with-reason) and the
  fold is held — the depth surfaces to the operator, not a length number's verdict
