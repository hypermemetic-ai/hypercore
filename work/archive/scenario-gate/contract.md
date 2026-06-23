# scenario-gate — ratified contract

Grilled 2026-06-23. The durable record of what the grilling pass settled.

## What the scan resolved from the ratified corpus (no operator stake)

- **Checks home by capability, not build-slice.** "One name, one concept, system-wide"
  (`intent.md:112`, `glossary:2`) plus everything durable already being capability-organized (the
  spec, the engine modules) settles the *direction*; "slice" overloaded (build-increment vs.
  capability) is a defect by the system's own rule. No operator stake in keeping `sliceN.py` naming.
- **The spec is the agent's render of the self-model, not an operator-facing artifact.** "read flat
  by the agent" (`glossary` *living spec*); the operator reads the **operator view** (`glossary`
  *self-model*). So `intent.md:10` "operator legibility is king" governs the operator view, not the
  spec's form — the spec is judged on agent-legibility and self-description fidelity. (An operator
  correction mid-pass; recorded because it inverted the form decision.)
- **The build-slice narrative becomes provenance**, not gate structure (`README` *On documents*).
- **The overclaiming rhetoric goes** — "the loop is the skill / the methodological keystone" is
  replaced by an honest naming of the mechanism. Spec-delta authoring, not a fork.

## The residual decisions (operator-settled)

- **D1 — the acceptance check is the architect-authored scenario** (not a worker-recorded command,
  not merely a hardened watched judgment). Closes the self-judging hole at the root: the builder no
  longer writes the oracle that judges it. Homes every check in its capability by construction.
- **D2 — the scenario *is* the executable check** (the self-model self-verifying), not a prose
  scenario beside a separate check. A self-model whose description is its own test cannot drift from
  the system it describes — derive-don't-hand-tend (slice-15's lesson) applied to the self-model
  itself. The vision already says it ("a requirement is a check that survives its node"; "scenario —
  machine-checkable and human-legible at once"); the code never realized it. Agent-legibility is
  preserved by keeping the scenario the high-signal WHEN/THEN interface, machinery hidden in a deep
  layer.
- **D3 — seam-first, proven on folding-conditions** (not a whole-self-model big-bang). Decomposition
  (`intent §106`): the whole migration outruns one check. Each remaining capability becomes named
  follow-on work (`intent §86`).

## The design (architect-resolved)

- **The gate.** A behavior change folds only when its capability's architect-authored scenario(s) —
  the ones the delta touches — execute red→green: red at the fork base (behavior not yet built),
  green at the tip. `conditions._feedback_loop` is replaced by a scenario-gate that runs the touched
  capability's scenarios; the worker records no loop.
- **The binding seam** (scenario → runnable) is a **deep module**: the scenario stays the high-signal
  WHEN/THEN interface; the harness / driver / scripted-transport machinery is hidden beneath. Its
  interface — and its home (`self-model` vs. a new `acceptance` capability) — is a **design-it-twice**,
  the arc's first child.
- **The worker** builds to make the architect's scenario green; its hand-off (`worker.py`) drops the
  self-authored `loop` field. Real test-first, with the oracle owned by the independent party.
- **First realization.** folding-conditions' requirements (the loop / length / ratchet / gated-watched
  scenarios across slices 5/7/9/20/21) are re-homed as executable scenarios in
  `spec/folding-conditions.md`; that slice content dissolves into them.

## The spec delta this realizes

- `intent.md` — ADD `[machine]`: a behavior's check is the self-model's own account of it — a
  capability's scenario is the executable gate, authored by the side that does not build it, the
  worker turning it red→green.
- `spec/folding-conditions.md` — REMOVE the recorded-loop / executed-not-narrated requirements; ADD
  the scenario-gate requirement; UPDATE the gated/watched table (`red-green-loop` → `scenario-gate`,
  gated; loop-relevance leaves *watched*).
- `spec/self-model.md` — ADD: the living spec is self-verifying (a capability's scenarios are the
  executable checks of its requirements).
- `spec/grilling.md` — MODIFY: the pass yields the executable scenario, not prose alone.
- `spec/worker.md` + `glossary.md` — MODIFY `worker` / `hand-off`: no self-authored loop; build to
  green.
- `spec/coherence.md` — MODIFY: check-relevance gated by construction; the contract check remains for
  what scenarios can't capture.
- new seam home — `self-model` or a new `acceptance` capability (the design-it-twice decides).
- `skills/` — derived: `grilling` / `coherence` / `depth` / `design-it-twice` re-render from their
  changed spec slices on fold (`engine/methodology.py`); no hand-edit.

## The contract (validated at the archive gate)

- a behavior change folds only when an architect-authored scenario goes red→green; a worker-supplied
  passing command cannot fold it.
- folding-conditions' scenarios are executable checks homed in `spec/folding-conditions.md`; the
  slice-5/7/9/20/21 content for it is gone.
- the scenario→executable binding is a deep module with a recorded design-decision; the scenario
  stays high-signal.
- `python3 -m engine --check` green (a real red→green), unconverted capabilities coexisting.
- each remaining capability's migration filed as standing follow-on work.
