# frame - 008-phase-two-acceptance

## work

Addressed node: root (`.`).

Node-local work name: `008-phase-two-acceptance`.

Target segments: `collaboration`, `loop`, and `adapter`.

Work in flight: this work node only. The active work sweep found no other active
`NNN-slug` work node under the root or known child-node paths.

Related adopted work read during orient:

- `003-phase-two-observability`, which made phase-two handoff state recoverable without
  changing the one-continuous-thread execution shape.
- `005-harden-loop-collaboration` and `006-collaboration-deliberation`, which hardened
  phase-one recoverability and common ground before `007` replaced their field pile.
- `007-phase-one-collaboration`, which established strict frame parsing, exact
  reversibility, direction before route, and mechanical one-way phase-one review.

The ad-hoc operator brief `PHASE-TWO-REDESIGN.md` is untracked orient material, not
governed intent. Its own preface says it must be deleted or shelved before adoption if it
becomes a work node.

## problem

Phase two still lets the builder be its own witness at the point where work becomes
current truth. Today `loop.sh execute` opens one cleared Codex session at implement, then
resumes that same session through the check sweep and archive decision. The same session
can write the material, update `check.sh`, run the checks, issue the semantic sweep
sentinel, choose adoption or shelving, and fold operator-endorsed statements into current
intent.

That creates a mirror of the phase-one defect fixed by `007`: a correct build is treated
as proved by the builder's own attestation, just as a real collaboration used to be
treated as proved by field presence. `check.sh` remains a mechanical floor, but the route
for methodology work often asks phase two to edit that floor. The current sweep is also
performed by the builder's resumed thread. The operator's signed acceptance condition is
read by archive prose, but there is no independent acceptance check against it before the
one-way adoption move and endorsement stamp.

The target is justified confidence that the build made current is the build the operator
signed: mechanical checks plus independent acceptance scrutiny before adoption, scaled by
reversibility.

## constraints

- Keep the five gates: orient, frame, implement, check, archive. Any added acceptance
  scrutiny is phase-two machinery inside the existing gates, not a sixth gate.
- Preserve the sign-off boundary. The machine still never writes operator direction or
  sign-off, and phase two remains heads-down after sign-off.
- Preserve memoryless re-derivation. New phase-two units or reviewers must derive from
  the signed frame, current disk state, and explicit lean handoff files rather than chat
  memory.
- Keep `check.sh` as the mechanical floor and run it at every boundary where a unit or
  archive fold claims to be green.
- Do not pretend the current sweep problem is solved. This work may move sweep judgement
  to an independent acceptance lens, but it must not add semantic indexing or a new sweep
  theory.
- Do not add a debate board, majority vote, or repair loop. Verifiers return structured
  `PASS` or `FLAG`; unresolved flags block and escalate rather than being outvoted or
  self-cleared.
- Do not weaken the existing phase-one contract from `007`: strict frame parsing,
  one-way review, direction before route, optional reviewer non-override, and exact
  `one-way`/`two-way` reversibility stay current.
- Keep two-way work fast. The heavy one-way door guard should not become default ceremony
  for reversible work.
- Do not rewrite adopted history.

## decision surface or open direction

Teach-back: the operator wants work `008` framed from the phase-two redesign brief before
implementation. The brief's core claim is that phase two currently has an author/judge
collapse: one session builds, checks, sweeps, decides, adopts, and stamps. The proposed
repair is independent acceptance before adoption, using the reviewer primitive introduced
by `007`, with scrutiny escalating at the one-way door.

Alternative framing A: minimal archive guard. Keep the current single implement/check
thread, keep `check.sh`, and add one independent read-only acceptance reviewer after
`check.sh` green and before archive. This is the smallest change, but it leaves the
builder's long thread and self-graded sweep largely intact.

Alternative framing B: full phase-two acceptance funnel. Build in green proof-advancing
units, clear context between units, run one independent implementation-acceptance reviewer
per unit, then for one-way work run an independent implementation-acceptance panel before
archive. Add required observable acceptance and excluded-interpretation frame fields so
reviewers have concrete signed expectations to check. This matches the brief's
recommended design and closes the builder-as-judge defect most directly, at higher
implementation cost.

Alternative framing C: frame-field hardening only. Require observable acceptance and an
excluded interpretation, but keep phase-two execution, sweep, and archive self-attesting.
This improves recoverability but does not address the independent-acceptance defect.

Information-gain questions whose answers would change the frame:

- Should the selected route be the full funnel in Alternative B, or a smaller first step
  such as Alternative A?
- Should tier two be the brief's one-way-only implementation-acceptance panel, or should
  any panel also run for some high-risk two-way work?
- What exact tier-two lens list should be required if the full funnel is selected:
  whole-acceptance conformance, proof integrity, independent coherence, security and
  permissions, and red-team; or a smaller/larger named roster?
- Should `observable acceptance` and `excluded interpretation` be added as required frame
  fields for all new work, or only for one-way work?
- Should the untracked `PHASE-TWO-REDESIGN.md` be deleted during adoption, moved into this
  work node as shelved orient material, or retained as explicit debt?

Open direction: the operator must record the selected route, constraint, or delegation in
`intent/frame/direction.md` before this frame can settle `## route`.

Selected operator direction, recorded in `intent/frame/direction.md`: Full Funnel. Phase
two should work in green proof-advancing units, clear context between units, run one
independent implementation-acceptance reviewer per unit, run a full
implementation-acceptance panel before one-way archive, require observable acceptance and
excluded-interpretation frame fields, and block unresolved `FLAG`s before adoption.

Review state: `./review 008-phase-two-acceptance` wrote
`intent/frame/review.md`. All four base roles are `FLAG` because their reviewer
subprocesses exited `1`; the artifact disposition is `escalated`. This is not a
substantive route objection, but it means the current harness did not obtain independent
review signal before route settlement. The operator should treat that as an explicit
limitation when giving direction or signing off.

Reversibility: one-way

## route

Adopt the Full Funnel phase-two acceptance route.

Parent intent amendments:

- `collaboration`: add that phase-two acceptance is an operator-reliance concern, not only
  loop mechanics. The machine must make the built result independently checkable against
  what the operator signed before one-way adoption stamps the operator's endorsement.
- `collaboration`: add that unresolved implementation-acceptance `FLAG`s are feedback
  material. They block and surface to the operator rather than being self-cleared,
  averaged away, or treated as warnings.
- `loop`: keep exactly five gates. Phase-two acceptance review, per-unit handoff, and
  one-way panel review are machinery inside implement/check/archive, not new gates.
- `loop`: extend new-work frame completeness with two strictly parsed fields in canonical
  `intent/frame/frame.md`: `observable acceptance` and `excluded interpretation`.
  `acceptance condition` remains required; `observable acceptance` is the concrete command,
  state, check, or externally inspectable condition that acceptance review can test.
- `loop`: define an implementation unit as the smallest proof-advancing delta that leaves
  `./check.sh` green. Units are vertical slices: statements, material, and checks land
  together when the work requires all three.
- `loop`: require `./check.sh` green at every phase-two unit boundary and before any
  acceptance verdict or archive fold is trusted.
- `loop`: after each unit, run a single independent implementation-acceptance reviewer in
  a fresh read-only session, not by resuming the builder. The reviewer reads the signed
  frame, the unit's proof obligation, the unit diff, and any lean per-unit handoff, then
  returns exactly `PASS` or `FLAG`.
- `loop`: for one-way work, require a tier-two implementation-acceptance panel before the
  irreversible archive move and endorsement stamp. Two-way work does not run the panel
  unless later intent explicitly requires it.
- `loop`: make unresolved tier-one or tier-two `FLAG`s halt phase two before archive. The
  active work node remains in flight for the operator; the builder cannot clear its own
  flag, and optional/advisory verdicts cannot override required flags.
- `loop`: move the semantic sweep judgement for one-way adoption into the independent
  tier-two panel's `independent-coherence` lens. Do not claim this redesign solves the
  deeper semantic-indexing problem named in the brief.
- `adapter`: update Codex machine statements so the rigid workflow no longer describes
  one implement thread resumed through check and archive. It should describe per-unit
  cleared builder sessions, independent acceptance sessions, recoverable phase-two
  acceptance artifacts, and one-way panel gating.
- `adapter`: define the phase-two implementation-acceptance reviewer and panel lenses.
  Tier one is a grouped implementation-acceptance reviewer. Tier two for one-way work has
  five required lenses: `whole-acceptance-conformance`, `proof-integrity`,
  `independent-coherence`, `security-permissions`, and `red-team`.

Material amendments:

- Update `hypercore.md` so the loop summary says phase two builds in small green units,
  independent acceptance checks each unit, one-way adoption is guarded by a full
  implementation-acceptance panel, and unresolved implementation-acceptance flags block
  archive.
- Update `intent/collaboration.md`, `intent/loop.md`, and `intent/adapter.md`, plus their
  machine-statements files, with the parent intent amendments above.
- Update `adapter/codex.md` so the Codex adapter prose routes phase two through per-unit
  clearing and independent acceptance without weakening sign-off or adding a sixth gate.
- Update `adapter/gates/implement.md` so implement builds one proof-advancing green unit
  at a time and writes only lean handoff state needed by later cleared sessions.
- Update `adapter/gates/check.md` so check verifies `./check.sh`, runs tier-one
  implementation acceptance for completed units, and makes the one-way panel responsible
  for independent coherence before archive.
- Update `adapter/gates/archive.md` so archive is allowed to fold and stamp one-way work
  only after required implementation-acceptance artifacts are clean.
- Update `adapter/loop.sh`:
  - add `observable acceptance` and `excluded interpretation` to strict frame
    completeness and start scaffolding;
  - add phase-two acceptance state under the addressed work frame, with recoverable unit
    records and verdict artifacts;
  - replace the single `implement start` plus `check/archive resume` thread shape with a
    loop over green units, where each unit builder starts from a fresh Codex session;
  - run a fresh read-only tier-one implementation-acceptance reviewer after each unit;
  - run the tier-two one-way implementation-acceptance panel before archive;
  - parse `PASS`/`FLAG` verdicts exactly, treat malformed/missing/nonzero reviewer output
    as `FLAG`, and halt before archive on unresolved required flags;
  - keep approval/read-only isolation for reviewers at least as strict as phase-one
    `cmd_review`;
  - preserve phase-two run-state observability for the active gate, unit, verdict files,
    current state, and failure reason;
  - keep `./check.sh` green checks before acceptance, after archive fold, and after
    history move;
  - keep `ARCHIVE_DECISION` exact and singular.
- Update `check.sh`:
  - assert the new intent and adapter statements;
  - assert strict parsing and scaffolding of `observable acceptance` and
    `excluded interpretation`;
  - self-test that frames missing either field are rejected once the new contract is
    current;
  - self-test unit acceptance verdict parsing, malformed output as `FLAG`, required-flag
    blocking, and one-way panel gating;
  - self-test that two-way work pays tier one but not the one-way panel;
  - self-test that the loop no longer resumes one builder thread through all phase-two
    judgement points.
- Delete `PHASE-TWO-REDESIGN.md` during implementation or archive, because it is
  untracked orient material whose durable content is now in this frame and, on adoption,
  current intent/history.

Implementation units for phase two:

1. Frame-field unit: add `observable acceptance` and `excluded interpretation` to loop
   frame validation, scaffolding, gate prompts, adapter prose, and checks. This frame
   already includes those sections so the new validation can pass during work `008`.
2. Intent unit: update `collaboration`, `loop`, `adapter`, their machine statements, and
   `hypercore.md` with the Full Funnel contract while keeping `sweep` out of scope.
3. Acceptance-runner unit: implement recoverable unit records, tier-one acceptance
   reviewer spawning, strict verdict parsing, malformed-output-as-`FLAG`, and blocking
   behavior in `adapter/loop.sh`; prove with deterministic fake reviewers.
4. One-way panel/archive unit: implement required tier-two lenses for one-way work,
   archive gating, independent-coherence placement, and updated archive/check prompts;
   prove with deterministic fake panel outputs.
5. Settlement unit: remove `PHASE-TWO-REDESIGN.md`, run the full check suite, run the
   sweep, and archive according to this frame if the required acceptance artifacts are
   clean.

## acceptance condition

Adopt only if all of the following hold:

- `./check.sh` is green before sign-off, after implementation, after archive fold, and
  after history move.
- New work frames cannot be signable without `observable acceptance` and
  `excluded interpretation` fields in canonical `intent/frame/frame.md`.
- Phase-two acceptance artifacts are recoverable under the work node's `intent/frame/`.
- Each phase-two unit leaves `./check.sh` green and has a tier-one
  implementation-acceptance verdict.
- One-way archive is blocked unless the tier-two implementation-acceptance panel has clean
  required verdicts.
- Unresolved required `FLAG`s stop phase two before archive and leave the work node active
  for the operator.
- The loop no longer resumes one builder session through every phase-two judgement point.

## observable acceptance

Run `./check.sh`; run deterministic loop self-tests for the new frame fields, tier-one
acceptance verdict parsing, required-flag blocking, one-way panel gating, and
per-unit-cleared execution shape; run `./adapter/loop.sh execute 008-phase-two-acceptance
--dry-run` or an equivalent checked dry-run/probe that shows implement units, tier-one
acceptance, one-way panel, and archive are separate recoverable phase-two steps rather
than one resumed builder thread.

## excluded interpretation

Do not implement only new frame fields while leaving phase two self-attesting. Do not keep
one continuous builder thread that resumes through check sweep and archive. Do not make
acceptance review warning-only, advisory-only, majority-voted, self-cleared, or optional
for one-way adoption. Do not broaden this work into a semantic tagging or sweep-indexing
redesign.

## proof state

Current proof state before route settlement:

- `./adapter/loop.sh status 008-phase-two-acceptance` reports `phase=frame`,
  `frame_complete=no`, and `signed_off=no`.
- `./adapter/loop.sh frame 008-phase-two-acceptance` rejects the scaffold, proving phase
  two is sealed until framing and sign-off are complete.
- `./review 008-phase-two-acceptance` wrote the required one-way review artifact, with
  base-role `FLAG`s caused by reviewer subprocess exit status `1` and disposition
  `escalated`.
- The current `adapter/loop.sh execute` implementation still opens one Codex thread at
  implement and resumes it through check and archive.
- The current check gate still asks the resumed phase-two session to run the sweep and
  emit `SWEEP_VERDICT`.

Required proof after implementation depends on selected direction, but must include
mechanical checks for any new frame fields, acceptance artifacts, reviewer isolation and
verdict parsing, flag blocking, per-unit state if added, and archive gating.

Selected-route proof obligations:

- `adapter/loop.sh` strict frame parsing requires `observable acceptance` and
  `excluded interpretation` from canonical `intent/frame/frame.md`.
- `loop.sh start` scaffolds both new fields.
- Phase-two run state records units, unit handoff paths, tier-one verdict paths, panel
  verdict paths, current gate/unit, and failure reason.
- Unit builders are fresh Codex sessions; tier-one reviewers and tier-two panel reviewers
  are fresh read-only sessions and not resumes of the builder.
- Malformed, missing, nonzero, or non-`PASS`/`FLAG` acceptance reviewer output counts as
  `FLAG`.
- Required tier-one `FLAG`s and tier-two one-way panel `FLAG`s halt before archive and
  leave work active.
- Two-way work gets tier-one acceptance but does not require the one-way panel.
- One-way archive cannot stamp touched intent segments until the required panel is clean.
- The old one-thread implement/check/archive resume shape is absent from current adapter
  statements and covered by checks.

## sweep

Concept map before route settlement:

- `collaboration` owns reliance calibration, operator agency, phase-one direction and
  sign-off acts, and graceful stop when written ground is insufficient. It likely needs
  new statements that phase-two acceptance scrutiny is independent of the builder and
  that unresolved implementation-acceptance flags surface to the operator.
- `loop` owns the five gates, frame completeness, phase-two stop conditions, check and
  sweep obligations, and archive adoption or shelving. It likely needs statements for
  observable acceptance, excluded interpretation, per-unit check boundaries if selected,
  independent acceptance artifacts, one-way panel gating, and flag behavior.
- `adapter` owns the Codex harness materialization of the loop. It likely needs machine
  statements and material updates for new phase-two execution shape, acceptance reviewer
  spawning, state files, gate prompts, and `check.sh` coverage.
- `sweep` is touched conceptually but should not be amended unless direction explicitly
  broadens scope; the brief names sweep redesign as out of scope.
- `PHASE-TWO-REDESIGN.md` is untracked orient material and conflicts with the desired
  settled corpus if left at adoption without a claim.

No active sibling work currently collides with these segments. The main collision risk is
with adopted `007`: this work must extend the direction/review/reversibility machinery
without weakening the phase-one contract it established.

## adoption claim

Adopt this work only if the selected phase-two acceptance route is implemented,
mechanically checked, swept coherent with `007`, and archived so current intent and
adapter material agree about when independent acceptance is required before adoption.

## shelving claim

Shelve this work if operator direction rejects independent phase-two acceptance, if the
chosen route cannot be made mechanical without faking verifier independence, or if the
implementation would weaken sign-off, direction, strict frame parsing, or the green
`check.sh` floor.
