# accepted-length-home — ratified contract

Grilled 2026-06-23. The durable record of what the grilling pass settled, so the conversation that
produced it is disposable. This is the contract the result is validated against.

## What the scan resolved (no operator stake — recorded, not asked)

- **Not node-local.** The record must outlive the work that grew the file past the signal, so it
  cannot archive on a node (the ask's own framing; intent §50/§116).
- **Not in `spec/`.** Spec is vision/contract, not mutable per-file state — the spec/state
  separation rules it out. It is authored input, not derived-on-fold like the channels.
- **Shape unchanged.** The `accepted: <path> @<N> — <reason>` line stays — the parseable record the
  gate already emits verbatim for copy-paste, greppable, glossary-defined, built and tested.
  Restructuring buys only ceremony.
- **One seam.** Read *and* write encapsulated behind `conditions.py` so the file's location is a
  **hidden decision** and the record can never be written two ways.

## The two residual decisions (operator-settled)

- **D1 — the home: `engine/accepted-lengths.md`.** Beside its only reader (the gate) and the review
  that shares it; the doc-root stays pure docs. (Flip considered: repo-root de-provisionalized, or a
  new `state/` dir — the operator chose co-location with the reader.)
- **D2 — write-path scope: the writer seam only.** Build `conditions.accept(path, n, reason)` — the
  one ratcheting/idempotent writer — and leave the architect's settle/integrate path free to call
  it. **Defer the operator-facing acceptance-card UI to `card-kind`** (which owns the acceptance card
  kind, D18). This node ships home + shape + the single writer; `card-kind` wires the operator action.

## The spec delta this realizes

- `spec/folding-conditions.md` — a new requirement: *the accepted-length record is durable authored
  state, written through one seam* (`accepted_at` reads, `accept` writes; ratcheting), with a
  scenario; and the `length-ratchet` standard line names `accept` as the writer.

## The contract (validated at the archive gate)

- `conditions.accepted_at` and `conditions.accept` read/write one durable store at
  `engine/accepted-lengths.md`; the location lives behind those two seams.
- `accept` ratchets (records a higher length) and is a no-op at an already-cleared one.
- the PROVISIONAL repo-root arrangement is retired; the gate and the review read the new home.
- `python3 -m engine --check` is green, with an executable check pinning the relocation and the
  writer (extending slice 9, the accepted-length/ratchet slice).
