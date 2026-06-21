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

Build proceeds in slices (spec §9), slice 1 first. Slices 1–9 are built. Slice 6 split the
acceptance harness per-slice into `hyper/check/` (the first deepening work the review
surfaced); slice 7 re-grounded the architecture in Ousterhout's *A Philosophy of Software
Design* — depth is the criterion, length a context-cost signal that raises a *decision*
rather than auto-refusing (ADR 0006; `research/aposd.md`, `research/regrounding.md`); slice 8
re-grounded parallelism as the judgment use of the worktree fence — **design-it-twice** for
load-bearing interfaces, the architect picking machine-side on depth/locality/seam and
recording a structured design-decision (ADR 0007; `hyper/design.py`); slice 9 made a
length-acceptance **bounded** — it ratchets up rather than silencing a file forever, the
accepted length recorded as `accepted@<N>` and a stale acceptance surfaced distinctly by the
review (ADR 0008).

Next: item 2 (context files) is investigated (`research/context-files.md`), designed
(`research/assembly.md`), and **ratified** — ADR 0009, after a second validation pass against live
sources (assembly.md §8). The goal: two roles (architect = Opus 4.8 via `claude -p`; worker = GPT-5.5
via pi/OMP), each **maximally skilled and specialized**, assembled from repo documents (the single
source) feeding three derived channels — a **minimal agents file** (non-inferable operational lines
only), **skills** (on-demand specialization — the routing), and **prompts** (the per-node live task).
Placed by two axes (durability × reach): **skills + the agents file are derived renders regenerated
by the fold** (no hand-copy — this kills the `worker.DEPTH` smell); the worker's full scan is
**just-in-time** (a preloaded complete **capability index** as the awareness guarantee + the touched
slices, the rest pulled from the fenced checkout on demand); and placement is **one shared `AGENTS.md`
symlinked as `CLAUDE.md`**. Calibrated by field evidence (the ETH Zurich AGENTS.md study + Anthropic's
skills/context-engineering guidance): the agents file stays minimal/non-inferable, specialization
lives in skills. Next step: **build at §5 step 1** — retire `DEPTH` (render from `aposd.md`), then
the capability index and the derived-render mechanism; the worker-fenced side (JIT pull, the OMP flip)
lands on the parked pi/OMP harness seam.
