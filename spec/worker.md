# worker

The system-facing half of the split. A worker carries out a spawned ask: it builds,
fenced in its own git worktree and grounded in its capability's spec slice, and hands
the architect a complete technical result. It never faces the operator — every
word that crosses to the operator is the architect's, authored from the result.

### Requirement: a worker is system-facing and never reaches the operator
A worker's audience MUST be the architect and the spec, never the operator. Its
result is written for the machine; it has no channel to the operator at all, so a raw
worker output reaches the operator through no path — the architect authors every
operator-facing word from the result.

#### Scenario: a worker hands back
- WHEN a worker produces a technical result carrying raw, machine-facing prose
- THEN none of that prose appears on any card, render, or node; only what the
  architect authors from it crosses to the operator

### Requirement: a worker is grounded in its capability's spec slice, by construction
A worker MUST be handed the living spec with the capabilities its change touches marked as
its grounding — their requirements and scenarios foregrounded — AND the rest of the spec
carried beside them for scan, with the glossary and the system's decisions, assembled before
it runs, so there is no path that runs a worker without its grounding. It holds the spec,
never raw code, and never the operator view. A worker is **not slice-confined** (ADR 0009): a
delta cannot be authored or verified from one capability in isolation, so its
rescan covers the whole spec and catches a capability the handed delta mis-named or missed.

#### Scenario: assembling the context
- WHEN a worker is run on a node whose handed delta names a set of capabilities
- THEN its context contains the whole spec — the named capabilities marked as grounding and
  the rest carried for scan — plus the glossary and decisions, and its prompt foregrounds the
  grounding while keeping the full scan

#### Scenario: the rescan catches a mis-mapping
- WHEN a handed delta names a capability the change does not touch, or omits one it does
- THEN the worker's context still holds the whole spec, so its rescan can catch the
  mis-mapping rather than trust the delta's list — which a slice-confined worker could not

### Requirement: a worker is grounded in the depth disciplines, every episode
A worker MUST be handed the **depth disciplines** as standing grounding in every episode — the
deep-module framework (a lot of behavior behind a small interface; a simple interface matters
more than a simple implementation; pull complexity downward), strategic over tactical
programming, and the **red flags** of shallowness — so it builds **deep up front** rather than
relying on the gate to catch shallowness after the fact (ADR 0006). This is
the *proactive* primary anti-complexity defense: a worker that shares the long-term-health
concern produces deep modules, so the folding-conditions depth gate stays a rarely-tripped
backstop, not an operator-load generator. The grounding is assembled into the worker's prompt
by construction, like its spec slice — there is no path that runs a worker without it.

The disciplines MUST be **single-sourced**, not a frozen copy: depth is a capability like any other
(`spec/depth.md`, ADR 0019), carried in the worker's whole-spec grounding and foregrounded in its
prompt, so a sharpened slice reaches the next worker with no second copy to drift (ADR 0009). The
same slice renders the `depth` **skill** through the methodology seam, materialized on disk for the
harness that loads skills natively — one source, the channels derived from it, the way the as-built
is derived from the model and only the vision is authored.

#### Scenario: the depth disciplines are in the grounding
- WHEN a worker is assembled to run
- THEN its prompt carries the deep-module framework and the red flags, foregrounded as
  disciplines it is held to, so it builds deep up front

#### Scenario: the disciplines are derived from their source
- WHEN the depth capability (`spec/depth.md`) is sharpened
- THEN the next worker's depth grounding renders the change with nothing hand-copied, and the
  retired frozen constant cannot drift from the source because it no longer exists

### Requirement: a worker runs fenced in its own git worktree
A worker MUST run in its own git worktree — a separate checkout on its own branch, fenced
from its siblings and the main line. It builds in isolation and its own commits reach the
shared record without touching another worker's tree or the main line until the result
integrates.

#### Scenario: the fence holds
- WHEN a worker is delegated a node
- THEN it gets a worktree distinct from the main tree, commits its result there on its own
  branch, and that commit is reachable in the record but absent from the main line

### Requirement: concurrent workers advance the graph in isolation, each folding its own delta
The fence MUST compose: several workers MAY hold distinct worktrees at once, each building and
committing on its own branch, none touching a sibling's tree or the main line, and each folding
its own delta into the one spec independently. Isolation is the concurrency model — throughput is
many fences at once, and the same composition is what `design-it-twice` runs a contest of
candidates on (ADR 0007).

#### Scenario: two workers advance at once
- WHEN two workers hold two distinct fences at the same time
- THEN each commits in its own tree off the main line, and each folds its own delta into the
  spec with no interference between them

### Requirement: the worker applies and refines the delta the architect proposed
A worker MUST rescan the current spec to verify the handed delta against present reality,
build behind a feedback loop, and refine the delta to match what it built; the
architect then coherence-checks the result against the contract and archives the
delta. The crossing is propose (architect) → apply (worker) → archive
(architect), one delta end to end.

#### Scenario: the result integrates
- WHEN a worker hands back a refined delta and the architect judges the result
  coherent with the contract
- THEN the delta folds into the spec and the work leaves the work view in the same act;
  an incoherent result raises a decision instead of folding
