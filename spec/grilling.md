# grilling
<!-- vision: extraction, intent-setting -->

Intent extraction by grilling — how the architect turns a filed ask into ratified work
without authoring on the operator's behalf — carved from `communication` as its own skill. Before an
ask that opens real choices becomes work, the architect runs a grilling pass: it resolves every
decision it can from the living spec and intent, and surfaces only the residue — the decisions
the operator has a stake in — as questions on the queue, **one at a time**, in dependency order,
each carrying the machine's **lean** (its recommended answer) and the one thing that would
**flip** it. The operator settles each by accepting the lean or answering in their own words, so
they ratify far more often than they author. An ask whose every decision is already determined
files straight to standing work, ungrilled; the floor is a **standing guard**, not a front gate —
the same test re-fires whenever a stake-bearing choice surfaces mid-work. A resolved pass yields
two products: the **contract** (the operator-view entry the result is later validated against)
and the **spec delta** the change will realize.

### Requirement: a filed ask is grilled before it becomes work
An ask that opens real choices MUST pass a grilling floor before spawning work: the
architect resolves every decision it can from the living spec and intent, and
only a residual decision the operator has a stake in keeps the ask above the floor. An
ask whose every decision is already determined files straight to standing work,
ungrilled. The floor is a standing guard, not a front gate — the same test re-fires
whenever a stake-bearing choice surfaces mid-work.

#### Scenario: above the floor
- WHEN a filed ask leaves a stake-bearing decision open after the machine resolves
  what it can from intent and the spec
- THEN the ask is held and grilled, and no standing work exists for it yet

#### Scenario: below the floor
- WHEN every decision a filed ask needs is already determined by intent or the spec
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
