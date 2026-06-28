surfaced: 0

[CONTRACT]
The model-driven depth scan becomes a BUILT, WATCHED mechanism. A new shared depth-assessment seam (engine/depth_scan.py) holds the one place the model-driven depth judgment is computed: it is handed the architecture review's already-computed structural map (it CONSULTS that map, it never walks the tree a second time) and a target set, and returns a model-judged assessment of the depth red flags a tool cannot read but a model can, each carrying a lean and a flip. The verdict stays watched (no fixture certifies whether a module is actually shallow; the run leaves a verdict trace whose presence is its trail); the seam's structure is gated. The architecture review's standing gap no longer reads the unconditional 'not yet built' line — it reads the built scan.

BUILD GUIDANCE (machine-facing, load-bearing — a prior build broke self-model on merged main):
(1) DETERMINISM IS NON-NEGOTIABLE. review.gap(), review.complexity_debt(), review.backlog(), review.bars(), and EVERY view-render path MUST stay deterministic — they MUST NOT call a live model / the depth_scan assessment. self-model's gated scenarios (gap, gap-split, debt, structure) assert byte-exact equality on the view's gap and complexity_debt, and the whole-system re-verify runs them on merged main; a live model call in a render makes two calls differ and turns self-model RED, refusing the fold. The model is invoked ONLY inside the dedicated depth_scan run.
(2) MINIMAL review.py change: repurpose the existing review.DEPTH_NOT_YET constant's TEXT (keep the name — the architecture-review 'clean'/'circular dependency' scenarios assert the constant is in the backlog) from 'not yet built' to the built-watched statement, and keep review.gap() returning it. Leave review.complexity_debt()/review.bars() byte-identical to today UNLESS you surface depth findings by reading the COMMITTED depth-scan verdict trace (a deterministic file read, empty until a run commits one) — never a live model call.
(3) The three gated checks (depth-scan built / consults-map / finding-has-lean-flip) must transition red->green: implement _v_depth_scan in engine/worlds/architecture_review_world.py, lazily importing engine.depth_scan INSIDE the verb (absent at the fork base -> red, present at the tip -> green). Drive depth_scan.assess with a SCRIPTED transport in the world verb (deterministic).
(4) Keep engine/depth_scan.py a DEEP module WITHIN the 400-line length signal; do NOT hand-append an accepted-length record (a hand-appended one is a forged provenance trail that refuses the fold).
Scope note: the fold lands spec requirement-blocks and engine code; descriptive prose in spec preambles, glossary.md, and the self-model render body sits outside the fold's reach (doc-tidy).

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
