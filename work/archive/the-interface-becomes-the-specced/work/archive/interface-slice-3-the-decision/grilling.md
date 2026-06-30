surfaced: 0

[CONTRACT]
The decision card grows its full anatomy. A decision card stops showing only its subject line and the bare approve/cut/explain commands: it carries and lays out the synthesis of the call, the options on the table and what each entails (what it unblocks, what it breaks, what keeps running unbacked, what reversing it later costs), the cost of its delay (what it blocks, what compounds while it waits), and the machine's lean with the one thing that would flip it — read off the node where it is recorded, never guessed from the card's shape, the same authority the card's kind is read from. Every heading on the card is a synthesis stating its finding outright, not a label the operator must open to learn what it says; what is needed to decide is on the face, and the confirming detail behind any line sits one keystroke below it — held off the face until summoned. A request for approval stays the lighter card: its kind matches its call and it is not dressed with the decision anatomy. Validated against: the gated scenarios (the carried anatomy and the lighter approval; the laid-out face with its synthesis headings; the confirming detail held one keystroke below) go red→green. Watched on the running window: the full decision card painting its anatomy and folding its confirming detail one keystroke below, confirmed on python3 -m engine.

[DELTA]
# delta — the decision-card anatomy (queue + interface)

## ADDED — queue

### Requirement: a decision card carries its full anatomy
A decision card MUST carry its full anatomy on its node, recorded where the render reads it and never
guessed from the card's shape — the same authority the card's kind is read from: the synthesis of the
call, the options on the table and what each entails (what it unblocks, what it breaks, what keeps running
unbacked, and what reversing it later would cost), the cost of its delay (what it blocks, what compounds
while it waits), the machine's lean, and the one thing that would flip it. A request for approval is the
lighter card and MUST NOT be dressed with the decision anatomy; its kind matches its call.

#### Scenario: a decision carries its anatomy, a request for approval stays lighter
- WHEN a decision card carrying its full anatomy and a request-for-approval card are raised
- THEN the decision card carries its anatomy read off the node — the options and their entailments, the
  cost of its delay, and the machine's lean with the one flip — while the request for approval stays the
  lighter card, not dressed with the decision anatomy, its kind matching its call

  ```check
  raise decision
  anatomy
  raise approval
  lighter
  ```

## ADDED — interface

### Requirement: the decision card lays out its full anatomy, decidable at a glance
The opened decision card MUST lay out its full anatomy on the grid — the synthesis, the options and what
each entails, the cost of its delay, and the machine's lean with the one flip. Every heading MUST state its
finding outright, never a bare label the operator must open to learn what it says. What is needed to decide
MUST be on the face; the confirming detail behind a line MUST sit one keystroke below it — held off the
face, advertised by its affordance, and surfaced only when summoned — so the card is decidable at a glance.

#### Scenario: the opened decision card lays out its anatomy, every heading a synthesis
- WHEN a decision card carrying its full anatomy is opened on the resting face
- THEN its detail lays out the synthesis, the options and what each entails, the cost of its delay, and the
  machine's lean with the one flip, every heading stating its finding outright rather than naming a label to
  open

  ```check
  decide-card
  laid-out
  synthesis
  ```

#### Scenario: what is needed to decide is on the face, the confirming detail one keystroke below
- WHEN a decision card is opened on the resting face
- THEN what is needed to decide is on the face, and the confirming detail behind its lines is held off the
  face one keystroke below — advertised by its affordance and surfaced only when summoned

  ```check
  decide-card
  face
  confirm-below
  ```
