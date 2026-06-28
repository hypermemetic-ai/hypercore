surfaced: 0

[CONTRACT]
A coherence reply the model returns garbled no longer throws away a verified build. When the architect integrates a worker hand-off whose deterministic gate is already green — its scenarios went red->green and the whole system re-verified on the merged tree — a coherence reply that omits or mangles the `coherent` verdict is re-asked a few times: a transient garble folds as normal, and a persistent one surfaces a distinct "coherence reply unreadable" decision that keeps the verified build and stays live, never the "did not honor the contract" refusal. An explicit `coherent: false` still raises its incoherence card unchanged — the model keeps its veto on a genuine incoherence judgment; only the unreadable reply is reclassified. This is the live blocker between the watchably-driven dispatch and hands-off autonomy: a flaky envelope can no longer force a human into the architect seat to rescue a gate-proven build.

[DELTA]
# delta — the integrate-stage coherence judgment distinguishes an unreadable reply from incoherence

## ADDED — coherence
### Requirement: an unreadable coherence reply is a distinct outcome, never a false incoherence refusal
The architect's coherence judgment at the archive gate MUST distinguish a reply that carries **no usable
`coherent` verdict** — the flag absent or unparseable — from an explicit `coherent: false`. By the time
integrate runs, the build is already proven sound deterministically: its capability's scenarios went
red->green at the gate and the whole system re-verified green on the merged tree. So a coherence reply
the model returns garbled MUST NOT discard that verified build as incoherent. The architect MUST re-ask
the coherence judgment a bounded number of times: a transient unreadable reply that resolves on retry
folds as normal, and a reply that stays unreadable across the retries surfaces a **distinct** retryable
decision — the coherence reply was unreadable — that keeps the verified build and stays live, never the
"did not honor the contract" incoherence refusal. An explicit `coherent: false` still raises its
incoherence card unchanged: the model keeps its veto on a genuine incoherence judgment, and only the
unreadable reply is reclassified — the same shape a re-verify timeout was made a distinct outcome rather
than a discarded build.

#### Scenario: an unreadable coherence reply retries, then surfaces a distinct outcome
- WHEN the architect integrates a gate-proven hand-off whose coherence reply omits the `coherent` flag —
  once before a usable verdict in one case, and on every attempt in another
- THEN the transient case folds on retry, while the persistent case raises a distinct unreadable-reply
  decision that keeps the verified build and stays live; neither is raised as the incoherence refusal

  ```check
  hand unreadable-then-coherent
  fold lands
  spec folds
  card none
  hand unreadable-persistent
  fold held
  card unreadable
  node live
  ```
