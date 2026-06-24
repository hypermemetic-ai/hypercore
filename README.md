# hypercore

Clean rebuild from zero. History erased on 2026-06-20; the prior epoch was torn
down, not patched.

Start here (a fresh session reads these, in order — all in this repo):

1. `intent.md` — the durable vision: what the system is for. Every statement is
   machine-owned until the operator ratifies it; the markers say what still awaits a word.
2. `glossary.md` — the ubiquitous language: one name, one concept, system-wide. At the root
   because it governs the vision, the spec, and the code alike.
3. `spec/` — the living spec: one specification segmented into flat `spec/<capability>.md` files
   (a capability is a document segment, not a folder), `depth` among them as a capability
   like `design-it-twice`. Small by design, meant to be scanned whole — the high-signal core.

A decision needs no separate record: a settled card carries the decision and its grounds on its node,
and the node archives with its work; the decision's outcome lives in the living spec; a design pick and
its grounds are material on the contest node. The live work *is* the tree: `work/` holds the open
execution trees and `work/archive/` the folded
ones — each a folder with its own `intent.md` (its ask and folding condition), the archive tucked one
level down. The tree on disk is the
folder, not the node — hypercore dogfooding its own §structure. Run the acceptance harness with
`python3 -m engine --check`; open the live system with `python3 -m engine`.

## Where it stands

hypercore is **two roles over one tree**. The **architect** holds the operator-facing voice and the
design judgment; the **worker** builds fenced in its own git worktree and hands a machine-facing result
back. Between them is the **tree** — `work/` (open) and `work/archive/` (folded), every execution tree a
folder with its own `intent.md`, a fold = moving that folder one level down so the front of the tree
stays legible. The operator meets all of it through one keyboard-only **window**. The system's behavior
is its **capabilities** — fourteen flat `spec/<capability>.md` slices, each its own single source. Twelve
are **self-verifying**: their prose scenarios are their executable checks (the scenario gate, below); the
two they rest on — `tree`, the durable folder-tree, and `depth`, the standards — are proven through the
capabilities that use them. `python3 -m engine --check` is green; the check count is not restated here
because it drifts.

**The spine.** The tree and the fold; intent extraction by **grilling** (resolve what the spec and
intent already settle, surface only the stake-bearing residue as queue cards one question at a time —
each with a lean and a flip — yielding the contract and the spec delta); the **worker** fenced in its
worktree; the **folding conditions** every result clears before it lands; and the **architecture
review** that scans the tree live for complexity debt. Length is a context-cost *signal* that raises a
decision, never an auto-refusal (re-grounded on Ousterhout's *A Philosophy of Software Design*); a
length-acceptance **ratchets** — recorded as `accepted@<N>` through one writer seam, a stale acceptance
surfaced distinctly — so a file is bounded to the length it was accepted at, not silenced forever. The
review also reads the *mechanical* red flags a tool can judge without a model — dead module-level
symbols, import cycles — live off the tree; the model-driven shallow/leakage *verdict* stays judgment,
still unbuilt.

**Design-it-twice.** The judgment use of the worktree fence: a load-bearing interface is designed
several ways in isolation, the architect picking machine-side on **depth, locality, and seam placement**
and recording a structured design-decision as material on the contest node — which archives with the
work, so there is no separate decision log.

**The roles, assembled from the repo.** Both roles are grounded from the repo documents (the single
source) across three **derived channels**: the per-episode **prompt** (assembled live, never stale),
on-demand **skills**, and a minimal shared **anchor** (`AGENTS.md`). The worker holds the whole spec
preloaded by construction; just-in-time is reserved for the long history and grounds in `work/archive/`.
The static channels (skills, anchor) are **materialized on fold** from the spec by the `channels`
capability — `engine/methodology.py` renders each skill from its slice, `engine/anchor.py` renders the
anchor (non-inferable operational lines plus a registry-derived skills index) and its `CLAUDE.md` bridge
(a derived `@AGENTS.md` import, because Claude Code reads `CLAUDE.md`, not a bare `AGENTS.md`) — so a
committed artifact can no more drift from the spec than the spec from a folded delta. The worker runs at
its fence on a *different* model (GPT via `omp`, the operator's settled spend decision); whether a live
session actually loads the fence's anchor and skills is **watched evidence** the first autonomous run
confirms, never faked into the harness — the honest limit.

**The autonomy seam.** The scheduler (`engine/schedule.py`) consumes the ready work the tree computes —
dispatch → build fenced → integrate → fold — continuous and concurrent off the operator's input loop,
idling only on a decision; a worker that cannot complete returns as a decision rather than stalling.
Concurrency made the shared git line **single-writer**, lifting `tree`'s durable-write floor into
`engine/record.py` (atomic write, scoped commit, the one lock).

**The self-model verifies itself — the scenario gate.** The acceptance harness was once a stack of
by-slice check modules — the unit of *construction*, so one capability's checks smeared across several
files and "slice" carried two meanings against the one-name-one-concept rule. It is retired: a
capability's prose `#### Scenario:` blocks **are** its executable checks. The architect authors the
WHEN/THEN and, where a behavior is mechanically checkable, a fenced `check` block of domain verbs; the
`scenario` binding (`engine/scenario.py`) compiles those verbs into assertions over the real engine
seams, with per-capability **worlds** (`engine/worlds/`, one module each) supplying the fixtures — so a
behavior's description cannot drift from the behavior, because the description *is* the test, and the
builder never authors the oracle that judges it. The gated/watched register is **derived** off the
blocks (a requirement is gated exactly when one of its scenarios carries a check block); the fold gate
runs a touched capability's scenarios red at the fork base and green at the tip, replacing the worker's
self-authored loop with a check the side that does not build it owns. All twelve capabilities have
migrated; `engine/check/` is now just the tally and the one scenario acceptance path, and no `sliceN.py`
remains.

**The discipline through all of it — derive, don't hand-tend.** A coherence pass found the one anti-drift
mechanism wired to the fold never rotted, while every hand-maintained restatement did; so each surface
was pulled to a single fold-driven source — the depth grounding and skills from `spec/depth.md`, the
operator view's per-capability vision a binding each spec declares, the architecture review's red flags
read live, the model **transport** named in one place (dissolving a `communication↔grill` cycle), and the
scenario→check above. A frozen second copy that can drift is the smell; one source the fold re-renders is
the cure.

*Provenance.* The build ran in numbered construction slices (1–23) and the post-slice arcs above; that
order lives in `git log` and the folded work under `work/archive/` (`role-assembly/`, `coherence-audit/`,
`scenario-gate/`, and `scenario-migration/`) — cited as a footnote, never depended on.
The spec, the code, and the decisions on their nodes stand alone.

## On documents

Research and design notes are **provenance** — they informed decisions but nothing standing depends
on them. They are *material*, so they live with the execution tree whose ask produced them (the role-assembly
design in `work/archive/role-assembly/`, the depth-regrounding design in `work/archive/depth-regrounding/`),
folding to `work/archive/` with it — not in a root directory of their own (the old root `research/` was dissolved).
The decisions — settled cards on their nodes, archiving with the work — the spec, and the code stand
alone, so a clone is
self-sufficient: a standing artifact may *cite* provenance as a footnote, never *depend* on it (read
it at runtime, or pin acceptance to a section). That discipline retired the
bootstrap `rebuild-spec` scaffold and placed provenance on its node.
