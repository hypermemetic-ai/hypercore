---
kind: ask
state: folded
owner: operator
created: 2026-06-23
folded: 2026-06-23
---
# actor-guard-vocabulary — sharpen schedule and folding-conditions in place

The two specs already *describe* actor-supervisor and guard semantics without naming them, so the
load-bearing claims are softer than they could be. Sharpen the prose **in place** — revise the
load-bearing sentence, never append a gloss (intent §86, no accretion) — so each named term earns its
place by licensing a checkable invariant or making a class of mistake unsayable.

The three redlines (full before/after in `../../study.md`):

- **`schedule` intro** — "several workers advance the one tree at once, each fenced, the shared record
  single-writer" → **"a supervisor over isolated actors … the single-writer record, its only
  mailbox"** (makes "a worker reaches a sibling" unsayable — §62 stated as the single channel).
- **`folding-conditions` intro** — "the engineering standards made structural … the gates on the
  material" → **"made into guards … a guard says when a node may move, never what moving does"**
  (forbids folding a side effect into a condition).
- **`folding-conditions` depth requirement** — the three MUST/MUST-NOT clauses → **"the system's one
  escalating guard"** (one concept entailing all three; forbids simplifying the §58 floor into a
  silent block).

## open decisions
- **the fold kind of a prose-only sharpen.** The living spec is never separately edited — a fold
  applies a delta (`spec/self-model.md`). **Lean:** these land as a **MODIFIED-requirement delta**
  (the requirement's words are part of the as-built model) carrying **no red→green**, because no
  behavior moves — the scenario gate fires on behavior change, not wording, so the touched
  requirements' existing scenarios stay green. **Flip:** if the model requires every MODIFIED
  requirement to show a red→green transition, a prose-only sharpen has no standalone fold path and
  must instead ride a behavior-bearing tree. This is the one seam this tree turns on. [machine]
- **the "dispatch is total" line is out of scope here** — it rides with **dispatch-totality** so the
  sharpened requirement prose and the scenario that gates it land in one fold, never a requirement
  claiming a property no scenario gates. This tree carries only the supervisor/guard framing. [machine]

## folding condition
- the three redlines land as the touched requirements' prose, applied by a delta (not a separate spec
  edit), the fold-kind decision above settled;
- `python3 -m engine --check` is green — no scenario regresses. [machine]

## result — built, green, awaiting acceptance (2026-06-23)

The fold-kind seam settled on its **lean**: this is a **MODIFIED-requirement delta carrying no
red→green**. The three redlines change only the load-bearing prose of requirements whose behavior was
already built and already gated — the scenario gate fires on behavior, not wording — so the right
discipline is to apply, run the harness, and witness that **no scenario moved**, not to manufacture a
red→green a prose sharpen cannot honestly show. The flip (every MODIFIED must ride a behavior tree)
did not bind: the spec's own scenario-gate requirement scopes red→green to a *behavior change*, and a
wording sharpen is not one.

What landed (the delta, hand-applied, all three sharpened **in place** — no appended gloss, intent §86):
- `spec/schedule.md` intro — "several workers advance the one tree at once, each fenced, the shared
  record single-writer" → "the scheduler is a supervisor over isolated actors … the single-writer
  record, its only mailbox … no worker can touch another's." Buys: **"a worker reaches a sibling" is
  now unsayable** — §62 stated as the single channel, not a list of can'ts.
- `spec/folding-conditions.md` intro — "the engineering standards made structural … the gates on the
  material" → "made into **guards** … a guard says when a node may move, never what moving does," with
  the `fold` guard and `dispatch` readiness named as the two transitions of one vocabulary. Buys:
  **folding a side effect into a condition is now visibly wrong** — a gate that acts instead of decides.
- `spec/folding-conditions.md` depth requirement — the three MUST/MUST-NOT clauses → "the depth guard
  is the system's **one escalating guard** … neither passes silently nor refuses on its own, but
  raises." Buys: **the §58 floor cannot be "simplified" into a silent block** — the likeliest future
  regression — and the three clauses now read as entailed by one concept.

`python3 -m engine --check` is green; every touched requirement's scenarios stayed green (no regression
— the whole point of a prose-only sharpen). Folding condition met. Awaiting the operator's acceptance
to fold (apply the delta + archive the node); not committed. [machine]
