surfaced: 0

[CONTRACT]
Make a hand-driven crossing's failure impossible to lose. Today the guarantee that every crossing ends in exactly one outcome — its work folds, or one decision lands on your queue — holds only while the autonomous loop is the one running the worker. Run a crossing by hand (the documented dispatch path) and a build that errors out quietly puts the node back to standing with no card and no reason recorded, so it silently re-offers itself for work and invites a blind retry. This relocates that guarantee into the worker itself: any failed crossing — whether the loop wrapped it or it was run bare — raises exactly one decision card on your queue, parented to the node so the node is blocked until you settle it (abandon / re-cut / change the ask), never silently re-offered. The single place that turns a failure into a decision now lives at the worker boundary; the loop's now-redundant copy is removed, so there is one guarantee, not two halves that only add up under the scheduler. Under the loop you watch, nothing changes — a failed worker still surfaces the same one card; the fix is invisible where it already worked and correct where it was silently broken.

[DELTA]
## ADDED — worker
### Requirement: a crossing is total at the worker boundary, whatever its caller
`worker.run` MUST resolve every crossing to exactly one terminal on its own — its delta folds, or a
decision card is raised on the operator's queue parented to the node — whether the autonomous scheduler
wraps it or it is called bare, the documented hand-driven dispatch path (`worker.run(tree.find(id))`).
When a build raises mid-crossing — a transport error, a model failure, a malformed seam — `worker.run`
MUST raise that decision card itself, carrying the could-not-complete reason and the operator's fork
(abandon / re-cut / change the ask), then recover the node, so the parented card blocks the node from
re-entering the ready work; a bare crossing that raises therefore never recovers the node to a silently
re-dispatchable standing state with no card and no reason. The totality logic MUST live in exactly one
place — this boundary — so the scheduler carries no second copy that raises a redundant card, and a
crossing under the scheduler still surfaces exactly one decision, the same one, on a failed worker.

#### Scenario: a bare crossing that raises leaves one parented decision card and blocks the node
- WHEN `worker.run` is called with no scheduler around it and its build raises mid-crossing
- THEN a decision card carrying the could-not-complete reason is raised on the operator's queue parented
  to the node, and the node is recovered out of flight but does not re-enter the ready work — it is
  blocked on that card, not silently re-dispatchable — so the failure reason is never lost

  ```check
  fails bare
  card parented
  node not-ready
  ```
