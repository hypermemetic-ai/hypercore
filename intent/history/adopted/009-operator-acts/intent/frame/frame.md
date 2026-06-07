# frame - 009-operator-acts

## work

Addressed node: root (`.`).

Node-local work name: `009-operator-acts`.

Target segments: `collaboration`, `loop`, and `adapter`.

Work in flight: this work node only. The active work sweep found no other active
`NNN-slug` work node under the root, `home`, or the mounted `home/codex-cockpit`
entry point.

Orient material: `OPERATOR-ACTS-FINDINGS.md` is untracked scratch input. It is not
current intent and must be deleted or otherwise removed from the live root before
adoption if this work carries its content into governed artifacts.

## problem

Phase one now names direction and sign-off as the two anchored operator acts, and says the
machine performs neither for itself. The current root helpers still make those acts mostly
normative: `./direction` accepts route text through ordinary process arguments or stdin,
and `./signoff` can write a bare sign-off artifact from ordinary command invocation. That
keeps the acts lightweight, but it does not mechanically distinguish the legitimate
operator path from the machine's command path, and sign-off does not show the operator the
signed frame's reliance surface at the moment of attestation.

The scratch findings identify a channel distinction available in this Codex harness:
normal tool commands have no controlling terminal, and `/dev/tty` fails immediately with
`No such device or address`. A helper that reads its decisive confirmation from `/dev/tty`
therefore cannot be completed by the phase-one machine command path, while an operator at
a real terminal can answer it. The target is to use that simple channel distinction to make
direction and sign-off real, informed operator acts without claiming cryptographic
non-repudiation.

## constraints

- Keep the five loop gates. Direction and sign-off remain phase-one acts inside orient and
  frame, not new gates.
- Keep phase one fast. The operator act should be a short terminal choice or confirmation,
  not a long manual transcription ritual.
- Do not overclaim. `operator-gate: tty` proves the legitimate helper crossed a terminal
  liveness gate; it is not tamper-evidence, non-repudiation, PKI, a hardware-token
  scheme, or protection against same-user file forgery.
- Direction must become a real choice among materially distinct, neutrally presented
  options. The machine may draft options; it may not choose one by writing direction for
  itself.
- Sign-off must become informed at the moment of attestation by rendering a short brief
  from the frame before it reads the confirming token.
- Preserve the existing strict phase-one contracts: direction before route, no
  retrospective direction, one-way base review before route settlement, optional reviewer
  non-override, exact `one-way`/`two-way` reversibility, and frame completeness from
  canonical `intent/frame/frame.md`.
- Keep the `operator-gate:` field format open to a later passphrase-keyed value such as
  `hmac:<...>` without implementing secrets in this route.

## decision surface or open direction

Decision surface: `intent/frame/options.md` records three materially distinct options:
Route A (`tty-options`), Route B (`tty-hmac-ready`), and Route C (`tty-free-text`).

Teach-back: the operator wants the scratch findings made current through a real loop run.
The essence is to make direction a neutral multiple-choice operator pick, make sign-off a
brief informed terminal confirmation, and have both artifacts carry an `operator-gate:`
marker written only by helpers that successfully opened `/dev/tty`.

Alternative framing A: protect the operator acts as liveness events. Add a shared
terminal gate and neutral options, but make no cryptographic claim. This directly matches
the scratch finding and the operator's stated assurance bar.

Alternative framing B: treat the residual same-user file-forgery gap as the main problem.
Add a passphrase-keyed marker now. This would be stronger against bypass but asks the
operator for a secret on every act and is outside the stated non-cryptographic scope.

Alternative framing C: preserve today's free-text direction surface and only add terminal
confirmation. This is smallest, but it does not make direction a real multiple choice and
leaves the "machine proposed one route, operator stamped it" weakness mostly intact.

Information-gain questions whose answers would change the frame:

- Should the work add only `operator-gate: tty`, or also implement a passphrase-keyed
  marker now?
- Should sign-off confirmation require the work number, or accept a single `y`?
- Should option presentation allow a machine recommendation, or remain strictly neutral?
- Should old explicit direction/signoff argument forms remain as a compatibility escape,
  or should they fail unless the operator gate can run?

Selected operator direction, recorded in `intent/frame/direction.md`: Route A:
tty-gated acts plus neutral options; add `options.md`, require `operator-gate: tty` on
direction and signoff, make signoff informed, and keep `operator-gate` B-ready without
adding HMAC yet.

Review state: `./review 009-operator-acts` wrote `intent/frame/review.md`. All four base
roles are `FLAG` because their reviewer subprocesses exited `1`; the artifact disposition
is `escalated`. This is an explicit limitation: the route did not receive substantive
independent reviewer signal before settlement. The frame answers it by keeping the route
small, preserving the no-cryptographic-overclaim constraint, requiring mechanical proof in
`./check.sh`, and leaving unresolved one-way implementation-acceptance flags to block
archive in phase two.

Reversibility: one-way

## route

Adopt Route A: terminal-gated operator acts plus neutral direction options.

Parent intent amendments to fold at archive:

- `collaboration`: strengthen the anchored operator-act contract so direction and
  sign-off are not only norms. A legitimate helper-written operator act crosses an
  operator gate, records `operator-gate: tty`, and remains simple enough for the operator
  to use without turning phase one into transcription work.
- `collaboration`: direction is a real choice when the frame provides neutral,
  materially distinct options and the helper copies the selected prewritten option into
  `direction.md`. The machine may draft options; it may not choose one for the operator.
- `collaboration`: sign-off is informed at the moment of attestation when the helper
  renders the signed frame's route, acceptance, observable acceptance, excluded
  interpretation, reversibility, and target segments before reading the confirming token.
- `collaboration`: `operator-gate: tty` is a liveness marker for the helper path, not
  cryptographic non-repudiation or tamper-evidence.
- `loop`: add `intent/frame/options.md` as the neutral options artifact for new work that
  needs operator route selection. It records numbered options with kind, summary,
  reversibility, and tradeoff, plus reject/abort choices.
- `loop`: direction helpers for new work select one option from `options.md` through
  `/dev/tty`, then write `direction-by:`, `direction-given-at:`, `operator-gate: tty`,
  and exactly one selected route, constraint, or delegation copied from the option.
- `loop`: sign-off helpers render a concise frame-derived attestation brief through
  `/dev/tty`, require the work number as confirmation, then write `signed-off-by:`,
  `signed-off-at:`, and `operator-gate: tty`.
- `loop`: frame/sign-off validation requires gated operator artifacts for new work, while
  preserving strict non-retrospective direction and the one-way review requirement.
- `adapter`: update the Codex adapter and loop machine statements so the root `./direction`
  and `./signoff` helpers are terminal-gated operator-act helpers rather than ordinary
  argument-transcription commands for new work.
- `adapter`: state the Codex limitation honestly: the gate relies on the current harness
  lacking `/dev/tty`; it does not prove network isolation, non-repudiation, or file
  integrity.

Material amendments:

- Update `adapter/loop.sh` with a shared operator-gate primitive that opens `/dev/tty`,
  renders a short prompt/brief, reads a short token, and fails loudly when `/dev/tty` is
  unavailable.
- Rework `cmd_direct` so its primary no-argument path infers the active unsigned work when
  unambiguous, reads `intent/frame/options.md`, renders neutral numbered choices to the
  terminal, accepts a bare number, `n` for none-of-these, or `q` for abort, and writes the
  chosen option text into `direction.md` with `operator-gate: tty`.
- Keep the `operator-gate:` value syntax B-ready by accepting a value token shape that can
  later be `hmac:<...>`, but implement only `tty` in this work.
- Rework `cmd_signoff` so its primary no-argument path infers work and operator when
  unambiguous, renders a concise frame-derived brief to the terminal, requires the work
  number as the confirm token, and writes `signoff.md` with `signed-off-by:`,
  `signed-off-at:`, and `operator-gate: tty`.
- Decide compatibility explicitly in material: legacy explicit direction/sign-off forms
  may remain only as non-gated legacy/admin forms if they cannot satisfy the new
  operator-gate contract; they must not make a new frame signable when gated operator acts
  are required.
- Add frame validation for `options.md` when a new work node needs route selection:
  numbered options must be materially present, have a supported `kind`, carry summary,
  reversibility, and tradeoff fields, and include none/abort outcomes.
- Update `adapter/gates/orient.md`, `adapter/gates/frame.md`, `adapter/codex.md`,
  `hypercore.md`, and `check.sh` so the written adapter, prose material, and proof floor
  carry the new operator-gate contract.
- Update root helper scripts only as needed to dispatch to the new loop behavior.
- Delete `OPERATOR-ACTS-FINDINGS.md` before adoption because its findings are now carried
  by the signed frame and eventual history.

Implementation units for phase two:

1. Add the shared `/dev/tty` operator-gate primitive, add exact `operator-gate:` parsing,
   make non-interactive direction and sign-off attempts fail to satisfy new-work
   validation, and add focused `check.sh` coverage for `/dev/tty` refusal and marker
   validation.
2. Add and validate the neutral `options.md` contract, rework the primary direction helper
   to render numbered options and copy the selected option text into `direction.md`, and
   add checks for selection, none/abort handling, neutrality-relevant structure, and
   non-retrospective direction.
3. Rework the primary sign-off helper to render the frame-derived attestation brief,
   require the work number confirmation through `/dev/tty`, write `signed-off-at:` and
   `operator-gate: tty`, and add checks that old bare sign-off artifacts cannot satisfy
   new-work signability.
4. Align adapter prose, gate prompts, methodology prose, and proof checks with the new
   operator-act contract; remove `OPERATOR-ACTS-FINDINGS.md`; leave parent intent document
   amendments for the archive gate to fold and stamp from this signed frame.

## acceptance condition

Adopt the Route A operator-gate design only if the root helper workflow is materially
changed so future operator direction and sign-off artifacts are written by `/dev/tty`
gated helpers, the new contract is represented in current intent and adapter material, and
`./check.sh` is green.

## observable acceptance

`./check.sh` passes; direct probes show non-interactive commands cannot open `/dev/tty`;
the direction and sign-off helpers refuse when `/dev/tty` is unavailable; helper-written
`direction.md` and `signoff.md` include `operator-gate: tty`; sign-off renders a concise
frame-derived attestation brief before reading its confirm token; frame validation requires
neutral `options.md` for new work before direction selection.

## excluded interpretation

This work does not claim cryptographic non-repudiation, tamper-evidence, protection
against same-user manual file edits, external identity proof, or that this work's already
recorded `direction.md` and later sign-off were produced through the new gate before the
gate exists.

## proof state

Verified during orient in this Codex harness:

- `tty` on the normal command path returns `not a tty`.
- `: < /dev/tty` fails immediately with `/dev/tty: No such device or address`.
- Allocating the tool's PTY mode reports `/dev/console` for `tty`, but `: < /dev/tty`
  still fails immediately.

These probes support the liveness premise for Route A in the current harness. They do not
prove cryptographic authorship or artifact integrity.

Phase-one review produced no substantive independent reviewer signal: every base reviewer
subprocess exited `1` and was counted as `FLAG`. The review artifact disposition is
escalated. The remaining proof burden is therefore mechanical checks plus phase-two
implementation acceptance, not phase-one reviewer agreement.

## sweep

Mapped concepts:

- `hypercore.md` and `intent/collaboration.md` already name direction and sign-off as the
  two anchored operator acts and say the machine performs neither for itself.
- `intent/loop.md` and `intent/machine-statements/loop.md` currently specify explicit
  `loop.sh direct [<work-name> [<operator>]] --route|--constraint|--delegate <text-or->`
  and explicit `loop.sh signoff <work-name> <operator>` forms. These will need amendment.
- `intent/adapter.md`, `intent/machine-statements/adapter.md`, `adapter/codex.md`,
  `adapter/gates/frame.md`, and `adapter/loop.sh` carry the current Codex mechanics for
  direction, review, sign-off, frame validation, and root helpers.
- `check.sh` already checks strict frame parsing, direction/review helpers, sign-off
  behavior, and adapter prose. The proof floor must move with the new operator-gate
  contract.
- Adopted work `007-phase-one-collaboration` is directly related: it introduced direction
  before route, the one-way review command, optional reviewer non-override, and strict
  parsing to avoid retrospective direction.
- Adopted work `008-phase-two-acceptance` is related because it made one-way archive depend
  on independent implementation acceptance; this work must preserve that phase-two door
  guard.

Likely clash: the new terminal-only helper contract conflicts with the current explicit
argument forms in loop machine statements and adapter material. The route must either
retire those forms for new operator acts or preserve them only as non-gated legacy/admin
paths that cannot satisfy the new operator-gate contract.

## adoption claim

Adopt by folding accepted statements and material into the root methodology, stamping
`collaboration`, `loop`, and `adapter` with the signing operator, and recording
`009-operator-acts` as adopted history.

## shelving claim

Shelve if `/dev/tty` cannot serve as a reliable operator-only liveness channel in the
Codex phase-one harness, if the implementation cannot keep the operator action simple, if
neutral options make phase one too heavy, or if the route would need to claim
non-repudiation to satisfy the acceptance condition.
