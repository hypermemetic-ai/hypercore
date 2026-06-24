# xstate inheritance study — provenance for xstate-lessons

A read of xstate / Harel statecharts against hypercore, to extract what is worth **inheriting
cheaply** (emulating in hypercore's narrow form) versus **declining**. Never adopt the library: the
finding is that hypercore has already re-derived most of the actor/statechart core natively, so the
yield is vocabulary, two small sharpenings, and one visual lesson. This file is the durable record so
the three child trees, and any future session, need not reread the originating thread (the thread is
disposable; this node is not). [machine]

## The two-layer framing (load-bearing for all three children)

hypercore relates to statecharts in two opposite ways, by layer:

- **Layer A — node lifecycle + worker/scheduler supervision.** A *fixed* topology: a node wears five
  states (standing → in flight → awaiting-you | done, plus grilling); the scheduler is an actor
  supervisor; the worker is an invoked child with two total exits (onDone = integrate/fold,
  onError = escalate). This layer **is** state-machine-shaped and maps to xstate idiomatically.
- **Layer B — the execution tree.** A *grown* topology (intent §104: "a dynamically composed
  workflow, not a fixed template"). The tree's shape **is** the runtime state; it cannot be declared
  ahead. This is xstate's runtime *actor system*, not a statechart — you cannot pre-draw it.

The decisive distinction a newcomer misses: a statechart's defining property is a **declared, fixed**
topology (that is what makes it visualizable and statically analyzable). Layer A has one; Layer B by
design does not. Every conclusion below follows from which layer it touches.

## What to inherit vs. decline (the narrow-needs column)

- **Inherit (cheap):** explicit states + one legal-transition authority; invoke **totality**
  (onDone xor onError, never neither/both); guards as pure named predicates; final-state → output
  (the fold). Most already present natively.
- **Already exceeded:** snapshot persistence — the tree on disk is the deeper version
  (operator-legible, git-durable, recovered structurally; `spec/tree.md` "no session is resumed").
- **Decline:** actor-to-actor messaging mesh (isolation §62 forbids it — the record is the only
  mailbox); history / session resumption (episodes are disposable); orthogonal regions within a node
  (concurrency is across nodes, not within one); the runtime/library itself (a shallow dependency by
  `spec/depth.md` — adds interface surface for behavior already hidden).

The test applied to every term below: it earns its place only if it **licenses a checkable
invariant** or **makes a class of mistake unsayable**. Otherwise it is decoration.

## Child 1 reference — the three in-place redlines (actor-guard-vocabulary)

Sharpen the load-bearing sentence in place; never append a gloss (intent §86, no accretion).

**`spec/schedule.md` intro.** Replace *"several workers advance the one tree at once, each fenced, the
shared record single-writer so their builds overlap while their integrations serialize"* with:
*"the scheduler is a supervisor over isolated actors. Each fenced worker shares no state and reaches
the one tree through a single channel — the single-writer record, its only mailbox — so builds
overlap, integrations serialize onto the shared history, and no worker can touch another's."*
Buys: "its only mailbox" makes **"a worker reaches a sibling" unsayable** (§62 stated as the single
channel, not a list of can'ts).

**`spec/folding-conditions.md` intro.** Replace *"the engineering standards made structural … this
capability owns the gates on the material"* with: *"the engineering standards made into guards. A
guard is a pure predicate the system evaluates over a node's material and state to decide whether a
transition may fire … this capability owns the guards on the `fold` transition; readiness
(`tree.ready()`) is their sibling on the `dispatch` transition. One vocabulary, two transitions — a
guard says when a node may move, never what moving does."* Buys: **forbids folding a side effect into
a condition** — a gate that *does* something instead of *deciding* something is now visibly wrong.

**`spec/folding-conditions.md` depth requirement.** Replace the three MUST/MUST-NOT clauses with:
*"The depth guard is the system's one escalating guard. Where an ordinary guard that fails simply
withholds its transition, the depth guard neither passes silently nor refuses on its own — it raises,
escalating a decision (re-cut / deepen / accept-with-reason) and holding the fold pending it."* Buys:
**forbids "simplifying" the §58 floor into a silent block** — the most likely future regression.

The "dispatch is total" redline is deliberately **not** here; it rides with child 2 so prose and gate
land together.

## Child 2 reference — the dispatch-totality invariant (dispatch-totality)

`schedule` today promises a worker "never silently dropping the node" — two negatives, untestable. The
actor reading sharpens to a positive, checkable invariant: **dispatch is total — every worker the
scheduler spawns resolves to exactly one terminal (folded or escalated); no node sits in flight
without a live worker.** This is xstate's `invoke` totality (onDone xor onError), the property a
hand-rolled loop loses first. It is the one move that yields a real harness assertion.

## Child 3 reference — the visual lesson (visualizer-grammar)

The one inheritable insight from xstate's tools: **draw the fixed topology once and overlay the live
position on it** — one diagram, two readings (shape + where execution sits). But apply it only where a
topology is fixed:

- **Layer A (node lifecycle + supervision):** fixed → borrow the **static chart + live highlight**
  wholesale. Small, drawable once; the overlay answers "what is happening to *this* node."
- **Layer B (execution tree):** grown → **not** the chart editor. Borrow the inspector's **live
  actor-tree**: a tree that grows as work decomposes, lights as runs land, collapses as subtrees
  fold. §104 forbids pre-drawing it.

Visual grammar to steal regardless of layer: **events on the edges** (every move shows its cause —
dispatch / integrate / escalate / settle); **hierarchy as containment, fold as collapse** (the archive
is a collapsed subtree); **guards shown, the unmet clause named** (so "why isn't this running?" is
answerable from the picture — the visual form of §60); **the event log as the time axis** (the folded
steps *are* the history; "shape from several angles" = project the one tree by structure / state /
owner / time). Decline xstate's **altitude**: it is a developer tool showing state IDs and function
names; §44 and "operator legibility is king" put hypercore's at the operator's altitude — operator
words on the edges, the *shape* of a model's reasoning, not its stack. §44's "several angles, real
time, a pull not a push" is the *inspector* model, not the *editor* — weight the build toward live
inspection.
