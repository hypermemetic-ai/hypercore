# hypercore

Clean rebuild from zero. History erased on 2026-06-20; the prior epoch was torn
down, not patched.

Start here (a fresh session needs these, in order):
1. `~/Documents/build-handoff.md` — the construction handoff
2. `~/Documents/rebuild-spec-1.md` — the methodology spec (machine-owned, awaits ratification)
3. `intent.md` — the durable vision (in this repo)

Parked for later (not in the build): the pi/glm/gpt multi-model harness —
`~/Documents/hypercore-parked/` (`harness-ideas.md` + `harness-source/`). The full
pre-teardown repo is `~/Documents/hypercore-next-cold-backup-2026-06-20.tar.gz`.

Build proceeds in slices (spec §9), slice 1 first. Slices 1–7 are built. Slice 6 split the
acceptance harness per-slice into `hyper/check/` (the first deepening work the review
surfaced); slice 7 re-grounded the architecture in Ousterhout's *A Philosophy of Software
Design* — depth is the criterion, length a context-cost signal that raises a *decision*
rather than auto-refusing (ADR 0006; `research/aposd.md`, `research/regrounding.md`).

Next: slice 8 — parallelism re-grounded (design-it-twice for load-bearing interfaces).
