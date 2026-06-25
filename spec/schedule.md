# schedule
<!-- vision: scheduler, continuous, concurrent, ready work, idle -->

The autonomous loop — how work keeps moving. The tree computes the ready work; the scheduler
consumes it, running a worker on each ready node and keeping work in flight while any remains, so a
ratified ask is *built* rather than left standing while the system idles (intent §60). Work runs
concurrently as well as continuously: the scheduler is a supervisor over isolated actors. Each fenced worker shares no state and reaches
the one tree through a single channel — the single-writer record, its only mailbox — so builds overlap,
integrations serialize onto the shared history, and no worker can touch another's. The loop runs
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

### Requirement: the loop runs off the operator's path, and dispatch is total
The scheduler MUST run independently of the operator's input loop — each worker on its own thread,
leaving the loop free — so autonomous work never delays a keystroke and the operator watches progress
live. Dispatch MUST be total: every worker the scheduler spawns resolves to exactly one terminal — its
delta integrates and folds, or it escalates as a decision on the queue (abandon / re-cut / change the
ask). A node can therefore neither crash the loop nor sit stranded in flight with no live worker, and the
loop keeps serving the rest. Escalation hands the operator the fork; the scheduler runs no retry
strategy of its own.

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

#### Scenario: dispatch is total — every dispatched worker reaches exactly one terminal
- WHEN the loop runs over ready work where one worker folds and one cannot complete
- THEN every node the scheduler dispatched resolves to exactly one terminal — folded, or escalated as a
  decision on the queue — and none is left in flight with no live worker

  ```check
  failing
  run
  total
  ```

### Requirement: exactly one autonomous loop runs against a tree
The autonomous loop MUST be single-instance per tree: at most one scheduler dispatches work against a
given tree at a time, elected by a held repo-root lease using the record's advisory-lock mechanism at
loop scope. A second engine started over the same tree acquires no lease and dispatches nothing; it
stays a full operator window — filing, grilling, and ratifying in parallel through the node-local
single-writer record — and the one live loop builds whatever any window files, because the ready work
is read live off the shared tree. This is the guarantee the loop already assumed: with one loop,
`_recover_stranded`'s invariant (an in-flight node not under this scheduler is stranded) and dispatch's
read→in-flight window are true, where across two loops they were false. The lease releases when its
holder's process dies or its window closes, and the next window's loop acquires it on its next poll and
recovers any node left in flight, so the election is self-healing and needs no manual reclaim. The
lease is keyed on the tree's root, so a throwaway harness root never contends with the live tree, and
the loop owns its own lease (it is acquired where the loop starts or steps, not where the window opens),
so the guarantee holds wherever a loop runs.

#### Scenario: a second loop over one tree dispatches nothing
- WHEN two schedulers run against the same tree with ready work present
- THEN exactly one holds the lease and dispatches it; the other dispatches no worker and never recovers
  the holder's in-flight node

  ```check
  ready 1
  loops 2
  step
  dispatched 1
  peer dispatched-none
  peer recovered-none
  ```

#### Scenario: the lease is self-healing on its holder's exit
- WHEN the loop holding the lease exits — its process dies or its window closes — while a peer window is
  open
- THEN the lease releases, the peer's loop acquires it on its next poll and dispatches the ready work,
  and any node left in flight is recovered to standing

  ```check
  ready 1
  holder dispatches
  holder exits
  peer acquires
  folded 1
  ```

#### Scenario: a non-holding window's filed work is still built
- WHEN a window that does not hold the lease files ready work on the shared tree
- THEN the lease-holding loop reads ready work live and builds it, so the non-holding window strands
  nothing

  ```check
  loops 2
  step
  peer files 1
  holder-polls
  folded 1
  ```
