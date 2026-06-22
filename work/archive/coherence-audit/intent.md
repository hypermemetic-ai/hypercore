---
kind: ask
state: folded
owner: operator
created: 2026-06-21
folded: 2026-06-21
---
# coherence-audit — the findings parked from the 2026-06-21 coherence pass

A coherence pass over the repo surfaced more than the structural smells the operator
acted on in the same conversation (the `thread`/transient reconciliation, the `hyper`→`engine`
rename, the `spec/` re-cut, the archive nesting). The findings below were **not** addressed
there and are held here so none is silently dropped — the intent's own discipline ("if it
doesn't matter enough for the operator to hear about it, it isn't a statement"; "inherited
debt is not carried"). Each is a separate sub-call; this node decomposes as they are taken.

## the plot-level call (the reason this audit ran)

- **The product soul is parked while the meta-layer compounds.** `intent.md` is mostly the
  operator product — the live interface, **continuous and concurrent autonomous work** (§work),
  the live conversation, the reasoning-visual key. The build (slices 1–14, item 2) has gone
  almost entirely into the self-build machinery. The single most distinctive promise — the
  scheduler cutting the next seam and a worker building it — is **unbuilt and unreachable from
  the interface**: `worker.run` and the whole `design.py` are called only by the acceptance
  harness, never by `window.py`. The operator can ratify work in the live system but nothing
  picks it up and runs it. (Verified 2026-06-21: `graph.standing()` *computes* the ready frontier —
  the half-bridge is built — but no loop **consumes** it, so a ratified ask lands as standing work
  and the system then idles. Run as-is, that is precisely the defect intent §60 names — "an idle
  system with unblocked work left is a defect, not rest" — built into the product.) This is the
  parked pi/OMP harness seam (role-assembly steps 5–6).
  **The decision owed: is the next arc more self-build, or the worker seam that makes the
  product *do* the thing?** That is an operator sequencing call, not a machine one.
- **No "live visual of a model's reasoning"** (intent §44) — unbuilt; only a thinking-spinner.
- **The conversation is one-shot** `claude -p` request/response, not the persistent "summon on
  the spot, answer lands while you watch" of intent §42. Partial against intent.

## naming / structure residue

- **`coherence` has no module — and the real seam is the shared model transport.** ADR 0013 carved
  `coherence` into its own capability but left its code in `conversation.integrate`. So `conversation.py`
  implements two carved-apart capabilities. But the continuation pass (2026-06-21) sharpened the
  framing: `grilling` only *looks* aligned. `grill.py` reaches back into `conversation`'s **privates**
  for the model transport (`conversation._claude`, `conversation._parse`), making the two import each
  other — a **circular dependency** (`conversation ↔ grill`). And it is not just those two: `worker`,
  `design`, and `grill` all call `conversation._claude` / `conversation._parse`, and `window`/`preview`
  read `conversation.MODEL_LABEL`. Five modules reach **past `conversation`'s public interface into its
  underscore internals** — textbook information leakage (`spec/depth.md`'s gravest red flag after
  shallowness). So `conversation.py` is silently the home of the un-named **transport** capability (the
  `claude -p` call, the JSON parse, the model identity). The deep-module move dissolves both questions
  at once: pull the transport into its own small module; then `conversation`, `grill`, `design`,
  `worker`, and a clean new `coherence` module each depend *downward* on it — no circular import, no
  reaching through privates, and coherence carves cleanly because the only thing that blocked it was the
  same plumbing. Decide: carry it, give coherence its own module, or (recommended) name the transport.
- **`operator view` vs `operator brief`** — the glossary's own flagged-open name (it now carries
  the authored vision too, so "brief" may be wrong). Unresolved.

## hand-maintenance drift (the system's own anti-pattern)

- **`README.md` carries hand-typed numbers that drift** ("157 checks green" no longer matches the
  live harness — verified 2026-06-21: the harness now runs **173**, so the gap widened, and the
  README was hand-updated as recently as the last commit without catching it). For a
  derive-don't-hand-maintain system, the README is the one large hand-kept artifact. At least the
  check count could be rendered, not typed.
- **The `CLAUDE.md` symlink lives on in the prose after the code dropped it** (new, 2026-06-21).
  ADR 0009 §4 was *amended* — the `CLAUDE.md → AGENTS.md` symlink is dropped as redundant; one
  `AGENTS.md` serves both roles — and the code obeys (`anchor.py` writes only `AGENTS.md`, no symlink;
  no `CLAUDE.md` on disk; the harness even asserts "no `CLAUDE.md` is materialized"). Yet three
  artifacts still describe the symlink: `README.md` (twice — "symlinked as `CLAUDE.md`", lines 51 and
  61), the **`channels.py` docstring** (lines 19–20, source code describing the opposite of what its
  own registry does), and this very audit node's earlier draft (the generated-channels item below listed
  `CLAUDE.md`). The docs contradict an amended ADR, the implementation, and a green check at once —
  the exact hand-maintenance drift the system names as its own anti-pattern.
- **Stale docstrings/refs**: `check/harness.py` says "slice1 … slice7" with 14 slices present; the
  `role-assembly` arc's folded-history cites `engine/depth.py`, retired by ADR 0019 (history, kept as
  written). (`depth.py`'s own `aposd.md` ref is moot — the module was deleted in the depth normalization.)
  Add (2026-06-21): `conditions.py:48` cites "the 6,348-line `window.py` it exists to catch early" as
  live rationale, but that god-file was the *prior epoch's* (torn down 2026-06-20); this repo's
  `window.py` is 274 lines. Reads as a claim about the current file — it is a cautionary tale about the
  old one. A motivating anecdote, not a false as-built claim, but it mis-points a reader who greps.
  Add (2026-06-21): `methodology.py:65` — the `skill()` docstring says single-sourced from
  `spec/<cap>/spec.md`, the **retired folder-form** spec path (flattened to `spec/<cap>.md` by ADR
  0014/0018; commit efe8cf9). The code reads `spec.cap_path` = `spec/<cap>.md`, and the same function's
  rendered output (line 78) says `spec/<cap>.md` — so the docstring contradicts its own function body.
- **A brittle worker-grounding check**: `slice4` asserts `"import " not in` the worker prompt as a
  code-leak proxy, so ADR prose that mentions "import" trips it (ADR 0015 did, and was reworded). The
  check guards a real invariant by a fragile substring — it wants a sturdier signal.
- **`design.py` is real but orphaned** — reachable only from `slice8`. Either the worker seam wires
  it, or it is dead-from-the-operator engine code to mark as parked.

## spec ⇄ code mismatch (continuation pass, 2026-06-21)

- **A dead state in the core model: `graph.PENDING`.** `graph.py:36` defines `PENDING = "pending"`,
  commented "a grilling question waiting its turn (held in grilling.md)" — but **no path produces or
  reads it** (verified: the only occurrence is its own definition). It is a vestige of the
  pre-Design-B model where each grilling question was its own node; Design B (ADR 0011) made the pass
  durable *inside* `grilling.md` (a `surfaced` index), so questions are no longer nodes and need no
  state. The comment describes a model the system abandoned. This violates intent's own §work rule —
  "[a kind] stays only while a statement reads it" — applied to states. Cut it (and its comment).
- **The fold's "atomic, both directions" is an overclaim against the code.** `self-model.md` requires
  folding to apply the delta "atomically, both directions" — "the spec is never merged unless the
  graph folds, and the graph never folds unless the delta merges" — and `delta.py`/`conversation.py`
  echo it ("one act", "archive ⟺ fold, one act"). The implementation is **three sequential commits**:
  `delta.fold` (spec files + channels) → `graph.integrated` `_persist` (state=DONE) → `_fold` (move the
  folder to `archive/`). It guarantees one direction only — `delta.fold` checks-then-writes and raises
  `CannotFold` before touching anything, so *no graph folds without its delta merging*. The reverse is
  **not** structural: if any step after `delta.fold` fails, the spec is already merged while the graph
  is **not** folded (and since `folded` is read from *location*, a `state=DONE` graph still sitting in
  `work/` reads as un-folded). Worse, that partial state is not cleanly re-runnable: a retried
  `delta.fold` hits "ADDED requirement already exists" → `CannotFold`. Low operational stakes today
  (the integrate path is harness-only, never reached from `window.py`), but the spec asserts a
  transactional guarantee the code approximates sequentially. Either weaken the spec's wording to the
  honest "land-then-commit, best-effort" model the rest of the engine uses, or make the fold genuinely
  atomic (stage all writes, one commit, move-as-last-or-first with idempotent retry).

- **The operator view's per-capability vision is silently empty for the carved capabilities — via a
  hand-maintained map the module's own docstring disclaims.** `self-model.md` requires the operator
  view to render "the vision (authored, from `intent.md`) beside the as-built and the gap, **at every
  altitude**." But `view.py:27` slices the vision per capability through a hand-typed keyword map
  (`TERMS`) covering only 6 capabilities — `interface`, `graph`, `queue`, `conversation`, `self-model`,
  `worker`. The spec now has **12**. The six carved out after `TERMS` was written get no entry and fall
  back to matching their own bare name in `intent.md`, which mostly fails. Verified live: vision-slice
  counts are `architecture-review` **0**, `depth` **0**, `design-it-twice` **0**, `folding-conditions`
  **0**, `grilling` **0**, `coherence` **1**, `worker` **1** — versus 6 each for the mapped ones. So
  half the capabilities show as-built requirements with **no authored vision beside them**, reading as
  pure machine scaffolding with no operator backing — the opposite of the view's purpose. Two smells in
  one: (a) the requirement is degraded by construction for new capabilities; (b) `view.py`'s docstring
  claims "everything but the vision is derived here and now… never hand-tended," yet the vision *slicing*
  rides a hand-tended map that drifted — the system's own anti-pattern. The fix wants a derived mapping
  (a capability claims its own vision statements, e.g. via a marker or the grilling that carved it),
  not a keyword table a human must extend on every carve.

## generated-output-at-root legibility

- The root mixes authored source (`intent.md`, `spec/`) with **generated channels**
  (`skills/`, `AGENTS.md` — not `CLAUDE.md`; see the drift item above) with nothing marking which is
  derived. ADR 0014 deferred
  the channels' home to the harness seam. The `spec/` re-cut and the archive nesting tidy part of
  the root; whether the generated channels want a marked home is still open and tied to that seam.

## synthesis — the findings are a map, not a list (2026-06-21)

The operator asked the load-bearing question: would these have happened if the build had **followed
the methodology directly** — and can we tell? We can. The repo holds a clean natural experiment.

**The build never ran the methodology — at all.** Across the whole of git history there is **not one**
`grilling.md`, `delta.md`, or `RESULT.md` (only `spec/grilling.md`, the capability). Every folded graph
in `work/archive/` carries only an `intent.md` (+ hand notes). So no grilling pass was ever run, no
worker ever produced a result, no delta was ever folded through `delta.fold`. The spec, the engine,
the ADRs, the folds — **100% hand-authored.** A system whose thesis is "derive, don't hand-tend; run
work through the fold" was bootstrapped entirely by hand. The unbuilt worker seam (the plot-level
finding) is not a separate gap — it is *why* the build couldn't dogfood: there is no loop to run.

**But the experiment still resolves, because of the one mechanism that did run.** The fold's
derive-on-change render (`delta.fold → channels.materialize`) is deterministic, and someone ran it:
the committed `skills/` + `AGENTS.md` are **byte-identical** to a fresh re-render (verified). That is
the controlled comparison. Sort every finding by *how the methodology would enforce it*:

- **Mechanically derived-on-fold** (skills, the anchor): **zero drift.** The one surface with a single
  generating function wired to the fold is the one surface that did not rot — even though no real fold
  ever fired, because there is one canonical generator, not a transcription.
- **Hand-typed transcriptions of derivable facts** (README's `157`→now 173, the `CLAUDE.md` prose,
  the stale path/anecdote docstrings): every one drifted. The methodology's *mechanical* gates
  (delta-applies, red→green, length) do not police prose, comments, or READMEs, so **following the
  methodology as written would NOT have caught these** — only a manual coherence pass (this one) does.
- **Code-structure red flags** (`PENDING` dead, the `conversation` transport reached through privates +
  the `conversation↔grill` circular import, the `TERMS` hand-map): the mechanical gates miss these too
  (every offending file is under the length signal, every delta applies, every test is green). They are
  precisely the red flags `depth.md` enumerates — information leakage, dead/nonobvious code,
  comment-drift — i.e. the **model-driven red-flag scan `architecture-review.md` says is "not yet
  built."** So the methodology *names* the discipline that would catch them but has not *built* it.
- **Requirement prose over-claiming its scenarios** (the atomic-fold case): caught by nothing, because
  nothing checks that a requirement's prose is covered by its scenarios.

**So the answer to "can we tell": yes — and the finding is that hand-building did not *cause* the drift;
it *revealed* the shape of the methodology's enforcement.** hypercore has exactly **one** working
anti-drift mechanism (derive-on-fold), and it works perfectly. Every finding is a surface that
mechanism does not yet reach. Following the methodology directly would have prevented exactly the class
the methodology mechanizes — the class that already shows zero drift — and nothing else, because the
rest is assigned to judgment disciplines that exist only as prose and were never run.

### the structural solution (not N situational fixes)

Point the one proven mechanism at the rest, and make the spec'd-but-unrun disciplines actually run:

1. **Extend "derived, materialized on fold" to every remaining derivable surface.** The fold already
   owns a render registry (`channels.CHANNELS`). The README's mechanical facts (check count, slice
   status, the module map) and the operator-view vision binding (`TERMS`) are derivable — render them
   or assert them at fold, or (better, per ADR 0009's own ETH finding that files should carry only
   non-inferable content) **strip the restated facts from prose entirely** so there is nothing to
   drift. A derived `capability → vision` binding (each capability claims its intent statements, e.g.
   recorded by the grilling that carves it) replaces the hand-typed `TERMS`.
2. **Build the red-flag scan the spec already promises, wired as a folding condition / standing review
   output.** This is not new scope — `architecture-review.md` already owns it and marks it not-yet-built;
   the audit just produced its first test cases. Even a cheap mechanical subset — unused module-level
   symbols, cross-module access to `_private` names, doc/path references that do not resolve — would have
   caught 4–5 of these findings and would run every fold. Add a sibling check: every load-bearing claim
   in a requirement's prose has a scenario (or tighten the prose).
3. **Close the dogfooding loop — wire the worker seam (the root cause).** Until `worker.run →
   integrate → fold` runs per change, the judgment disciplines (grilling, depth, coherence) never fire
   and every invariant in classes 2–4 above is enforced only by occasional manual audits like this one.
   The cost of not dogfooding is now *measured* — it is this findings list — which is the strongest
   argument for sequencing the seam next. The deepest structural fix and the deepest product promise are
   the same act.

The through-line: the drift is not a quality lapse in the hand-build; it is the negative image of where
derive-on-fold has not been pointed. The system proved the mechanism. The work is to generalize it and
to build the loop that runs the disciplines instead of merely writing them down. [machine]

## next steps — moves 1 and 2 (handoff, ratified 2026-06-21)

The operator ratified moves 1 and 2 of the structural solution above (move 3, the worker seam, stays
the parked plot-level sequencing call). A fresh session should read this file top to bottom — the
findings (both passes), the synthesis (the natural experiment + why these are one structural call), then
execute the two slices below. Everything needed is here; the conversation that produced it is disposable.

**Framing the two moves (do not lose this distinction).** Move 1 is **prevention** — *remove* a
hand-maintained surface so nothing can drift. Move 2 is **detection** — *scan* for the drift that
can't be derived away, and fail the build on it. Move 1 has two patterns per surface: **(A) derive it**
(generate from the single source, ideally on fold via `channels`, the way `skills/`+`AGENTS.md` already
are — the one zero-drift surface in the repo), or **(B) delete the restatement** (drop prose that merely
repeats a derivable fact; keep only the non-inferable — ADR 0009's own ETH finding, turned inward).

### recommended sequencing — build move 2 first, for a real red→green loop
Build move 2's scan first: it goes **red** on the live findings (dead `PENDING`, the `_private`
cross-access, the dangling path refs). Then apply move 1 + the ride-along cleanup: the scan goes
**green**. That red→green is a genuine feedback-loop record — and would be the **first actual use of the
methodology's feedback-loop discipline in the repo's history** (no `RESULT.md`/`delta.md` has ever
existed). Record it as such: this slice is where the build first dogfoods, in miniature.

### MOVE 2 — the red-flag / coherence scan the spec already owns (build first)
Not new scope: `architecture-review.md` already owns the "model-driven red-flag depth scan" and marks
it **not-yet-built (ADR 0006)**. This audit produced its first test cases. Build a cheap mechanical
subset in `engine/review.py` (the standing scan), surfaced in the deepening backlog / operator-view gap,
and wired into `python3 -m engine --check`; consider also a `folding-conditions` gate so it bites on fold.
- **dead module-level symbols** (defined, never referenced across the package) → catches `graph.PENDING`.
- **cross-module access to another module's `_private` names** → catches the `conversation._claude/_parse`
  leakage and flags the `conversation↔grill` circular import (depth.md's "information leakage").
- **doc/path references that don't resolve** — paths named in docstrings/markdown that don't exist on
  disk → catches `methodology.py:65` (`spec/<cap>/spec.md`), the README/`channels.py` `CLAUDE.md` refs,
  the `conditions.py` 6,348-line anecdote.
- *(phase 2)* **requirement prose ↔ scenario coverage** — every requirement has ≥1 scenario; flag prose
  claims with no scenario (the atomic-fold overclaim). 
- **Folding condition:** the scan runs in `--check`; on a clean tree it reports the current known
  instances (red), and after move 1 + cleanup it reports none (green); a newly introduced instance of
  any rule is caught by the scan going red. The red→green record is the slice's feedback loop.

### MOVE 1 — remove the hand-maintained derived surfaces (prevention)
Two structural surfaces (these keep drifting), plus one-time ride-along cleanup.
- **README live numbers → Pattern B.** Drop `157 checks green` (and any hand-typed count/status that
  restates a harness fact); point to `python3 -m engine --check` as the single source. Keep only
  narrative that is non-inferable. *(Pattern A fallback: a fold/`--check` step that rewrites the count.)*
- **`view.py` `TERMS` → derive the `capability → vision` binding from one source.** The binding (which
  `intent.md` statements a capability realizes) must not live as a hardcoded keyword table. The *source*
  of the binding is itself a small **design-it-twice-worthy** decision — sketch ≥2 shapes before
  committing: (i) each capability **spec file declares the vision it realizes** (authored at carve /
  grilling time — the binding lands with the as-built, where it belongs); (ii) semantic match at render
  time (derived, but non-deterministic); (iii) a marker on intent statements (couples vision to as-built
  structure — likely wrong, the system separates them on purpose). Lean: (i). Honest benefit to bank: a
  pure-machinery capability (`folding-conditions`, `architecture-review`) then correctly shows **no**
  vision, distinct from a bug — today they're indistinguishable.
- **Ride-along one-time cleanup** (pure restatements / dead code — Pattern B, fix in the same arc):
  the `CLAUDE.md` symlink refs (README ×2, `channels.py:19-20` docstring, and this node's earlier draft),
  the stale docstrings (`methodology.py:65`, `harness.py` "slice1…slice7", `conditions.py:48` anecdote),
  and dead `graph.PENDING` + its comment. Move 2's scan should turn green precisely as these land.
- **Folding condition:** no hand-typed restatement of a derivable fact remains in `README.md` or
  `view.py`; the operator view yields a `capability → vision` binding derived from source (verified by a
  test that a newly-added capability gets its vision with no edit to `view.py`); move 2's scan is green.

### what this arc deliberately does NOT do
Move 3 (wire `worker.run → integrate → fold` to the interface — the autonomy seam) stays parked as the
operator's sequencing call. The atomic-fold overclaim is recorded but only its scenario-coverage flag
(move 2 phase 2) is in scope here; making the fold genuinely transactional is its own later ask.

## folding condition

Each finding is either resolved by a delta/ADR or consciously deferred with a recorded reason on
its node — none silently dropped. The plot-level sequencing call is the operator's and folds when
they make it; the residue items fold as they are taken or explicitly parked. The synthesis above
reframes the whole set as one structural call (generalize derive-on-fold; run the disciplines); it
folds when the operator rules on sequencing it against the worker seam. [machine]

## result — folded (2026-06-21)

The operator ratified moves 1 and 2 and chose to **name the transport**. Both moves are built and the
acceptance harness is green (`python3 -m engine --check`). This is the repo's **first red→green dogfood**
of its own feedback-loop discipline — no `RESULT.md`/`delta.md` had ever existed.

**The red→green loop (the slice's feedback record).**
- command: `python3 -m engine --check`
- red: `slice15` — "the real engine tree carries no mechanical red flags" — FAILED, found
  `['graph.PENDING', 'render.Span', 'delta.load', 'conversation ↔ grill']` (the move-2 scan, built
  first, going red on the live findings).
- green: after move 1 + the ride-along + naming the transport, the same assertion PASSES — the scan
  reads a clean structural tree. `slice15`'s green half is kept as the standing assertion.

**What landed (ADR 0020, ADR 0021).**
- **Move 2** — the mechanical red-flag scan in `engine/review.py`: dead module-level symbols and
  circular dependencies, read live, surfaced in the operator-view gap, asserted by `engine/check/slice15`.
  Two of the audit's three proposed rules were dropped after a measured false-positive analysis — the
  blanket `_private`-access rule fires on six de-facto-shared package internals (`graph._root` and kin);
  the dangling-path rule fires on runtime/retired/relative paths — recorded in ADR 0020. The model-driven
  *verdict* (shallow module, leakage, deletion test) stays judgment, not-yet-built.
- **Move 1** — the README check count dropped (`--check` is its single source); the operator-view vision
  became a **per-capability declared binding** (`<!-- vision: ... -->` in each spec slice), retiring the
  hand-typed `view.TERMS` map. `engine/check/slice2` asserts a newly carved capability gets its vision
  with no edit to the view, and a pure-machinery capability correctly shows none.
- **Transport named** — `engine/transport.py` (the `claude -p` call, the JSON read, the model identity),
  dissolving the `conversation ↔ grill` cycle and the five-module reach into `conversation`'s privates.
- **Ride-along** — dead `graph.PENDING`, `delta.load`, `render.Span` cut (the last two found by the scan
  on its first run, missed by this hand-audit); stale docstrings fixed (`methodology` spec path, the
  harness slice range, the `conditions` length anecdote framed as the prior epoch's god-file); the
  dropped-`CLAUDE.md` symlink prose removed from the README and `channels`.
- **Spec made as-built** — `architecture-review.md` (the mechanical red-flag subset is built; the verdict
  not), `self-model.md` (the vision is a declared binding); the requirement↔scenario coverage floor (≥1
  scenario per requirement) is enforced by the harness (`slice2`).

**What is parked (consciously deferred, not dropped).**
- **Move 3 — the worker seam** (`worker.run → integrate → fold` to the interface): the operator's
  sequencing call, tracked in `work/role-assembly/`. The single largest finding; the autonomy unlock.
- **The atomic-fold overclaim** (`self-model.md`'s "atomically, both directions" vs the three sequential
  commits): the mechanical floor (≥1 scenario per requirement) is enforced, but the prose-vs-scenario
  *overclaim* is judgment (the not-yet-built model-driven scan); making the fold transactional is its own
  later ask.
- **`design.py` orphaned** (reachable only from `slice8`): tied to the worker seam (move 3); the scan
  does not flag it dead because the check references it.
- **The brittle `"import "` substring checks** (`slice4`, and its twin in `slice6` which this arc
  surfaced): recorded; a sturdier code-leak signal is a later ask — this arc only worded around `slice6`.
- **Coherence's own module**: the real blocker (the shared transport) is named; coherence stays a
  rendered capability with its judgment in `conversation.integrate`. The operator's chosen resolution was
  naming the transport; a further `engine/coherence.py` extraction is optional, not required.
- **`operator view` vs `operator brief`** naming (the glossary's flagged-open name): unresolved.
- **Generated-output-at-root legibility** (marking which root files are derived): tied to the channels
  home (ADR 0014), still open.
- **The product-soul gaps** — no live visual of a model's reasoning (intent §44); the one-shot
  `claude -p` conversation vs the persistent live conversation (intent §42): unbuilt, not in this arc.

Every finding above is resolved (ADR 0020/0021) or parked with a reason — none silently dropped. The arc
folds. [machine]
