---
kind: decide
state: settled
owner: operator
created: 1782599218
---
the verified build is stale: engine/communication.py on main has moved since the fence was cut — re-cut the build off current main

--- OPERATOR DECISION (settled): re-cut off current main; T1 prioritized ahead of #4 ---
Benign staleness collision: the sibling crossing the-live-run-gate-sees-the-crossing folded engine/communication.py onto main while T1 was building, so the staleness guard correctly refused to clobber it; T1's build was not defective. Operator policy: T1 goes FIRST on the engine/communication.py serialize lane — #4 (architect-prompts-route-to-skills) is parked until T1 lands. Resolution: re-cut off current main and re-dispatch. The grilled contract, the operator's option-B delta (scenario-gate skip for watched-only deltas + the _capped_run re-verify-timeout fix), and the design materials all STAND — no re-grill, no redesign.
