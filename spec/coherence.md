# coherence
<!-- vision: coherence -->

The architect's judgment at the archive gate — how it integrates a worker's hand-off without
the worker's raw output ever reaching the operator — carved from `communication` as its own skill. When a
worker hands a result back, the architect holds it against the contract at the **operator's
altitude** — a coherence check, not a code review — and against the **depth** bar. The raw report
is *input* to that judgment, never output: every operator-facing word is authored fresh, so the
report crosses to the operator through no path. A result that honors the contract folds its
refined delta into the spec — the work leaving the work view in the same act; a result that
does not, or whose material is past the length signal with no accepted-length record accepting it, surfaces
as exactly one of two outcomes — a fold, or a **decision** (re-cut / deepen / accept-with-reason /
abandon / change the ask) on the operator's queue. The architect's
structural opposition to the worker's investment in its own product is the defense against
self-judging.

### Requirement: the architect integrates the worker's hand-off
The architect MUST archive a worker's result: the **folding conditions** run first — the delta
applies, and the touched capability's architect-authored scenarios go red→green (the scenario gate).
**Check-relevance is therefore gated by construction**: a worker cannot hand back a result that passes
a check of the wrong behavior, because the check is the architect's own scenario, not one the worker wrote. The
architect then coherence-checks what no scenario can capture — does the result honor the contract at the
operator's altitude, not a code review — and on a pass folds the refined delta into the spec, the work
leaving the work view in the same act. The raw report is input to that judgment, never output.

#### Scenario: a result that honors the contract folds
- WHEN a worker hands a result back whose folding conditions are met (its scenarios went red→green)
  and the architect judges it coherent with the contract
- THEN the refined delta folds into the spec and the work leaves the work view in the same act

  ```check
  hand coherent
  fold lands
  spec folds
  card none
  ```

#### Scenario: a result that does not honor the contract is held as a decision
- WHEN a worker hands a result back whose folding conditions are met but the architect judges it
  incoherent with the contract
- THEN the fold is refused, the spec is left untouched, the node stays live, and a decision
  (re-cut / abandon / change the ask) is raised on the queue — never a silent fold and never a
  silent drop

  ```check
  hand incoherent
  fold held
  spec untouched
  card decide
  node live
  ```

### Requirement: the architect judges depth at the archive gate
The architect MUST hold the design judgment the worker cannot hold over its own product: at
the archive gate, a result whose material is past the length signal with no accepted-length record
accepting it surfaces as exactly one of two outcomes — a fold, or a **decision** (re-cut /
deepen / accept-with-reason) on the operator's queue.
Depth surfaces to the operator as a decision rather than hiding in a number, so the operator
reads the system's depth; the architect's structural opposition to the worker's investment in
its own product is the defense against self-judging.

#### Scenario: a shallow-or-long result reaches the gate
- WHEN a worker hands back material past the length signal with no accepted-length record accepting it
- THEN the architect raises a decision (re-cut / deepen / accept-with-reason) and the
  fold is held — the depth surfaces to the operator, not a length number's verdict

### Requirement: a new verb the gate cannot run at the base is a watched archive-gate judgment
A new domain verb whose fixture needs a **brand-new engine seam** — one absent from the fork base —
cannot be run at the base at all, so the gate's base run cannot carry it and red→green cannot
structurally prove the verb **tests** the behavior rather than merely **names** it. The architect MUST
NOT let the gate claim a guarantee it does not have here: when the gate cannot structurally vouch for a
new verb, the honest classification is **watched-and-said-so**, never gated. The adequacy of such a verb
is a **watched judgment the archive gate must actually make** — the single, named exception to
coherence's standing rule that it is not a code review and never reads the fixture: at the archive gate
the architect **reads this one residue's fixture** and **attests that the new verb exercises the
behavior** it names, recorded honestly in the open, exactly as `build_reaches_main` is a watched check
proven from outside the fold it tests. The classification is read off the **structural reachability** of
the verb at the base, so the **worker never authors its own classification**, and the residue lands as the
architect's attestation on the archive path, **never as operator-queue load**. The gate's reach and this
watched residue together exhaust the new-verb case: gated where the verb runs at the base, watched-and-said-so
where it cannot — never a structural guarantee silently assumed.

#### Scenario: a brand-new-seam verb's adequacy is attested, not gated
- WHEN a fold introduces a new domain verb whose fixture needs an engine seam absent at the fork base, so
  the gate cannot run the verb at the base to prove the behavior transitioned
- THEN its adequacy is a watched archive-gate judgment — the architect reads this one residue's fixture
  and attests at coherence that the verb exercises the behavior, recorded as watched-and-said-so, never
  claimed as a structural gate guarantee and never the worker's to classify
- watched — the attestation is a model judgment no fixture certifies, proven from outside at the archive
  gate the way `build_reaches_main` is, and the same honest home

### Requirement: an unreadable coherence reply is a distinct outcome, never a false incoherence refusal
The architect's coherence judgment at the archive gate MUST distinguish a reply that carries no usable
`coherent` verdict — the flag absent or unparseable — from an explicit `coherent: false`. An unreadable
reply is an envelope failure, not a contract judgment. The deterministic folding conditions run before
the judgment can matter, and a code-bearing fold still re-verifies the merged tree before commit; an
unreadable watched envelope MUST NOT masquerade as the model's veto over a gate-proven build. The
architect MUST re-ask the coherence judgment a bounded number of times: a transient unreadable reply
that resolves to `coherent: true` folds as normal, and a reply that stays unreadable across the retries
raises a distinct retryable decision — the coherence reply was unreadable — that leaves the node live.
The unreadable-reply decision MUST NOT use the "did not honor the contract" refusal. An explicit
`coherent: false` still raises its incoherence card unchanged: the model keeps its veto on a genuine
incoherence judgment, and only the unreadable reply is reclassified.

#### Scenario: an unreadable coherence reply retries, then surfaces a distinct outcome
- WHEN the architect integrates a gate-proven hand-off whose coherence reply omits the `coherent` flag
  once before a usable verdict in one case, and on every attempt in another
- THEN the transient case folds on retry, while the persistent case raises a distinct unreadable-reply
  decision that leaves the node live; neither is raised as the incoherence refusal

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
