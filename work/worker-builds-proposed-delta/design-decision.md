# design-it-twice: worker-builds-proposed-delta — a worker only ever applies an architect-proposed delta [machine]

A load-bearing interface for *worker-builds-proposed-delta* was designed twice — candidates
grilling-pass, readiness-predicate, worker-boundary, each designed in isolation to its own brief — and
compared on **depth, locality, and seam placement**. The load-bearing question: *where* is the guarantee
"a worker only ever applies an architect-proposed delta" enforced, and what becomes of an ask that today
reaches work with no delta (the below-floor ask, and the hand-authored standing node)? This record
**retires and replaces** the hand-fabricated pick that sat retracted here — the byte-indistinguishable
fabrication the operator caught — with a real contest carrying its candidate set.

design-decision: worker-builds-proposed-delta → worker-boundary (hybrid, with the grilling-pass closing the below-floor door) — the boundary is the one narrow waist every crossing funnels through, so it covers the bare hand-driven call the totality requirement demands, makes `worker._touched` a total function, and lets the author-from-scratch fallback be deleted (not guarded); the grilling-pass seam closes the below-floor door so a below-floor ask carries an architect-proposed delta and stays buildable rather than surfacing forever; the readiness-predicate seam is rejected for inverting the tree→grill dependency and leaking the bare call.

## Grounds

- **grilling-pass** (`grill.consider`/`products`): enforce where deltas are born — `consider` always
  produces a propose product, even below-floor. *Hides:* the which-door distinction inside grilling.
  *Seam:* between intent-capture and work-spawn. *Verdict:* closes the below-floor door, but does **not**
  cover the hand-authored standing node (placed on disk, never through `consider`) nor a bare
  `worker.run`. The guarantee at the worker boundary stays unenforced, so the worker must still distrust
  its input and the fallback cannot be deleted — shallow against the invariant, which bites at the worker.
  Kept as the hybrid's **door-closer**, not the enforcement.
- **readiness-predicate** (`tree.ready`): a standing node is ready only if it carries an
  architect-proposed delta; `ready` filters out delta-less nodes. *Hides:* the delta-presence rule inside
  the readiness computation. *Seam:* between standing work and schedulable work. *Verdict:* covers both
  doors **for the scheduler**, but `tree.ready` is a pure read in `tree.py`, and making it depend on
  `grill` artifacts inverts the dependency (`grill` imports `tree` → an import cycle) — a locality
  violation. And a bare `worker.run(tree.find(id))` — the documented hand-driven path — **bypasses**
  `ready` entirely, leaking the guarantee exactly where the folded `a crossing is total at the worker
  boundary` requirement says the boundary must hold "whatever its caller." **Rejected.**
- **worker-boundary** (`worker.run`): `worker.run` refuses a node with no architect-proposed delta
  (`grill.entry_of` finds no propose product) — raises one parented decision card and builds nothing — at
  the one chokepoint every crossing funnels through, scheduled or bare. *Hides:* the entire
  "did a delta get proposed, through which door" concern behind one pre-dispatch check. *Seam:* the worker
  boundary — the narrow waist. *Verdict:* deepest (one check makes a whole class of caller-distrust
  vanish; `worker._touched` becomes total, so the author-from-scratch fallback is **deleted and
  unreachable**, not guarded), most local (the guarantee lives exactly where author-from-scratch would
  occur), best seam (covers the bare call readiness leaks). **Chosen**, hybridized with the grilling-pass
  door-closer so a below-floor ask stays buildable.

## Stake — none crosses to the operator

The one behavioral change — a below-floor ask now runs the architect's propose at file time, and a
hand-authored node with no delta surfaces a decision instead of silently building — is already ratified
by this node's folding conditions and the operator's stated intent ("the propose stage owned by the
architect, not the worker"). No unsettled fork remains, so no decision card crosses; the pick is
machine-side design judgment, recorded here.
