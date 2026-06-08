# options - 012-self-applied-phase-two

Direction options are drafted by the machine for operator selection. The operator selects one
route, rejects all options, or aborts without writing direction. Both routes carry the same
three fixes — cache soft-fail (a cache-record failure becomes a rebuild, never a halt), the
implement-gate/archive reconciliation (a unit may edit intent when its own proof is a check
over that intent; archive adopts = verify-against-signed-frame + stamp + record), and the
handoff (`execute` auto-detects the single signed unarchived node; adapter prose names the
Opus->codex launch + supervise path and separates `start` from `execute`). They differ only on
orchestrator self-edit safety.

## option 1

id: include-orchestrator-safety
kind: selected-route
summary: Ship all four fixes. Cache soft-fail; implement-gate/archive reconciliation; handoff
  auto-detect + Opus-launch + kickoff prose; and orchestrator self-edit safety — the
  orchestrator runs from a snapshot so a unit that edits `loop.sh` mid-run cannot corrupt the
  live run, with a self-test proving it. Deep fold/intent-vs-material semantics defer to the
  work-node-collapse loop.
reversibility: one-way
tradeoff: Delivers a fully hands-off autonomous self-applied phase two: units may freely edit
  `loop.sh`/`check.sh`/intent and the run stays safe. Cost: the snapshot/self-edit-safety
  change is the largest and least-exercised piece, so it carries the most build and review risk
  in this node.

## option 2

id: defer-orchestrator-safety
kind: selected-route
summary: Ship three fixes — cache soft-fail; implement-gate/archive reconciliation; handoff
  auto-detect + Opus-launch + kickoff prose — and carry orchestrator self-edit safety as an
  explicit recorded debt for a later loop. Deep fold semantics also defer to work-node-collapse.
reversibility: one-way
tradeoff: Leaner, lower-risk node that still fixes the 011 halt and makes the handoff real.
  Cost: a unit that rewrites `loop.sh` mid-run remains a latent hazard, so a self-change that
  edits `loop.sh` heavily may still need Opus to intervene during supervision until the debt is
  paid.

## rejection choices

none: The operator may reject all options and send the work back to frame.
abort: The operator may abort without writing direction.
