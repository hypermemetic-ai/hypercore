---
kind: ask
state: done
owner: operator
created: 1782360151
---
The model-driven depth scan — build the standing module-depth judgment the system names everywhere as not-yet-built.

hypercore's foundational standard is depth (deep modules, Ousterhout), but its *automated* enforcement is only the mechanical subset: the architecture review computes the length signal and the two tool-readable red flags (dead module-level symbols, import cycles), and honestly names the model-driven verdict — is this module actually shallow? — as not built (`spec/depth.md`, `spec/architecture-review.md`, `spec/self-model.md`, `glossary.md`, and `review.py`'s `DEPTH_NOT_YET`, emitted on every scan). Depth-as-judgment is exercised at the coherence archive gate and held on the worker every episode, but there is no standing, whole-tree, automated assessment of shallowness, information leakage, or the deletion test. The honesty line is load-bearing and correct — the system refuses to fabricate a depth score it cannot compute — but nothing in the tree builds the judgment, so "not yet built" can read forever.

Build the model-driven red-flag depth scan: a standing assessment that reads the source tree for the depth red flags a tool cannot judge but a model can — a shallow module (little behavior behind its interface), information leakage (a design decision smeared across modules, past the mechanical cycle), a module that fails the deletion test — and surfaces each as complexity debt in the operator's gap, beside the length and mechanical findings the review already shows. It raises a finding for a judge to weigh; it never scores or certifies depth, and never a gameable metric (the clarity/length-signal discipline applied to depth). On completion the architecture review's unconditional not-yet-built line is replaced by the built scan, and `depth.md` / `architecture-review.md` / `self-model.md` / `glossary.md` stop naming the absence.

To surface in grilling: whether the verdict is watched evidence (a model judgment no deterministic fixture can certify — likely a dedicated run leaving a trace the fold checks for presence, the way vocabulary-check's watched half does) rather than a gated check; whether it runs only in the standing whole-tree scan or also as a per-fold folding condition; how it composes with the existing review (`engine/review.py`) and the per-fold depth condition (`engine/conditions.py`) with no second copy of the depth standard to drift; and how a model judgment stays cheap enough to run live (the tree fits a context window).
