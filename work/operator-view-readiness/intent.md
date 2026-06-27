---
kind: ask
state: standing
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

## To surface in grilling — a suggestion, not yet settled (design work remains)
A coupling raised while grilling `worker-builds-proposed-delta`, filed here as input to weigh, not a
requirement: that node would delete the worker's silent author-from-scratch fallback so a node never
builds from a plan the architect did not propose. But deleting it only *relocates* the invisibility —
from the worker's fallback to a `grilling.md` the operator would have to hunt for — unless the view
makes an autonomous build **legible to the eye**: what is building, and the architect-proposed plan
(delta) behind it, surfaced where the operator already looks, not filed where they must dig. The stake
is **legibility, not control** — the operator wants to *see* an autonomous build, not *approve* it, so a
blocking approval gate is the wrong tool (it charges approval-cost for a sight-problem). Consider whether
this readiness surface should also carry a standing "what's building and why" view, and whether
`worker-builds-proposed-delta` should sequence *after* it (view first). Open: what "at a glance"
requires, and whether the live-build surface belongs to this node or its own.
