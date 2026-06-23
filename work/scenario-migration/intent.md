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
- **self-model / delta** — slices 17 / 19 → scenarios (the transactional fold, the single-writer line).
- **grilling** — slices 3 / 14 → `spec/grilling.md` scenarios (the floor, one-question-at-a-time).
- **design-it-twice** — slice 8 → `spec/design-it-twice.md` scenarios (the contest, the recorded pick).
- **schedule** — slices 16 / 18 → `spec/schedule.md` scenarios (the ready-work loop, failure recovery).
- **communication / channels / interface** — slices 1 / 2 / 11 / 12 / 13 / 22 → their own scenarios
  (the architect's one voice, the derived channels, the conformance gate).

Each migration extends the `scenario` verb vocabulary **only as its first scenario needs it** (the
locality discipline, `spec/depth.md`) — never pre-built — and dissolves that capability's by-slice
content the same way folding-conditions did (the slice files shrink to their other-capability content,
then disappear; the gaps in the slice numbering mark where the migration has reached — **done so far:
folding-conditions, coherence, worker, architecture-review, design-it-twice, grilling**, leaving slices
1 / 2 / 3(residue) / 8(residue) / 11–14 / 16–19 / 22). Done when no `engine/check/sliceN.py` remains
and `python3 -m engine --check` runs entirely off capability scenarios.

The migration surfaced that the remaining slices are not clean per-capability — three cross-cutting
seams run through them, each needing one home before the capabilities they touch can finish:

- **the concurrency / single-writer-line proof** (slice 8 residue #1, slice 17) — described in both
  `worker.md` and `schedule.md`. **Decision: it homes in `schedule.md`'s "work runs concurrently on
  one record"** (the only spec that names *single-writer*), gated when schedule migrates; the
  record-mechanism facts (exact-path commits, the flock line, slug reservation) become watched
  invariants; `worker.md`'s concurrency line stays watched, proven by schedule's executable gate. This
  unblocks self-model and fully dissolves slice 8. [machine]
- **card-kind** (slice 3 residue) — the queue's card-kind seam; migrates with the queue/card-kind work.
- **methodology / channels** (slice 14, the grilling+coherence skill render) — migrates with the
  communication/channels/interface group.

self-model is the most entangled (slices 2 + 17 + 19) and is gated on the concurrency decision above
plus the slice-2 split; it is the natural piece after schedule.

Provenance: `work/archive/scenario-gate/` (the binding contest and the contract this realizes).
