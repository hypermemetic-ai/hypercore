# ADR 0007 — design-it-twice as its own capability; selection is machine-side

Status: machine-owned, awaiting ratification — except the selection-landing decision, which the
operator ratified during slice 8's grilling (2026-06-21). [machine]

## Context

Slice 8 (rebuild-spec §9.8, §7.5) builds the judgment use of the worktree concurrency:
**design-it-twice** for load-bearing interfaces. The worktree fence already isolates a worker
for throughput (slice 4); the same isolation, run as a contest of candidates, serves design
quality. Two questions had to be settled to build it: where the new behavior lives (a capability
boundary, like ADRs 0003/0004/0005), and where the **selection** among candidates lands — the
one stake-bearing fork, because it is a "what crosses to the operator" call.

## Decision

**design-it-twice is its own capability, and the selection is machine-side.**

- **Its own capability boundary.** The contest — candidates in isolated fences, the comparison
  on depth/locality/seam, the machine-side pick, the stake-escalation — is a coherent, deep slice
  of behavior that *orchestrates* `worker` (it borrows the fence) and `conversation` (the
  architect judges) without belonging to either, exactly as `architecture-review` (0005)
  orchestrates the scan without belonging to `folding-conditions`. It owns `spec/design-it-twice/`
  and `hyper/design.py`. The boundary is decided machine-side (the operator's anchor is the
  contract, not the decomposition), consistent with 0003/0004/0005.
- **Selection is machine-side — operator-ratified.** The architect compares the candidates on
  depth/locality/seam, picks or hybridizes, and records the pick as a **structured
  design-decision ADR** (`design-decision: <subject> → <chosen> — <reason>`). The interface shape
  is machine-side design, like the spec delta: the operator's trust anchor is the contract it
  ratifies, never the machine-side design (rebuild-spec §6.4). So the pick does not spend the
  operator's go. *The operator chose this landing during grilling* — over an operator-facing
  decision card and over a "machine picks + always notify" middle ground.
- **A stake-bearing difference still reaches the operator.** When the comparison reveals a
  difference the operator has a stake in (operator-visible behavior, hard to reverse, real cost),
  it re-enters grilling as a decision card carrying only the architect-authored stake — the
  standing-guard floor (§5.1). Only that stake crosses; the candidate designs and the reasoning
  stay machine-side, in the fences and the ADR — the same routing that keeps a raw worker output
  off the operator's surfaces.
- **Candidates design, they do not implement.** A candidate produces an interface design — the
  interface, what it hides, the seam, the deletion-test argument — not a built-out
  implementation; depth, locality, and seam placement are judgable from the design, and building
  each one out would throw most of the work away. The winning design carries forward as the
  contract for one ordinary worker apply.
- **The concurrency clause is composition, not a scheduler.** The check's first clause —
  concurrent workers advance one graph in isolation and each folds its delta — is satisfied by
  the slice-4 fence composing: several workers hold distinct fences at once, each folding
  independently. No throughput scheduler is built; the judgment use is the slice (next-work.md:
  "slice 8 is the judgment use," held apart from throughput parallelism).

## Grounds

The fence is the keystone the resolution rests on. Isolation already makes throughput safe; the
same isolation makes a contest safe, so design-it-twice borrows the fence (`worker.worktree`,
tagged per candidate) rather than inventing a parallelism primitive — `worker.commit_tree` is the
one in-fence commit both the worker's result and a candidate's design land through, so the
fence-commit knowledge stays in one place. Selection lands machine-side for the same reason delta
authorship does (0006/§6.4): design judgment co-locates with the role that holds it (the
architect), and the operator's leverage is the contract, kept whole by surfacing only a
stake-bearing difference. The trigger — judging an interface load-bearing — is the architect's
judgment (§7.5) with the depth gate's "cannot deepen in place" (§7.1) as a second entry; the
capability is invoked on that judgment, the automatic detection during live grilling being the
natural next integration, recorded honestly rather than fabricated (the slice-7 F1 precedent).

## Consequences

A new capability `design-it-twice` and `hyper/design.py`. `worker` gains a tagged-sibling fence
and a shared `commit_tree`, and a requirement that concurrent workers fold in isolation;
`conversation` gains the architect's selection-judgment requirement; the glossary gains
design-it-twice, design contest, candidate, design brief, and design-decision. ADR 0003/0004/0005
(capability boundaries, one criterion at two scopes) stand unchanged; this ADR neither supersedes
nor is superseded. A future change that re-cuts this boundary, or that moves selection to the
operator, carries an ADR superseding this one.
