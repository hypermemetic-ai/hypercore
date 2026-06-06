# Claude Code adapter

This is the **adapter** segment of hypercore's intent, materialized for the Claude Code
harness (`intent/adapter.md`). It states no rule of its own: every rule lives in the
intent, and where this file and the intent disagree, **the intent wins**. It routes you to
the intent and the loop — and makes them enforceable.

This repository is hypercore applied to itself. You are the machine in "operator and
machine," and you begin each session memoryless.

## What the adapter promises

Agreement between this harness and the methodology: that you act in accordance with the
intent and run the loop — not because you chose to, but because the workflow makes the
gates unskippable. Pointing alone is a request; the orchestrator is how agreement is kept.

## Orient before you touch anything

Read, in this order — this is where orient begins:

1. `material/hypercore.md` — the methodology.
2. `intent/organizing-document.md` — how the intent is divided into segments.
3. The segment the work touches (`intent/<segment>.md` and its
   `machine-statements/<segment>.md`), every work node in flight across the node tree,
   and any legacy change records named by a frame.

Don't guess. Search the web for what you don't know. Ask the operator what the artifacts
can't tell you.

## The rigid workflow — `material/adapter/loop.sh`

Every work node runs the loop's five gates, driven by the orchestrator in two phases split at
the operator's **sign-off**:

- **Phase one — orient, frame — design-phase collaboration.** You and the operator choose
  direction before sign-off by naming the addressed node, node-local work name, target
  segments, work in flight, and any open direction; before settling an open route, surface
  the problem, constraints, and decision surface for operator direction. You frame the work
  node under the addressed node's `material/` tree, with the written frame under
  `intent/frame/`, and run the sweep over the whole corpus and work in flight across the
  node tree, including related work named by a frame. Interaction
  surfaces here. It ends when the operator signs off:
  `loop.sh [-C <node-path>] signoff <work-name> <operator>` writes a `signed-off-by`
  line. **You never sign off for them.**
- **The session clears at sign-off.** Phase two runs on a fresh, memoryless `claude -p`
  that re-derives the work from the written frame alone. If the frame doesn't tell it
  something it needs, the frame was incomplete — that is the test.
- **Phase two — implement, check, archive — heads-down.** `loop.sh [-C <node-path>] execute
  <work-name>` builds the delta, runs `./material/check.sh` (green or it stops) and
  the sweep, then the archive gate adopts or shelves the work according to the signed
  frame. Adoption folds the accepted delta into the addressed node's intent, stamps each
  touched segment's foot with the signer, and records adoption history; shelving records
  history without making proposed parent amendments current.

A work name is a node-local `NNN-slug`. The root node is assumed when no node is named.
`loop.sh -C material/work-home start 001-example` addresses work in the work-home child
node. Slash-separated child-change paths and five-file change folders are legacy history
when retained, not the route for new work; legacy nested child-change archives may be read
if present, but the orchestrator no longer scaffolds them.

The gates and their order are the loop, already intent (`intent/loop.md`); the
orchestrator only operationalizes them and blocks a gate whose preconditions fail. (This
very change introduced the orchestrator, so it was done by hand — nothing yet enforced it.)

## Disciplines the intent does not yet state (debts)

Each line is a **debt**: carried here only until a later change folds it into the intent as
a checked statement, then dropped.

- **Never fabricate content.** An unmaterialized child node is a dormant slot — a real,
  empty node — not a fake app with invented sub-projects.
- **Name in hypercore's own vocabulary** — node, segment, contract, mount, materialize, the
  loop. Reject domain words that collide with the methodology's own concepts.

The earlier third debt — *the machine never endorses* — is **dropped**: it is now the
sign-off gate, and the statement already lives in the `endorsement` segment. A debt the
intent has absorbed leaves the adapter.

---
This adapter is itself governed: the `adapter` segment is its intent, and the sweep reads
this file against that intent, so any rule it drifts into restating — or any debt the intent
has since absorbed — is caught as drift.
