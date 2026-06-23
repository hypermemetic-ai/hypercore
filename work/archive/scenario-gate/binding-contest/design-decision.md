# binding-contest — design-decision (the scenario→runnable binding)

A `design-it-twice` over `scenario-gate`'s load-bearing interface: how a prose WHEN/THEN scenario in
a capability spec becomes a runnable red→green check the gate executes, with the **architect**
authoring the assertion and the plumbing hidden. Four candidates, each fenced and briefed to diverge.
(ADR 0007 form.) Candidate designs stay machine-side — in the fences and this record.

## design-decision: scenario→runnable binding → a closed domain-verb `check` block, homed in the capability spec beside its requirement — reason: it is the only shape that lets the architect author the runnable assertion (closing self-judging) with no escape hatch into the weeds, while the check lives next to the requirement it tests (the self-model literally self-verifying), grounded in hypercore's existing assertion patterns. Candidate **C** base, hybridized with **D**'s decoupling-and-classification and **B**'s closed-vocabulary discipline.

## The contest (four fenced candidates)

- **A — minimize the interface** *(fence a2d38faee8e6f2020)*: a `command/red/green` block reusing the
  worker's loop shape, the command a named `engine.scene <name>` dispatcher. Smallest surface, zero
  new vocabulary.
- **B — maximize flexibility** *(fence afdc50b31bc3f25bf)*: a `World` with `given`/`when`/`then`
  namespaces (~25 verbs); the architect scripts multi-step assertions, plus a `then.holds(lambda)`
  universal predicate.
- **C — optimize the common caller** *(fence aaa719feb95441570)*: six verbs (`grow` / `accept` /
  `hand` / `gate` / `spec` / `coherence`) shaped to the folding-conditions assertion patterns; the
  delta synthesized from the requirement name; three-line common case.
- **D — ports-and-adapters** *(fence a92843c188aad34e2)*: a `bind:` line of domain verbs naming no
  engine symbol, DSL registry → driver/adapter → engine; the worker cannot edit the scenario to pass.

## The judgment — depth, locality, seam, feasibility

The bar agreed with the operator: the **architect** must author the runnable assertion at contract
time, plumbing hidden, **without** the oracle returning to the builder (the self-judging D1 closes).

- **A fails the bar.** Its minimalism is bought by relocating the oracle: the architect names a scene,
  but its body — the actual assertion — is **worker-authored**. That is the exact hole D1 exists to
  close. Its depth ratio is the highest but illusory: the small interface fronts a hand-written
  per-scenario fixture, not reusable behavior. Rejected.
- **B passes the bar but leaks.** The architect authors the assertion, but `then.holds(lambda w: …)`
  is a hole into raw Python below the seam — a regenerating author could write implementation-coupled
  or model-judgment assertions there and call them gated. Its ~25-verb surface also strains the
  high-signal/agent-legible criterion (clause 1). The expressiveness is real; the leak and the size
  are disqualifying for the seam-first proof.
- **C passes cleanly.** Six domain verbs over the engine's public surface; no escape hatch; the check
  block lives in the spec **beside the requirement** (best locality, and the truest realization of the
  self-verifying self-model); grounded in the real patterns the existing slices already assert, so the
  first migration is largely re-homing, not invention. Its weakness — narrowness (six verbs fit
  folding-conditions; other capabilities will need more) — is **exactly acceptable under seam-first**:
  prove on folding-conditions now, extend the vocabulary per capability as we migrate, in the same edit
  as the scenario that first needs it (the §114 discipline).
- **D is the most principled on decoupling but the heaviest.** Its central risk — the driver as a
  god-module-in-waiting — is the very flip the contract warned of, and a *new* assertion cannot be
  authored green by the architect alone (a worker must build the adapter first). Deferred, not
  discarded.

## The pick — C base, hybridized

- **Adopted from D:** the check names **domain verbs, never engine symbols / paths / commands**, so a
  worker rewriting the engine has nothing in the scenario to tamper to pass; and the **presence or
  absence of a check block *is* the gated/watched classification** — derive-don't-hand-tend (slice-15's
  lesson) applied to the standards register, retiring the hand-maintained `standard: … — gated|watched`
  table.
- **Adopted from B:** a **closed** vocabulary with **no raw-Python escape hatch**. A scenario that needs
  something outside the vocabulary either earns a new verb (in the same edit) or stays **watched** —
  never a `lambda` into the weeds. This keeps the feasibility bar's integrity.
- **Base from C:** few domain verbs fronting the engine's public seams; the check block beside the
  requirement; the common case three lines.

## Home

- the **claim** — *"the living spec is self-verifying: a capability's scenarios are the executable
  checks of its requirements"* — one requirement ADDED to `self-model`.
- the **gate** — run the touched capability's scenarios red→green at the fork base and the tip — stays
  in `folding-conditions`, replacing `_feedback_loop`.
- the **binding** — the verb vocabulary + compiler + base/tip runner — a focused module, **not yet a
  new `acceptance` capability**.
- **watched trigger (architecture-review):** promote the binding to its own `acceptance` capability if
  its vocabulary/driver grows past the length signal — D's god-module warning, honored as a signal, not
  pre-paid.

## No card raised (the standing-guard floor)

The pick is interface shape — machine-side design judgment. It changes no operator-visible behavior,
nothing hard to reverse beyond what seam-first (D3) already settled, and the operator reads the
operator view, not the spec's internal organization. Per `design-it-twice`, the selection does not
spend the operator's go; the reasoning stays here, on the node. The operator's stake was settled in
grilling (D1/D2/D3 + the feasibility bar).

## Carry-forward — the contract for one ordinary worker apply

Realize folding-conditions' scenarios behind this interface. The god-file scenario becomes:

```markdown
#### Scenario: a tree grows a module past the signal
- WHEN a tree's material adds or grows a source file past the length signal and no
  accepted-length record accepts it
- THEN a decision (re-cut / deepen / accept-with-reason) is raised, the fold is held, and
  the spec is left untouched — never a silent refusal and never a silent pass

  ```check
  grow  engine/giant.py  past-signal
  gate  held  because depth  names engine/giant.py
  spec  untouched
  ```
```

- the verbs name domain nouns; the binding compiles them to the real `tree`/`worker`/`conditions`/
  `communication` seams (the hidden slice machinery), runs the chain at `HEAD~1` (red) and `HEAD`
  (green), trusts exit codes;
- the gate (replacing `_feedback_loop`) runs the touched capability's scenarios; a scenario with no
  `check` block is watched, never faked;
- the slice-5/7/9/20/21 content **for folding-conditions** dissolves into its now-executable scenarios;
- `python3 -m engine --check` green throughout (a real red→green), unconverted capabilities coexisting.
