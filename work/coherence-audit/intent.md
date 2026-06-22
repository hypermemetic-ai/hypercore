---
kind: ask
state: standing
owner: operator
created: 2026-06-21
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
  picks it up and runs it. This is the parked pi/OMP harness seam (role-assembly steps 5–6).
  **The decision owed: is the next arc more self-build, or the worker seam that makes the
  product *do* the thing?** That is an operator sequencing call, not a machine one.
- **No "live visual of a model's reasoning"** (intent §44) — unbuilt; only a thinking-spinner.
- **The conversation is one-shot** `claude -p` request/response, not the persistent "summon on
  the spot, answer lands while you watch" of intent §42. Partial against intent.

## naming / structure residue

- **`coherence` has no module.** ADR 0013 carved `coherence` into its own capability but left
  its code in `conversation.integrate` ("the code is untouched"). So `conversation.py` implements
  two carved-apart capabilities. `grilling` aligned (its `grill.py`); `coherence` did not. Decide:
  carry the misalignment, or give coherence its own module.
- **`operator view` vs `operator brief`** — the glossary's own flagged-open name (it now carries
  the authored vision too, so "brief" may be wrong). Unresolved.

## hand-maintenance drift (the system's own anti-pattern)

- **`README.md` carries hand-typed numbers that drift** ("157 checks green" no longer matches the
  live harness). For a derive-don't-hand-maintain system, the README is the one large hand-kept
  artifact. At least the check count could be rendered, not typed.
- **Stale docstrings/refs**: `check/harness.py` says "slice1 … slice7" with 14 slices present; the
  `role-assembly` arc's folded-history cites `engine/depth.py`, retired by ADR 0019 (history, kept as
  written). (`depth.py`'s own `aposd.md` ref is moot — the module was deleted in the depth normalization.)
- **A brittle worker-grounding check**: `slice4` asserts `"import " not in` the worker prompt as a
  code-leak proxy, so ADR prose that mentions "import" trips it (ADR 0015 did, and was reworded). The
  check guards a real invariant by a fragile substring — it wants a sturdier signal.
- **`design.py` is real but orphaned** — reachable only from `slice8`. Either the worker seam wires
  it, or it is dead-from-the-operator engine code to mark as parked.

## generated-output-at-root legibility

- The root mixes authored source (`intent.md`, `spec/`) with **generated channels**
  (`skills/`, `AGENTS.md`, `CLAUDE.md`) with nothing marking which is derived. ADR 0014 deferred
  the channels' home to the harness seam. The `spec/` re-cut and the archive nesting tidy part of
  the root; whether the generated channels want a marked home is still open and tied to that seam.

## folding condition

Each finding is either resolved by a delta/ADR or consciously deferred with a recorded reason on
its node — none silently dropped. The plot-level sequencing call is the operator's and folds when
they make it; the residue items fold as they are taken or explicitly parked. [machine]
