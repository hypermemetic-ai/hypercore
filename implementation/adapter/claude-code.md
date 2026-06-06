# Claude Code adapter

This is the **adapter** segment of hypercore's intent, materialized for the Claude Code
harness (`documentation/adapter.md`). It states no rule of its own: every rule lives in the
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

1. `implementation/hypercore.md` — the methodology.
2. `documentation/organizing-document.md` — how the intent is divided into segments.
3. The segment you're about to change (`documentation/<segment>.md` and its
   `machine-statements/<segment>.md`), and every change in flight under
   `documentation/changes/`.

Don't guess. Search the web for what you don't know. Ask the operator what the artifacts
can't tell you.

## The rigid workflow — `implementation/adapter/loop.sh`

Every change runs the loop's five gates, driven by the orchestrator in two phases split at
the operator's **sign-off**:

- **Phase one — orient, frame — interactive.** You and the operator frame the change as a
  delta in `documentation/changes/NNN-slug/` (five files: `delta why proof endorsement
  plan`) and run the sweep over the whole corpus and the changes in flight. Interaction
  surfaces here. It ends when the operator signs off: `loop.sh signoff <slug> <operator>`
  writes a `signed-off-by` line. **You never sign off for them.**
- **The session clears at sign-off.** Phase two runs on a fresh, memoryless `claude -p`
  that re-derives the work from the written frame alone. If the frame doesn't tell it
  something it needs, the frame was incomplete — that is the test.
- **Phase two — implement, check, archive — heads-down.** `loop.sh execute <slug>` builds
  the delta, runs `./implementation/check.sh` (green or it stops) and the sweep, then folds
  the delta into the intent, stamps each touched segment's foot with the signer, and moves
  the change to `documentation/changes/archive/`.

The gates and their order are the loop, already intent (`documentation/loop.md`); the
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
