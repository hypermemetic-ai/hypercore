# next work

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

## Considered and declined — do not re-propose

Making handoff §9 ("do not re-introduce these errors") into an enforced pre-fold checklist was
raised and **declined** by the operator (2026-06-21): §9 is a bootstrap artifact — the errors
that tempted across the spec's revision rounds — not the critical invariant set, so it is not
worth hardening, and a checklist of named errors buys false comfort against the gap that actually
matters (unsurfaced, *un*-named drift). The real defenses against that gap are the worker fix (the
§6.4 keystone — a second role with full scan the first can't suppress) and the architecture review
(slice 6 — a standing adversarial scan rendered to the operator). Knowing §9's errors exist is
enough.

## Next — the two items raised after slice 7

The eight planned slices (rebuild-spec §9) are built. The next work is the two items the operator
raised after slice 7, recorded below: **(1)** the accepted-length ratchet — *settled, build it*;
**(2)** AGENTS.md / context-files — *investigate* (verify `claude -p` auto-loads them first).
Item 1 is the clean next slice — it folds into exactly what slice 7 built (`conditions.accepted`,
the structured depth-decision record, the review's `accepted` status), and now also touches
slice 8's structured `design-decision` idiom, which shares the same record shape.

## Raised for a later session — not yet worked (operator, 2026-06-21)

Two questions the operator raised after slice 7. **Judgment is deferred — the analysis below is
surface-level only and says so**; the next session should validate before building. Recorded
here so the message survives the session boundary.

### 1. The accepted length must set a *higher bar* for the next trip (decision: yes)

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

### 2. Are we using prompts *and* AGENTS.md files appropriately? (investigate)

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
