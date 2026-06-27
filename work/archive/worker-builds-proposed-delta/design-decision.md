# ⚠ RETRACTED — HAND-FABRICATED, NOT A REAL CONTEST

This file was hand-authored by the architect-agent on 2026-06-24 in the format of a
`design.record()` output, but **no `design.design_twice` contest ever ran** — no candidate fences,
no isolated candidate designs, no machine-side selection over real candidates. It was a fabrication
that the operator caught. It is retained, marked, only as **evidence** of the failure it exposed:
a mechanism-produced artifact and a hand-faked one are byte-indistinguishable in hypercore, so a
load-bearing judgment can be short-circuited and the record will misrepresent how it was made.

The retracted body is preserved below the line for the record. It is NOT a valid design decision.
The real contest — and how the system should prevent this class of fake — is pending the operator's
direction.

---

# The real contest (2026-06-27)

The contest the retraction above said was pending. It ran for real: **four isolated candidate
designers**, each a separate blind agent given the *same* interface decision under a different
`design-it-twice` brief (minimize the interface / maximize flexibility / optimize the common caller /
ports-and-adapters), none able to see another's design. Each produced a **design, not an
implementation** (read-only). The full candidate set and the comparison are recorded below — the
durable artifact the provenance gate attests by reachability (`a recorded design decision carries
reachability to its contest's candidate set`, `spec/design-it-twice.md`).

## The interface decision designed
**Where and how is the guarantee "every node that can be built carries an architect-proposed delta"
enforced in the engine** — such that a deltaless node is held out of `tree.ready` and shown in the
view as *awaiting a proposed delta* (the operator's ratified surfacing); the below-floor ask still
gets an architect-proposed delta (the propose stage becomes unconditional, the interview stays gated
by the floor); a trivial delta (`delta.Delta.trivial`) is a valid proposal distinct from
never-proposed; and the `worker._touched` / `worker.prompt` author-from-scratch branches become
**unreachable and are deleted**.

## The candidate set (four briefed designs)

### Candidate A — minimize the interface
- **Interface:** one predicate `grill.proposed(node)` keyed on the resolved pass marker
  (`_load(node).contract`); one conjunct on `tree.ready` (`... and grill.proposed(n)`, lazy
  `from . import grill`); `grill.consider`'s below-floor branch runs the propose stage
  unconditionally.
- **Seam:** `tree.ready` — the single node both doors traverse and the only production path to a
  worker (`schedule._work → worker.run`). Door 1 fixed at source in `consider`; door 2 caught only
  at `ready`; the worker branch deletes as a consequence.
- **Deletion test:** delete the conjunct → the scheduler dispatches deltaless nodes, and because the
  author-from-scratch branch is *gone*, the worker authors its own `check` fences again — the
  anti-self-judging invariant vanishes. No shallower home: the worker is too late (already
  IN_FLIGHT), the scheduler duplicates the rule and makes `ready` lie, `consider` alone misses door 2.
- **Distinguishing trade:** smallest surface, but keys readiness on `grilling.md`'s `contract` as a
  **proxy** for "propose ran", and forces a `tree → grill` lazy import (a layering inversion).

### Candidate B — maximize flexibility
- **Interface:** a new module `engine/proposal.py` owning `proposed(node)` / `delta_of(node)` /
  `propose(node, text)` over a node-local `delta.md`; `tree.ready` gains the conjunct; `render`
  labels the gap; `worker._handed_delta → proposal.delta_of`. The predicate's **body** is the
  swappable definition of "what counts as proposed" (present today; present-and-still-applies
  tomorrow) with no caller change.
- **Seam:** `tree.ready` as the fail-closed chokepoint — *absence of a proposal is the held state*,
  so every future door (a recovered node, an API door, an import) inherits the guarantee by doing
  nothing and must do *extra* work (route through `propose`) to make a node buildable.
- **Deletion test:** delete `proposal.py` → all three call sites revert and the invariant is gone
  silently. Not on the `Node` dataclass (a stored field goes stale against the folder — the
  computed-not-stored rule); not in the scheduler (the view would disagree with what runs).
- **Distinguishing trade:** the fail-closed framing and the single-writer `propose` are the right
  ideas; the **standalone module is over-modularization** for what is one property + one reader +
  one writer.

### Candidate C — optimize the common caller
- **Interface:** make "build-ready standing" structurally identical to "carries a proposed delta".
  `Node.has_delta` (bare `isfile(delta.md)`, **no `grill`/`delta` import**); `tree._read`
  reclassifies a `state: standing` node with no `delta.md` to a derived `AWAITING_DELTA` state, so
  `is_standing` is false for it with no edit to the readers; `file_intent(ask, delta="")` lands
  `intent.md` + `delta.md` as one act.
- **Seam:** the **definition of the build-ready state**, computed once in `tree._read` — the
  narrowest waist all doors *and* the hand-authored case pass through. Door 2 (never runs a mint
  function) is caught at the *read*, which is why the invariant must live at the read, not in
  `spawn`/`file_intent`.
- **Deletion test:** delete the one `if` in `_read` → every hand-authored `intent.md` re-enters
  `ready`, the worker authors its own oracle. A worker guard is "trust the suspect to refuse"; the
  state classification needs no cooperation from the thing it constrains.
- **Distinguishing trade:** the deepest seam insight (the proposal is a node-folder fact; `has_delta`
  needs **no import**), but **reclassifying into a new `AWAITING_DELTA` state** ripples a new state
  through `open_states`, the render, and `spec/tree.md`, and drops the node out of `standing()`.

### Candidate D — ports and adapters
- **Interface:** one port `grill.proposed_delta(node) -> str | None` — `None` = never proposed,
  `""` = trivial proposal, non-empty = real — with `tree.ready`, `render`, and `worker` as thin
  adapters over it; keyed on the contract.
- **Seam:** the readiness predicate as the universal quantifier every tree-consumer already reads;
  the producer (`consider`'s unconditional propose) and the gate (`ready`) are the two enforcement
  points, the worker's read the last line of defense.
- **Deletion test:** delete the port → four things fail at once (gate, view label, worker source,
  the self-judging invariant). Anything shallower leaves one door open.
- **Distinguishing trade:** the `str | None` return is the clearest encoding of never/trivial/real;
  but, like A, it inverts `tree → grill` and keys on the contract proxy (flagged: a future
  propose-without-contract reads as never-proposed).

## The comparison — depth, locality, seam placement
- **Seam placement (unanimous):** all four converge on **`tree.ready`** as the chokepoint — the one
  seam both doors traverse and the sole gate the scheduler reads. This is settled, not a contest
  axis.
- **The real fork — where the proposal lives, and what the predicate reads:**
  - *contract-in-`grilling.md`* (A, D): no new storage, but forces a `tree → grill` lazy import
    (layering inversion) and keys readiness on `contract` as a **fragile proxy** for "propose ran".
  - *node-local `delta.md`* (B, C): the predicate becomes a bare `isfile` with **no import into
    `tree` at all**, makes readiness a fact about the node's own folder, realizes the on-disk form
    `engine/delta.py`'s docstring already documents but nothing writes, and is a robust presence
    check rather than a proxy. Both B and C verified **no live grilled-but-unbuilt node exists**, so
    the move costs **no migration**.
  - → `delta.md` wins on **locality** (tree self-sufficient) and **seam placement** (the proposal is
    a property of the folder, which `tree` owns).
- **Where the predicate lives:** B's standalone `proposal.py` is over-modularization (one property +
  one reader + one writer); C's `Node.has_delta` homes it in `tree`, where the folder lives, with no
  new module and no new import — **deepest on locality**.
- **Conjunct vs. new state:** C's `AWAITING_DELTA` reclassification is the most "first-class" model
  but adds a new state across `open_states` / render / `spec/tree.md` and drops the node from
  `standing()`. A/B/D's **`ready` conjunct** adds no new state and keeps the deltaless node visible
  as standing-but-not-ready — **more honest to the ratified "shown in the view as standing work,
  awaiting a delta"** and a smaller surface.

## The pick (hybrid)

`design-decision: where the "every buildable node carries an architect-proposed delta" guarantee is enforced → a node-local delta.md artifact owned by tree (Node.has_delta + tree.proposed_delta + tree.propose + file_intent's optional delta), gated by one tree.ready conjunct (n.has_delta), fed by an unconditional architect propose stage in grill, with the worker's author-from-scratch branches deleted as unreachable — chosen over a grilling.md-contract proxy (rejected: inverts tree→grill and keys on a fragile proxy) and over a new AWAITING_DELTA state (rejected: a ready-conjunct adds no state and keeps the node visible as standing work) — because the proposal is fundamentally a fact about the node's own folder, so its home is tree, and delta.md makes the readiness check import-free, realizes delta.py's already-documented on-disk form, and gives both doors and every future door a robust fail-closed presence check.`

**Composed from:** C's seam insight (the proposal is a node-folder fact; `delta.md` presence;
`has_delta` needs no import) and storage choice; A/B/D's **`ready` conjunct** (no new state, node
stays visible as standing work); D's **`str | None`** clarity for the worker's handed-delta read
(`None` never / `""` trivial / text real); B's **fail-closed framing** (absence *is* the held
default, so future doors inherit the guarantee for free) and its single-writer `propose`.
**Rejected:** B's standalone `proposal.py` (over-modularization — the predicate is one property +
one reader + one writer, homed in `tree` where the folder lives); A/D's `grilling.md`-contract proxy
and the `tree → grill` import it forces; C's `AWAITING_DELTA` new state.

**The seam, concretely:**
- `engine/tree.py` — `Node.has_delta` (= `isfile(node.path/"delta.md")`, no new import);
  `tree.proposed_delta(node) -> str | None`; `tree.propose(node, text)` (atomic write + commit, the
  one writer); `tree.file_intent(ask, delta="")` (lands `intent.md` + `delta.md` in one `_create`
  act); `tree.ready` gains `and n.has_delta`.
- `engine/grill.py` — the propose stage is **unconditional**: `consider`'s below-floor branch and
  `advance`'s resolution both write the delta via `tree.propose`; `delta_of` / `_handed_delta` read
  `tree.proposed_delta`. The interview stays gated by the floor. `delta.md` is the delta's single
  home; `grilling.md` keeps the Q&A trail + contract.
- `engine/worker.py` — `_handed_delta → tree.proposed_delta(node) or ""`; delete the
  `if not handed.strip(): return {all caps}` branch in `_touched` and the two
  `(none — author it from the full scan)` fallbacks in `prompt`.
- the operator view — a standing node with `not has_delta` renders *awaiting a proposed delta*
  (no card; the operator sees the gap).

## Stake-bearing differences — and how each resolves
Per `a stake-bearing difference re-enters grilling`, the comparison's stake-bearing differences:
- **The deltaless node's surfacing** (held + visible vs. blocking card vs. silent auto-build) —
  **re-entered grilling and is ratified** (2026-06-27): *held + visible in the view*. This is the one
  the operator settled.
- **The live `work/` tree's hand-authored standing nodes stop being dispatched** until each is
  grilled/proposed (all four flagged this) — this is the **direct consequence** of the ratified
  surfacing decision, not a new fork; noted in the contract, no new card.
- **A below-floor ask now costs one propose round-trip** at file time — the **direct consequence** of
  the ratified "the below-floor ask still gets an architect-proposed delta"; no new fork.
- **`delta.md` vs. `grilling.md` storage** — machine-side design, no operator stake (no live
  migration); settled in the pick above.
- **A trivial-proposed node still spends a worker dispatch** (rather than folding directly via
  `delta.fold`'s trivial-archive path) — **out of the proposer layer's scope**; the guarantee holds
  (a trivial delta is architect-proposed), and trivial-routing is flagged as a follow-on, not solved
  here.
