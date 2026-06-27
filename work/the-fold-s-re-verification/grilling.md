surfaced: 2

[Q] Must a re-verify time-budget overrun become a DISTINCT outcome (retry, or an honest "resource limit reached" surfaced to the operator), never silently equal to "scenario broken", while a genuine failure-to-run (missing binary, OSError) still refuses?
lean: Yes — distinct. An overrun is a benign resource-limit outcome: retried once with headroom for a transient blip, and on a persistent overrun surfaced as a retryable "resource limit reached" decision, never the "could not be re-verified" / "build did not hold once merged" refusal. A genuine could-not-run (OSError, missing binary) still refuses. The intent already leans this; the spec's re-verify keystone names "the node recovering to a decision" — this only distinguishes WHICH decision.
flip: If the operator wanted a slow run to hard-fail the build (treat slowness as a defect to fix, not a condition to tolerate), the distinction would collapse back to a refusal. Nothing in intent or spec asks for that; the named harm is precisely that a slow machine reads as a broken build.
answer: Distinct, settled by the lean. Overrun = a benign, retryable resource-limit outcome (retry once, then a "resource limit reached" decision), never "broken"; a genuine could-not-run still refuses. No operator fork.

[Q] Should the per-fold cost be cut by scoping the re-verify, caching the gate's base/tip runs, or parallelizing the merged sweep?
lean: Not in this node. SCOPING is forbidden — `spec/self-model.md` makes the re-verify's whole-system reach structural ("no caller can narrow it"); narrowing reopens the green-on-touched/red-on-system blind spot the keystone exists to close. CACHING the gate's base/tip for the merged run is unsound — they verify different trees (fork base + tip in the fence vs merged main), so the merged verdict cannot be inherited. PARALLELIZING the merged sweep is a pure machine-side optimization with no operator stake and a real downside (15 concurrent `python3 -m engine` startups contend for the very resource whose exhaustion causes the timeout) — deferred as its own optimization ask, made non-urgent once an overrun is benign.
flip: If a real fold's re-verify tail were measured to exceed the operator's patience even after the budget scales, parallelizing would re-enter as its own grilled ask. It is an optimization, not a correctness fix; this node delivers the correctness fix.
answer: Deferred, settled by the lean — scoping forbidden by spec, base/tip caching unsound, parallelizing a separate optimization the benign-timeout fix de-urgents. No operator fork; noted as a follow-on.

[Q] Is 180s the right SHAPE of bound — per-scenario, per-suite, or whole-sweep?
lean: Keep the per-SUITE shape (one capped subprocess per capability — preserves the 15-startup cost, never the 134-startup explosion a per-scenario bound forces) but make the budget SCALE with the suite it runs (a per-scenario allotment with a floor), replacing the fixed 180s constant that a growing scenario count creeps past (the intent's fault #3: "the constant is fixed; the load grows"). A whole-sweep bound lets one slow suite starve the rest; a per-scenario bound multiplies process startups ~9x. Per-suite-that-scales dominates on the operator's only stake — folds complete reliably without exploding cost.
flip: If process-startup cost were ever shown to dominate the budget (so a per-suite bound that scales still creeps), the shape would re-open. With an overrun now benign, the exact shape stops being load-bearing for correctness — it only tunes how rarely the benign resource-limit decision fires.
answer: Per-suite shape kept; the budget scales with the suite (per-scenario allotment + floor) instead of a fixed constant. Settled by the lean — dominant on the operator's stake, no fork.

[CONTRACT]
Today every code-bearing fold ends with a whole-system re-verification, and that re-verification gives a slow machine the same verdict as a broken build: a capability whose scenarios overrun the fixed 180-second-per-suite budget is caught as "could not be re-verified", the entire verified ~20-minute build is discarded, and the operator cannot tell "your machine was slow" from "the scenario is broken". As capabilities accumulate scenarios the fixed budget is crept past load- and variance-dependently, so folds begin failing non-deterministically with that misleading verdict. This ask makes a time-budget overrun a distinct outcome. The re-verify's per-suite time bound scales with the suite it runs instead of a fixed constant the growing scenario count outgrows; a budget overrun is retried once with headroom and, if it persists, surfaces as an honest, retryable "resource limit reached" decision on the operator's queue — never the "the build did not hold once merged" refusal (red on the system) and never the "the scenarios could not run" refusal that a genuinely unrunnable scenario (a missing binary, an OSError) still earns. A performance blip stops throwing away a verified build; a slow machine reads as a slow machine, a broken build as a broken build, and an unrunnable scenario still refuses.

[DELTA]
# delta — a re-verify timeout is a distinct, scaling resource limit, not a broken build

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

#### Scenario: an overrun is a distinct resource limit, an unrunnable run still refuses
- WHEN the capped-run seam the re-verify enforces its bound through is given, against a small budget, a
  run that overruns the budget, a run whose interpreter or binary cannot be started, and a run that
  completes
- THEN it classifies the overrun as a distinct resource-limit outcome, the unstartable run as a
  could-not-run refusal, and the completing run by its exit code — and the resource-limit outcome is
  never collapsed into the could-not-run refusal, so a slow run and a broken run are distinguishable at
  the seam where the distinction is made

  ```check
  verify-run overruns-budget
  outcome resource-limit-distinct
  verify-run cannot-start
  outcome refusal
  verify-run completes
  outcome exit-code
  ```

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
