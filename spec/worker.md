# worker
<!-- vision: worker, worktree, isolat, concurren, fence, parallel -->

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

  ```check
  build
  leak none
  ```

### Requirement: a worker is grounded in its capability's spec slice, by construction
A worker MUST be handed the living spec with the capabilities its change touches marked as
its grounding — their requirements and scenarios foregrounded — AND the rest of the spec
carried beside them for scan, with the glossary, assembled before it runs, so there is no path
that runs a worker without its grounding. The spec capabilities and the glossary are
**preloaded whole** — the small, scannable, high-signal core, the defense against the architect's
mis-scoping and against worker myopia. The **long history and grounds of past decisions** are NOT
preloaded into the prompt: they are the long reference with no whole-picture stake, so the worker
runs at its fence and greps **just-in-time** for them in its own checkout (`work/archive/`, where a
node archives with its work) as the change needs. It holds the spec, never raw code, and never the
operator view. A worker is **not slice-confined**: a delta cannot be authored or verified from one
capability in
isolation, so its rescan covers the whole spec and catches a capability the handed delta mis-named
or missed.

#### Scenario: assembling the context
- WHEN a worker is run on a node whose handed delta names a set of capabilities
- THEN its context contains the whole spec — the named capabilities marked as grounding and
  the rest carried for scan — plus the glossary, all preloaded whole; the long history and grounds
  of past decisions are not inlined but reachable in its checkout (`work/archive/`) for a
  just-in-time grep, and its prompt foregrounds the
  grounding while keeping the full scan

  ```check
  plant-grounds
  spawn worker communication
  grounding marks worker communication
  grounding whole-spec
  grounding carries-spec
  grounding holds-no-code
  grounding omits-grounds
  grounding points-to-archive
  ```

#### Scenario: the rescan catches a mis-mapping
- WHEN a handed delta names a capability the change does not touch, or omits one it does
- THEN the worker's context still holds the whole spec, so its rescan can catch the
  mis-mapping rather than trust the delta's list — which a slice-confined worker could not

  ```check
  spawn tree
  grounding marks tree
  grounding whole-spec
  ```

### Requirement: a worker is grounded in the depth standards, every episode
A worker MUST be handed the **depth standards** as standing grounding in every episode — the
deep-module framework (a lot of behavior behind a small interface; a simple interface matters
more than a simple implementation; pull complexity downward), strategic over tactical
programming, and the **red flags** of shallowness — so it builds **deep up front** rather than
relying on the gate to catch shallowness after the fact. This is
the *proactive* primary anti-complexity defense: a worker that shares the long-term-health
concern produces deep modules, so the folding-conditions depth gate stays a rarely-tripped
backstop, not an operator-load generator. The grounding is assembled into the worker's prompt
by construction, like its spec slice — there is no path that runs a worker without it.

The disciplines MUST be **single-sourced**, not a frozen copy: depth is a capability like any other
(`spec/depth.md`), carried in the worker's whole-spec grounding and foregrounded in its
prompt, so a sharpened slice reaches the next worker with no second copy to drift. The
same slice renders the `depth` **skill** through the methodology seam, materialized on disk for the
harness that loads skills natively — one source, the channels derived from it, the way the as-built
is derived from the model and only the vision is authored.

#### Scenario: the depth standards are in the grounding
- WHEN a worker is assembled to run
- THEN its prompt carries the deep-module framework and the red flags, foregrounded as
  disciplines it is held to, so it builds deep up front

  ```check
  spawn worker
  grounding carries-depth
  ```

#### Scenario: the disciplines are derived from their source
- WHEN the depth capability (`spec/depth.md`) is sharpened
- THEN the next worker's depth grounding renders the change with nothing hand-copied, and the
  retired frozen constant cannot drift from the source because it no longer exists

  ```check
  spawn worker
  sharpen
  grounding renders
  ```

### Requirement: a worker runs fenced in its own git worktree
A worker MUST run in its own git worktree — a separate checkout on its own branch, fenced
from its siblings and the main line. It builds in isolation and its own commits reach the
shared record without touching another worker's tree or the main line until the result
integrates. The worker's **model transport runs with its working directory set to that
worktree**, so the checkout is the worker's working directory: its source, the archived grounds
(`work/archive/`), and the derived channel files (the anchor and skills) are read from the
checkout, and the harness auto-loads the fence's anchor and discovers its skills.

#### Scenario: the fence holds
- WHEN a worker is dispatched a node
- THEN it gets a worktree distinct from the main tree, commits its result there on its own
  branch, and that commit is reachable in the record but absent from the main line

  ```check
  fence off-main
  ```

#### Scenario: the worker runs at its fence
- WHEN a worker's model is summoned to build
- THEN its transport runs with the worktree as its working directory, so it reads the archived
  grounds and its channel files from its own checkout rather than from an inlined prompt

  ```check
  fence binds-cwd
  ```

### Requirement: concurrent workers advance the tree in isolation, each folding its own delta
The fence MUST compose: several workers MAY hold distinct worktrees at once, each building and
committing on its own branch, none touching a sibling's tree or the main line, and each folding
its own delta into the one spec independently. Isolation is the concurrency model — throughput is
many fences at once, and the same composition is what `design-it-twice` runs a contest of
candidates on.

#### Scenario: two workers advance at once
- WHEN two workers hold two distinct fences at the same time
- THEN each commits in its own tree off the main line, and each folds its own delta into the
  spec with no interference between them

### Requirement: the worker applies and refines the delta the architect proposed
A worker MUST rescan the current spec to verify the handed delta against present reality,
build to turn the capability's architect-authored scenarios **red→green**, and refine the delta —
including any new or sharpened scenario the behavior needs — to match what it built. It authors **no
loop** and no check that judges its own work: the oracle is the self-model's own scenario, run
red→green by the gate over its fence, so the builder can never write the check that clears it. The
architect then coherence-checks the result against the contract and archives the delta. The crossing
is propose (architect) → apply (worker) → archive (architect), one delta end to end.

#### Scenario: the result integrates
- WHEN a worker hands back a refined delta and the architect judges the result
  coherent with the contract
- THEN the delta folds into the spec — only when the touched capability's scenarios went red→green —
  and the work leaves the work view in the same act; an incoherent result, or a scenario that did not
  transition, raises a decision instead of folding

  ```check
  build
  integrates
  ```
