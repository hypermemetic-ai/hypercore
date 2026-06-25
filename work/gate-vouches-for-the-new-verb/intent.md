---
kind: ask
state: standing
owner: operator
created: 1782277200
---
# gate-vouches-for-the-new-verb — the scenario gate must prove a new verb tests its behavior, not just that the verb appeared

The scenario gate is the load-bearing replacement for the worker's self-authored loop: a behavior folds
only when its capability's **architect-authored scenarios** go red→green — red at the fork base (the
behavior absent), green at the tip (`engine/scenario.py:gate`). Its whole claim is structural: "the
builder can never author the oracle that judges it."

That claim does **not** hold for the case it most needs to — building genuinely **new** behavior. By
design, a new domain verb is the **worker's** to write ("nothing below the seam is the architect's to
write … a scenario that needs something the vocabulary cannot say earns a new verb here, in the same
edit" — `engine/scenario.py`). So the worker adds the behavior **and** the new world-fixture verb
(`engine/worlds/<cap>_world.py`) in the **same fence commit**. The gate then runs the tip's scenario at
the base checkout, whose world **lacks that verb** — so the base run is red with `unknown scenario verb`,
**red because the verb is missing, not because the behavior is absent**.

The redness at base is therefore overdetermined by the verb's absence. A worker that writes a **vacuous**
fixture (a `_v_<verb>` that asserts nothing real) gets base-RED (verb unknown) → tip-GREEN (vacuous verb)
and **clears the gate having tested nothing**. The builder authored the oracle after all, and red→green
cannot tell a real oracle from a hollow one. Nothing downstream catches it: the whole-system re-verify
(`scenario.reverify`) runs the **same** new verbs, and coherence is "not a code review" and never reads
the fixture.

Demonstrated against the real engine: at the `schedule` base world, `do("limit", ["4"])` →
`(False, "unknown scenario verb 'limit'")`, and `scenario._run_one` turns that unknown verb straight into
a red outcome — so any newly-named verb is red at base by construction.

This compounds `worker-builds-proposed-delta`: when a worker reaches a node with no architect-proposed
delta it authors its **own** scenarios too, so it then writes both the check *and* its fixture — total
self-judging. But the gap here is independent and lands even on the intended path (architect proposes the
scenario; worker writes the verb), because authorship of the *fixture* always falls below the seam.

## the integrity stack (one of three composable nodes)
hypercore's self-verification rests on one claim — the description is the test, and the builder cannot
fake the verdict. It can fail three independent ways, each its own node; none subsumes another, and a
short-circuit at any layer defeats the whole:
- **proposer** — did the architect author the check (WHEN/THEN + verbs), or the builder? — `worker-builds-proposed-delta`
- **run** — did the mechanism actually run and leave a trail, or is the record hand-faked? — `a-record-a-load-bearing`
- **adequacy** — when it ran, did the check test the property, or a builder-authored proxy? — *this node*
This node owns the **adequacy** layer, the one the other two cannot reach: it lands even when the architect
proposed every scenario (proposer satisfied) and the build genuinely ran in its fence (run/trail
satisfied), because the *fixture under the verb* is still builder-authored and red→green cannot tell a
real oracle from a hollow one. It refutes the keystone of `a-record-a-load-bearing`'s resolved pass —
that the scenario verdict self-certifies via re-derivation — which that node must re-derive to defer
adequacy here. The three touch shared seams (`spec/worker.md`, the scenario gate in `conditions`/`scenario`):
each must **ADD** its own requirement rather than co-MODIFY a shared one (two MODIFYs of one requirement
clobber at fold), or be sequenced on another's tip — so three concurrent fences compose.

## The interface decision to design
What makes a new verb's red→green prove the **behavior** transitioned rather than that the **verb**
appeared — and where is that enforced? Candidate seams:
- **the gate's base run** (`scenario._run_at` / `gate`): carry the **tip's** world fixtures onto the base
  **engine** checkout, so the new verb *exists* at the base run and base-red can only mean the behavior
  is genuinely absent (it already carries the tip's check *source* into each checkout — this extends that
  to the binding);
- **the binding's authorship seam** (`engine/scenario.py`, `spec/self-model.md`): who owns a new
  fixture, and how a worker-authored fixture is kept from being its own hollow oracle;
- **coherence** (`spec/coherence.md`): whether a new fixture's adequacy is a watched judgment the
  archive stage must actually make, recorded honestly, rather than an unstated assumption.
Distinguish a verb that genuinely cannot exist at base (a brand-new engine seam) from one that could have
been exercised against the old behavior to show real red. Decide what the honest classification is when
the gate cannot structurally vouch for a new verb — gated, or watched-and-said-so.

## folding condition
- a newly-introduced verb's red→green proves the behavior transitioned, not merely that the verb was
  added: a vacuous fixture for a new verb cannot clear the gate (or the gate's limit is recorded as a
  watched judgment, never claimed as a structural guarantee it is not);
- the touched capabilities (`spec/self-model.md`, and any seam the chosen design moves — `spec/coherence.md`)
  carry the change with their scenarios, and `python3 -m engine --check` is green.
