surfaced: 3

[Q] Must a re-verify time-budget overrun become a DISTINCT outcome (retry, or an honest "resource limit reached" surfaced to the operator), never silently equal to "scenario broken", while a genuine failure-to-run (missing binary, OSError) still refuses?
lean: Yes — distinct. An overrun is a benign resource-limit outcome: retried once with headroom for a transient blip, and on a persistent overrun surfaced as a retryable "resource limit reached" decision, never the "could not be re-verified" / "build did not hold once merged" refusal. A genuine could-not-run (OSError, missing binary) still refuses. The intent already leans this; the spec's re-verify keystone names "the node recovering to a decision" — this only distinguishes WHICH decision.
flip: If the operator wanted a slow run to hard-fail the build (treat slowness as a defect to fix, not a condition to tolerate), the distinction would collapse back to a refusal. Nothing in intent or spec asks for that; the named harm is precisely that a slow machine reads as a broken build.
answer: Distinct, settled by the lean. Overrun = a benign, retryable resource-limit outcome (retry once, then a "resource limit reached" decision), never "broken"; a genuine could-not-run still refuses. No operator fork.

[Q] Should the per-fold cost be cut by scoping the re-verify, caching the gate's base/tip runs, or parallelizing the merged sweep? And is 180s the right SHAPE of bound?
lean: Cost-cut deferred — SCOPING is forbidden (the re-verify's whole-system reach is structural, narrowing reopens the green-on-touched/red-on-system blind spot); CACHING base/tip-for-merged is unsound (different trees); PARALLELIZING is a separate optimization the benign-timeout fix de-urgents (and 15 concurrent startups contend for the very resource whose exhaustion causes the timeout). Bound shape: keep the per-SUITE shape (one capped subprocess per capability — no 134-startup explosion) but make the budget SCALE with the suite (per-scenario allotment + floor), replacing the fixed 180s the growing scenario count creeps past.
flip: If a measured re-verify tail exceeded operator patience even after the budget scales, parallelizing re-enters as its own grilled ask.
answer: Deferred/leaned — scoping forbidden, caching unsound, parallelizing separate; per-suite shape kept, budget scales. No operator fork.

[Q] The one red→green self-test for the re-verify behavior cannot be honestly gated — its fixture needs the new capped-run seam absent at the fork base, so the gate's base run errors across all of self-model and its red→green is spurious. Drop it, or mark it watched?
lean: (Escalated to the operator — both presented options assumed a watched-only addition would still fold.)
flip: A watched-only addition to a gated capability is VERIFIED to refuse at the scenario gate ("already passed at the fork base — proved nothing"): self-model's existing scenarios are green at the base and the change adds no transitioning gated scenario, so there is no red→green. The prior crossing's gate passed only because the dishonest probe's import error reddened the base by accident.
answer: OPERATOR SETTLED — B: fix the scenario gate, land in one crossing. The re-verify behavior is documented WATCHED (proven in the keystone build_reaches_main.py); the scenario gate is TIGHTENED so a delta adding only watched scenarios to a gated capability (its gated check-block source unchanged base→tip) is nothing-to-gate / skipped — exactly as a wholly-watched capability already is — instead of mis-refused "already passed". The gate fix is proven by its OWN red→green gated scenario (driving the real gate over a planted watched-only delta: refused at the base checkout's old gate, folds at the tip checkout's fixed gate), which doubles as self-model's required transition — so everything lands in self-model in one crossing, no bootstrapping (the transition rides the base/tip checkout-engine difference; the judging gate only reads base-red/tip-green).

[CONTRACT]
Today every code-bearing fold ends with a whole-system re-verification, and that re-verification gives a slow machine the same verdict as a broken build: a capability whose scenarios overrun the fixed 180-second-per-suite budget is caught as "could not be re-verified", the entire verified ~20-minute build is discarded, and the operator cannot tell "your machine was slow" from "the scenario is broken"; as scenarios accumulate the fixed budget is crept past load-dependently, so folds fail non-deterministically with that misleading verdict. This ask delivers two hardenings of the fold's gate machinery, in one crossing. First, the re-verify's per-suite time bound scales with the suite it runs instead of a fixed constant, and a budget overrun becomes a distinct outcome — retried once with headroom and, if it persists, surfaced as an honest, retryable "resource limit reached" decision, never the "the build did not hold once merged" refusal and never the "the scenarios could not run" refusal a genuinely unrunnable scenario (a missing binary, an OSError) still earns. Second, the scenario gate is tightened so that a fold which adds only watched documentation to a capability — leaving its executable check-block source unchanged — is recognized as having nothing to gate and folds, instead of being mis-refused "already passed at the fork base — proved nothing"; the skip is narrow (only when the gated source is genuinely unchanged base→tip), so any change that touches a gated scenario still gets the full red→green. A performance blip stops throwing away a verified build, a slow machine reads as a slow machine and a broken build as a broken build, and a legitimately watched-only refinement is no longer falsely accused of proving nothing.

[DELTA]
# delta — a re-verify overrun is a distinct, scaling resource limit; a watched-only addition is nothing-to-gate

## ADDED — self-model
### Requirement: a re-verify time-budget overrun is a distinct, scaling resource limit, never a broken build
The whole-system re-verify the fold runs before it commits MUST NOT treat a slow run as a broken build.
Its per-suite time bound MUST **scale with the suite it runs** — a per-scenario allotment with a floor —
rather than a fixed constant a growing scenario count creeps past; the per-suite shape is kept (one
capped subprocess per capability), so the cost does not explode into a per-scenario startup multiplier.
The bound MUST be enforced through a **single capped-run seam** that takes the bound as a parameter and
classifies the subprocess at the one point the bound is reached into exactly one of three outcomes: it
**completed** (its exit code is the verdict), it **overran the bound** (a distinct **resource-limit**
outcome), or it **could not run at all** (an OSError — a missing interpreter, a missing binary). The
conflation that returns the same `None` for an overrun and a could-not-run MUST be removed: a genuine
could-not-run still refuses ("the scenarios could not be re-verified — a build that cannot be re-verified
does not land"), but an overrun is **never** that refusal and **never** the "red once merged" refusal.
A resource-limit overrun MUST be retried once with headroom (absorbing a transient blip without
discarding the in-hand verified build) and, if it persists, surface to the operator as a distinct,
**retryable** "resource limit reached" decision — honest that the machine ran out of time, not that the
build is broken — so the node recovers to that decision rather than being declared a failed merge. A
slow machine reads as a slow machine; a perf blip never discards a verified build; a genuinely
unrunnable scenario still refuses.

#### Scenario: a fold whose re-verify overruns its bound surfaces a resource limit, never a broken build
- WHEN a code-bearing fold's whole-system re-verify overruns its (scaled) time bound on a slow run,
  versus one whose merged scenarios genuinely cannot run
- THEN the overrun surfaces a distinct, retryable "resource limit reached" decision with the verified
  build not discarded as broken and not reported as "did not hold once merged", while the
  genuinely-unrunnable case still refuses — and the bound scales with the suite rather than a fixed
  constant a growing scenario count outgrows
- watched — proven from outside the fold in `engine/check/build_reaches_main.py` (the re-verify
  keystone's own home), never from inside the fold it tests, the same self-reference the whole-system
  re-verify already carries

#### Scenario: an overrun is classified distinctly from a could-not-run at the capped-run seam
- WHEN the capped-run seam the re-verify enforces its bound through meets, against a small budget, a run
  that overruns the budget, a run whose interpreter or binary cannot start, and a run that completes
- THEN it yields a distinct resource-limit outcome for the overrun, a could-not-run refusal for the
  unstartable run, and the exit code for the completing run — the overrun is never collapsed into the
  could-not-run refusal
- watched — proven from outside the fold in `engine/check/build_reaches_main.py`, the same home and for
  the same self-reference reason as the re-verify keystone it refines

### Requirement: the scenario gate skips a capability whose gated scenarios a delta does not change
The scenario gate MUST demand a red→green transition only for the gated scenarios a delta actually adds
or changes. A delta that adds **only watched** scenarios to a capability — leaving the capability's
executable check-block source **unchanged** between the fork base and the tip — has **nothing for the
gate to run**, exactly as a wholly-watched capability does, and MUST be **skipped**, not refused. Today
such a delta is mis-refused: the gate runs the capability's whole suite, finds it already green at the
base (the existing gated scenarios are unrelated to this change), and reports "already passed at the
fork base — proved nothing", flattening a legitimate watched-only refinement into a false claim that the
change should have transitioned. The skip MUST be **narrow** — it applies only when the gated
check-block source is genuinely unchanged base→tip, so a delta that adds or changes any gated scenario
still gets the full red→green. This is a **tightening** of the gate's existing wholly-watched-capability
handling (a capability with no check blocks is already skipped), extended to a capability whose check
blocks this change does not touch — never a loosening: a watched-only refinement's proof is still its
capability's watched scenarios and the whole-system re-verify, not a transition it has no gated oracle to
make.

#### Scenario: a watched-only addition to a gated capability folds; an already-green gated addition still refuses
- WHEN the scenario gate judges a delta that adds only a watched scenario to a gated capability whose
  executable check-block source is unchanged base→tip, versus a delta that adds a gated scenario already
  green at the base
- THEN the watched-only addition is skipped — nothing to gate, it folds — while the already-green gated
  addition is still refused "proved nothing"; the gate demands a transition only for the gated scenarios
  the delta changes

  ```check
  gate-judges watched-only-addition
  gate-verdict folds
  gate-judges already-green-gated-addition
  gate-verdict refused
  ```
