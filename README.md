# hypercore

Clean rebuild from zero. History erased on 2026-06-20; the prior epoch was torn
down, not patched.

Start here (a fresh session reads these, in order — all in this repo):

1. `intent.md` — the durable vision: what the system is for. Every statement is
   machine-owned until the operator ratifies it; the markers say what still awaits a word.
2. `spec/` — the living spec: each capability's `spec.md`, the cross-cutting `glossary.md`,
   and `spec/depth.md` (the depth disciplines the system is built to). Small by design and
   meant to be scanned whole — the high-signal core.
3. `spec/decisions/` — the ADRs: every decision and its grounds, in order. The reference tail.

The live work *is* the graph: `work/` holds the open execution graphs, `archive/` the folded
ones — each a folder with its own `intent.md` (its ask and folding condition). That is hypercore
dogfooding its own §structure (ADR 0011): the graph on disk is the folder, not the node. Run the
acceptance harness with `python3 -m hyper --check`; open the live system with `python3 -m hyper`.

## Where it stands

Build proceeds in slices, slice 1 first. **Slices 1–10 are built.**

- **1–6 — the spine.** The graph and the fold; intent extraction by grilling; the worker and
  its git-worktree fence; the folding conditions; the architecture review. Slice 6 split the
  acceptance harness per-slice into `hyper/check/` — the first deepening work the review surfaced.
- **7 — depth is the criterion (ADR 0006).** Re-grounded against Ousterhout's *A Philosophy of
  Software Design* (`spec/depth.md`): length is demoted to a context-cost *signal* that raises a
  decision, never an auto-refusal.
- **8 — design-it-twice (ADR 0007; `hyper/design.py`).** The judgment use of the worktree fence:
  a load-bearing interface designed several ways in isolation, the architect picking machine-side
  on depth/locality/seam and recording a structured design-decision.
- **9 — bounded acceptance (ADR 0008).** A length-acceptance ratchets up rather than silencing a
  file forever; the accepted length is recorded as `accepted@<N>`, a stale acceptance surfaced
  distinctly by the review.
- **10 — the depth source single-sourced (ADR 0009).** The worker's depth grounding and the
  `depth` skill render from `spec/depth.md` via `hyper/depth.py` — never a frozen copy.

**Next — item 2 (role assembly, ADR 0009).** Two roles, each maximally specialized, assembled
from the repo documents (the single source) across three derived channels: a minimal shared
`AGENTS.md` (symlinked as `CLAUDE.md`), on-demand **skills**, and the per-episode **prompt**. The
worker holds the whole spec preloaded by construction (the slice-4 keystone); just-in-time is
reserved for the reference tail. The depth single-sourcing (above) is the first step built; the
derived-render / materialize-on-fold mechanism, the shared anchor, and the architect's skills land
next, with the fenced-worker side on the parked multi-model harness seam. See `work/role-assembly/`
— currently paused under `work/graph-on-disk/` (conforming the engine to the folder shape, ADR 0011).

## On documents

Research and design notes are **provenance** — they informed decisions but nothing standing depends
on them. They are *material*, so they live with the work graph whose ask produced them (the item-2
design in `work/role-assembly/`, the slice-7 design in `archive/depth-regrounding/`), folding to
`archive/` with it — not in a root directory of their own (ADR 0012 dissolved the old `research/`).
The decisions (`spec/decisions/`), the spec, and the code stand alone, so a clone is
self-sufficient: a standing artifact may *cite* provenance as a footnote, never *depend* on it (read
it at runtime, or pin acceptance to a section). ADR 0010 records that discipline and retired the
bootstrap `rebuild-spec` scaffold; ADR 0012 placed provenance on its node.
