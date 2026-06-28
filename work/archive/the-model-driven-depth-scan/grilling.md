surfaced: 0

[CONTRACT]
The model-driven depth scan becomes a BUILT, WATCHED mechanism. A new shared depth-assessment seam (engine/depth_scan.py) holds the one place the model-driven depth judgment is computed: handed the architecture review's already-computed structural map (it CONSULTS that map, never walking the tree a second time) and a target set, it returns a model-judged assessment of the depth red flags a tool cannot read but a model can, each carrying a lean and a flip. The verdict is watched (no fixture certifies whether a module is shallow; the dedicated run leaves a verdict trace whose presence is its trail); the seam's structure is gated. The architecture review's standing gap stops reading the unconditional 'not yet built' line.

BUILD GUIDANCE (machine-facing, LOAD-BEARING — two prior builds broke self-model on merged main by leaking non-determinism into the view-render; follow EXACTLY):
(1) review.py's ONLY permitted change is the VALUE of the DEPTH_NOT_YET string literal — reword it from 'not yet built' to a 'built (watched)' statement. Do NOT change the bodies of review.gap(), review.complexity_debt(), review.backlog(), or review.bars() — gap() already returns the constant, so rewording the literal alone flips the gap line. Do NOT add any import of depth_scan to review.py or view.py. Rationale: self-model's gated scenarios (structure, debt, gap, gap-split) assert BYTE-EXACT equality between the view's render and a fresh review.* call, re-run on merged main by the whole-system re-verify; ANY non-determinism (a live model call) or shape change there turns self-model RED and refuses the fold.
(2) engine/depth_scan.py is a STANDALONE deep module imported by NOTHING on the view-render path (not review.py, not view.py). It is exercised only by its world verb (scripted transport, deterministic) and, in production, its own dedicated run. The model is invoked ONLY there. Keep it WITHIN the 400-line length signal; do NOT hand-append an accepted-length record (a forged trail).
(3) The three gated checks (depth-scan built / consults-map / finding-has-lean-flip) must transition red->green: implement _v_depth_scan in engine/worlds/architecture_review_world.py, lazily importing engine.depth_scan INSIDE the verb (absent at fork base -> red, present at tip -> green); drive depth_scan.assess with a SCRIPTED transport.
Scope note: surfacing the watched run's findings into the live view is a deferred follow-up (it would need the committed-trace path, not a live call); #8 delivers the built seam + the honesty-flip. Spec preambles, glossary.md, and the self-model render body are out-of-fold doc-tidy.

[DELTA]
# delta — the model-driven depth scan is built

## ADDED — architecture-review
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
it), surfaced as complexity debt beside the length and mechanical findings, for a judge to weigh. The
review's standing gap MUST no longer carry the unconditional *not-yet-built* line: the scan is built,
its verdict watched. The model verdict itself stays **watched** — no `#### Scenario:` certifies whether
a module is actually shallow — while the seam's *structure* (it is built, it consults the handed map
and never re-scans, it yields a finding carrying a lean and a flip) is gated below.

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
