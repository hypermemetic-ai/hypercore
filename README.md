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

Next: item 2 (context files) is **investigated** — `research/context-files.md`. Verified on the real
heterogeneous stack (architect = Opus 4.8 via `claude -p`; worker = GPT-5.5 via pi/OMP): OMP
auto-loads **`AGENTS.md`** from the worktree cwd, Claude auto-loads **`CLAUDE.md`** and ignores
AGENTS.md, and a `CLAUDE.md` → `@AGENTS.md` adapter bridges the two. So **AGENTS.md is the source of
truth** (the open standard, north-star-aligned) and **CLAUDE.md a thin adapter** — the depth
framework moves there (retiring `worker.DEPTH`'s duplication), while per-capability routing stays
prompt-assembled. A transport/seam blocker (the worker does not yet run in its fence; pi/OMP is
parked) sets the sequencing. Five forks now await the operator's pick before the ADR and build.
