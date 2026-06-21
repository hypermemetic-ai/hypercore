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
