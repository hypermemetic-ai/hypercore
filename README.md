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

Build proceeds in slices (spec §9), slice 1 first. Slices 1–6 are built. With slice 6
the acceptance harness was split per-slice into `hyper/check/` — the first deepening
work the architecture review surfaced (ADR 0004/0005).

Next: slice 7 — parallelism re-grounded (design-it-twice for load-bearing interfaces).
