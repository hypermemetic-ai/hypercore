# schedule
<!-- vision: scheduler, continuous, concurrent, ready work, idle -->

The autonomous loop — how work keeps moving. The tree computes the ready work; the scheduler
consumes it, running a worker on each ready node and keeping work in flight while any remains, so a
ratified ask is *built* rather than left standing while the system idles (intent §60). Work runs
concurrently as well as continuously: several workers advance the one tree at once, each fenced, the
shared record single-writer so their builds overlap while their integrations serialize. The loop runs
off the operator's path — its own threads — so it never blocks the window, and a worker that cannot
complete returns as a decision rather than stalling the loop.

### Requirement: standing work is consumed continuously — the system never idles with unblocked work
The scheduler MUST take the ready work and run a worker on each node, so a ratified ask is built
without the operator re-prompting; while any unblocked work remains a worker is on it. The system goes
quiet only when all that remains is a decision the operator owns — an idle system with unblocked work
left is a defect, not rest (intent §60).

#### Scenario: a ratified ask is built without re-prompting
- WHEN standing work exists and no decision blocks it
- THEN the scheduler dispatches it to a worker, which builds it fenced, the architect integrates the
  result, and the delta folds — the work moves and leaves the work view without the operator acting

  ```check
  ready 1
  run
  folded 1
  ```

#### Scenario: the system rests only on a decision
- WHEN nothing is ready and only awaiting decisions remain
- THEN the scheduler dispatches no worker and rests; while ready work is present it never rests

  ```check
  blocked
  step
  rests
  ```

### Requirement: the ready work is read live, and readiness gates scheduling
The ready work the scheduler consumes MUST be read off the one tree each time — standing work with its
folding condition named and nothing open beneath it — never a stored work-list. The same readiness
that gates spawning gates scheduling, so a node blocked on an open child is not taken and nothing in
the schedule can go stale (intent §110).

#### Scenario: a blocked node is not scheduled
- WHEN a standing node has an unresolved child tree beneath it
- THEN it is absent from the ready work and the scheduler runs no worker on it, while its sibling
  leaves that are clear are taken

  ```check
  blocked-sibling
  unready blocked
  run
  folded sibling
  idle blocked
  ```

### Requirement: work runs concurrently on one record
The scheduler MAY run several workers at once, up to a bound, each fenced in its own worktree; the
shared git line MUST be single-writer, so concurrent builds overlap while their integrations serialize
and each folds its own delta into the one spec with no fold corrupting the record (intent §62). This is
the same isolation the worker's fence provides and `design-it-twice` runs a contest on — applied to
throughput.

#### Scenario: two workers advance at once
- WHEN two nodes are ready and the bound allows it
- THEN two workers build at the same time in distinct fences, and each result integrates and folds
  into the one spec with no interference between them

  ```check
  ready 2
  dispatch held
  flight 2
  fences distinct
  off-main
  release
  folded 2
  ```

### Requirement: the loop runs off the operator's path and surfaces failure as a decision
The scheduler MUST run independently of the operator's input loop — each worker on its own thread, the
loop never blocking — so autonomous work never delays a keystroke and the operator watches progress
live. A worker that cannot complete MUST return as a decision on the queue (abandon / re-cut / change
the ask); the loop surfaces it and keeps serving the rest, never crashing and never silently dropping
the node.

#### Scenario: a keystroke during autonomous work
- WHEN workers are building and the operator types
- THEN the keystroke is serviced the same frame, because the scheduling and the builds run off the
  input loop on their own threads

#### Scenario: a worker cannot complete
- WHEN a dispatched worker errs before handing back
- THEN a decision card is raised on its node and the scheduler keeps serving other ready work

  ```check
  failing
  run
  folded good
  decision raised
  fence gone
  recovered
  loop idle
  ```
