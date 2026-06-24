# queue
<!-- vision: queue, card, decision, approve, endorse -->

The decision surface. The queue is a view of every node awaiting the operator,
read fresh each time. A card carries its **kind** — the call it makes on the
operator — and the operator settles it with one of three endorsements.

### Requirement: the queue is a view of awaiting nodes
The queue MUST be the set of nodes in the awaiting state, read live; settling a
node removes it from the view in the same act, with no list to keep in sync.

#### Scenario: a card is settled
- WHEN a machine-owned statement is raised and then approved or cut
- THEN it appears on the queue while awaiting and is gone from the queue once settled

  ```check
  raise decision
  on-queue
  approve
  off-queue
  ```

### Requirement: the operator endorses with approve, cut, or explain
The operator MUST settle a card by exactly one of three commands: **approve** drops
the [machine] marker and settles the node; **cut** removes the words; **explain**
returns the story toward the decision and leaves the card standing.

#### Scenario: approve
- WHEN the operator approves a machine-owned card
- THEN the node's [machine] marker is dropped, its owner becomes the operator, and
  it leaves the queue

  ```check
  raise decision
  approve
  endorsed
  off-queue
  ```

#### Scenario: cut
- WHEN the operator cuts a card
- THEN the node's words are removed and recoverable from the record

  ```check
  raise statement
  cut
  gone
  ```

#### Scenario: explain
- WHEN the operator presses explain on a card
- THEN the architect returns the story toward the decision and the card
  stays on the queue

  ```check
  raise decision
  explain
  told
  ```

### Requirement: a card's kind is recorded and matches its call
A card's **kind** MUST be recorded on the node and read at render time, never guessed from the
card's shape. The kind is one of five along the work's life — a **grilling question**, a
**ratification**, a **request for approval**, a **decision**, or an **acceptance** — and it MUST
match the call: a real judgment the operator must reason through is a **decision**; a step needing
only the operator's go is a lighter **request for approval**, not dressed as a decision.

#### Scenario: a genuine fork versus a go-ahead
- WHEN the machine raises a card
- THEN its recorded kind says whether it is a decision or a lighter request for approval, and the
  render reads that kind rather than inferring it from the card's shape

  ```check
  raise decision
  reads decision
  raise approval
  reads approval
  raise acceptance
  reads acceptance
  ```

### Requirement: a grilling question is a card carrying its lean and flip
A grilling question MUST appear on the queue as a card showing the question, the
machine's lean, and the one thing that would flip it — a lighter card, not a decision
dressed full; approving it accepts the lean.

#### Scenario: a question is shown
- WHEN a grilling question reaches the queue
- THEN its card carries the lean and the flip, and approving it accepts the lean while
  the operator may instead answer in their own words

  ```check
  surface
  question
  accepts-lean
  ```

### Requirement: work does not spawn until the view entry is ratified
A behavior-changing ask MUST NOT become standing work until the operator ratifies its
view entry. Ratifying the entry is the operator's informed go and the contract the
result is later checked against; until then the held ask is neither a card to clear
nor work in flight.

#### Scenario: the gate holds
- WHEN a grilling pass has produced its view entry but the operator has not ratified it
- THEN no standing work exists for the ask, and ratifying the entry spawns it

  ```check
  surface
  resolve
  unspawned
  ratify
  spawned
  ```

### Requirement: approving a length decision records the accepted length
The acceptance of a flagged file length is the producer of the accepted-length record: when the
operator approves a length decision — the depth gate's accept-the-length outcome — the system MUST
record the accepted length through the writer seam, so the gate then clears for that file. The
operator's go is the act; the durable record is its consequence.

#### Scenario: approving a length decision
- WHEN the operator approves a decision the depth gate raised over a file's length
- THEN the accepted length named in the decision is recorded, the card leaves the queue, and the
  gate clears for that file at the recorded length

  ```check
  raise length
  accept-length
  off-queue
  recorded
  ```
