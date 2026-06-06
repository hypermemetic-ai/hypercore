# organizing document

hypercore's intent is held in two groups of segments, one document each.

The **methodology** — the eight segments describing the rules themselves, leaf-materialized by `implementation/hypercore.md` and `implementation/check.sh`, divided along one axis (the parts of the methodology):

- **foundations** — the premise, the three properties, and what the intent is.
- **structure** — the two trees, how the corpus is laid out, and how a node nests inside another.
- **statements** — what a statement is, and ownership.
- **endorsement** — who stands behind a set, per segment and per change, and where the node boundary stops it.
- **change** — the change folder and its four things.
- **loop** — the five steps a change goes through.
- **sweep** — how coherence is checked across the corpus and across node boundaries.
- **adapter** — the binding between a harness and the loop: what the harness loads at the start of work, promising agreement and enforcing it as a rigid workflow. Materialized at the root not only by the methodology prose but by the harness adapter the machine loads (`CLAUDE.md` for Claude Code) and the orchestrator that runs the loop (`implementation/adapter/`).

The **governed work** — work-home, the home the operator's work folders mount into, materialized by a child node rather than by leaf code:

- **work-home** — a child node of the root that materializes this segment, with its own intent and code. The root keeps only the contract — the home mounts the operator's work folders and governs them within itself — which the work-home node at `implementation/work-home/` satisfies. A mounted work folder is in turn a child node of the home node: a separate corpus governed within its own repository. work-home holds zero work folders yet.

Each segment has an intent document at `documentation/<segment>.md` and a machine-statements file at `documentation/machine-statements/<segment>.md`. The work-home segment is materialized by a child node — the work-home node at `implementation/work-home/` — whose intent must satisfy the root segment's contract; a mounted work folder is a child node of that home node, a separate corpus governed within its own repository.

This is two groups, not a tag: nothing is partitioned twice. A tag is added only the first time a real second partition of the whole corpus forces it, not before.
