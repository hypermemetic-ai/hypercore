---
kind: ask
state: in flight
owner: operator
created: 1782190800
---
# operator-view-readiness — make the operator view answer "can I trust a run on this?"

The question that started the vocabulary sweep — "how far are we from trusting hypercore to do
operator-initiated work on itself without drifting?" — has no home in the operator view. The view
models **complexity debt** (where the code wants deepening), not **readiness** (whether the system
can be trusted to take a run unattended). The one question the operator most needs answered is the
one the interface cannot show.

Grow the operator view into a readiness surface:
- an **honest list of the standards** and how each is held — **gated** (a deterministic check) vs
  **watched** (judgment, leaves a trace) — so the operator sees exactly what rests on trust;
- the **never-run-live** status — the autonomy seam is built but the first autonomous run is still
  unverified (the honest limit recorded in the README); the view must say so, not imply green;
- a clean split of **gap** (wanted-but-not-built) from **complexity debt** (built-but-weak), which
  the old view conflated.

Provenance: `work/archive/vocabulary-sweep/decisions.md` (build-work #1; D3 gap/complexity-debt,
D5/D19 gated/watched/trace).

## folding condition
- the operator view renders the standards honest-list (each gated/watched) and the never-run-live
  status, and separates gap from complexity debt;
- `python3 -m engine --check` carries an acceptance check for the new surface and is green.

## Settled in grilling (2026-06-26) — the proposer↔view legibility coupling
The coupling raised while grilling `worker-builds-proposed-delta` is **resolved: already homed**. The
live "what's building and why" surface — an autonomous build and the architect-proposed plan (delta)
behind it — is a standing-work-surface concern, not a readiness-surface one: intent §58/§60 already show
a run as live work on the node that spawned it, with its plan kept as material on that node. So this node
stays scoped to the three readiness additions, no live-build view is built here, and
`worker-builds-proposed-delta` carries **no view precondition** (no sequencing dependency on this node).
The pass — question, lean, flip, the operator's answer, and the contract + delta it produced — is in
`grilling.md`.
