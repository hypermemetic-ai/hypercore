# hypercore

Clean rebuild from zero. History erased on 2026-06-20; the prior epoch was torn
down, not patched.

Start here (a fresh session reads these, in order — all in this repo):

1. `intent.md` — the durable vision: what the system is for. Every statement is
   machine-owned until the operator ratifies it; the markers say what still awaits a word.
2. `glossary.md` — the ubiquitous language: one name, one concept, system-wide. At the root
   because it governs the vision, the spec, and the code alike (ADR 0018).
3. `spec/` — the living spec: one specification segmented into flat `spec/<capability>.md` files
   (a capability is a document segment, not a folder — ADR 0014), `depth` among them as a capability
   like `design-it-twice` (ADR 0019). Small by design, meant to be scanned whole — the high-signal core.
4. `spec/decisions/` — the ADRs: every decision and its grounds, in order. The reference tail.

The live work *is* the graph: `work/` holds the open execution graphs and `work/archive/` the folded
ones — each a folder with its own `intent.md` (its ask and folding condition), the archive tucked one
level down so the front of the tree stays legible (ADR 0011, ADR 0017). The graph on disk is the
folder, not the node — hypercore dogfooding its own §structure. Run the acceptance harness with
`python3 -m engine --check`; open the live system with `python3 -m engine`.

## Where it stands

Build proceeds in slices, slice 1 first. **Slices 1–14 are built.**

- **1–6 — the spine.** The graph and the fold; intent extraction by grilling; the worker and
  its git-worktree fence; the folding conditions; the architecture review. Slice 6 split the
  acceptance harness per-slice into `engine/check/` — the first deepening work the review surfaced.
- **7 — depth is the criterion (ADR 0006).** Re-grounded against Ousterhout's *A Philosophy of
  Software Design* (`spec/depth.md`): length is demoted to a context-cost *signal* that raises a
  decision, never an auto-refusal.
- **8 — design-it-twice (ADR 0007; `engine/design.py`).** The judgment use of the worktree fence:
  a load-bearing interface designed several ways in isolation, the architect picking machine-side
  on depth/locality/seam and recording a structured design-decision.
- **9 — bounded acceptance (ADR 0008).** A length-acceptance ratchets up rather than silencing a
  file forever; the accepted length is recorded as `accepted@<N>`, a stale acceptance surfaced
  distinctly by the review.
- **10 — the depth source single-sourced (ADR 0009).** The worker's depth grounding and the
  `depth` skill render from `spec/depth.md`, never a frozen copy. (Depth was later normalized into a
  capability rendered like the others — ADR 0019 — retiring its bespoke module.)

Since the slices, the repo was made to obey its own §structure (ADR 0010–0012): the live work **is**
the graph — `work/` (open) + `archive/` (folded), each graph a folder with its `intent.md`.
`engine/graph.py` is now folder-native (fold = move the folder, `work/`→`work/archive/`) and grilling lives
in each graph's `grilling.md`; `next-work.md` is retired and `research/` dissolved into material on
its node. 157 checks green.

**Item 2 (role assembly, ADR 0009) — the pre-seam build is complete (slices 11–14).** Two roles, each
maximally specialized, assembled from the repo documents (the single source) across three derived
channels: a minimal shared `AGENTS.md` (symlinked as `CLAUDE.md`), on-demand **skills**, and the
per-episode **prompt**. The worker holds the whole spec preloaded by construction (the slice-4
keystone); just-in-time is reserved for the reference tail. The single-source-on-fold spine is built:
**depth single-sourcing** (step 1, slice 10), **materialize-on-fold** (step 2, slice 11 — the fold
re-derives the static channels from the spec via `engine/channels.py`, so `skills/` is regenerated
output a committed artifact can't drift from), the **architect's methodology skills** (steps 4 + 4b,
slices 12 + 14 — `engine/methodology.py` renders all four — `design-it-twice`, `architecture-review`,
and now `grilling` and `coherence`, carved into their own capabilities (ADR 0013) — from their spec
slices into the same fold-driven registry), and the **minimal shared `AGENTS.md` anchor** (step 3,
slice 13 — `engine/anchor.py`, non-inferable operational lines plus a registry-derived skills index,
materialized on fold and symlinked as `CLAUDE.md`). What remains is parked: the fenced-worker side on
the multi-model harness seam (steps 5–6, the autonomy unlock — transport `cwd` = the fence, the
reference tail pulled just-in-time, the OMP flip). The open arc is `work/role-assembly/` (its
`intent.md` carries the steps). The engine conformance is done (`work/archive/graph-on-disk/`).

## On documents

Research and design notes are **provenance** — they informed decisions but nothing standing depends
on them. They are *material*, so they live with the work graph whose ask produced them (the item-2
design in `work/role-assembly/`, the slice-7 design in `work/archive/depth-regrounding/`), folding to
`work/archive/` with it — not in a root directory of their own (ADR 0012 dissolved the old `research/`).
The decisions (`spec/decisions/`), the spec, and the code stand alone, so a clone is
self-sufficient: a standing artifact may *cite* provenance as a footnote, never *depend* on it (read
it at runtime, or pin acceptance to a section). ADR 0010 records that discipline and retired the
bootstrap `rebuild-spec` scaffold; ADR 0012 placed provenance on its node.
