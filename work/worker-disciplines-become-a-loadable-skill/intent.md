---
kind: ask
state: standing
owner: operator
created: 2026-06-27
---
# worker-disciplines-become-a-loadable-skill — the worker loads its disciplines, it does not re-read them inline

The worker is the one role whose own standing disciplines are **not a skill**. `worker` is absent from
`methodology.METHODOLOGIES`, so `channels` materializes no `worker/SKILL.md`; the disciplines are
rendered inline only, by `worker._worker_disciplines`. By the writing-for-the-machine test — a channel
is earned by a role-discipline the role runs by judgment — the worker's judgment disciplines (write for
the machine, author no loop, refine the delta, never reach the operator) earn a skill exactly as the
architect's methodologies do.

This is why the prompt is long. Measured: ~12,275 tokens for a one-capability change, ~38,884 when no
delta is handed. Three structural costs, only one of which is fat:

- **~35% is standing boilerplate re-sent verbatim every episode** — the ~2,240-token disciplines and
  the ~1,481-token depth standards, identical bytes each time, when `depth` is **already** a
  materialized skill in the worker's own checkout (`skills/depth/SKILL.md`). The spec mandates depth
  "foregrounded in full every episode" (`spec/worker.md`, the depth requirement) as a hedge, because
  whether the worker (codex) loads its skills in the fence is **watched, unproven** evidence (README;
  `transport.worker_transport`).
- **the grounding mixes discipline with mechanism** — lines like "you run fenced, the host is
  read-only at the OS level" and "grounded by construction" describe guarantees the engine enforces
  and the worker cannot act on, spending attention without changing behavior. Keep the mechanism facts
  that change what the worker does (stage the exact files, author no loop); drop the ones merely true.
- **a worker-touching change renders `spec/worker.md` twice** — once as the `_worker_disciplines`
  statements, once as the foregrounded capability body.

The whole-spec **index** is NOT a cost to cut: it is the deliberate, cheap anti-myopia map (vision plus
requirement titles, ~5-10% of bodies' cost), and it stays.

The intent: register `worker` as a skill so its disciplines materialize on disk through `channels`;
route the worker prompt to **load** its `worker`, `depth`, and `writing-for-the-machine` skills from
its checkout (the last is a real worker skill — it authors deltas and scenario prose — that the prompt
never points at today); remove the inline re-send; relevance-filter the mechanism facts to the
actionable ones; and remove the double-render.

**The de-inlining is gated on watched evidence** that a live worker reliably loads its anchor and
skills inside the fence (the same evidence the README holds open). Until that lands, keep a minimal
inline hedge rather than trusting an unproven load. This likely carries a stake-bearing fork — how far
to trust codex's skill-load before dropping the hedge — so weigh it in grilling. Sequence after /
compose with `work/worker-prompt-leads-with-the-task`.

## folding condition
- a `worker` skill materializes from `spec/worker.md` through `channels` like the other methodologies
  — registered, rendered to both skill locations, and audited against the slice;
- the worker prompt points the worker to load its `worker`, `depth`, and `writing-for-the-machine`
  skills from its checkout;
- the inline re-send of the depth standards and the worker disciplines is removed, or reduced to a
  minimal hedge once the watched skill-load evidence is recorded;
- `spec/worker.md` renders only once in the prompt for a worker-touching change;
- `python3 -m engine --check` is green.
