# organizing document

hypercore's intent is held in two groups of segments, one document each.

The **methodology** -- the nine segments describing the rules themselves, leaf-materialized
by `material/hypercore.md` and `material/check.sh`, divided along one axis:

- **foundations** -- the premise, the three properties, and what the intent is.
- **collaboration** -- how operator and machine work together: role partition, common
  ground, reliance calibration, control, feedback, handoff, and graceful failure.
- **structure** -- the two trees, how the corpus is laid out, and how a node nests inside
  another.
- **statements** -- what a statement is, and ownership.
- **endorsement** -- who stands behind a set, per segment and per work, and where the node
  boundary stops it.
- **active-work** -- the work-node lifecycle and the root contract for active child work.
- **loop** -- the five gates a work node goes through.
- **sweep** -- how coherence is checked across the corpus, work in flight, proposed parent
  amendments, and node boundaries.
- **adapter** -- the binding between a harness and the loop: what the harness loads at the
  start of work, promising agreement and enforcing it as a rigid workflow. Materialized at
  the root by the methodology prose, the harness adapter (`AGENTS.md` for Codex), and the
  orchestrator under `material/adapter/`.

The **governed work** -- durable child nodes and mounted work under this root:

- **home** -- the named child node at `material/home/`, with its own `intent/` and
  `material/`, that mounts linked project nodes and governs them within itself. home holds
  zero mounted project nodes yet.

Each segment has an intent document at `intent/<segment>.md` and a machine-statements file
at `intent/machine-statements/<segment>.md`. A child node is housed under `material/` or
reached through a settled mount path, carrying its own `intent/` plus `material/`; a
mounted project is a child node of home, a separate corpus exposed through
`material/home/material/<name>` as a symbolic link to its own repository.

This is two groups, not a tag: nothing is partitioned twice. A tag is added only the first
time a real second partition of the whole corpus forces it, not before.
