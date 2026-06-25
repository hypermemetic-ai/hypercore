surfaced: 0

[Q] Building genuinely new behavior is the one case the scenario gate's core promise — "the builder can never author the oracle that judges it" — cannot fully keep: the architect authors the verb, but the worker writes the fixture *under* it, and when the verb needs a brand-new engine seam (so the verb cannot even exist at the fork base), the gate's red→green cannot tell a fixture that truly tests the behavior from a hollow one. Two honest ways to land this node:

(A) **Strengthen-and-flag.** Harden the gate to catch hollow fixtures wherever it structurally can — any new verb that *can* run at the base — and for the residue it genuinely cannot reach (brand-new-seam verbs), record that limit as **watched**, stated in the open: the architect attests at the archive gate that the verb exercises the behavior, exactly as `build_reaches_main` is a watched, proven-from-outside check the fold cannot certify from inside itself.

(B) **Close the residue by construction.** Forbid a new verb from riding the same fence as the engine seam it needs — require that seam to land in a prior fold so every new verb is exercisable at the base and its red→green is fully structural — paying a two-step (sequenced) workflow cost on new-seam behaviors to keep the adequacy layer's guarantee ironclad.

Which promise should hypercore make about new-behavior adequacy?
lean: (A), the strengthen-and-flag hybrid. The gate ends up strictly stronger than today and the common hollow-fixture hole closes structurally; the one hole it genuinely cannot reach is told plainly rather than papered over. Intent repeatedly prefers an honestly-flagged watched limit to a forced guarantee ("recorded honestly as not mechanically enforced, never faked"; "a number standing in for the judgment of depth is the error being removed"), and the self-model already lives this exact pattern — the code-fold scenarios the gate cannot certify from inside are watched, said-so, and proven from outside in `engine/check/`. (B)'s pre-sequenced seam-fold for every new-seam behavior is the drawn-ahead seam and bookkeeping the intent flags as "the first sign that ceremony has won."
flip: If you judge that *any* watched hole in the **adequacy** layer voids the integrity stack's whole claim — that "the builder cannot fake the verdict" must hold with no architect-trust residue, because a single hollow new-seam fixture is a door a careless or adversarial builder walks straight through — then (B)'s workflow cost is worth paying to make the guarantee structural everywhere.
answer: Choose (A) strengthen-and-flag. Harden the gate to close the hollow-fixture hole wherever it is structurally reachable: carry the tip's world fixtures (the _v_<verb> methods) onto the base ENGINE checkout in the gate's base run, so a new verb EXISTS at the base and base-red can only mean the behavior is genuinely absent, never that the verb is missing — the gate already carries the tip's check SOURCE into each checkout, so this extends that to the binding. A vacuous fixture for such a verb then cannot clear the gate, because base would be green (the vacuous check passes against the old behavior too). For the one residue the gate genuinely cannot reach — a verb that needs a brand-new engine seam, so it cannot exist at the base at all — record the limit as a WATCHED judgment, stated in the open: the architect attests at the coherence/archive gate that the new verb exercises the behavior, exactly as build-reaches-main is a watched, proven-from-outside check the fold cannot certify from inside itself. The gate must NEVER claim a structural guarantee it does not have: when it cannot structurally vouch, the honest classification is watched-and-said-so, never gated. This lands the watched judgment at the architect's coherence gate, not as operator queue load, and the worker never authors its own classification. Compose with the other two integrity-stack nodes: ADD this node's own requirements to self-model and coherence rather than co-MODIFYing a shared scenario-gate requirement, and let the enforcement seam (the gate's base run in scenario run-at/gate, versus the authorship binding, versus coherence) be picked machine-side by a design-it-twice contest. Keep adequacy strictly distinct from a-record's trail-presence layer: a-record proves the run happened; this node proves the run tested the behavior wherever it structurally can, and honestly watches the residue where it cannot.

[CONTRACT]
hypercore folds a new behavior only when its architect-authored scenario goes red at the fork base and green at the tip — but when the behavior is genuinely new, the scenario names a fixture-verb that did not exist before, and the worker writes that verb below the seam in the same fenced commit. Today the base run is red merely because the new verb is missing there, not because the behavior is absent, so a hollow fixture that asserts nothing still rides base-red→tip-green and clears the gate having tested nothing — the builder authoring the oracle after all. This ask closes that hole wherever the gate can structurally reach it: the gate's base run will carry the tip's fixtures onto the base checkout so the new verb already exists at the base, and then a base-red can only mean the behavior was genuinely absent — a vacuous fixture for such a verb goes green at the base too, fails to transition, and is refused, while a real fixture that exercises the behavior still goes red→green and folds. For the one residue the gate genuinely cannot reach — a verb whose fixture needs an engine seam that does not exist at the base at all — the system stops pretending it has a structural guarantee: the limit is recorded honestly as watched, and the architect attests at the archive (coherence) gate that the new verb exercises the behavior, stated in the open exactly like the build-reaches-main check, never claimed as gated and never handed to the worker to certify about its own work. This is the adequacy layer, kept strictly distinct from the run/trail layer: that a run happened is one claim; that the run tested the behavior is this one. The result is validated against precisely this — a hollow fixture for a base-reachable new verb can no longer pass the gate, the unreachable residue is watched-and-said-so rather than silently trusted, the change lands in the self-model and coherence capabilities carrying their own scenarios (added, never co-modifying a shared scenario-gate requirement), and `python3 -m engine --check` is green.

[DELTA]
## ADDED — self-model

### Requirement: a new verb's red→green proves the behavior transitioned, not that the verb appeared
The scenario gate runs a touched capability's tip scenarios at the fork base (must be **red** — the
behavior absent) and at the tip (must be **green**), and a behavior folds only on that transition. For
genuinely **new** behavior the architect's scenario names a **new domain verb** whose fixture
(`engine/worlds/<cap>_world.py`) the worker writes below the seam in the same fence commit — so at the
base checkout the world **lacks that verb** and the base run is red with `unknown scenario verb`: **red
because the verb is missing, not because the behavior is absent**. The redness is overdetermined, and a
**vacuous** fixture that asserts nothing rides base-red (verb unknown) → tip-green (hollow check) and
**clears the gate having tested nothing** — the builder authoring the oracle after all, red→green unable
to tell a real oracle from a hollow one. The gate MUST close this **wherever it is structurally
reachable**: its base run MUST carry the **tip's world fixtures** onto the **base engine checkout** —
exactly as it already carries the tip's check **source** into each checkout, extended to the binding — so
a new verb **exists** at the base run. Base-red can then mean only that the behavior is genuinely absent:
a **vacuous** fixture for such a verb is **green at the base** too (the hollow check passes against the
old behavior), fails to transition red→green, and is **refused**; a **real** fixture that asserts the
behavior stays red at the base and green at the tip and folds. The gate MUST NOT claim a structural
guarantee it does not have — a verb it genuinely cannot run at the base (one needing a brand-new engine
seam) is **not** certified by this requirement and is the watched residue (`coherence`). This is the
**adequacy** layer, kept distinct from trail-presence (`a mechanism-output record folds only when its
mechanism's trail is present`): that the run happened is one claim; that the run tested the behavior,
where the gate can structurally vouch, is this one — so the re-derived red→green that node attests no
longer over-claims self-certification.

#### Scenario: a vacuous fixture for a base-runnable new verb cannot clear the gate
- WHEN a worker builds a behavior whose architect-authored scenario names a brand-new domain verb that
  can run at the fork base, and writes a vacuous fixture for it that asserts nothing real
- THEN the gate's base run carries the tip's world fixtures onto the base engine checkout, finds the
  vacuous verb green at the base too, sees no red→green transition, and refuses the fold — a hollow
  fixture for a base-reachable new verb cannot clear the gate

  ```check
  stage-new-verb vacuous
  gate held
  ```

#### Scenario: a real fixture for a new verb still transitions and folds
- WHEN the same brand-new verb instead carries a real fixture that genuinely asserts the behavior
- THEN it is red at the base (the behavior absent) and green at the tip, transitions red→green, and
  folds — the hardening refuses only the hollow fixture, never the real one

  ```check
  stage-new-verb real
  gate folds
  ```

## ADDED — coherence

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
