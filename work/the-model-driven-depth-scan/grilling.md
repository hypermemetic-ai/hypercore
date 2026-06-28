surfaced: 0

[CONTRACT]
The model-driven depth scan becomes a BUILT, WATCHED mechanism. A new shared depth-assessment seam (engine/depth_scan.py) holds the one place the model-driven depth judgment is computed: it is handed the architecture review's already-computed structural map (it CONSULTS that map, it never walks the tree a second time) and a target set, and returns a model-judged assessment of the depth red flags a tool cannot read but a model can — a shallow module, information leakage past the mechanical cycle, a failed deletion test — each carrying a lean and a flip, surfaced as complexity debt for a judge to weigh. The verdict stays watched (no fixture certifies whether a module is actually shallow; the run leaves a verdict trace whose presence is its trail); the seam's structure is gated. The architecture review's standing gap no longer reads the unconditional 'not yet built' line — it reads the built scan.

BUILD GUIDANCE (machine-facing): (1) The three gated checks (depth-scan built / consults-map / finding-has-lean-flip) must transition red->green — implement _v_depth_scan in engine/worlds/architecture_review_world.py, lazily importing engine.depth_scan INSIDE the verb so it is absent at the fork base (red) and present at the tip (green). (2) Keep engine/depth_scan.py a DEEP module WITHIN the 400-line length signal — pull complexity into tight private helpers — so the crossing's own fold does not trip the depth gate on your new file. (3) Do NOT hand-append an accepted-length record to clear any length decision: that is the operator's seam, and a hand-appended (uncommitted) record is a FORGED provenance trail that refuses the fold with 'no trail'. (4) Repurpose the existing review.DEPTH_NOT_YET constant's TEXT (keep the name so the existing 'clean'/'circular dependency' scenarios stay green) from 'not yet built' to the built-watched statement; do not delete the constant. Inject the model transport (do not call a live model at import or render time). Scope note: the fold lands spec requirement-blocks and engine code; descriptive prose in spec preambles, glossary.md, and the self-model render body sits outside the fold's reach and is left as trivial doc-tidy.

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
