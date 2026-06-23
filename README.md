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

The live work *is* the tree: `work/` holds the open execution trees and `work/archive/` the folded
ones — each a folder with its own `intent.md` (its ask and folding condition), the archive tucked one
level down so the front of the tree stays legible (ADR 0011, ADR 0017). The tree on disk is the
folder, not the node — hypercore dogfooding its own §structure. Run the acceptance harness with
`python3 -m engine --check`; open the live system with `python3 -m engine`.

## Where it stands

Build proceeds in slices, slice 1 first. **Slices 1–16 are built.** (The check count is not
restated here — it drifts; `python3 -m engine --check` is its single source.)

- **1–6 — the spine.** The tree and the fold; intent extraction by grilling; the worker and
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
the tree — `work/` (open) + `archive/` (folded), each tree a folder with its `intent.md`.
`engine/tree.py` is now folder-native (fold = move the folder, `work/`→`work/archive/`) and grilling lives
in each tree's `grilling.md`; `next-work.md` is retired and `research/` dissolved into material on
its node. The acceptance harness is green.

**Item 2 (role assembly, ADR 0009) — the pre-seam build is complete (slices 11–14).** Two roles, each
maximally specialized, assembled from the repo documents (the single source) across three derived
channels: a minimal shared `AGENTS.md` (one file serves both roles — ADR 0009 §4), on-demand
**skills**, and the per-episode **prompt**. The worker holds the whole spec preloaded by construction (the slice-4
keystone); just-in-time is reserved for the reference tail. The single-source-on-fold spine is built:
**depth single-sourcing** (step 1, slice 10), **materialize-on-fold** (step 2, slice 11 — the fold
re-derives the static channels from the spec via `engine/channels.py`, so `skills/` is regenerated
output a committed artifact can't drift from), the **architect's methodology skills** (steps 4 + 4b,
slices 12 + 14 — `engine/methodology.py` renders all four — `design-it-twice`, `architecture-review`,
and now `grilling` and `coherence`, carved into their own capabilities (ADR 0013) — from their spec
slices into the same fold-driven registry), and the **minimal shared `AGENTS.md` anchor** (step 3,
slice 13 — `engine/anchor.py`, non-inferable operational lines plus a registry-derived skills index,
materialized on fold; one `AGENTS.md` serves both roles, the `CLAUDE.md` symlink dropped as redundant,
ADR 0009 §4). The fenced-worker side on the multi-model harness seam is now **built** (steps 5–6,
slice 23): the worker's model transport runs at its fence (cwd = its worktree, `transport.worker_transport`),
the ADR/reference tail is pulled just-in-time while the spec stays preloaded whole, and the worker is
flipped to GPT via `omp` — a *different* model from the architect (ADR 0009), the operator's settled
spend decision. The live loading (`omp` auto-loading the fence's anchor and discovering its skills) is
watched evidence the first autonomous run verifies, never faked into the harness (the honest limit). The
arc folded to `work/archive/role-assembly/`. The engine conformance is done (`work/archive/tree-on-disk/`).

**15 — the mechanical red-flag scan (ADR 0020).** A coherence pass over the repo (`work/archive/coherence-audit/`)
found that the one anti-drift mechanism wired to the fold — derive-on-render — never rotted, while every
hand-maintained restatement did. So two surfaces were generalized toward derive-don't-hand-tend: the
architecture review grew the *mechanical* subset of its red-flag scan — dead module-level symbols and
circular imports, read live off the tree, surfaced in the operator-view gap (the model-driven shallow/leakage
*verdict* stays judgment, still not built); and the operator view's per-capability vision became a binding each
capability declares in its own spec slice, replacing a hand-typed keyword map. The same arc named the model
**transport** (`engine/transport.py`), dissolving a `communication↔grill` cycle, and cut the dead code the new
scan caught. It is the repo's first red→green dogfood of its own feedback-loop discipline.

**16 — the autonomy seam (ADR 0022; `engine/schedule.py`).** The system's most distinctive promise —
continuous, concurrent autonomous work (intent §60/§62) — was unreachable from the interface: `tree`
computed the ready work but nothing consumed it, so a ratified ask landed as standing work and the
system idled, the exact §60 defect. The **scheduler** is the loop that consumes it — it reads the
ready work (`tree.ready`, the §110 readiness predicate) and runs `worker.run` (dispatch → build fenced →
integrate → fold) off the operator's input loop, continuous and concurrent, idling only on a decision;
a worker that cannot complete returns as a decision rather than stalling. Concurrency made the shared
git line single-writer, which deepened `tree` by lifting its durable-write floor into `engine/record.py`
(atomic write, scoped commit, the one lock). Wiring `worker.run` end-to-end also surfaced a latent bug
the harness had never exercised: it dropped the scripted transport on the integrate step, falling back
to a live model call — fixed. The worker has since been flipped to GPT via `omp`, fenced at its
worktree (role-assembly steps 5–6, slice 23).

## On documents

Research and design notes are **provenance** — they informed decisions but nothing standing depends
on them. They are *material*, so they live with the execution tree whose ask produced them (the item-2
design in `work/role-assembly/`, the slice-7 design in `work/archive/depth-regrounding/`), folding to
`work/archive/` with it — not in a root directory of their own (ADR 0012 dissolved the old `research/`).
The decisions (`spec/decisions/`), the spec, and the code stand alone, so a clone is
self-sufficient: a standing artifact may *cite* provenance as a footnote, never *depend* on it (read
it at runtime, or pin acceptance to a section). ADR 0010 records that discipline and retired the
bootstrap `rebuild-spec` scaffold; ADR 0012 placed provenance on its node.
