# design-it-twice
<!-- vision: candidate, isolat, fence -->

The judgment use of the worktree concurrency. The fence that isolates a
worker for throughput also isolates several candidates for design quality: for an interface the
architect judges load-bearing, the decision is **designed twice** — several candidates, each in
its own fence, each briefed to design the *same* interface radically differently — and the
architect picks or hybridizes on **depth, locality, and seam placement**. The first shape
committed is rarely the deepest, so design-it-twice applies hypercore's existing isolation where
first-draft commitment hurts most: the shape of a deep module. It rests on the worker's fence composing —
several candidates advancing one decision at once, isolated, exactly as concurrent workers
advance the tree at once.

### Requirement: a load-bearing interface decision is designed twice, in isolation
A load-bearing interface decision MUST be designable as a contest of several candidates, one per
brief (minimize the interface / maximize flexibility / optimize the common caller /
ports-and-adapters), each running in its own fence — the worker's worktree, tagged per candidate
— so the candidates advance the same decision at once, isolated from each other and the main
line. The architect judges an interface load-bearing; the depth gate's "cannot deepen in
place" is the second entry.

#### Scenario: the decision is designed twice
- WHEN a load-bearing interface decision is designed twice with N briefs
- THEN N candidates are produced, each in its own fence, each committing its design on its own
  branch, none touching a sibling's tree or the main line

  ```check
  contest 2
  candidates 2
  branch each
  off-main DESIGN.md
  ```

### Requirement: candidates design, they do not implement
A candidate MUST produce an interface **design** — the interface, what it hides, where the seam
falls, and the deletion-test argument for its depth — not a built-out implementation. Depth,
locality, and seam placement are judgable from the design; building each candidate out would
throw most of the work away. The winning design carries forward as the contract for one ordinary
worker apply.

#### Scenario: a candidate hands back a design
- WHEN a candidate runs under its brief
- THEN it produces the interface, what it hides, the seam, and the depth argument, and no
  implementation is required for the comparison

  ```check
  contest 2
  design complete
  ```

### Requirement: the architect selects machine-side and records the design decision
The architect MUST compare the candidates on **depth, locality, and seam placement**, pick one
or hybridize, and record the pick as a **structured design decision** — a parseable
`design-decision: <subject> → <chosen> — <reason>` line, the same structured-record idiom the
accepted-length record uses. The selection is machine-side design judgment: the operator's trust anchor
is the contract, not the machine-side design, so the pick does not
spend the operator's go. The candidate designs and the reasoning stay machine-side — in the
fences and the recorded design decision — never on a card.

#### Scenario: the pick is recorded, machine-side
- WHEN the architect picks or hybridizes across the candidates with no stake-bearing difference
- THEN the pick is recorded as a structured design decision, no card reaches the operator,
  and no raw candidate design reaches a card, render, or node

  ```check
  twice nostake
  recorded
  card none
  no-leak
  scratch torn-down
  ```

### Requirement: a stake-bearing difference re-enters grilling
WHEN the comparison reveals a difference the operator has a stake in — operator-visible
behavior, hard to reverse, or real cost — the architect MUST raise it as a decision card
parented to the decision node (the standing-guard floor), carrying only the
architect-authored stake. The interface shape stays machine-side; only a stake-bearing
behavioral difference crosses to the operator.

#### Scenario: a stake surfaces in the comparison
- WHEN the architect's comparison finds a stake-bearing difference between candidates
- THEN a decision card carrying the authored stake is raised on the queue, parented to the node,
  and the raw candidate designs do not cross to the operator

  ```check
  twice stake
  card decide
  stake-crosses
  no-leak
  ```
