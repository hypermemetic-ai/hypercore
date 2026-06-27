surfaced: 0

[Q] Should operator-view-readiness also build a live "what's building + its plan" surface, or stay scoped to the three readiness additions (standards honest-list, never-run-live, gap/complexity-debt split)?
lean: Keep it scoped — the live-build surface is a standing-work concern (intent §58/§60: a run already shows as live work on its node, its plan material there), a different surface with its own unsettled "at a glance" design, so it earns its own node that worker-builds-proposed-delta then sequences after.
flip: If the operator reads "never run live" and "what's building now" as one inseparable readiness glance the operator cannot split.
answer: Already homed — intent §58/§60 already shows a run as live work on its node with its plan as node material; no new view surface, and worker-builds-proposed-delta carries no view precondition.

[CONTRACT]
operator-view-readiness grows the operator view (opened with `v` from the window) into a readiness surface that answers "can I trust a run on this?". Beside the existing vision and as-built, the view renders three additions, every one derived and none hand-tended: (1) an honest list of the standards, each marked **gated** — a scenario carries an executable check block — or **watched** — model judgment no fixture certifies, its only trail presence — so the operator reads exactly what rests on trust; (2) the **never-run-live** status, derived from the watched-evidence trail's emptiness, rendered so it says the autonomy seam is built but the first autonomous run is still unverified, never implying green, and flipping on its own when the first run leaves a trace; and (3) the **gap** (wanted-but-not-built) rendered distinctly from the **complexity debt** (built-but-weak, the architecture review's standing output), which the old view conflated into one list. The result is validated against this entry and gated by a new self-model scenario; `python3 -m engine --check` is green. Out of scope, resolved in this pass: the live "what's building and why" surface — already homed on the standing-work tree (intent §58/§60), so worker-builds-proposed-delta carries no view precondition.

[DELTA]
# delta — grow the operator view into a readiness surface

## RENAMED — self-model
### Requirement: the operator view renders vision beside as-built and gap
→ the operator view renders vision beside as-built, readiness, gap, and complexity debt

## MODIFIED — self-model
### Requirement: the operator view renders vision beside as-built, readiness, gap, and complexity debt
The operator view MUST render, at every altitude, the **vision** (authored, from `intent.md`) beside the **as-built** (derived from the living spec), and — answering *can I trust a run on this?* — a **readiness** surface, the **gap**, and the **complexity debt**, as a recursive tree to the depth the work reaches. The readiness surface is an honest list of the standards, each marked **gated** (a scenario carries an executable check block) or **watched** (model judgment no fixture certifies, its only trail presence), so the operator reads exactly what rests on trust; and it carries the **never-run-live** status — the autonomy seam is built but the first autonomous run is still unverified — rendered so it says so rather than implying green, derived from the watched-evidence trail's emptiness so it flips when the first run leaves its trace, never hand-set. The **gap** (wanted-but-not-built) renders distinctly from the **complexity debt** (built-but-weak) — the standing output of the architecture review (`architecture-review`), kept honest between folds — which the old view conflated. That map renders the system's **depth**, not merely its length: length is a context-cost signal against the threshold, and the model-driven red-flag depth assessment is recorded as not-yet-built, never fabricated. Readiness, as-built, gap, and complexity debt are all derived; only the vision is authored.

#### Scenario: the view is read
- WHEN the operator opens the view
- THEN it shows the vision, the as-built capabilities and their requirements, the readiness surface, the gap, and the complexity debt; drilling into a capability zooms the same to that grain

  ```check
  read view
  vision present
  asbuilt
  gap
  ```

#### Scenario: a capability's vision is a declared binding
- WHEN the view slices the vision per capability
- THEN it reads the intent each capability declares it realizes, recorded in the capability's own spec slice, so a newly carved capability shows its vision with no change to the view, and a capability that declares none — pure machinery — shows no vision, distinct from a bug

  ```check
  plant machinery
  read view
  vision derived
  vision blank
  ```

#### Scenario: the root's upper levels
- WHEN the operator opens the root of the view
- THEN its structural map of as-built reality and its complexity debt are the architecture review's standing output, derived from the scan, not hand-authored

  ```check
  read view-real
  structure
  debt
  ```

#### Scenario: the readiness surface names what rests on trust
- WHEN the operator opens the view
- THEN it renders an honest list of the standards, each marked gated (a scenario carries an executable check) or watched (model judgment, no fixture), and a never-run-live status that says the first autonomous run is unverified rather than implying green — all derived, never hand-set

  ```check
  read view
  readiness
  never-live
  ```

#### Scenario: gap is distinct from complexity debt
- WHEN the operator reads the view's shortfalls
- THEN the wanted-but-not-built gap renders as its own region, distinct from the built-but-weak complexity debt the architecture review produces, which the old view conflated

  ```check
  read view
  gap-split
  ```
