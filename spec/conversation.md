# conversation

The thread and the architect. A thread is one throwaway session; the architect is the single
voice between the operator and the system, reading the operator's words and landing one concrete
consequence on the graph. The role is named **architect** because it holds the operator-aligned
**design judgment** across the work's life — but that judgment is decomposed into capabilities of
its own, so each can be carried as its own skill (ADR 0013): the pre-work intent extraction is
**`grilling`**, the archive-gate judgment over a worker's hand-off (coherence and depth) is
**`coherence`**, and the load-bearing-interface contest is **`design-it-twice`** (ADR 0007).
What `conversation` itself owns is the **thread** and the **single operator-facing voice**: every
word that crosses to the operator comes from the architect, the thread holds no durable state, and
the architect selects among design-it-twice candidates and renders the result back. The capability
stays `conversation`: the thread is a conversation and the operator-facing channel is what it owns.

### Requirement: a thread is throwaway and holds no durable state
A thread MUST be one conversational session, opened when the operator types in and
closed when they have what they came for. It MUST hold no durable state and not be
bound to a piece of work; durability lands on the graph.

#### Scenario: filing intent then reopening
- WHEN the operator files intent in a thread and the thread closes on satisfaction
- THEN the work is on the graph, and reopening the system shows that work and no
  resumed thread; no thread is persisted anywhere

### Requirement: the architect is the single operator-facing voice
Every word that crosses to the operator MUST come from the architect. It
reads the operator's words, decides what they are, and lands exactly one concrete
consequence: filed intent, a card returned to the queue, or an answer.

#### Scenario: the three consequences
- WHEN the operator speaks
- THEN the architect either files intent as standing work, raises a card on
  the queue, or answers the question — one concrete, findable consequence per turn

### Requirement: the operator's act never makes them wait
A turn MUST be summoned off the input loop so the interface stays live while the
machine thinks, and the consequence lands when it returns.

#### Scenario: a slow turn
- WHEN a turn is in flight
- THEN the window keeps painting and servicing keys, and integrates the reply when
  the off-loop call completes

### Requirement: a raw worker output never reaches the operator
No output written for the machine MUST reach the operator unmediated; the
architect authors every operator-facing render. The worker has no channel to the
operator at all, so this is a path that does not exist rather than a rule to keep.

#### Scenario: a worker hands back
- WHEN a worker produces a technical result carrying raw, machine-facing prose
- THEN the architect authors the operator-facing words from it, and none of the
  raw prose appears on any card, render, or node

### Requirement: the architect selects among design-it-twice candidates
For a load-bearing interface designed twice (`design-it-twice`), the architect MUST compare the
candidates on depth, locality, and seam placement and pick or hybridize — machine-side design
judgment recorded as an ADR, not an operator decision (ADR 0007). It
surfaces a card only when the comparison reveals a stake-bearing difference, which re-enters
grilling. The candidate designs and the reasoning stay machine-side; only the
architect-authored stake crosses to the operator, the same routing as a raw worker output.

#### Scenario: the architect picks the interface
- WHEN candidate interfaces for a load-bearing decision are handed to the architect
- THEN it records the pick as a structured design-decision ADR and raises no card unless a
  stake-bearing difference surfaces, in which case the authored stake — not the raw designs —
  reaches the operator
