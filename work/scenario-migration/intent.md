---
kind: ask
state: standing
owner: operator
created: 2026-06-23
---
# scenario-migration — move each remaining capability's checks from by-slice to its own scenarios

`scenario-gate` proved the seam on **folding-conditions**: its acceptance moved from the by-slice
harness (slices 5/7/9/20/21) into executable `#### Scenario:` check blocks homed in
`spec/folding-conditions.md`, compiled by the `scenario` binding. The remaining capabilities are still
checked **by build-slice** in `engine/check/sliceN.py` — the unit of construction, not the unit of
behavior — so one capability's checks still smear across several slice files, and "slice" still carries
two meanings against the one-name-one-concept rule. This is the standing follow-on the seam-first
decision named: migrate the rest, one capability at a time, until the by-slice harness is gone.

Each capability's migration, named:

- **worker** — slices 4 / 7(#1) / 10 / 23 → `spec/worker.md` scenarios (the fence, the grounding,
  the OMP seam).
- **coherence** — slice 21 → `spec/coherence.md` scenarios (the incoherent branch, the fold decision).
- **architecture-review** — slices 6 / 7(#2) / 9 / 15 → `spec/architecture-review.md` scenarios (the
  review render, the exceeded/over/accepted distinction, the mechanical red-flag scan).
- **self-model / delta** — slice 19 + the self-model half of slice 2 → `spec/self-model.md` scenarios
  (the spec read, the delta, the transactional fold incl. crash/retry, the operator view). *(The
  single-writer line — slice 17 — homed in `schedule`, not here: the concurrency-home decision below.
  The self-verifying requirement stays watched — it is the harness's own structure.)*
- **grilling** — slices 3 / 14 → `spec/grilling.md` scenarios (the floor, one-question-at-a-time).
- **design-it-twice** — slice 8 → `spec/design-it-twice.md` scenarios (the contest, the recorded pick).
- **schedule** — slices 16 / 18 → `spec/schedule.md` scenarios (the ready-work loop, failure recovery);
  took the cross-cutting single-writer-line proof (slice 8 residue, slice 17) home with it.
- **communication** — slice 1's window half + slice 2's glossary residue → `spec/communication.md`
  scenarios (the thread, the architect's single voice, the three consequences, the no-raw-leak archive);
  *the operator's act never makes them wait* stays watched (the window's off-input-loop threading), and
  *the architect selects design-it-twice candidates* stays watched here because its gate already lives
  in `design-it-twice`'s own scenarios — three gated, two watched.
- **queue / interface / channels** — slices 1(residue) / 3(residue) / 11 / 12 / 13 / 14 / 22 → their own
  scenarios (the settle path and card-kind, the pure-frame window, the derived channels, the gate).

Each migration extends the `scenario` verb vocabulary **only as its first scenario needs it** (the
locality discipline, `spec/depth.md`) — never pre-built — and dissolves that capability's by-slice
content the same way folding-conditions did (the slice files shrink to their other-capability content,
then disappear; the gaps in the slice numbering mark where the migration has reached — **done so far:
folding-conditions, coherence, worker, architecture-review, design-it-twice, grilling, schedule,
self-model, communication**, leaving slices 1(residue) / 3(residue) / 11–14 / 22). Done when no
`engine/check/sliceN.py` remains and `python3 -m engine --check` runs entirely off capability scenarios.

The migration surfaced that the remaining slices are not clean per-capability — three cross-cutting
seams run through them, each needing one home before the capabilities they touch can finish:

- **the concurrency / single-writer-line proof** (slice 8 residue #1, slice 17) — was described in both
  `worker.md` and `schedule.md`. **Decision (now enacted with the schedule migration): it homes in
  `schedule.md`'s "work runs concurrently on one record"** (the only spec that names *single-writer*) —
  the behavior gated by the "two workers advance at once" scenario; the record-mechanism facts
  (exact-path commits, the flock line, same-file fold, slug reservation) and the failure-recovery
  facts (strict hand-off parse, crash-stranded recovery) are watched invariants in
  `engine/check/scenarios.py`'s schedule section; `worker.md`'s concurrency line stays watched, proven
  by schedule's executable gate. This dissolved slices 8 and 17 and unblocked self-model. [machine]
- **card-kind** (slice 3 residue) — the queue's card-kind seam; migrates with the queue/card-kind work.
- **methodology / channels** (slice 14, the grilling+coherence skill render) — migrates with the
  communication/channels/interface group.

The slice-2 split is complete: self-model took its behaviors (the delta, the fold, the view), and the
communication migration took the rest — the glossary's content (`thread`, the open *operator view*
naming question) now homes as communication's watched invariant in `engine/check/scenarios.py`, so
slice 2 is gone. Slice 1 split the same way: communication took its window half (the thread, the single
voice, the three consequences, the no-raw-leak archive); slice 1 survives as a thin residue — the
queue's settle path (approve/cut/explain), the interface's pure-frame render, and the durable record —
kept by-slice until queue and interface migrate. (Deleting slice 2 also retired a hidden fixture
coupling: slice 14 had read its carve from the spec slice 2 seeded into the shared root; it now
self-seeds the real spec the way slice 22 does.)

What remains is the **queue / interface / channels** group — slices 1(residue) / 3(residue) / 11 / 12 /
13 / 14 / 22: the queue's settle path and card-kind, the interface's window, and the channels mechanism
(the materialize-on-fold registry, the anchor, the methodology skill render, the conformance gate). One
open decision that group must settle first: the channels mechanism has **no `spec/channels.md`** of its
own — it is referenced as a mechanism across worker/self-model/folding-conditions but never given its
own capability requirements — so where its slices (11–14, 22) home is the next stake-bearing call, the
way the concurrency-home decision was for schedule. That group is the last of the by-slice harness.

Provenance: `work/archive/scenario-gate/` (the binding contest and the contract this realizes).
