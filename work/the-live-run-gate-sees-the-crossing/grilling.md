surfaced: 0

[CONTRACT]
Make the operator view's live-run signal track reality: it flips from `never-run-live` to a trace-present live status the moment a real fenced `worker.run` crossing builds on codex and folds, so #11's gate reads the fenced evidence the dispatch path actually produces. Today `view._live_status` (engine/view.py) gates on `_has_watched_trace`, true iff *any* node folder holds a `*.verdict.md` — a file only `provenance.commit_verdict` writes, called solely by the watched mechanisms (the vocabulary check, the depth scan) and a test fixture's `autonomous-run` verdict, never by `worker.run`. So a fenced crossing folds and leaves no such trace, `never-run-live` cannot flip however many crossings run, and the same over-broad reader would wrongly flip on a vocabulary or depth verdict that has nothing to do with a fenced run. "Live-run" is resolved to FENCED — a codex worker built it in the fence and it folded, regardless of who pressed go — settled by #11's own prose and the dispatch grounds, which gate #11 on a worker loading its skills and completing a build in the fence, never on the machine self-dispatching unattended. The fix: `communication.integrate` writes a distinct `fenced-run` verdict trace on the node it folds, riding the existing `commit_verdict` watched-evidence seam under its own mechanism name; `view._live_status` reads *that* mechanism specifically — never any committed verdict — so a fenced crossing flips the signal and a vocabulary or depth trace never does. The readiness label is reworded to say honestly that a fenced crossing has, or has not yet, folded — never implying the unattended autonomy loop is proven. Two gated red→green self-model scenarios lock it: a fenced crossing's fold flips the live status, and a non-fenced watched trace alone leaves it `never-run-live`. The dispatch command's Step 3 caveat and the hand-cranked snapshot's #11/#12 claims are corrected as a separate architect-direct doc-debt follow-up — orchestrator-facing prose outside the spec delta, which the fold's engine/spec reach cannot land.

[DELTA]
# delta — the-live-run-gate-sees-the-crossing

## MODIFIED — self-model
### Requirement: the operator view renders vision beside as-built, readiness, gap, and complexity debt
The operator view MUST render, at every altitude, the **vision** (authored, from `intent.md`) beside the
**as-built** (derived from the living spec), and — answering *can I trust a run on this?* — a
**readiness** surface, the **gap**, and the **complexity debt**, as a recursive tree to the depth the
work reaches. The readiness surface is an honest list of the standards, each marked **gated** (a scenario
carries an executable check block) or **watched** (model judgment no fixture certifies, its only trail
presence), so the operator reads exactly what rests on trust; and it carries the **never-run-live**
status — the fenced-crossing seam is built but no fenced `worker.run` crossing has folded yet, so the
first live run is still unverified — rendered so it says so rather than implying green, derived from the
**fenced-run** trail's emptiness so it flips the moment a fenced crossing folds and leaves its trace,
never hand-set. "Live-run" is **fenced** (a codex worker built it in the fence and it folded, whoever
pressed go), not autonomous (the machine self-dispatched, no operator in the loop): the signal #11 reads
is that a worker loaded its skills and completed a build in the fence, the evidence the dispatch path
actually produces. The fenced-run trace is written by the integrate stage on the node it folds and is
read **by its own mechanism name** — never any committed verdict — so it is never conflated with the
vocabulary or depth watched traces that ride the same `commit_verdict` seam under their own names. The
**gap** (wanted-but-not-built) renders distinctly from the **complexity debt** (built-but-weak) — the
standing output of the architecture review (`architecture-review`), kept honest between folds — which the
old view conflated. The gap is the **open work** read through the tree's one reader — the standing and
in-flight units, never a second walk of the work folders. A decision awaiting the operator is a queue
card, not gap. Whether a tree is folded is read from its location alone, never from a `state:` field a
stale archive can contradict. That map renders the system's **depth**, not merely its length: length is a
context-cost signal against the threshold, and the model-driven red-flag depth assessment is recorded as
not-yet-built, never fabricated. Readiness, as-built, gap, and complexity debt are all derived; only the
vision is authored.

#### Scenario: the view is read
- WHEN the operator opens the view
- THEN it shows the vision, the as-built capabilities and their requirements, the readiness surface, the
  gap, and the complexity debt; drilling into a capability zooms the same to that grain

  ```check
  read view
  vision present
  asbuilt
  gap
  ```

#### Scenario: a capability's vision is a declared binding
- WHEN the view slices the vision per capability
- THEN it reads the intent each capability declares it realizes, recorded in the capability's own
  spec slice, so a newly carved capability shows its vision with no change to the view,
  and a capability that declares none — pure machinery — shows no vision, distinct from a bug

  ```check
  plant machinery
  read view
  vision derived
  vision blank
  ```

#### Scenario: the root's upper levels
- WHEN the operator opens the root of the view
- THEN its structural map of as-built reality and its complexity debt are the
  architecture review's standing output, derived from the scan, not hand-authored

  ```check
  read view-real
  structure
  debt
  ```

#### Scenario: the readiness surface names what rests on trust
- WHEN the operator opens the view
- THEN it renders an honest list of the standards, each marked gated (a scenario carries an executable
  check) or watched (model judgment, no fixture), and a never-run-live status that says no fenced
  crossing has folded yet — the first live run unverified — rather than implying green, all derived,
  never hand-set

  ```check
  read view
  readiness
  never-live
  ```

#### Scenario: the live-run signal flips when a fenced crossing folds
- WHEN a fenced `worker.run` crossing builds on codex and folds, leaving its fenced-run trace on the
  node it archived
- THEN the view no longer renders never-run-live; it renders the trace-present live status without a
  hand-set flag

  ```check
  fenced-crossing folds
  read view
  live-trace
  ```

#### Scenario: a non-fenced watched trace alone does not flip the live-run signal
- WHEN a watched mechanism (the vocabulary check or the depth scan) commits its verdict trace but no
  fenced `worker.run` crossing has folded
- THEN the live-run signal stays never-run-live — the gate reads the fenced-run trace alone, never any
  committed verdict, so the vocabulary and depth traces are never conflated with fenced evidence

  ```check
  watched-evidence present
  read view
  never-live
  ```

#### Scenario: gap is distinct from complexity debt
- WHEN the operator reads the view's shortfalls
- THEN the wanted-but-not-built gap renders as its own region, distinct from the built-but-weak
  complexity debt the architecture review produces, which the old view conflated

  ```check
  read view
  gap-split
  ```

#### Scenario: the gap is the open work, not a decision on the queue
- WHEN the view renders the gap with both a standing unit of open work and a decision awaiting the
  operator open at once
- THEN the gap surfaces the standing work and excludes the decision — the gap is the open work read
  through the tree's one reader, not every non-folded node, so a queue card never reads as
  wanted-but-not-built work

  ```check
  plant open-mix
  read view
  gap-is-work
  ```
