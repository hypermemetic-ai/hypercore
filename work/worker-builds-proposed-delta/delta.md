# delta — every buildable node carries an architect-proposed delta; the worker never authors its own

## ADDED — worker
### Requirement: a worker applies only an architect-proposed delta, never authoring its own
A worker MUST build only from the architect-proposed delta it is handed; it never authors its own
delta from a full scan. The handed delta is the node's own **proposed delta** (`tree.proposed_delta`),
the architect's product of the propose stage — read from the node's folder, not reconstructed by the
worker. A node reaching dispatch with **no** architect-proposed delta MUST NOT build: it is held out of
the ready work and surfaces to the operator as **awaiting a proposed delta**, never silently built from
a whole-spec scan. The author-from-scratch fallback — a worker that, handed no delta, foregrounds every
capability and authors its own scenarios, so the builder writes the oracle that clears its own fold — is
**deleted, not guarded**: once every buildable node carries a proposed delta, that branch is
unreachable, and an unreachable branch is removed, not left as a guarded path. A **trivial** proposed
delta (an empty proposal, `delta.Delta.trivial`) is a valid architect proposal and its node is
buildable; only the **never-proposed** node — no proposal at all — is the one held. This is the
**proposer** layer of the integrity stack: the delta and its scenarios come from the architect, so the
anti-self-judging invariant (`the worker applies and refines the delta the architect proposed`) cannot
be bypassed by a deltaless dispatch.

#### Scenario: a node with a proposed delta builds from it
- WHEN a worker is dispatched a node carrying an architect-proposed delta that names a set of
  capabilities
- THEN its handed delta is exactly that proposed delta — read from the node, not reconstructed — and its
  grounding marks exactly those capabilities, so it builds from the proposal and authors no delta of its
  own

  ```check
  proposed worker communication
  built from-proposal
  grounding marks worker communication
  ```

#### Scenario: a node with no proposed delta is held, not built
- WHEN a node reaches dispatch with no architect-proposed delta — a below-floor ask filed before any
  propose stage, or a hand-authored standing node — and, separately, a node carrying a trivial proposal
- THEN the never-proposed node is held out of the ready work and surfaces as awaiting a proposed delta,
  with no path that foregrounds the whole spec for the worker to author its own delta from; the
  trivially-proposed node is build-ready, since a trivial proposal is still an architect proposal

  ```check
  unproposed
  held off-ready
  awaiting-delta surfaced
  trivial-proposed ready
  no-author-from-scratch
  ```

## MODIFIED — grilling
### Requirement: a grilling pass yields the contract and the spec delta
A resolved grilling pass MUST produce the operator-view entry — the contract the result is later
validated against — and the spec delta the change will realize, authored by the architect against the
concise specs its scan reaches. The propose stage that authors the delta is **unconditional**: every ask
that becomes work carries an architect-proposed delta, whatever door it entered through. The
**interview** stays gated by the floor — an ask whose every decision is already determined files
straight to standing work, ungrilled — but filing straight through does **not** skip the proposal: a
below-floor ask still gets an architect-proposed delta authored for it as it files, so it reaches a
worker with a delta and is build-ready, never deltaless. The delta's scenarios are the **executable
checks** the change is gated by: the architect authors the WHEN/THEN and, where the behavior is
mechanically checkable, the check block that turns it red→green — so the pass settles not only what to
build but the oracle that will judge it, owned by the side that does not build it.

#### Scenario: the pass resolves
- WHEN the last grilling question is answered
- THEN the architect produces the view entry and a well-formed spec delta whose scenarios carry the
  executable checks the behavior is gated by, and raises the entry on the queue for ratification

  ```check
  ask above-floor
  answer lean
  answer words
  entry raised
  delta folds
  ratify spawns
  ```

#### Scenario: a below-floor ask still carries an architect-proposed delta
- WHEN every decision a filed ask needs is already determined, so it files straight to standing work
  with no interview
- THEN it still carries an architect-proposed delta — the propose stage ran unconditionally, even with
  no questions asked — so the ask reaches a worker with a delta and is build-ready, never deltaless

  ```check
  ask below-floor
  filed standing
  carries-proposed-delta
  ```

## ADDED — tree
### Requirement: a node is build-ready only when it carries an architect-proposed delta
A node MUST carry an architect-proposed delta — recorded as `delta.md` in its own folder — to be
build-ready. The proposal is a fact about the node's **own folder**: `has_delta` is the presence of that
file, read with no import into the tree from grilling or delta — the readiness check stays a bare
file-presence test the tree owns. The ready work is narrowed to nodes that carry a proposed delta, so a
node with none is held out of scheduling and shown to the operator as **awaiting a proposed delta** —
standing work, not yet ready, no card. The proposed delta is distinct in three states: **never proposed**
(no `delta.md`) holds the node; a **trivial** proposal (an empty `delta.md`) and a **real** one
(non-empty) are both proposed, so both are build-ready. The proposal has one writer
(`tree.propose`, an atomic write-and-commit); intent MAY be filed with its proposed delta in a single act
(`tree.file_intent(ask, delta=…)`), so a node and its proposal never disagree and no door lands a node
that is build-ready yet deltaless.

#### Scenario: a node carries its proposed delta in its own folder
- WHEN intent is filed for a node together with an architect-proposed delta, and, separately, a node's
  folder carries no `delta.md`
- THEN the proposed-delta node lands its `delta.md` in its own folder, reads as carrying a delta, and is
  in the ready work; the node with no `delta.md` is not in the ready work and surfaces as awaiting a
  proposed delta
