# frame - 010-phase-two-performance

## work

Addressed node: root (`.`).

Node-local work name: 010-phase-two-performance

Target segments: `collaboration`, `loop`, and `adapter`.

Work in flight: this work node only. The active work sweep found no other active
`NNN-slug` work node under the root or `home`. The proposal names
`DECOMPOSITION-FINDINGS.md` as related through shared resumable-execute machinery, but
that document is unframed scratch input, not an active work node.

Orient material: `PERFORMANCE-FINDINGS.md` is untracked scratch input. It is not current
intent and must be deleted or otherwise removed from the live root before adoption if
this work carries its content into governed artifacts. `DECOMPOSITION-FINDINGS.md` and
`WORK-NODE-COLLAPSE-FINDINGS.md` are sibling scratch inputs and remain out of scope except
where the route explicitly reuses resumable-execute ideas.

## problem

Phase-two acceptance work became slow enough to break the methodology's `fast` test after
the phase-one collaboration and two-tier phase-two acceptance changes. The empirical
proposal says `009-operator-acts` reran roughly ten times on 2026-06-07 and consumed about
three hours for work that should have been short.

The proposal diagnoses three coupled causes. First, acceptance reviewers produce only one
bit, `PASS` or `FLAG`, under an uncertainty-defaults-to-`FLAG` rule, so an operator cannot
act on a flag without guessing. Second, each flag forces a whole rerun because execute is
not resumable and does not memoize passed units. Third, each run is slow because builders
and reviewers inherit the same strong model settings and the tier-two panel lenses run
serially.

The same proposal also identifies two correctness bugs and one door-integrity hole in the
hot path: phase-one review subprocesses may exit `1` and convert the whole base roster to
crash flags; persisted panel artifacts may carry stale lens instructions; and
`HYPERCORE_ACCEPTANCE_FAKE_DIR` can manufacture non-dry-run acceptance artifacts before a
real reviewer is spawned.

## constraints

- Preserve the strict door: uncertainty still flags, unresolved required acceptance flags
  still block archive, and the one-way tier-two panel stays strong.
- Do not cheapen reviewers. Tier-one and tier-two acceptance remain semantic proof-floor
  work, not builder work.
- Use fast routing only for builders, and only behind `./check.sh` plus strong tier-one
  acceptance.
- Keep builder retry and escalation to build attempts only. The tier-two panel never
  auto-retries, and structural or route failures still surface to the operator.
- Make acceptance flags actionable by recording rationale and concrete evidence, not by
  weakening the verdict rule.
- Keep resumable execute derived from signed-frame and on-disk artifacts so phase two
  remains memoryless across runs.
- Treat fake acceptance as self-test/dry-run material only. Real execute and archive must
  reject fake-source acceptance artifacts.
- Add proof-floor coverage before trusting changed routing, retry, memoization, parallel
  panel, or fake-acceptance behavior.
- Do not adopt the scratch findings files as current intent. Fold only the accepted frame
  and implementation into current material/history.

## decision surface or open direction

Decision surface: `intent/frame/options.md` records three materially distinct routes. All
are one-way because they change the proof/acceptance hot path and the adapter material
that enforces it.

Teach-back: the operator wants the performance proposal carried through a real loop run,
not treated as scratch truth. The core ask is to keep the acceptance door strict while
making review output legible, lowering only builder cost, adding builder retry then
escalation, making execute resumable, running the tier-two panel in parallel, and fixing
known proof-floor bugs and fake-acceptance bypass risk.

Alternative framing A: treat the issue as a reviewer-signal problem. Cure the blind
`FLAG` loop first so future performance work has evidence and does not rerun blindly.

Alternative framing B: treat the issue as an execute-resumption problem. Keep the review
contract mostly intact and first make reruns reuse already-passed units.

Alternative framing C: treat the issue as model-routing latency. Route builders to the
fast model behind the existing proof floor and add retry/escalation, while leaving
artifact shape and resumability mostly alone.

Information-gain questions whose answers would change the frame:

- Should the first adopted route carry the whole proposal, or split proof-integrity fixes
  from model-routing and resumability work?
- Should the memoization key invalidate on the frame, unit proof text, unit diff, prior
  unit state, loop implementation version, check output, or some narrower subset?
- Should builder retry counters and escalation be per unit only, or can a strong-model
  escalation lift the rest of the run?
- Should cache reuse require a fresh `./check.sh` green result before accepting a stored
  tier-one `PASS`, or can the old green result be part of the cache key?
- Should fake acceptance be completely unavailable in real execute, or available only
  when artifacts are marked fake-source and mechanically rejected by archive?

Pending operator direction: select one route from `intent/frame/options.md` through the
terminal-gated `./direction 010-phase-two-performance [operator]` helper before writing
the route.

Selected operator direction, recorded in `intent/frame/direction.md`: carry the full
performance proposal as one loop: legible acceptance artifacts, strong-review floor, fast
builder routing, builder retry then escalation, resumable execute, parallel tier-two
panel, phase-one review crash fix, stale-lens verification, and fake-acceptance
hardening; delegate cache-key and retry-detail choices to the machine under the signed
constraints.

Review state: `./review 010-phase-two-performance` wrote `intent/frame/review.md`.
All four base roles are `FLAG` because their reviewer subprocesses exited `1`; the
artifact disposition is `escalated`. This gives no substantive independent review signal.
The route treats that as a live defect to fix in the phase-one review path, keeps the
selected route constrained by mechanical proof and strict phase-two implementation
acceptance, and does not treat optional or missing reviewer signal as clearance.

Reversibility: one-way

## route

Adopt the selected full performance bundle.

Parent intent amendments to fold at archive:

- `collaboration`: implementation-acceptance signal is part of reliance calibration.
  Required acceptance artifacts must carry a parseable verdict plus enough rationale and
  concrete evidence for the operator or a later machine to act on a `FLAG`; uncertainty
  still flags, and legibility does not weaken the door.
- `collaboration`: build retry is bounded proof-floor recovery, not a structural
  re-decision. A builder may retry a failed unit within the signed route; structural
  mismatches, tier-two flags, or exhausted escalation still surface to the operator.
- `loop`: tier-one and tier-two acceptance reviewers return structured output with one
  parseable verdict and required rationale/evidence fields. Missing, malformed, nonzero,
  unsupported-source, non-`PASS`/`FLAG`, or evidence-free required acceptance still counts
  as `FLAG`.
- `loop`: acceptance artifacts record their source as real reviewer, dry-run/self-test, or
  fake/self-test. Real archive refuses dry-run or fake-source required acceptance
  artifacts.
- `loop`: phase-two builders may be routed separately from reviewers. Builder routing may
  use `gpt-5.3-codex-spark` at high effort when available; tier-one acceptance, tier-two
  acceptance, and phase-one review remain on the strong review model/floor.
- `loop`: a unit build attempts the fast builder first, retries failed builds up to three
  fast attempts when `./check.sh` or tier-one acceptance fails, escalates that unit to the
  strong builder after the fast budget is exhausted, and then returns to the operator if
  the strong attempt still fails.
- `loop`: execute is resumable from signed-frame and on-disk artifacts. Passed unit
  build/tier-one evidence may be reused only when its cache key still matches the signed
  frame, unit proof obligation, relevant prior-unit state, loop implementation version,
  recorded diff, and green mechanical check evidence.
- `loop`: the tier-two one-way panel lenses run concurrently after all required tier-one
  evidence is clean; each lens remains independent and read-only, and any required lens
  `FLAG` blocks archive.
- `adapter`: the Codex loop materializes the separate builder/reviewer routing knobs,
  structured review and acceptance artifacts, retry/escalation ladder, resumable execute
  cache, parallel panel, fake-source rejection, and phase-one review crash fix.
- `adapter`: the gate prompts and checks describe the new acceptance artifact shape and
  continue to prohibit builders from speculating about future acceptance evidence.

Material amendments:

- Update `adapter/loop.sh` so acceptance parsing accepts exactly one verdict field plus
  required rationale and evidence fields, preserves strict `FLAG` defaults, records raw
  output without discarding rationale, and exposes concise notes in status/events.
- Update tier-one and tier-two prompts to request a frame-anchored reason and concrete
  evidence citation for every verdict. A `PASS` should cite what proves the unit or whole
  work; a `FLAG` should cite the missing, mismatched, stale, or uncertain evidence that
  blocks acceptance.
- Add an acceptance source marker. Real reviewer artifacts are accepted for real archive;
  dry-run and fake/self-test artifacts are rejected for real tier-two/archive gates. Keep
  fake acceptance available only for dry-run/self-test coverage.
- Fix the phase-one review subprocess path so crashes are not silently flattened into
  content-free base-roster flags. The review artifact should preserve subprocess status
  and stderr/stdout enough to diagnose a crash, and `./check.sh` should prove the fake
  review self-test still works.
- Verify whether persisted panel artifacts can carry stale lens instructions. If the live
  code is correct, add or keep a check that each required lens artifact contains its
  specific instruction; if live code is wrong, fix the lens threading.
- Add per-role model and effort routing. The default builder route is
  `gpt-5.3-codex-spark` at xhigh effort when available under the current Codex auth; review subprocesses
  remain on the strong review model. Environment knobs may override the defaults, but the
  route must not make reviewers cheaper by default.
- Add bounded per-unit builder retry and escalation. Failed fast attempts are discarded or
  overwritten in a controlled way so only a green, accepted attempt becomes unit evidence.
  The retry counter is per unit; escalation affects only that unit.
- Add resumable execute. Re-running `execute` skips unchanged units whose cached build,
  diff, green-check evidence, and tier-one `PASS` match the current cache key. Any cache
  miss rebuilds and re-reviews the unit and invalidates later dependent unit evidence.
- Parallelize tier-two panel lenses with separate read-only reviewer subprocesses and
  deterministic artifact paths. The panel completes only after all lenses finish, and any
  failed subprocess or `FLAG` blocks archive.
- Update `adapter/gates/check.md`, `adapter/gates/implement.md`, `adapter/codex.md`,
  `hypercore.md`, current intent machine statements, and `check.sh` so the written
  methodology, adapter material, and proof floor carry the selected route.
- Delete `PERFORMANCE-FINDINGS.md` before adoption because its accepted content is carried
  by this signed frame and eventual history. Leave `DECOMPOSITION-FINDINGS.md` and
  `WORK-NODE-COLLAPSE-FINDINGS.md` untouched unless a later signed work adopts them.

Implementation units for phase two:

1. Acceptance legibility and fake-source hardening: update acceptance verdict parsing,
   tier-one and tier-two prompts, acceptance artifact writing, source markers, and archive
   validation so required acceptance carries verdict, rationale, evidence, and real-source
   proof while fake/self-test artifacts are impossible to use for real adoption; add
   `./check.sh` coverage for structured PASS/FLAG, evidence requirements, malformed
   output, dry-run behavior, and real-run fake-source rejection.
2. Phase-one review crash and lens-specific proof: fix or harden the phase-one review
   subprocess path that produced exit-1 base-roster flags, preserve diagnostic output in
   `review.md`, keep optional reviewers advisory, and prove each tier-two panel lens uses
   its own live instruction rather than stale copied text.
3. Role routing and builder retry/escalation: add separate builder and reviewer model
   knobs/defaults, route only builders to `gpt-5.3-codex-spark` by default when available,
   keep all reviews strong, and implement the per-unit fast-builder three-attempt budget
   followed by strong-builder escalation and operator stop on strong failure; add focused
   self-tests using deterministic fake builders/reviewers rather than external model
   availability.
4. Resumable execute cache: add a signed-frame-derived per-unit cache key covering the
   frame, unit proof obligation, relevant prior-unit state, loop implementation version,
   diff/check evidence, and tier-one PASS; on rerun, skip unchanged accepted units,
   rebuild cache misses, and invalidate downstream units when prior state changes; prove
   skip and invalidation behavior in `./check.sh`.
5. Parallel tier-two panel and state alignment: run all tier-two lenses concurrently with
   bounded subprocesses, collect deterministic artifacts and events, preserve the final
   all-lenses-clean archive gate, align status output and gate prompts with structured
   acceptance/resumability, update methodology and adapter intent statements, and remove
   `PERFORMANCE-FINDINGS.md` from live root material.

## acceptance condition

Adopt the selected route only if the phase-two hot path remains strict and becomes faster
and more legible without weakening proof: required acceptance artifacts carry actionable
rationale/evidence, real archive rejects fake or dry-run acceptance sources, reviewers
stay on the strong floor, builders have separate fast routing with bounded retry then
strong escalation, unchanged accepted units are reusable on rerun, tier-two lenses run in
parallel, the phase-one review crash path is fixed or diagnostically exposed, stale lens
reuse is mechanically guarded, the selected contract is represented in current intent and
adapter material, and `./check.sh` is green.

## observable acceptance

`./check.sh` passes. Focused checks or deterministic probes show: structured acceptance
outputs with verdict, rationale, and evidence are accepted; malformed or evidence-free
outputs still flag; real execute/archive refuse fake-source and dry-run required
acceptance artifacts; `./review` no longer collapses subprocess crashes into opaque base
flags without diagnostics; each tier-two lens prompt/artifact is lens-specific; builder
and reviewer routing are separate with reviewers kept strong by default; a fast-builder
failure retries up to three times then escalates only that unit; a rerun skips an
unchanged accepted unit and rebuilds after cache invalidation; and tier-two panel lenses
start concurrently while any lens `FLAG` still blocks archive.

## excluded interpretation

This work does not mean acceptance becomes less strict, reviewer flags become warnings,
the tier-two panel becomes cheap or optional, structural failures are auto-recovered, or
scratch findings files become current intent without adoption.

## proof state

Read during orient:

- `hypercore.md`
- `intent/organizing-document.md`
- `intent/collaboration.md` and `intent/machine-statements/collaboration.md`
- `intent/loop.md` and `intent/machine-statements/loop.md`
- `intent/active-work.md` and `intent/machine-statements/active-work.md`
- `intent/adapter.md` and `intent/machine-statements/adapter.md`
- `PERFORMANCE-FINDINGS.md`
- `DECOMPOSITION-FINDINGS.md`
- `WORK-NODE-COLLAPSE-FINDINGS.md`
- `adapter/gates/orient.md`
- `adapter/gates/frame.md`
- selected `adapter/loop.sh` sections for work naming, direction options, review, and
  frame scaffolding

Current proof limitation: no mechanical checks have run for this work yet.

Review proof limitation: the required one-way phase-one review ran, but every base role
returned `FLAG` only because the reviewer subprocess exited `1`. The frame carries this
as an escalated limitation and makes the crash path part of the selected route's proof
obligation.

## sweep

Preliminary sweep:

- `collaboration` already requires review artifacts to record structured signal and says
  phase-two acceptance is an operator-reliance concern. Bare one-word acceptance artifacts
  satisfy current parsing but are weak against that reliance statement.
- `loop` currently requires tier-one reviewers to return exactly `PASS` or `FLAG` and
  treats malformed or missing output as `FLAG`; any legibility change must preserve a
  parseable verdict while adding rationale/evidence.
- `loop` says unresolved required flags halt phase two and leave the active work in
  flight. Builder retry must be framed as repeated build attempts before a final required
  acceptance failure, not as self-clearing a required acceptance flag.
- `adapter` materializes the current serialized tier-two panel, builder/reviewer routing
  knobs, fake acceptance path, and review artifacts in `adapter/loop.sh`; material changes
  need intent and proof-floor alignment.
- `DECOMPOSITION-FINDINGS.md` names re-entrant execute as shared machinery, but it is
  scratch, not active work. This frame may reuse resumability mechanics without adopting
  decomposition semantics.
- No active sibling work node currently competes for the same root intent segments.

## adoption claim

If signed and accepted, this work adopts the selected performance route into current root
intent, adapter material, proof checks, and history.

## shelving claim

If the selected route cannot be proved without weakening the acceptance door or making the
hot path incoherent, shelve this work with the findings preserved in history and leave
current intent unchanged.
