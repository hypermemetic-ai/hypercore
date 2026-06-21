# conversation

The thread and the conversationalist. A thread is one throwaway session; the
conversationalist is the single voice between the operator and the system, which
reads the operator's words and lands one concrete consequence on the graph.

### Requirement: a thread is throwaway and holds no durable state
A thread MUST be one conversational session, opened when the operator types in and
closed when they have what they came for. It MUST hold no durable state and not be
bound to a piece of work; durability lands on the graph.

#### Scenario: filing intent then reopening
- WHEN the operator files intent in a thread and the thread closes on satisfaction
- THEN the work is on the graph, and reopening the system shows that work and no
  resumed thread; no thread is persisted anywhere

### Requirement: the conversationalist is the single operator-facing voice
Every word that crosses to the operator MUST come from the conversationalist. It
reads the operator's words, decides what they are, and lands exactly one concrete
consequence: filed intent, a card returned to the queue, or an answer.

#### Scenario: the three consequences
- WHEN the operator speaks
- THEN the conversationalist either files intent as standing work, raises a card on
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
conversationalist authors every operator-facing render.

#### Scenario: a worker hands back
- WHEN a worker produces a technical result
- THEN the conversationalist distills it before any of it crosses to the operator
- NOTE: the worker role is unbuilt at this slice; this requirement is the contract
  the worker slice must honor, and is shallow until then

### Requirement: a filed ask is grilled before it becomes work
An ask that opens real choices MUST pass a grilling floor before spawning work: the
conversationalist resolves every decision it can from the living spec and intent, and
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
authored by the conversationalist against the concise specs its scan reaches.

#### Scenario: the pass resolves
- WHEN the last grilling question is answered
- THEN the conversationalist produces the view entry and a well-formed spec delta, and
  raises the entry on the queue for ratification
