# worker

The system-facing half of the split. A worker carries out a spawned ask: it builds,
fenced in its own git worktree and grounded in its capability's spec slice, and hands
the conversationalist a complete technical result. It never faces the operator — every
word that crosses to the operator is the conversationalist's, authored from the result.

### Requirement: a worker is system-facing and never reaches the operator
A worker's audience MUST be the conversationalist and the spec, never the operator. Its
result is written for the machine; it has no channel to the operator at all, so a raw
worker output reaches the operator through no path — the conversationalist authors every
operator-facing word from the result.

#### Scenario: a worker hands back
- WHEN a worker produces a technical result carrying raw, machine-facing prose
- THEN none of that prose appears on any card, render, or node; only what the
  conversationalist authors from it crosses to the operator

### Requirement: a worker is grounded in its capability's spec slice, by construction
A worker MUST be handed the living spec with the capabilities its change touches marked as
its grounding — their requirements and scenarios foregrounded — AND the rest of the spec
carried beside them for scan, with the glossary and the system's decisions, assembled before
it runs, so there is no path that runs a worker without its grounding. It holds the spec,
never raw code, and never the operator view. A worker is **not slice-confined** (rebuild-spec
§4.1, §6.4): a delta cannot be authored or verified from one capability in isolation, so its
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

### Requirement: a worker runs fenced in its own git worktree
A worker MUST run in its own git worktree — a separate checkout on its own branch, fenced
from its siblings and the main line. It builds in isolation and its own commits reach the
shared record without touching another worker's tree or the main line until the result
integrates.

#### Scenario: the fence holds
- WHEN a worker is delegated a node
- THEN it gets a worktree distinct from the main tree, commits its result there on its own
  branch, and that commit is reachable in the record but absent from the main line

### Requirement: the worker applies and refines the delta the conversationalist proposed
A worker MUST rescan the current spec to verify the handed delta against present reality,
build behind a feedback loop, and refine the delta to match what it built; the
conversationalist then coherence-checks the result against the contract and archives the
delta. The crossing is propose (conversationalist) → apply (worker) → archive
(conversationalist), one delta end to end.

#### Scenario: the result integrates
- WHEN a worker hands back a refined delta and the conversationalist judges the result
  coherent with the contract
- THEN the delta folds into the spec and the work leaves the threads view in the same act;
  an incoherent result raises a decision instead of folding
