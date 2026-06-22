---
kind: ask
state: folded
owner: operator
created: 2026-06-21
folded: 2026-06-21
---
# depth-regrounding — re-ground the architecture in depth (folded)

Slice 7. The line-count budget was reconsidered against John Ousterhout's *A Philosophy of Software
Design* and the constraint rebuilt around **depth**: length demoted to a context-cost *signal* that
raises a decision, never an auto-refusal; the worker grounded in the depth disciplines every
episode. The faithful synthesis became `spec/depth.md`; the design that got there is its material
here.

## folding condition — met

ADR 0006 records the decision; `spec/depth.md` is the synthesis; slices 1–7 were green at the fold.

## material

- `regrounding.md` — the slice-7 design (the companion to the synthesis, now `spec/depth.md`).
- result: ADR 0006; `spec/depth.md`; the depth gate in `hyper/conditions.py` and `hyper/review.py`.
