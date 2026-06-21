# graph

The durable model: nodes on disk, read live, written atomically and committed.
The graph is hypercore's one source of truth; the queue and the standing work are
both views computed from it, never lists kept in sync.

### Requirement: the graph is read live, never cached as a list
Every view of the graph MUST be computed by reading the nodes fresh, so nothing
can go stale and nothing can be lost in motion.

#### Scenario: computing the queue and the standing work
- WHEN the queue or the standing work is shown
- THEN it is derived by reading the nodes and filtering by state, not from a
  separately maintained list

### Requirement: a mutation lands at once and the commit follows behind
Every mutation MUST write one node file atomically, so the act lands on disk the
instant it is made; the durable commit follows behind and does not gate the act.

#### Scenario: filing intent
- WHEN the operator's captured intent is filed
- THEN one node file is written by atomic replace and is present immediately, and a
  commit of that file is attempted after; a failed commit does not lose the act

### Requirement: a node carries one operation and an endorsement state
A node MUST carry exactly one operation (ask, check, decide, or do) together with
the state that places it in a view and, for a statement, its endorsement.

#### Scenario: reading a node
- WHEN a node file is read
- THEN its operation kind, state, owner, and whether it carries the [machine]
  marker are recovered from the file

### Requirement: durable state is version-controlled and recoverable
Everything that crosses the operator–machine boundary MUST land on disk and be
committed, so the operator reads the state directly and any episode recovers from
the record.

#### Scenario: recovering after a restart
- WHEN the system is reopened
- THEN the graph read from disk is the whole durable state; no session is resumed
