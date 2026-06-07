# Codex adapter

This is the **adapter** segment of hypercore's intent, materialized for the Codex
harness (`intent/adapter.md`). It states no rule of its own: every rule lives in
the intent, and where this file and the intent disagree, **the intent wins**. It routes
you to the intent and the loop, and makes them enforceable.

This repository is hypercore applied to itself. You are the machine in "operator and
machine," and you begin each session memoryless.

## What the adapter promises

Agreement between this harness and the methodology: that you act in accordance with the
intent and run the loop, not because you chose to, but because the workflow makes the
gates unskippable. Pointing alone is a request; the orchestrator is how agreement is
kept.

## Orient before you touch anything

First classify the request surface. Ordinary conversation, explanation, and read-only
inspection can proceed directly when they do not need adoption or shelving. Governed work
starts or continues a work node before material changes; perceived simplicity, small file
count, convenience, or low risk never waives the loop for governed work.

Read, in this order. This is where orient begins:

1. `hypercore.md` — the methodology.
2. `intent/organizing-document.md` — how the intent is divided into segments.
3. The segment the work touches (`intent/<segment>.md` and its
   `machine-statements/<segment>.md`), every work node in flight across the node tree,
   and any related work named by a frame.

Don't guess. Search the web for what you don't know. Ask the operator what the artifacts
can't tell you.

## The rigid workflow — `adapter/loop.sh`

Every work node runs the loop's five gates, driven by the orchestrator in two phases split at
the operator's **sign-off**:

- **Phase one — orient, frame — design-phase collaboration.** You and the operator choose
  direction before sign-off by naming the addressed node, node-local work name, target
  segments, work in flight, work classification, and any open direction; before settling
  an open route, surface the problem, constraints, decision surface for operator
  direction, options and tradeoffs, evidence standard and basis, uncertainty, rejection
  conditions, and any
  unresolved operator discomfort or open judgement. The written frame records common
  ground and operator deliberation: operator decisions, authority, machine assumptions,
  evidence, uncertainty, open blockers, proof state, feedback capture, handoff state,
  problem/domain map, operator expectation, and rejection conditions. Evidence depth is problem-relative.
  Use relevant trustworthy external evidence when it helps, and avoid superficial research when local facts
  and reasoning are the better basis. You frame the work
  node directly under the addressed node as `<NNN-slug>/`, with the written frame under
  `intent/frame/`, and run the sweep over the whole corpus and work in flight across the
  node tree, including related work named by a frame. Interaction
  surfaces here. It ends when the operator signs off:
  from the root, `./signoff` signs the single frame-complete, unsigned active work node
  when the operator identity is unambiguous; the explicit
  `loop.sh [-C <node-path>] signoff <work-name> <operator>` form also writes a
  `signed-off-by` line. **You never sign off for them.**
- **The session clears at sign-off.** Phase two runs on a fresh, memoryless `codex exec`
  opened by implement and resumed across check and archive. It re-derives the work from
  the written frame alone. If the frame doesn't tell it something it needs, the frame was
  incomplete. That is the test.
- **Phase two — implement, check, archive — heads-down.**
  `loop.sh [-C <node-path>] execute <work-name>` builds the delta,
  runs `./check.sh` (green or it stops) and the sweep, then the archive gate
  adopts or shelves the work according to the signed frame. Adoption folds the accepted
  delta into the addressed node's intent, stamps each touched segment's foot with the
  signer, and records adoption history; shelving records history without making proposed
  parent amendments current.

A work name is a node-local `NNN-slug`. The root node is assumed when no node is named.
`loop.sh -C home start 001-example` addresses work in the home child node, and
`loop.sh -C home/<name> start 001-example` addresses work through a
linked mounted node's mount path. Current work is addressed by the node path plus one
node-local work name, with the frame under that work node's `intent/frame/`.

The gates and their order are the loop, already intent (`intent/loop.md`); the
orchestrator only operationalizes them and blocks a gate whose preconditions fail.

## Disciplines the intent does not yet state (debts)

Each line is a **debt**: carried here only until a later change folds it into the intent
as a checked statement, then dropped.

- **Never fabricate content.** An unmaterialized child node is a dormant slot — a real,
  empty node — not a fake app with invented sub-projects.
- **Name in hypercore's own vocabulary** — node, segment, contract, mount, materialize,
  the loop. Reject domain words that collide with the methodology's own concepts.

---
This adapter is itself governed: the `adapter` segment is its intent, and the sweep reads
this file against that intent, so any rule it drifts into restating, or any debt the intent
has since absorbed, is caught as drift.
