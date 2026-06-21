# queue

The decision surface. The queue is a view of every node awaiting the operator,
read fresh each time. A card carries the weight of its call, and the operator
settles it with one of three endorsements.

### Requirement: the queue is a view of awaiting nodes
The queue MUST be the set of nodes in the awaiting state, read live; settling a
node removes it from the view in the same act, with no list to keep in sync.

#### Scenario: a card is settled
- WHEN a machine-owned statement is raised and then approved or cut
- THEN it appears on the queue while awaiting and is gone from the queue once settled

### Requirement: the operator endorses with approve, cut, or explain
The operator MUST settle a card by exactly one of three commands: **approve** drops
the [machine] marker and settles the node; **cut** removes the words; **explain**
returns the story toward the decision and leaves the card standing.

#### Scenario: approve
- WHEN the operator approves a machine-owned card
- THEN the node's [machine] marker is dropped, its owner becomes the operator, and
  it leaves the queue

#### Scenario: cut
- WHEN the operator cuts a card
- THEN the node's words are removed and recoverable from the record

#### Scenario: explain
- WHEN the operator presses explain on a card
- THEN the conversationalist returns the story toward the decision and the card
  stays on the queue

### Requirement: a card's weight matches its call
A real judgment the operator must reason through MUST be presented as a decision;
a step needing only the operator's go MUST be presented as a lighter request for
approval, not dressed as a decision.

#### Scenario: a genuine fork versus a go-ahead
- WHEN the machine raises a card
- THEN its kind records whether it is a decision or a lighter approval, so the
  weight of the card matches the weight of the call
