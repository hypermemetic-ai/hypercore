# review - 007-phase-one-collaboration

This is the phase-one review artifact for the proposed redesign. It is machine output,
not operator direction.

## summary

Overall: `FLAG`, carried to frame.

Base roster verdicts:

- `contract-checkability`: `FLAG`
- `soundness-fit`: `FLAG`
- `simplicity-fastness`: `FLAG`
- `red-team`: `FLAG`

Additional seated reviewer verdicts:

- `implementation-maintainability`: `FLAG`
- `security-permissions`: `FLAG`
- `operator-ergonomics`: `FLAG`

Disposition: the flags do not block sign-off if the revised frame carries their required
changes as implementation obligations. Optional reviewers are additive only and do not
clear base-roster flags.

## routes reviewed

- Artifact-only review: one-way work requires `review.md`, but panel composition is
  posture and prose.
- Mechanical base roster: `loop.sh review` mechanically spawns a small base reviewer set
  for one-way work and writes `review.md`; optional extra reviewers are advisory.
- Large reviewer orchestrator: a broader panel system with hard claims about reviewer
  diversity, blinding, and independence.

## base verdicts

### contract-checkability - FLAG

The design is coherent in hypercore vocabulary if `direction` and review remain
phase-one acts/artifacts, not new loop gates. Current loop/adapter contracts must be
rewritten together because old deliberation-field requirements conflict with the new lean
contract. Sign-off wording must be clarified: sign-off is not earned by field bloat, but
it still requires a complete lean frame plus required acts.

Required response: keep five gates; call direction and review acts/artifacts; replace old
field requirements everywhere they are current.

### simplicity-fastness - FLAG

The lean frame, `direction.md`, and reversibility gate preserve the scrutable/sound/fast
shape. The risk is replacing field bloat with review ceremony. This reviewer preferred
artifact-only review and flagged `cmd_review` as an accretion risk unless the harness can
actually provide independent reviewers.

Required response: mechanize only a small base roster, only for one-way work, and avoid
checks that pretend to prove review quality.

### soundness-fit - FLAG

The route fixes the shape of the failure only if `direction.md` is substantive. A bare
`direction-by:` token would let the machine wait for a token and choose the route anyway.
Review must be independent enough to add signal, optional reviewers must not dilute base
flags, and reversibility classification must not become a scrutiny bypass.

Required response: direction records selected route, constraint, or explicit delegation
plus `direction-by:`; one-way defaults include methodology/loop/adapter/intent-contract
changes; unresolved base flags block or escalate.

### red-team - FLAG

The strongest failure is lighter-looking ceremony that still ratifies a machine-chosen
route. Specific risks: retrospective direction after a route is written; loose frame
scanner accidentally satisfying `route`; false reviewer independence; two-way
classification bypass; and a lean frame starving phase two of the operator's real intent.

Required response: `direct` refuses after route content; required fields are strictly
parsed from canonical frame content; `direction.md`, `review.md`, and `signoff.md` are
not scanned as required fields; base reviewers are predeclared, role-sliced, read-only,
blind to preference where possible, non-debating, and `PASS`/`FLAG`; the signed frame
carries observable acceptance and excluded interpretations.

## aggregated disposition

All reviewers returned `FLAG`, but none found a hard vocabulary or node-boundary blocker.
The flags narrow the adopted route rather than requiring shelving:

- choose mechanical base roster, but keep it small and limited to one-way work;
- make direction substantive and non-retrospective;
- tighten frame parsing;
- make optional reviewers advisory only;
- make unresolved base or red-team flags block or escalate instead of being outvoted;
- carry acceptance and excluded interpretations into the signed frame.

## additional seated verdicts

### implementation-maintainability - FLAG

Structured direction must be exact rather than heuristic. Require `direction-by:`,
`direction-given-at:`, and exactly one of `selected-route:`, `constraint:`, or
`delegation:`. Required frame parsing must read canonical labels from
`intent/frame/frame.md` only, not all markdown. Review command self-tests must use fake
reviewer output rather than live Codex. Reversibility must not let methodology, loop,
adapter, or intent-contract work bypass review. Archive decision parsing should be exact
and singular, with checks after the history move.

### security-permissions - FLAG

Reviewer spawning must be pinned to literal read-only sandbox and approval `never`; it
must not be weakenable by `CODEX_READ_SANDBOX`. Do not claim network isolation unless the
Codex CLI enforces it. Validate `CODEX_REVIEW_MODEL` as one token and pass it only as an
argv element. Treat direction text, review text, and reviewer output as untrusted data.
Malformed, missing, nonzero, or non-`PASS`/`FLAG` reviewer output counts as `FLAG`.

### operator-ergonomics - FLAG

Direction needs exact command forms, not vague free text. Root `./review` is required
because one-way work cannot proceed without review. `frame`, `signoff`, and `status`
should print actionable next commands and artifact paths for missing direction, missing
review, malformed artifacts, unresolved flags, and incomplete frames. `review.md` should
begin with a compact overall verdict, role verdicts, unresolved flags, and disposition.
Two-way work needs an explicit fast path with no review and a low-friction delegation
direction form.

## unresolved flags carried to frame

- Mechanical reviewer independence is limited by the available harness. The implementation
  must not overclaim it.
- If Codex cannot mechanically spawn read-only reviewer sessions with approval `never`,
  phase two must stop and surface that blocker rather than write a fake review.
- If strict parsing cannot be implemented without brittle behavior, the frame contract
  must be revised before adoption.
