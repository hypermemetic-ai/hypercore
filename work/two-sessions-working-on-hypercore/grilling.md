surfaced: 1

[Q] When two windows are open over one tree, only one holds the live loop; the other is a full operator window whose filed work the live loop still builds off the shared tree. Should the non-live window signal that it isn't the dispatching one?
lean: Quiet footer marker — the non-live window's footer shows it is not the live loop, so the operator can tell at a glance which window dispatches. Low noise, keeps the mental model straight with two windows open, and filed work builds regardless of which window holds the loop.
flip: Stay silent — both windows look identical; since filed work builds regardless of which window holds the loop, the distinction never changes an outcome and the marker would be noise without a decision attached.
answer: Accept the lean: quiet footer marker. The non-live window signals in its footer that it is not the dispatching loop, so the operator can always tell which window is live.

[CONTRACT]
hypercore gains the one guarantee its autonomous loop always assumed but never held: **exactly one loop runs against a tree.** Today every window starts its own scheduler (`window.run` calls `Scheduler().start()`), so two windows run two loops over the one tree, and the loop's orchestration invariants — true within a process, false across — corrupt each other: `_recover_stranded` resets a peer's live in-flight node back to standing every poll, and `step` double-dispatches a still-standing node into two fenced workers on one ask. The fix is the record's own mechanism at a coarser scope: the autonomous loop is **elected by a held repo-root lease** — the `flock` the single-writer line already uses, held for the loop's life rather than per act. A second `python3 -m engine` over the same tree acquires no lease and dispatches nothing; it stays a full operator window — filing, grilling, and ratifying in parallel, which the node-local single-writer record already makes safe — and the one live loop builds whatever any window files, because it reads the ready work live off the shared tree, so nothing a non-holding window files is stranded. The lease is **self-healing**: it releases when its holder's process dies or its window closes, the next window's loop acquires it on its next poll, and `_recover_stranded` — now correct, because with one loop "an in-flight node not under this scheduler" truly means stranded — returns any in-flight node to standing. The lease is keyed on the tree's root, so `--check`'s throwaway root never contends with the live tree. A non-holding window **shows in its footer that it is not the live loop**, so the operator can always tell which window dispatches; it loses no operator move, only the loop. The result is validated by two schedulers over one tree where exactly one dispatches and the other never recovers the first's live node, by a held lease that releases on its holder's exit and is taken over by the next loop, by a non-holding window whose filed work the live loop still builds, by its footer marking it not-live, and by `python3 -m engine --check` carrying the acceptance and staying green.

[DELTA]
## ADDED — schedule

### Requirement: exactly one autonomous loop runs against a tree
The autonomous loop MUST be single-instance per tree: at most one scheduler dispatches work against a
given tree at a time, **elected by a held repo-root lease** — the same advisory lock the single-writer
record holds per act, now held for the loop's life. A second engine started over the same tree acquires
no lease and dispatches nothing; it stays a full operator window — filing, grilling, and ratifying in
parallel through the node-local single-writer record — and the one live loop builds whatever any window
files, because the ready work is read live off the shared tree, so a non-holding window strands nothing.
This is the guarantee the loop already assumed: with one loop `_recover_stranded`'s invariant (an
in-flight node not under this scheduler is stranded) and dispatch's read→in-flight window are true, where
across two loops they were false — one loop reset the other's live work and a node double-dispatched. The
lease releases when its holder's process dies or its window closes, and the next window's loop acquires it
on its next poll and recovers any node left in flight, so the election is self-healing and needs no manual
reclaim. The lease is keyed on the tree's root, so a throwaway harness root never contends with the live
tree, and the loop owns its own lease (it is acquired where the loop starts, not where the window opens),
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
- WHEN the loop holding the lease exits — its process dies or its window closes — while a peer window is open
- THEN the lease releases, the peer's loop acquires it on its next poll and dispatches the ready work, and
  any node left in flight is recovered to standing

  ```check
  ready 1
  loops 2
  holder dispatches
  holder exits
  peer acquires
  folded 1
  ```

## ADDED — interface

### Requirement: a non-live window shows it is not the dispatching loop
A window that does not hold the autonomous-loop lease MUST signal in its footer that it is not the live
loop, so the operator can tell at a glance which window dispatches. It remains a full operator window —
every keystroke move still works and the work it files is built by the live loop — so the signal serves
the operator's mental model, not a restriction.

#### Scenario: the footer marks the non-live window
- WHEN a window is open over a tree whose lease another window holds
- THEN its footer shows it is not the live loop, while the lease-holding window's footer does not

  ```check
  loops 2
  render holder footer-live
  render peer footer-not-live
  ```
