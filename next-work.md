# next work

## Ratified — item 2, the assembly model (2026-06-21)

A second research pass validated the design against live sources (recorded in `research/assembly.md`
§8), and the operator **ratified the assembly model (ADR 0009)** with two amendments. The build is
now teed up; nothing below is open except the build itself.

- **Second pass — validated and sharpened.** The ETH Zurich study (`§4.5`'s [arXiv 2602.11988]) is
  real and its numbers hold (LLM-generated files −3% success/+20% cost; human-written +4%/+19%, "no
  gain for Claude Code"); its recommendation is *sharper* than "minimal" — **non-inferable details
  only** (the check command, custom build commands), no overview prose, since files "do not function
  as effective repository overviews." Skills + progressive disclosure are an open cross-vendor
  standard; the AGENTS.md-vs-skill division of labor is field consensus. Both back the design.
- **Amendment 1, made then withdrawn same day — the full scan stays whole (operator's coherence
  call).** First amended to just-in-time (preload a capability index + touched slices, pull the rest
  from the fence). The operator then re-raised the whole-picture concern — for the second time — and
  it exposed the JIT move as a category error: a conditional pull is gated on the worker *already
  suspecting* it must look, which a myopic worker won't, so it would turn the §6.4 keystone (the full
  rescan that catches the architect's mis-scoping, and guards against myopic locally-discordant
  builds) from a by-construction guarantee into a discipline. And the field's JIT evidence targets
  *large/external* context — hypercore's spec is deliberately small and scannable (a `self-model`
  requirement), the high-signal core the field's hybrid says to *preload*. So the worker keeps the
  **whole spec preloaded, touched foregrounded** (the original slice-4 behavior, already tested);
  JIT is reserved for the **ADR/reference tail**, which carries no whole-picture stake. The
  capability-index idea is dropped as premature.
- **Amendment 2 — the agents file is a single minimal shared anchor (operator's pick).** One
  `AGENTS.md`, **symlinked as `CLAUDE.md`** (`ln -s AGENTS.md CLAUDE.md` — Claude now reads
  `AGENTS.md`/the symlink, so no adapter, no two role files), holding only non-inferable operational
  lines. All specialization in skills.
- **The build sequence** (`research/assembly.md` §5), lowest-regret first, no harness seam needed:
  (1) retire `worker.DEPTH` — render the depth grounding from `research/aposd.md`, create the depth
  skill artifact; (2) the derived-render / materialize-on-fold mechanism; (3) the minimal shared
  `AGENTS.md` + `CLAUDE.md` symlink; (4) the architect's methodology skills. The worker's **spec
  grounding is untouched** (whole spec preloaded), so nothing here perturbs the slice-4 keystone.
  **With the parked pi/OMP seam:** transport `cwd` = the fence, the ADR/reference tail dropped from
  the prompt and pulled JIT (the spec capabilities stay preloaded), the OMP flip, OMP skill loading.
- **Still machine-side:** the exact per-harness skill format and the harness-seam build, pinned when
  that side is built. The acceptance harness asserts the scaffold (the frozen copy gone, channels
  render from source and regenerate on fold, the artifacts single-sourced, the whole-spec grounding
  unchanged; with the seam, the transport runs `cwd` = the fence and pulls the reference tail) —
  never that a live model loaded a file/skill (the §4 experiment, recorded not faked).

**Next step: begin the build at §5 step 1** (retire `DEPTH`, single-sourced from `aposd.md`).

## Designed — item 2, the assembly across channels (2026-06-21)

The §6 design the investigation handed the next session is done: `research/assembly.md` (the
concrete assembly, the analog of `regrounding.md` for this item) + **ADR 0009** (the assembly
model, machine-side awaiting ratification). It designs, builds nothing, and settles nothing the
operator owns. What it settles, for the operator to ratify:

- **The governing cut is two axes — durability × reach.** Durable + every-episode + operational →
  the **agents file** (minimal); durable + routed-by-task → **skills**; live (re-derived each fold)
  + every-episode → the **prompt**, by construction. This is why the living spec stays prompt-side
  (it is live) while the depth disciplines move to a skill (they are durable) — sharper than
  "always-on / on-demand" alone, which could not explain either placement.
- **Route the expertise, keep the requirements by-construction — this refines §6.4.** §6.4 leaned
  "map the per-capability self-model onto skills, replacing the whole-spec megaprompt." Worked
  against `worker.py`, that does not hold whole: the worker's full scan is *by construction* ("no
  path that runs a worker without it"), a structural guarantee, and routing the spec to on-demand
  skills would demote it to a discipline. So the per-capability **requirements** (the living spec —
  small, scannable) stay assembled into the grounding; only the per-capability
  **expertise/methodology** (plus the cross-cutting depth + design methodologies) routes to skills.
  The megaprompt is replaced *in part*. (Machine-side resolution; the operator can overturn it.)
- **Single-sourcing is a derived render, regenerated by the fold.** Skills + agents files are
  *generated* from the source (the `depth` skill from `research/aposd.md`; a per-capability skill
  from `spec/<cap>/spec.md`), never hand-copied — the same "as-built is derived, never authored"
  the operator view already obeys. The fold gains a render step that regenerates them; the one new
  mechanism is that, unlike the live-rendered view, these are **materialized on disk** for an
  external harness to auto-load. This is what kills the `worker.DEPTH` smell at the root.
- **The filename is the role router** (verified, not assumed): `AGENTS.md` (worker, OMP auto-loads
  it from the fence) + `CLAUDE.md` (architect, Claude auto-loads it, ignores `AGENTS.md`); shared
  core via `@AGENTS.md`. No distinct-cwd trick, no per-role subdirectory.
- **Sequencing.** Lowest-regret first, no harness seam needed: (1) retire the `DEPTH` frozen copy —
  render the worker's depth grounding from `aposd.md` (grounding unchanged, smell gone), and create
  the depth skill artifact; (2) the derived-render + materialize-on-fold mechanism. Then, on the
  operator's word and with content the operator sets: (3) minimal `CLAUDE.md`/`AGENTS.md`; (4) the
  architect's methodology skills. The worker-fenced side (transport `cwd` = the fence, the OMP flip,
  OMP skill loading) lands **with the parked pi/OMP harness seam**.

**The operator's to set, not committed (§6.0):** what "minimal" means, what (if anything) goes in
the agents file, **whether to have one at all** — and to **measure** its worth (an A/B) before
leaning on it, since §4.5 found context files often don't help and add ~20% cost. **The next step
is the operator ratifying the assembly model (ADR 0009)**; then the build proceeds in the order
above — steps 1–2 depend on none of the operator-owned content and can start the moment the model
is ratified (or even before, as the pure de-smelling they are).

## Investigated — item 2, assembling maximally skilled roles (2026-06-21)

The item-2 investigation is done and written up in `research/context-files.md`. **The goal the
operator set:** two roles — architect and worker — each as **skilled, specialized, and consistent** as
we can make them, assembled from the five moving parts: **repo documents, agents files, skills,
prompts**, across the **two roles**. The direction is *not* "files vs. prompts" — it is layering all
the parts, each for its strength. The next session designs the concrete assembly; the verification and
the model are settled below.

- **The model — five parts, three derived channels off one source.** Repo documents (`intent.md`,
  rebuild-spec, the living spec, ADRs, `research/`) are the **single source of truth**; **agents
  files** deliver the role's always-on identity + disciplines, **skills** deliver on-demand
  specialized expertise (this *is* the routing — per-capability, harness-native), **prompts** deliver
  the per-node live task. Nothing hand-copied between channels — that is the `worker.DEPTH` smell.
  The megaprompt `worker.prompt()` assembles today is what this *replaces*, split across the channels.
- **Specialization sits in skills + workflow; the agents file stays minimal** — *calibrated against
  the evidence* (see `research/context-files.md` §4.5; the question "is this backed by field
  consensus?" moved it). A 2026 study ([arXiv 2602.11988]) finds context files often *reduce* success
  and add ~20% cost, with **overview/identity prose** the failure mode and **minimal operational
  instructions** the part that helps. So the heavy methodology — the depth disciplines, each
  capability's self-model — goes in **on-demand skills** (Anthropic's own progressive-disclosure
  guidance backs this), not the always-on agents file, which stays a thin operational anchor (the
  check command, the tools, a pointer). And the file's value for hypercore's own agents is to be
  **measured, not assumed**. (The earlier "role identity belongs in the agents files, always on" was
  over-confident and is corrected.) **"Minimal" is not defined and nothing about the file's content
  is committed** — what (if anything) goes in the agents file is the operator's to set, and the
  operator may define it differently or decline the file entirely.
- **The mechanics are verified on the real harnesses** — canary tests with **tools disabled** (so it
  is genuine auto-load, not the agent reading the file) + negative controls. [omp, claude] **OMP (the
  worker) auto-loads `AGENTS.md` from the worktree cwd**; **Claude (the architect) auto-loads
  `CLAUDE.md`, ignores `AGENTS.md`**; the **`CLAUDE.md`→`@AGENTS.md` adapter** bridges them; and
  **both harnesses have a skills mechanism** (OMP native; Claude Code / Agent SDK). So `AGENTS.md` is
  the open, durable source of truth (north-star-aligned), `CLAUDE.md` a one-line adapter.
- **The blocker + sequencing.** [code] Today the transport runs `claude -p` with **no `cwd`** (repo
  root, not the fence), and the worker is still `claude -p`, not OMP — the pi/OMP seam that runs the
  worker fenced is **parked, not built**. So: the **architect side + `AGENTS.md`/adapter** (retiring
  `worker.DEPTH`) can start **now**; the **worker-fenced side** (transport cwd-awareness, the OMP
  flip, OMP skills) lands **with the harness seam**.

The next session's design work is `research/context-files.md` §6: (1) the **assembly map** — partition
each role's grounding across agents-file / skill / prompt; (2) **single-sourcing** skills + files from
repo documents, kept in sync as the spec folds; (3) **role-specialized file placement** (the fence is
a repo checkout, so a repo-root file is shared — how each role gets its own); (4) **skills as the
routing** — map the per-capability self-model onto skills, replacing the whole-spec megaprompt; (5)
**sequencing** the build. An ADR records the assembly model when the operator ratifies the partition.

## Done — slice 9, the accepted-length ratchet (2026-06-21)

The hole slice 7 left open — a structured depth-decision cleared a file *forever, regardless of
length*, so a file accepted at 450 lines could balloon to 2,000 and the gate stay silent — is
closed. Acceptance is now **bounded to the length it names, and ratchets**. The operator settled
the direction after slice 7 (set a higher bar for the next trip; don't silence forever, don't nag
on every touch); this slice builds it and settles the machine-side sub-questions. What landed:

- **The accepted length lives in the record** (`depth-decision: <path> accepted@<N> — <reason>`),
  not computed from git history. Durable, version-controlled, operator-legible — and recording
  the bar (rather than inferring a high-water mark) makes **shrink-then-regrow correct for free**:
  a shrink never lowers the bar, so a file that shrinks and regrows to its old size never re-nags.
- **`accepted` is bounded; `accepted_at` is the deep primitive.** `accepted(rel, lines, root)`
  clears the gate only while the file is within `N + N·SLACK` (the materiality margin, `SLACK =
  0.1` — a one-line edit past the bar does not re-open a settled decision; only material growth
  does). `accepted_at(rel, root)` reads the recorded bar — the **max** across all records naming
  the file, so the ratchet only rises and the live bar is order-independent. The margin logic
  lives in one place; the review consults the predicate, it does not reimplement it.
- **A bare `accepted` (no `@<N>`) no longer clears the gate** — an acceptance that names no bound
  is incomplete, so the decision re-fires. The same by-construction closure slice 7 used for the
  substring hole, applied to the length: the exception is the decision *at a stated size*, not the
  spelling. (This is the direct consequence of the settled direction, recorded machine-side.)
- **The review distinguishes a stale acceptance from a never-decided over-signal file.** A third
  over-signal status, **`exceeded`** (`hyper/review.py`, `Module.bar`): a file past the signal
  that *was* accepted at a lower bar and has since outgrown it. It returns to the deepening
  backlog (the finding names the stale bar), and the structural map marks it "grew past its
  accepted bar of N — decision re-opened" — read differently from a brand-new `over` file. So
  `over` = never decided, `exceeded` = accepted-but-outgrown, `accepted` = within the bar.

The four open sub-questions from the slice-7 hand-off are all settled, in the ADR: the **margin**
(proportional `SLACK`, a starting value to tune); **shrink-then-regrow** (correct by construction —
the bar is recorded, not a git high-water mark); the **review render** (the `exceeded` status);
and **where the high-water mark lives** (the record). ADR 0008 records the decision (it *refines*
0006 — the structured record now names its length; a bare `accepted` no longer clears) — the
direction operator-settled, the machine-side shape awaiting ratification. Spec deltas across
`folding-conditions` (acceptance is bounded and ratchets), `architecture-review` (the exceeded
rendering), and the glossary (accepted length / the ratchet / exceeded acceptance). Acceptance —
`hyper/check/slice9.py` (19 checks) — and **all of slices 1–9 pass** (`python3 -m hyper --check`,
126 checks, 0 fail). The slice's own work stayed deep: `conditions.py` is 201 lines, well within
the signal.

## Done — slice 8, parallelism re-grounded: design-it-twice (2026-06-21)

The worktree fence — slice 4's throughput isolation — now also serves design quality. For a
load-bearing interface the architect judges worth it, the decision is **designed twice**:
several **candidates**, each in its own fence (the fence, tagged per candidate), each briefed to
design the *same* interface radically differently (§7.5's four briefs), and the architect picks
or hybridizes on **depth, locality, and seam placement**. What landed:

- **`design-it-twice` is its own capability** (`spec/design-it-twice/`, `hyper/design.py`; ADR
  0007). It orchestrates `worker` (borrows the fence) and `conversation` (the architect judges)
  without belonging to either — the same boundary logic as `architecture-review` (0005). The
  deep entry is `design.design_twice(node, briefs, transport, root)`: it hides the parallel
  candidate fences, the comparison, the ADR write, the stake-escalation, and the teardown.
- **Selection is machine-side — the operator ratified this** (the one fork grilled this slice;
  chosen over an operator-facing card and over machine-picks-but-always-notify). The architect
  compares and records the pick as a **structured design-decision** ADR
  (`design-decision: <subject> → <chosen> — <reason>`, the depth-decision idiom). The interface
  shape is machine-side like the spec delta — the operator's anchor is the contract, not the
  machine-side design (§6.4). The pick does not spend the operator's go.
- **A stake-bearing difference still reaches the operator** — the standing-guard floor (§5.1):
  when the comparison reveals a difference the operator has a stake in, it re-enters grilling as
  a card carrying only the architect-authored stake. The candidate designs and the reasoning
  stay machine-side; the leak path that would put raw designs on a card does not exist.
- **Candidates design, they do not implement** — interface + what it hides + the seam + the
  deletion-test argument; depth/locality/seam are judgable from the design, and the winner
  carries forward as the contract for one ordinary `apply`. Cheap; no thrown-away builds.
- **The concurrency clause is composition, not a scheduler.** "Concurrent workers advance one
  graph in isolation and each folds its delta" is satisfied by the slice-4 fence composing — two
  workers, two fences, two independent folds, no interference. No throughput scheduler was built;
  the judgment use is the slice, held apart from throughput parallelism as the queue note asked.
- **The fence gained a tagged-sibling form** (`worker.worktree(..., tag=)`) and a shared
  `worker.commit_tree` — the one in-fence commit primitive both a worker result and a candidate
  design land through, so the fence-commit knowledge stays in one place (no duplication).

Spec deltas across the new `design-it-twice`, `conversation` (the architect's selection
judgment), `worker` (concurrent workers fold in isolation), and the glossary (design-it-twice,
design contest, candidate, design brief, design-decision). ADR 0007 records the boundary +
machine-side selection. Acceptance extended — `hyper/check/slice8.py` (18 checks) — and **all of
slices 1–8 pass** (`python3 -m hyper --check`, 107 checks, 0 fail). rebuild-spec §7.5/§9.8 are
the external methodology doc (`~/Documents/rebuild-spec-1.md`), not in this repo's commit.

### The fork, resolved by the operator

- **Selection lands machine-side** (operator's choice during grilling). The architect picks and
  records an ADR; the operator sees it only on a stake-bearing difference. Recorded in ADR 0007
  as operator-ratified, the rest of that ADR machine-owned awaiting ratification.

### Honestly not-yet-wired (recorded, not fabricated — the slice-7 F1 precedent)

The capability is invoked on the architect's judgment that an interface is load-bearing.
**Automatic detection of "load-bearing" inside live grilling** is the natural next integration
— a model judgment like the stake-floor, not deterministically harness-testable — so it is
recorded as the standing job to grow, not faked. The mechanism (contest → compare → record →
escalate) ships complete and tested.

## Done — slice 7, the architecture re-grounded in depth (Ousterhout) (2026-06-21)

Phase 3 landed. The line-count budget and the slice-6 `check.py` split were reconsidered against
John Ousterhout's *A Philosophy of Software Design* and the constraint rebuilt around **depth**
(`research/aposd.md` — the faithful synthesis; `research/regrounding.md` — the design; ADR 0006
— the recorded decision). What changed:

- **Depth is the criterion; length is one signal of it.** The gate (`hyper/conditions.py`) no
  longer auto-refuses on length: a source file past the **length signal** (`conditions.SIGNAL`)
  raises a **depth decision** — re-cut / deepen / accept-with-reason — surfaced to the operator
  (`conversation.integrate`), never a silent veto and never a silent pass. The non-negotiable
  facts (the delta applies, a behavior-changing graph carries a recorded loop) still auto-refuse;
  only the depth criterion is a judgment.
- **The review renders depth, not merely length.** `hyper/review.py` shows length as a labeled
  context-cost signal against the threshold and records the **model-driven red-flag depth scan**
  as not-yet-built — the honest self-record, never a fabricated verdict.
- **The justification hole is closed by construction.** Because length no longer auto-refuses,
  the loose substring escape hatch (`conditions.justified`) is **deleted**, replaced by a
  **structured depth-decision** record (`conditions.accepted`): a parseable
  `depth-decision: <path> accepted — …` line naming the exact file, so a coincidental mention
  grants no exception. (This resolves the "known debt" the slice opened with.)
- **The worker is grounded in the depth disciplines, every episode** (`worker.DEPTH`) — the
  *proactive* primary defense: it builds deep up front, so the gate is a rarely-tripped backstop.
- **conversationalist → architect** (the role; the capability stays `conversation`). The
  operator-facing role is the holder of design judgment and judges depth at the archive gate.
- **The slice-6 `check.py` split keeps, on locality** — each `sliceN` is a separate acceptance
  contract along the per-slice seam, not classitis. ADR 0006 records the reasoning.

Spec deltas across `folding-conditions`, `architecture-review`, `conversation`, `worker`,
`self-model`, and the glossary (the architect rename + the Ousterhout terms: deep module, depth,
context cost, length signal, red flag, depth decision, strategic/tactical). rebuild-spec
§6/§7.1/§7.4/§9/§11 revised (it is the external methodology doc — `~/Documents/rebuild-spec-1.md`
— so those edits are not in this repo's commit). ADR 0006 supersedes in part 0004 (the auto-refuse
ceiling + the substring hatch) and 0005 (the "measures length" framing). Acceptance harness
extended — `hyper/check/slice7.py`, with slices 5/6 updated to the new names and behavior — and
**all of slices 1–7 pass** (`python3 -m hyper --check`).

### The forks, resolved by the implementing session

- **F1 — the model-driven depth verdict is deferred** (settled in phase 2): this slice ships the
  mechanical, harness-testable scaffold; the model-driven red-flag depth scan is recorded as the
  review's standing job to grow (a real capability, likely its own later slice).
- **F2 — no hard length ceiling survives.** The architect's lean was a single *high*
  auto-refusing ceiling; resolved instead to **drop it entirely** — the flip the fork itself
  anticipated. An auto-refusing number at any height re-commits the removed error (a number
  standing in for the judgment of depth) and would force back the escape hatch this slice
  deletes — regrounding §6, already grilled, says length no longer auto-refuses and the hatch is
  closed by construction, which an auto-refusing ceiling would contradict. Length raises a
  decision across its whole range; the anti-dilution guarantee holds because over-signal material
  is *un-foldable* until the operator settles the decision — stronger than the old escape, not
  weaker. (Recorded [machine], awaiting ratification — the operator can override.)
- **F3 — the role is renamed `architect`; the capability stays `conversation`** (the architect's
  lean): the operator-facing channel is the boundary and it is unchanged, so this is a rename,
  not a re-cut — no new boundary ADR.

## Noted for a later session (machine, 2026-06-21)

- **`slice4`'s code-leak check uses substring proxies that false-positive on ADR prose.** The check
  "the worker is grounded in the spec, never the code" asserts `"import " not in prompt` and
  `"curses" not in prompt` — but `worker._decisions` feeds every `spec/decisions/*.md` into the
  worker prompt, so an ADR that *discusses* imports or curses trips it as if real code leaked. It
  bit us drafting ADR 0009 ("import adapter" → reworded). As ADRs accumulate and discuss code-ish
  topics, the substring proxy gets more false-positive-prone. Minor; worded around for now. A
  sturdier check would test the *grounding the worker assembles* (spec slices, glossary, decisions)
  rather than scan the whole rendered string for code-shaped substrings — but only if it earns the
  change; the current check still catches the real failure it was built for.

## Considered and declined — do not re-propose

Making handoff §9 ("do not re-introduce these errors") into an enforced pre-fold checklist was
raised and **declined** by the operator (2026-06-21): §9 is a bootstrap artifact — the errors
that tempted across the spec's revision rounds — not the critical invariant set, so it is not
worth hardening, and a checklist of named errors buys false comfort against the gap that actually
matters (unsurfaced, *un*-named drift). The real defenses against that gap are the worker fix (the
§6.4 keystone — a second role with full scan the first can't suppress) and the architecture review
(slice 6 — a standing adversarial scan rendered to the operator). Knowing §9's errors exist is
enough.

## Next — item 2 investigated; the operator picks the direction

The eight planned slices (rebuild-spec §9) are built; **item 1 — the accepted-length ratchet — is
built (slice 9, above)**; and **item 2 — context files — is now investigated** (see the top section
and `research/context-files.md`). The goal is set — **two maximally skilled, specialized roles
assembled from repo documents, agents files, skills, and prompts** — and the mechanics are verified
(OMP auto-loads `AGENTS.md`; Claude auto-loads `CLAUDE.md`; the `@AGENTS.md` adapter bridges; both
harnesses have skills). **The next step is the next session designing the concrete assembly**
(`research/context-files.md` §6): the per-role partition across the channels, single-sourced from repo
documents, with the architect side startable now and the worker-fenced side landing with the parked
harness seam. The surface-level analysis below (§2) is the slice-7 hand-off, **superseded by the
investigation** — kept for the record.

## Raised for a later session (operator, 2026-06-21)

Two questions the operator raised after slice 7. **Item 1 is now built (slice 9, above)** — the
original surface-level note is kept below for the record, struck through by the build. **Item 2 is
still an investigation** and must be validated before building. Recorded here so the message
survives the session boundary.

### 1. The accepted length must set a *higher bar* for the next trip — DONE (slice 9, ADR 0008)

*Built. The surface-level note below was the slice-7 hand-off; slice 9 settled every open
sub-question — see the slice-9 Done section above and ADR 0008. The shape it predicted held: the
record carries the accepted length (`accepted@<N>`), `accepted` clears only within the bar plus a
proportional materiality margin (`SLACK`), past it the decision re-fires and must be renewed, and
shrink-then-regrow is correct because the bar lives in the record, not a git high-water mark.*

**Current behavior (confirmed in `conditions.py`):** once a structured `depth-decision: <path>
accepted` record exists, `accepted(path)` matches that path **permanently and regardless of
length** — so the file never re-trips the depth signal again, *no matter how much further it
grows*. A file accepted at 450 lines can balloon to 2,000 in later changes and the gate stays
silent. That is a hole: acceptance is currently unbounded.

**Operator's direction (settled, build it):** when a length signal is accepted, **set a higher
bar for the next trip** — do not silence the file forever, and do not nag on every touch. The
acceptance should be *bounded to the length it was accepted at*; the signal re-fires only when
the file grows materially past that accepted length, re-opening the depth decision at the new,
higher level. Each acceptance ratchets the bar up to the current size; a stable or shrinking
file stays quiet, renewed growth re-opens the question.

*Surface-level shape (not validated — for the next session to settle):* the structured
depth-decision record should carry the **accepted length** (e.g. `depth-decision: hyper/foo.py
accepted@450 — reason`, or a separate field), and `accepted()` should clear the gate only while
`current_lines <= accepted_length` (perhaps + a small margin to avoid re-tripping on a one-line
edit). Past it, the signal trips again and the acceptance must be **renewed** at the new length.
Open sub-questions I have *not* thought through: the right margin; whether shrink-then-regrow
matters; how the review's `accepted` status and map render a stale/exceeded acceptance; whether
the high-water mark belongs in the record or is computed. This touches exactly what slice 7 built
(`conditions.accepted` + the structured record + `review` status), so it folds in naturally.

### 2. Are we using prompts *and* AGENTS.md files appropriately? — INVESTIGATED (research/context-files.md)

*Investigated. The surface-level note below was the slice-7 hand-off; the investigation reframed it
around the operator's goal — **two maximally skilled, specialized roles assembled from repo documents,
agents files, skills, and prompts**. It verified the mechanics on the real harnesses (worker =
GPT-5.5 via pi/OMP, auto-loads `AGENTS.md`; architect = Claude, auto-loads `CLAUDE.md`; the
`@AGENTS.md` adapter bridges; both harnesses have skills), set the model (one source → three derived
channels), and handed the next session the concrete assembly to design — see the top section and
`research/context-files.md`. The original note (which assumed both roles run `claude -p` and framed
it as files-vs-prompts) is kept for the record, superseded by the writeup.*

**Surface-level read (shallow — not a deep audit):** hypercore currently grounds its agents
**only through hand-assembled prompt strings** — `worker.prompt()` marshals the whole spec,
glossary, decisions, the `DEPTH` disciplines, the delta and the ask into one big string;
`conversation`/`grill` hold `SYSTEM`/`COHERENCE` prompts; the transport is headless
`claude -p <prompt> --model …`. There is **no AGENTS.md / CLAUDE.md anywhere** in the repo. The
operator's instinct that this leaves value on the table looks right at a glance, for two distinct
uses worth separating:

- **(a) hypercore *using* context files for its own roles.** Durable, role-invariant grounding —
  the depth disciplines, the "what hypercore is" frame, the glossary — wants to live in
  version-controlled context files the agent loads, not in code string literals. `worker.DEPTH`
  is the live smell: it is a compressed copy of `research/aposd.md` pasted into a Python constant.
  That contradicts intent.md's own "durable state in version-controlled files," and a file is
  operator-legible and editable where a string literal is not. A worker runs `claude -p` *inside
  its own worktree*, so an AGENTS.md placed there could be auto-loaded as standing grounding for
  free, instead of re-marshalling a giant prompt each episode.
- **(b) an AGENTS.md/CLAUDE.md *for agents building hypercore* (this very workflow).** The next
  session currently learns the ropes by convention (read `next-work.md`, then `rebuild-spec`,
  run `python3 -m hyper --check`). A repo AGENTS.md codifying that reading order, the slice
  workflow, and the check command would make each session start grounded rather than
  reconstructing it.

**The tension to resolve, not paper over:** AGENTS.md is auto-loaded and **shared / un-routed**,
which cuts across hypercore's deliberate *context routing* (rebuild-spec §6 — each role gets only
its render; the worker never holds the operator view, etc.) and risks the very "noisy
over-sharing" failure §6.2 names. So the real design question is **which layer belongs in files**
(the role-invariant durable grounding — likely a good fit) versus **which stays prompt-assembled
and routed** (the per-capability self-model slices — hypercore's own mechanism, should not be
flattened into one shared file). Probably: durable role-invariant grounding → context files;
self-model routing → stays assembled.

**Verify first (the whole idea hinges on it):** does headless `claude -p --model …` actually
auto-load AGENTS.md / CLAUDE.md from the worktree cwd? Believed yes (project memory loads in `-p`
mode), but confirm before designing around it.
