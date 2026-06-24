---
kind: ask
state: standing
owner: operator
created: 2026-06-24
---
# code-fold-verification-scope — a code-bearing fold can break an untouched capability its gates never check

**Needs grilling (design-it-twice territory) before it becomes work — filed, not yet grilled.**

The crossing's two correctness gates over a code-bearing build both scope to the **touched**
capabilities — the ones the worker's delta names:

- the **scenario gate** (`scenario.gate`) runs the touched capabilities' scenarios red→green in the fence;
- the **re-verify keystone** (`scenario.reverify`) runs the touched capabilities' scenarios on the
  merged tree before the commit.

But the worker's *code* can reach far past the capabilities it names. A worker that refactors a
**shared engine module** — `delta.py`, `tree.py`, `record.py`, `scenario.py` — can break a capability
it never named in its delta, and **neither gate runs that capability's scenarios**. The crossing
reports `done: True`, the fold lands the code on main, and only a *separate* full
`python3 -m engine --check` would catch the break. The autonomy loop does not run that full check, so
the broken code lands silently — the crossing's own verdict is green-on-the-touched-capability, not
green-on-the-system.

Provenance: the `requirement-rename-op` crossing (2026-06-24). The worker refactored `engine/delta.py`
— shared by folding-conditions, schedule, and channels — and the crossing folded green on `self-model`
alone (the only touched capability). A **manually run** full `--check` (115 checks) was what actually
confirmed nothing else broke. It was clean by the worker's skill, not because any gate verified it. Had
the refactor broken folding-conditions, that broken code would have reached main with `done: True`.

This is the autonomy loop's blind spot, not the build-only path's. It bites only code-bearing folds
that touch a module other capabilities depend on — but that is the common case for engine work.

## the design choice (for the grilling / design-it-twice pass)
How wide must a code-bearing fold's verification reach? Candidate shapes, each trading the
continuous/concurrent throughput the `worker-build-reaches-main` design recorded as a cost against
completeness:
- **full harness on merged main** — the re-verify runs the whole `--check`, not only the touched
  capabilities. Complete, simplest to reason about, heaviest per fold.
- **dependency-scoped re-verify** — re-verify the capabilities whose worlds/engine reach the touched
  *modules* (a dependency closure over the changed files), not only the named capabilities. Narrower
  than full, but needs a module→capability map that can itself drift.
- **a full `--check` as a fold precondition** — keep the touched-capability gate, add one full-harness
  gate before the commit. Same completeness as the first, framed as a distinct gate.

The `worker-build-reaches-main` design-decision (`work/archive/worker-build-reaches-main/`) already
recorded the re-verify throughput concern; this ask extends exactly that tradeoff to its blind spot.

## folding condition
- a code-bearing fold cannot land engine code that leaves the merged tree red anywhere a full
  `python3 -m engine --check` would catch — the crossing's own gates verify the whole affected surface,
  not only the capabilities the delta names;
- the chosen mechanism (full harness / dependency-scoped / precondition gate) and its grounds are
  recorded as material on the contest node;
- `python3 -m engine --check` carries an acceptance check that a code-bearing fold which breaks an
  **untouched** capability is refused (the node recovers to a decision, nothing landing), and is green.
