# conversation

The thread and the architect. A thread is one throwaway session; the
architect is the single voice between the operator and the system, which
reads the operator's words and lands one concrete consequence on the graph.
The role is named **architect** because it holds the operator-aligned **design
judgment** — it authors the spec delta (the design of the change), renders it back to
the operator, and judges **depth** at the archive gate — and communicating a design is
part of designing it (rebuild-spec §6, ADR 0006). The capability stays `conversation`:
the thread is a conversation and the operator-facing channel is what it owns.

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

### Requirement: the architect integrates the worker's hand-off
The architect MUST archive a worker's result: coherence-check it against the
contract at the operator's altitude — not a code review — and on a pass fold the refined
delta into the spec, the work leaving the threads view in the same act. The raw report is
input to that judgment, never output.

#### Scenario: coherence decides the fold
- WHEN a worker hands a result back
- THEN a result that honors the contract folds its delta and integrates, and a result that
  does not raises a decision (re-cut, abandon, or change the ask) rather than folding

### Requirement: the architect judges depth at the archive gate
The architect MUST hold the design judgment the worker cannot hold over its own product: at
the archive gate, a result whose material is past the length signal with no depth-decision
accepting it raises a **depth decision** — re-cut / deepen / accept-with-reason — on the
operator's queue, never a silent veto and never a silent pass (rebuild-spec §7.1, ADR 0006).
Depth surfaces to the operator as a decision rather than hiding in a number, so the operator
reads the system's depth; the architect's structural opposition to the worker's investment in
its own product is the defense against self-judging.

#### Scenario: a shallow-or-long result reaches the gate
- WHEN a worker hands back material past the length signal with no depth-decision accepting it
- THEN the architect raises a depth decision (re-cut / deepen / accept-with-reason) and the
  fold is held — the depth surfaces to the operator, not a length number's verdict

### Requirement: a filed ask is grilled before it becomes work
An ask that opens real choices MUST pass a grilling floor before spawning work: the
architect resolves every decision it can from the living spec and intent, and
only a residual decision the operator has a stake in keeps the ask above the floor. An
ask whose every decision is already determined files straight to standing work,
ungrilled. The floor is a standing guard, not a front gate — the same test re-fires
whenever a stake-bearing choice surfaces mid-work.

#### Scenario: above the floor
- WHEN a filed ask leaves a stake-bearing decision open after the machine resolves
  what it can from intent, the spec, and the ADRs
- THEN the ask is held and grilled, and no standing work exists for it yet

#### Scenario: below the floor
- WHEN every decision a filed ask needs is already determined by intent, the spec, or
  an ADR
- THEN it files directly as standing work, with no grilling

### Requirement: grilling asks one question at a time, each carrying a lean
A grilling pass MUST surface its residual decisions as questions on the queue one at a
time, in dependency order, each carrying the machine's recommended answer (the lean)
and the one thing that would flip it. The operator settles each by accepting the lean
or answering in their own words, so they ratify far more often than they author.

#### Scenario: the next question waits its turn
- WHEN a grilling question is on the queue
- THEN the pass's later questions are held off the queue until it is answered, and
  answering it surfaces the next one

### Requirement: a grilling pass yields the contract and the spec delta
A resolved grilling pass MUST produce the operator-view entry — the contract the
result is later validated against — and the spec delta the change will realize,
authored by the architect against the concise specs its scan reaches.

#### Scenario: the pass resolves
- WHEN the last grilling question is answered
- THEN the architect produces the view entry and a well-formed spec delta, and
  raises the entry on the queue for ratification
