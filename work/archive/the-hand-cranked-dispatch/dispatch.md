# the hand-cranked dispatch — the open work, ordered

*Snapshot 2026-06-27. Machine-owned. Not the live schedule — the system reads the order off the tree
each time; this is a frozen photograph for observation (see `intent.md`). Twelve open nodes, all leaves,
no open children.*

*"Hand-cranked" names the **order**, computed by hand here as a learning snapshot — never the **work**.
The work is executed by the orchestrator (`engine/schedule.py`'s `Scheduler`, driven watchably via
`.claude/commands/dispatch.md`): a Claude architect and codex workers, each fenced, run from a higher
thread. An assistant that builds these items by hand in one thread collapses the role split and
overflows its context — exactly the failure this snapshot must not invite.*

> **Update — 2026-06-27, after the first live crossing.** #1 `the-view-reads-through-the-tree` folded
> (a correctness fix), and #3 `the-candidate-prompt-speaks-as-the-architect` folded as the **first live
> fenced codex crossing** on this tree — the de-risk run. That run surfaced two defects in the dispatch
> *machinery itself*, now filed as their own asks and slotted **next, ahead of #2** (entries `A`/`B`
> below): `A` the auto-composed `fold:`/`dispatch:` commit subject is mangled, corrupting the
> operator-facing record of every crossing; `B` the live-run gate never flips on a fenced crossing, so
> #11's evidence stays keyed to an autonomous-run trace `worker.run` never writes. The de-risk run paid
> for itself — these were caught cheap before they reached a high-stakes node. The rank-2..12 entries are
> otherwise unchanged; this is annotation, not a re-crank.

> **Update — 2026-06-27, second pass.** `A` `the-fold-commit-speaks-faithfully` folded — its fix proved
> itself on its own faithful fold commit. Driving `A`/`B` by hand surfaced more machinery debt, now
> handled three ways. The **dispatch command** (`.claude/commands/dispatch.md`) was hardened directly:
> background-and-reap the ~20-min build (a synchronous Bash call hits the tool's ~10-min ceiling and
> strands the node; a raw `nohup` is untracked); classify a *raised* crossing as `failed` with no card,
> distinct from a carded `escalated`; confirm a crossing dead before touching its fence; judge de-risk by
> the archive, not the broken `never-run-live` gate. And two **engine** defects were filed as their own
> asks, slotted **ahead of `B` and #2**: `T1` `the-fold-s-re-verification` — the fold keystone's
> 180s-per-capability re-verify timeout silently reclassifies a slow run as a broken build, on the path
> of every code fold and not scaling with the scenario count; `E1` `worker-run-is-not-total` — a
> hand-driven `worker.run` that raises leaves no decision card (only the scheduler raises it), so the
> node silently re-readies and invites a blind retry. **Corrected next-up: `T1` → `E1` → `B` → resume
> the sweep at #2** — clear the dispatch-machinery debt before the substantive sweep so each crossing
> runs reliably. Grounds for `T1`/`E1` live in their own `intent.md`; route for each: `grilling` →
> `design-it-twice` → fenced build → `coherence`.

## the criterion

Ordered as the system orders: **what the operator's attention is worth next** — the cost of each item's
delay, measured by *what it blocks* and *what compounds while it waits* (intent §59, §66) — gated by
**readiness** (standing, folding condition named, nothing open beneath — `spec/schedule.md`) and bounded
by **composition** (two fenced workers that edit one engine file, or co-MODIFY one spec requirement,
clobber each other at integrate; they must serialize or each touch a *distinct* requirement —
`work/worker-builds-proposed-delta`).

Two of the twelve outrank the rest because their cost of delay is *correctness*, not friction: a latent
bug already returning wrong answers (#1) and a silent hole in the system's central trust claim (#2). The
middle band is per-episode compounding (prompt drift and fat) and structure-honesty refactors. The tail
is large, mostly-architect-authored, or dependency-gated work that blocks nothing downstream.

## how the orchestrator drives this

The orchestrator (`.claude/commands/dispatch.md`) consumes this snapshot; nothing here is executed by
hand. These are the grounds it drives by — the per-node detail below is read by the orchestrator, not by
a single assistant building in one thread.

- **Each item is its own crossing, in its own thread.** The architect (Claude) grills the node and
  authors the delta **and** the scenarios; a fenced **codex** worker only *applies* the
  architect-proposed delta (`spec/worker.md`, `work/worker-builds-proposed-delta`). Never let the side
  that builds a check also author it. The build runs in the worker's process, the integrate in the
  architect's — neither enters the orchestrator's context.
- **Route names what the architect loads.** Each **route** names the skills the architect's grilling
  pass loads first (`skills/<name>/SKILL.md`) — from the skill, not from memory.
- **The gate is the loop.** For any touched capability the fold gate runs its `#### Scenario:` checks
  **red at the fork base, green at the tip** (`spec/self-model.md`, the scenario gate);
  `python3 -m engine --check` is that loop.
- **design-it-twice before a line is built.** An item marked **design-it-twice** gets an isolated
  candidate contest first; the architect picks on depth, locality, seam placement and records the
  decision as material on the contest node.
- **Serialize where the conflict map says so.** Two fenced workers touching one `engine/*.py` file or
  one spec requirement churn at integrate — the scheduler honors no conflict map, so the orchestrator
  serializes within each file-contention group below and runs only the parallel-safe singles
  concurrently.
- **The flagged facts (⚑) are the first move of grilling.** They are real unknowns this snapshot could
  not settle, not rhetorical hedges — the architect resolves each in the node's grilling pass before its
  worker is dispatched.

## the dependency & conflict map

**Sequencing edges** (do the left before the right):

- `first-live-fenced-run` → `#11` — #11's de-inlining is gated on **watched evidence** that a live
  worker loads its skills and completes a build in the fence. That evidence is **not yet recorded**
  (`view._live_status` reads `never-run-live`). The codex-in-fence transport it rides is already landed
  (resolved at #12), so this gate is the live run, not the code.
- `#7 worker-prompt-leads-with-the-task` → `#11 worker-disciplines-become-a-loadable-skill` — sharpen
  the prose and reorder the prompt before moving the channel (#11's own note).
- *(no `operator-view-readiness → #2` edge — it was a candidate dependency, since dissolved.)* The
  proposer↔view coupling was **settled in the `operator-view-readiness` grilling pass (2026-06-26): #2
  carries no view precondition.** The "what's building and why" legibility is a standing-work-surface
  concern homed by intent §58/§60, not a blocker on #2. #2 is unblocked.
- the depth pair is ranks **8 and 9** (`the-model-driven-depth-scan` ↔
  `the-neighborhood-aware-depth-assessment`) — co-design one shared depth-assessment seam (one
  criterion, two scopes), do not build twice.

**File-contention groups** (concurrent fences here would clobber — serialize within each group):

- `engine/worker.py` + `spec/worker.md`: #2 (builds-proposed-delta), #7 (prompt-leads), #11
  (disciplines-skill). Each must touch a *distinct* requirement; the engine-code edits to `worker.py`
  still serialize.
- `engine/conditions.py`: #5 (vocabulary-own-module), #6 (provenance-leaves-leaf), #9
  (neighborhood-aware, which retypes `conditions.unmet`). Serialize.
- `engine/communication.py`: #4 (architect-prompts-route), #9 (neighborhood-aware render), #10
  (communication-mastery, caveat-survival on the integrate path). Serialize; #9 and #10 both touch
  `communication.integrate`.
- `engine/design.py`: #4 (architect-prompts-route, `design.SELECT`), #3 (candidate salutation,
  `design.CANDIDATE`). Serialize.

**Parallel-safe singles** (touch files nothing else open touches — run anytime, concurrently):

- #1 `the-view-reads-through-the-tree` — `tree.py` / `view.py`.
- #12 `weak-model-loop-harness` — its codex-in-fence prerequisite is already landed; the remaining
  campaign runs on disposable clones and touches no shared engine file.

---

## the order

*Two entries (`A`, `B`) were inserted at the head 2026-06-27, surfaced by the first live crossing and
slotted ahead of #2 at the operator's word. The original rank #1–#12 numbering below is preserved; #1 and
#3 are now folded (struck through), and so is `A` (see the second-pass update above). "Next up" =
`T1` → `E1` → `B` → resume the sweep at #2 — the two new machinery asks (`the-fold-s-re-verification`,
`worker-run-is-not-total`) lead; their grounds are in their own `intent.md`, not duplicated here.*

### ~~A. the-fold-commit-speaks-faithfully — fix the record before it corrupts #2~~ ✓ folded 2026-06-27 (fix proved on its own faithful fold commit)

**Why here.** The first live crossing's fold and dispatch commits came out mangled
(`fold: # the-candidate-prompt-speaks-as-the-architect — t → channels`): the `# ` heading leaks, the
summary collapses to one char, the capability defaults to `channels`. The fold commit is operator-facing
provenance and **every** fenced crossing inherits the defect — #2's record included. Cheap, contained,
and it cleans the record before more crossings write to it.

- **route:** `writing-for-the-machine` → fenced build → `coherence`.
- **grilling / readiness:** ⚑ fix on the *delta* (a trivial delta still carries an architect-authored
  subject + capability, so the fallback never fires) vs harden `tree._subject` (strip `#`, cut on a word
  boundary) vs both; ⚑ whether a code-only delta should attribute a capability at all, or
  `channels`-as-sentinel is itself the smell.
- **build:** the composed `fold:`/`dispatch:` subject of a fenced crossing strips the heading marker,
  carries a real summary, and names the capability the fold routed to (`delta.py:245`, `tree.py:182,244`).
- **compose:** touches `delta.py` / `tree.py` — currently parallel-safe, but **re-check against #6**
  (`provenance-leaves-the-leaf` also moves through `delta.py`); serialize if both are in flight.
- **fold:** a fenced crossing's commit subject reads faithfully; a red→green scenario locks it; `--check`
  green.

### B. the-live-run-gate-sees-the-crossing — unblock #11's evidence (next up)

**Why here.** The first live crossing folded green, yet `view._live_status` still reads `never-run-live`:
the gate keys on a `*.verdict.md` that only watched mechanisms write, never `worker.run`. So #11 stays
gated no matter how the loop is driven — its evidence is keyed to an autonomous-run trace the dispatch
path never produces. A genuine model error in the evidence seam, and the live blocker on #11.

- **route:** `grilling` (the fenced-vs-autonomous fork) → `design-it-twice` (the trace seam) → fenced
  build → `coherence`.
- **grilling / readiness:** ⚑ the load-bearing fork — does "live-run" mean *fenced* (codex built it) or
  *autonomous* (the machine self-dispatched, no operator in the loop)? #3 was fenced-but-operator-driven;
  whether that flips the gate is the decision #11 hangs on. ⚑ does `worker.run` write the verdict trace,
  or does the gate split into two distinct signals.
- **build:** a fenced `worker.run` crossing leaves a durable trace the live-run gate reads; the dispatch
  command's Step 3 and this snapshot's #11/#12 claims are corrected to match (`view.py:102-111`,
  `worker.run`, `provenance.commit_verdict`).
- **compose:** touches `view.py` / `worker.py` / `provenance.py` — `worker.py` group (serialize with #2,
  #7, #11). **Sequence before #11** — it is #11's evidence gate.
- **fold:** a fenced crossing flips the live-run signal; #11's gate reads true evidence; `--check` green.

### ~~1. the-view-reads-through-the-tree — fix the bug first~~ ✓ folded 2026-06-27

**Why here.** The only item already returning *wrong answers*: two readers disagree on what counts as
open work (`tree.work()` vs `view._open_work`), and one reader trusts a `state:` field that is stale
across ~half the archive. Cost of delay is silent incorrectness in the operator's own gap view. Nearly
independent of every other open node, so it costs the contended files nothing to start now.

- **route:** `depth` → `design-it-twice` (light) → fenced build → `coherence`.
- **grilling / readiness:** residue is small and already leaned. ⚑ Decide: drop the `state:` field from
  the schema (lean **drop** — `Node.folded` ignores it, one less denormalized copy) vs normalize it at
  `_fold`. ⚑ Confirm no second work-tree walker survives (the `audit.py:91` and `review.py:206` `os.walk`
  are over *different* trees and correctly stay).
- **design:** one load-bearing seam — `read_tree(root=None)` threaded through `_scan`, vs threading
  `root` through a shared engine context. Lean the former; a single light contest settles it.
- **build:** add `read_tree(root=None)`; delete `view._open_work` / `_done` / `_intent_subject` /
  `_has_watched_trace`'s hand-walk; have the view consume `Node` objects. Removes the `os.walk`, the
  git shell-out from the presentation layer, and the open-work divergence in one move.
- **compose:** parallel-safe single. Conflicts with nothing open.
- **fold:** one reader for the work tree; `Node.folded` the only arbiter of foldedness; `--check` green.

### 2. worker-builds-proposed-delta — close the trust hole

**Why here.** The system's whole self-verification rests on one claim — the builder never authors the
oracle that clears its own fold. A node reaching a worker with **no** architect-proposed delta defeats
it silently: the worker authors its own scenarios. It triggers invisibly on every below-floor ask and
every hand-authored standing node. Cost of delay is a standing integrity risk that compounds with every
autonomous dispatch.

- **route:** `grilling` → `design-it-twice` → fenced build → `coherence`.
- **grilling / readiness:** the view-first lean is **resolved — no view precondition** (settled in the
  `operator-view-readiness` grilling pass, 2026-06-26): the proposed-plan legibility is homed in the
  standing-work surface (intent §58/§60), so #2 holds behind nothing. (The "lean view-first, not
  settled" note still on `worker-builds-proposed-delta/intent.md` is now stale — worth pruning.)
  Distinguish a delta *never proposed* (the bug) from one the architect proposed and judged *trivial*
  (`delta.Delta.trivial`, a valid no-op).
- **design:** load-bearing — *where* the guarantee "a worker only ever applies an architect-proposed
  delta" is enforced. Candidate seams: the grilling pass (`grill.consider`/`products`), the readiness
  predicate (`tree.ready`), the worker boundary (`worker.run`/`context`). Contest them; the
  author-from-scratch fallback must become *unreachable and deleted*, not guarded.
- **build:** delete the author-from-scratch branches in `worker._touched` / `worker.prompt`; ensure every
  buildable node carries an architect-proposed delta whatever door it entered. Scope precisely: a worker
  authors no *delta*; it may still author *fixtures* (that adequacy belongs to the folded
  `gate-vouches-for-the-new-verb`, parked per the operator).
- **compose:** `worker.py` group — serialize with #7 and #11. **ADD** its own requirement to
  `spec/worker.md` (two MODIFYs of one requirement clobber).
- **fold:** a no-delta node surfaces and builds nothing; the fallback is gone; `--check` green.

### ~~3. the-candidate-prompt-speaks-as-the-architect — the one-line correction (best first watch)~~ ✓ folded 2026-06-27 (first live crossing — surfaced A & B)

**Why here.** Low cost of delay (a salutation contradicts the seat: `design.CANDIDATE` opens "You are a
hypercore worker" but runs on the architect transport). It ranks low — but it is the **recommended first
observation**: a below-floor, single-edit ask that runs the full grill→apply→fold cycle in one pass with
nothing to design, so the operator sees the whole machine turn over once on something safe.

- **route:** (below-floor — files straight to work) → fenced build → `coherence`.
- **grilling / readiness:** none needed; folding condition already named. Trivial delta.
- **design:** none.
- **build:** the candidate-design prompt's salutation names the architect; the transport stays `call`,
  unchanged; the "like workers" similes in the module docstring stay.
- **compose:** `design.py` group — serialize with #4.
- **fold:** salutation matches the seat; `--check` green.

### 4. architect-prompts-route-to-skills — stop the architect prompts drifting

**Why here.** Per-episode drift risk: the architect's prompt constants restate, in less-faithful form,
disciplines already single-sourced in `spec/<cap>.md`, and no prompt ever points at a skill, so the
on-demand specialization is never loaded. Safe to land **today** — the architect is Claude Code, which
discovers `.claude/skills/` natively (unlike the worker, whose skill-load is still watched: see #11).

- **route:** `writing-for-the-machine` → fenced build → `coherence`.
- **grilling / readiness:** light; ⚑ decide what minimal task/material stays inline (the digest, the
  contract, the report, the ask, the reply envelope) vs what moves wholly to the skill.
- **design:** none load-bearing.
- **build:** each architect per-episode prompt **instructs the model to load its skill** and carries no
  hand-authored restatement of that skill's methodology; the structured reply envelope each prompt
  declares is unchanged.
- **compose:** `design.py` group (serialize with #3) and `communication.py` group (serialize with #9,
  #12). Touches `communication.py`/`grill.py`/`design.py` prompt constants.
- **fold:** no architect prompt restates a discipline its skill single-sources; reply envelope intact;
  `--check` green.

### 5. the-vocabulary-gate-is-its-own-condition — one module per condition (clean extraction)

**Why here.** Structure honesty, low risk, contained. A ~77-line glossary-consistency gate is inlined in
`conditions.py` against the codebase's own one-module-per-condition pattern (the scenario gate, provenance,
delta each got a module; vocabulary alone is a bolt-on with dead `result`/`node` parameters). This is
`spec/depth.md`'s special-general mixture verbatim.

- **route:** `depth` → fenced build → `coherence`.
- **grilling / readiness:** ⚑ decide whether `vocabulary.py` owns only the gate or also the
  glossary-corpus assembly it reads (lean: own the corpus reader too, so no second reader appears); ⚑
  folding-condition-only vs also feeding a standing scan (the watched half at `conditions.py:159-178`,
  which would mirror the architecture review's shape).
- **design:** none load-bearing beyond the cut above.
- **build:** extract the gate (`conditions.py:149-225`) into `vocabulary.py`; `material_unmet` calls it
  as it already calls `provenance` and `delta.check`; drop the dead `result`/`node` parameters.
- **compose:** `conditions.py` group — serialize with #6 and #9. **ADD** a requirement to the touched
  capability rather than co-MODIFY the folding-conditions requirement.
- **fold:** `conditions.py` coheres around the length/depth signal alone; `--check` green.

### 6. provenance-leaves-the-leaf — make the layer visible in the graph

**Why here.** Architectural legibility: `provenance` reads as an L0 leaf but is a top-of-stack fold gate;
its true layer is hidden because five imports are deferred inside functions to dodge a `conditions ↔
provenance` cycle. The no-static-cycles property holds only on import-timing band-aids. Refactor, not a
behavior change — but it needs a real design for the cut.

- **route:** `grilling` → `design-it-twice` → fenced build → `coherence`.
- **grilling / readiness:** ⚑ the exact cut of the `ledger` leaf — does it own both the accepted-length
  record's read *and* the commit-attest, or only the read with the write staying on `conditions.accept`;
  ⚑ whether the `delta ↔ scenario` deferred back-edge (`delta.py:226`) is dissolved in the same pass or
  left as one localized edge.
- **design:** load-bearing — the seam of the new `ledger` leaf both modules import downward. Contest the
  cut; the result must keep the cycle scan green *by construction* (the graph is acyclic because the seam
  points one way, never because an import is deferred).
- **build:** extract the shared accepted-length ledger into a small lower leaf `ledger`; `provenance` then
  imports `conditions`/`scenario`/`tree` at module scope and lands at its true layer; `conditions →
  provenance` disappears; the deferred `import provenance` sites become real static edges.
- **compose:** `conditions.py` group — serialize with #5 and #9. Touches `provenance.py`, `scenario.py`,
  `delta.py`.
- **fold:** `review.red_flags` cycle scan green by construction; `--check` green.

### 7. worker-prompt-leads-with-the-task — lead with the mission, sharpen the prose

**Why here.** Per-episode compounding: the worker reads its ask *last* (position five, after ~2,240
tokens of disciplines and ~1,481 of depth standards), spending its freshest attention on the rulebook
before it learns the job. Safe today, contained, and the **prerequisite for #11**.

- **route:** `writing-for-the-machine` → fenced build → `coherence`.
- **grilling / readiness:** light; the reorder and the flagged sentences are already named.
- **design:** none load-bearing.
- **build:** the ask and its handed delta come right after the salutation; disciplines / record grounding
  / depth standards follow as "how you are held"; the reply envelope stays last (the transport's
  reason-first, format-last invariant). Rewrite the worker.md statements that trip the
  writing-for-the-machine signal — the 111-word sentence at `spec/worker.md:249` and the compound
  negation at line 43 — to one instruction per sentence, in positive form, **at the source**, so the
  sharpened prose flows into both the prompt and the rendered disciplines.
- **compose:** `worker.py` group — serialize with #2 and #11. ADD/MODIFY distinct requirements.
- **fold:** ask-before-disciplines, envelope last; flagged sentences no longer trip the signal;
  `--check` green.

### 8–9. the depth pair — co-design one assessment seam, two scopes

These two are **one design, two scopes**: build the depth judgment once and trigger it two ways. Grill
and run `design-it-twice` over them **together** — the alternative the nodes name is folding one into the
other; decide that first.

**8. the-model-driven-depth-scan** — *proactive, whole-tree.* hypercore's foundational standard is
depth, but its automated enforcement is only the mechanical subset (length signal, dead symbols, import
cycles); the model-driven verdict — *is this module actually shallow?* — is named "not yet built"
everywhere and emitted on every scan. Cost of delay is mostly reputational (the absence reads forever),
not operational.

- **route:** `grilling` → `design-it-twice` (with #9) → `architecture-review` → fenced build →
  `coherence`.
- **grilling / readiness:** ⚑ watched evidence (a model judgment no fixture can certify — likely a
  dedicated run leaving a trace the fold checks for presence, like vocabulary-check's watched half) vs a
  gated check; ⚑ standing-only vs also a per-fold condition; ⚑ how it composes with `review.py` and the
  per-fold depth condition in `conditions.py` with no second copy of the depth standard; ⚑ how a model
  judgment stays cheap enough to run live (the tree fits a context window).
- **build:** a standing scan reading the source tree for the depth red flags a model can judge but a tool
  cannot — shallow module, information leakage past the mechanical cycle, failed deletion test — surfaced
  as complexity debt beside the length and mechanical findings. It raises a finding for a judge; it never
  scores or certifies depth (no gameable metric). On completion, `review.py`'s unconditional
  `DEPTH_NOT_YET` line is replaced, and `depth.md` / `architecture-review.md` / `self-model.md` /
  `glossary.md` stop naming the absence.

**9. the-neighborhood-aware-depth-assessment** — *reactive, at the fold.* Today the depth gate raises a
bare template ("N lines, past the 400-line signal — re-cut / deepen / accept") that
`communication.integrate` forwards verbatim, collapsing the deliberation to shorten-or-accept. The
ratchet's purpose was the opposite: a length past the signal should *invite architectural reflection*.

- **route:** `grilling` → `design-it-twice` (with #8) → `communication` → fenced build → `coherence`.
- **grilling / readiness:** ⚑ how it composes with #8 — distinct asks sharing one seam vs folding in; ⚑
  the concrete seam the architect is fed (the standing review's rendered map + debt, plus the flagged
  file's content and diff) — it must *consult* the standing whole-tree read, not spin up a second scan; ⚑
  how the gate **types** its outcomes so only the escalating-guard decision (depth, and the vocabulary
  guard) triggers the assessment, never the flat refusals (delta-does-not-apply, provenance-no-trail),
  which must not be dressed as negotiable — `conditions.unmet` today flattens every unmet condition to
  one opaque string.
- **build:** on a depth-gate trip, the architect runs a reasoned depth/length assessment of the flagged
  file *read in its neighborhood* (callers, siblings, cross-module boundaries) and raises it **with a
  lean and a flip** in place of the bare template. The operator still settles (approve/cut/explain); the
  assessment informs, does not gate (the depth condition already holds the fold). Lean advisory prose,
  no extra watched-trace (the accepted-length record carries its own provenance).
- **compose (pair):** `conditions.py` group (serialize with #5, #6) and `communication.py` group
  (serialize with #4, #12 — #9 and #12 both touch `communication.integrate`). Touches `review.py`.
- **fold (pair):** one depth criterion, judged in one place, triggered two ways; the not-yet-built line
  gone; `--check` green.

### 10. communication-mastery — reground the clarity standard

**Why here.** Large, high-value, mostly **architect-authored** (the compression-spine reground lives in
the preamble, which the fold discards — `delta._apply` keeps PREAMBLE verbatim), so it is not a clean
fenced-worker job and blocks nothing downstream. Reground: clarity is *compression to a decoder the one
reader already runs*; jargon is the cheap encoder aimed at a private key (encryption wearing depth's
clothes), demoting the prior "expert-reader inversion" spine to a conditioned corollary.

- **route:** `communication` → `writing-for-the-machine` → (one fenced behavior) → `coherence`.
- **grilling / readiness:** findings already authored beside the node (`synthesis.md`, `research.md`,
  `draft-spec.md`). ⚑ preserve the just-folded vocabulary-check requirement (commit 54a116b) — edit
  around it.
- **division of labor (read before building):** **author directly** — the preamble spine, the two
  reframed clarity requirements (the second carrying the nested, named `reach for the shared symbol`
  directive with its before→after pair), and flip the `engine/check/scenarios.py` assertion that greps
  the skill for `"removal of scaffolding"` to the compression spine, or `--check` goes red. **Build
  through a fenced worker** — the one new BEHAVIOR: a **gated** caveat-survival requirement (a dropped
  load-bearing caveat is caught before it reaches the operator) with its red→green scenario and the
  engine seam on `communication.integrate` + `communication_world.py` verbs. The architect authors the
  scenario; the worker turns it green.
- **watched/gated split:** the routing is gated (a dropped caveat is provably caught against a scripted
  oracle); the entailment *verdict* stays watched/model-driven (`--check` is deterministic and
  in-process — a live NLI call can never be the gate).
- **compose:** `communication.py` group — serialize with #4 and #9.
- **fold:** regrounded preamble + two reframed requirements; the gated caveat-survival requirement lands
  red→green; the skill re-renders; `scenarios.py` asserts the new spine; eight-front provenance placed on
  the node; `--check` green.

### 11. worker-disciplines-become-a-loadable-skill — gated on watched evidence

**Why here.** The de-inlining is **gated** on watched, unproven evidence that a live worker reliably
loads its anchor and skills inside the fence — and that evidence is **not yet recorded**
(`view._live_status` reads `never-run-live`). The codex-in-fence transport is already landed (commit
`1d6285d`), so what blocks #11 is the first live fenced run leaving its trace, not any code. **Sequence
after #7.**

- **route:** `writing-for-the-machine` → `grilling` (the trust fork) → fenced build → `coherence`.
- **grilling / readiness:** ⚑ the stake-bearing fork — how far to trust codex's skill-load before
  dropping the inline hedge. Until the evidence lands, keep a minimal inline hedge rather than trusting
  an unproven load.
- **build:** register `worker` in `methodology.METHODOLOGIES` so `channels` materializes `worker/SKILL.md`
  from `spec/worker.md`; route the worker prompt to **load** its `worker`, `depth`, and
  `writing-for-the-machine` skills from its checkout; remove the inline re-send (or reduce to a minimal
  hedge once the evidence is recorded); relevance-filter the mechanism facts to the actionable ones;
  remove the double-render of `spec/worker.md`. Keep the whole-spec **index** (the cheap anti-myopia map).
- **compose:** `worker.py` group — serialize with #2 and #7; depends on #7 (sequence after) and on the
  #12 codex-in-fence evidence.
- **fold:** a `worker` skill materializes and is audited against the slice; the prompt loads it; the
  inline re-send is gone (or a minimal hedge); `spec/worker.md` renders once; `--check` green.

### 12. weak-model-loop-harness — the long pole, with a high-leverage prerequisite

**Why here.** A large research campaign (run the full loop under GLM-5.2 via codex-shim, capture per-run
evidence to direct methodology refinement) — last by scope and effort, blocking nothing downstream **as
a campaign**. Its codex-in-fence prerequisite is **already landed** (commit `1d6285d`: "worker runs on
codex, not omp — engine/codex.py + slimmed transport"); the production worker runs on codex, OS-fenced,
and the experiment env profile (`codex.experiment_provider`) is in place. So #12's first
folding-condition bullet is already met, and the worker cluster is **not** waiting on it. What remains is
the harness, the runs, and the per-run reports — and, as a by-product, the first live run produces the
watched evidence #11 is gated on.

- **route:** `grilling` → run the campaign → `coherence` per run.
- **grilling / readiness:** the spine is validated (2026-06-24, `setup-notes.md`): codex 0.142 speaks
  only the Responses API, synthetic speaks only chat-completions, bridged by codex-shim on
  `127.0.0.1:8765`. The engine override rides an env profile in `engine/codex.py` (extraction, not a
  transport ratchet), so production defaults never change.
- **build:** (codex-in-fence already landed) bring up the synthetic spine; drive the full loop
  end-to-end under GLM-5.2 on **disposable clones** (the live tree is never touched by a weak model)
  across a variety of asks; store a per-run report as material on the node.
- **compose:** parallel-safe single (`codex.py` / `transport.py`); the prerequisite gates #11.
- **teardown (scaffolding to clear on fold):** stop the codex-shim daemon; remove temporary
  permission allow-rules; the pipx install and `~/.codex-shim/models.json` stay or go at the operator's
  word.
- **fold:** the loop runs end-to-end under the weak model on disposable clones (codex-in-fence already
  landed); a detailed per-run report is captured on the node.

---

## the first watch — what to observe first (the learning recommendation)

Priority is not pedagogy. For *learning the dispatch shape*, watch a clean full cycle before a messy one:

1. **#3 the-candidate-prompt-speaks-as-the-architect** — below-floor, one edit, no design: the whole
   grill→apply→fold turn in a single pass.
2. **#5 the-vocabulary-gate-is-its-own-condition** — a clean extraction with a real (small) grilling
   residue and a depth rationale: shows the methodology doing actual judgment without high stakes.
3. **#7 worker-prompt-leads-with-the-task** — shows `writing-for-the-machine` reshaping prose at the
   source and flowing into a derived channel — the system's "derive, don't hand-tend" discipline live.

Then watch a **design-it-twice** item (#6 provenance-leaves-the-leaf, or the depth pair) to see the
candidate contest, and #2 to see how a genuine *decision* (where to enforce a guarantee) reaches the
operator.

## what would flip this order

- **If the autonomous loop is about to run for real** — #2 (worker-builds-proposed-delta) jumps to
  absolute first and hardens its view-first gate: every autonomous dispatch risks the self-judging
  defect, and its own note forbids deleting the fallback before the view shows the autonomy.
- **If operator attention is the binding constraint** — front-load the leaned, no-decision items (#1, #5,
  #7, #4, #3) to bank autonomous progress, and defer the design-heavy ones (the depth pair, #2, #6, #10)
  to the rate the operator can settle decisions.
- **When the first live fenced run lands** — #11 unblocks. Codex-in-fence is already in production, so
  the only thing between #11 and its fold is the watched evidence still open at `never-run-live`. A
  deliberate first run (or #12's campaign) flips #11 from gated to ready.
