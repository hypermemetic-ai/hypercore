---
kind: ask
state: in flight
owner: operator
created: 1782689546
---
Interface slice 4 — the reasoning loop. A key pressed on any visible element tied to a model's working opens a live loop onto that model's reasoning, rendered as one surface scoped to that node. The architect's own thread is fully steerable — the operator prunes a step, edits a step, resets and reruns, steering the work by changing its shape. A fenced worker's trace is shown read-only — its steps are never edited (no mid-run injection into the worker's session) — and the operator acts at the node grain: prune the node, re-ask it, rerun it. The loop earns trust by what acting on it changes, not by how convincing the account looks: a model's account of its own reasoning can be a confabulation, so the acts are the trust anchor, not the trace's polish. The live loop intent §52, §62, §64 describes, made concrete on the grid.

Folding condition: spec/interface.md carries the reasoning-loop requirements with their scenarios; the gated render scenarios (the loop opens on a model's working as one surface; the architect's thread steerable at the step grain while a fenced worker's trace is read-only with node-grain acts; the trust anchored in acting, not the account) go red→green; the watched fact — the live reasoning loop opened and steered by keystroke on the running window (python3 -m engine) — is confirmed; python3 -m engine --check is green.
