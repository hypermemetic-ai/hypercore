# frame - 005-harden-loop-collaboration

## work

Harden the Codex loop so methodology adherence is not waived by machine judgment, make
operator-machine communication a checked work artifact rather than transient chat, and
remove the old change-folder compatibility path from current corpus semantics.

Addressed node: root (`.`).

Node-local work name: `005-harden-loop-collaboration`.

Target segments: `collaboration`, `loop`, `adapter`, `sweep`, `active-work`,
`structure`, and `endorsement`.

Work in flight: this work node only. No other active work node was found under the root
or `home`. The related adopted records are:

- `002-direct-path-greenfield-adapter`, which fixed direct-path openings by routing them
  back to root governance.
- `003-phase-two-observability`, which made phase-two run state recoverable.
- `004-root-managed-greenfield-entrypoints`, which moved mounted-node direct-path
  process material back under root management.

Operator direction added after the first frame draft: remove references to the old
change-folder semantics from this work and from current corpus material while doing this
work.

Open direction needing operator input: choose the enforcement shape below. If the
operator signs off this frame without revision, sign-off selects Route B, the minimal
checked frame contract, plus the compatibility removal.

## problem

Three current behaviors are too dependent on the machine's willingness to obey prose.

First, a machine can rationalize that a request is "simple enough" and skip the loop. The
current adapter says the loop is rigid, but it does not force a first-step classification
between ordinary conversation and governed work. The current frame precondition is also
weak: for new work nodes, any non-empty file under `intent/frame/` is enough for the loop
to consider the frame complete.

Second, collaboration is named as first-class intent, but the durable material is still
thin. Phase two records run state, and frame prompts ask for several collaboration facts,
but the loop does not require a recoverable communication record before sign-off. Common
ground can remain scattered across chat: what the operator decided, what the machine is
assuming, what evidence was checked, what uncertainty remains, and what feedback should
become intent, proof, machine statements, or debt.

Third, the current corpus still carries compatibility text and code for the retired
change-folder path. That path no longer exists in current material, but its presence in
the adapter, loop, checks, and intent gives the machine another alternate route to
rationalize against.

## constraints

- Keep the five-gate loop. Do not add a new gate unless the operator explicitly chooses
  that larger route.
- Preserve the sign-off boundary: the machine never signs off, and phase two still
  re-derives from the written frame alone.
- Preserve fastness. A direct answer, explanation, or read-only inspection that does not
  need adoption or shelving should not become a work node by ceremony.
- Do not allow simplicity, file count, perceived risk, convenience, or obsolete
  compatibility paths to waive the loop when work changes governed material or needs
  adoption or shelving.
- Keep frame validation small and mechanical. The proof can require named communication
  fields; the sweep still judges semantic quality.
- Preserve the active-work statement that frame content is recoverable under
  `intent/frame/` without restoring the retired compatibility shape.
- Do not rewrite adopted history records in this work unless the operator explicitly
  makes historical rewriting part of the signed frame. History remains the record of why
  earlier statements changed, not current corpus semantics.

## decision surface

Route A: instruction hardening only.

Update `adapter/codex.md`, the gate prompts, and checks so they explicitly reject
"simple enough" as a loop waiver and describe first-class communication more strongly.
This is low-friction, but it leaves the original failure mode mostly intact because the
machine can still skip or underfill the frame.

Route B: minimal checked frame contract. Recommended.

Keep the five-gate loop and add a small mechanical contract for new work frames. The
adapter classifies requests up front: ordinary conversation can proceed directly, but
governed work must start or continue a work node, and simplicity is never a waiver. The
loop accepts a new work frame only when the frame directory contains recoverable fields
for addressed node, node-local work name, target segments, work in flight, problem,
constraints, decision surface or open direction, route, proof state, sweep, and adoption
or shelving claim. `loop.sh start` can scaffold `intent/frame/frame.md`, but validation
should scan the frame directory rather than make the filename itself the rule.

This route makes communication first-class by requiring the common ground needed for
sign-off to be written before sign-off: operator decisions, machine assumptions,
evidence, uncertainty, open blockers, proof state, and handoff state. It is still small
enough to keep work fast.

Route C: full collaboration ledger.

Add a distinct collaboration artifact or event log for every work node, with loop status
support and possibly current pointers similar to phase-two run state. This would make
communication highly visible, but it is likely too much mechanism before Route B proves
what the durable shape must be.

All routes now include removal of the retired change-folder compatibility path from
current intent, adapter material, loop implementation, checks, and user-facing prose.

## proposed route

Adopt Route B unless the operator redirects.

Parent intent amendments:

- `collaboration`: state that first-class collaboration is materialized in work frames as
  recoverable common ground, including operator decisions, authority, assumptions,
  uncertainty, evidence, proof state, feedback capture, and handoff state.
- `loop`: state that governed work is not optional by perceived simplicity; before
  sign-off, a new work frame must carry the minimum recoverable communication and
  compliance fields needed for a cleared phase-two session.
- `adapter`: state that the Codex adapter must classify the request surface before
  changing material, route governed work into the loop, and reject "simple enough" as a
  waiver.
- `sweep`: state that the sweep reads the frame's common-ground record as part of the
  corpus relation, not just proposed parent amendments.
- `active-work`, `structure`, and `endorsement`: remove current statements that preserve
  the retired change-folder path as a readable or signable route.

Material amendments:

- Update `adapter/codex.md` so the first decision is whether the request is ordinary
  conversation/read-only inspection or governed work. Governed work starts or continues a
  work node; the machine must not bypass the loop because the work appears small.
- Update `adapter/gates/orient.md` so orient reports the work classification and the
  durable common-ground state needed before frame, and no longer asks for old change
  records.
- Update `adapter/gates/frame.md` so frame requires a written common-ground record and a
  methodology adherence record before sign-off.
- Update `adapter/gates/implement.md` and `adapter/gates/archive.md` so phase two reads
  and signs only current work-node frames.
- Update `adapter/loop.sh` so `start` scaffolds a minimal frame template and `frame` /
  `signoff` block new work frames that do not contain the required recoverable fields.
- Remove the old change-folder branches from `adapter/loop.sh`: old frame filenames,
  old active/archive resolution, old sign-off file handling, old history destination, and
  old source descriptions.
- Update `check.sh` so the material contract is mechanically checked without invoking
  live Codex: adapter intake language, gate prompt requirements, loop frame-validation
  functions, start scaffolding, and absence of the retired compatibility branch in
  current material.
- Update `README.md` and any other current user-facing prose that still names the retired
  compatibility path.

## proof state

Baseline observations:

- `intent/collaboration.md` already says collaboration is first-class and keeps common
  ground written.
- `intent/adapter.md` already says the adapter operationalizes a rigid workflow and
  blocks failed preconditions.
- `adapter/codex.md` already says the loop is unskippable, but it does not require an
  up-front governed-work classification or explicitly reject "simple enough" reasoning.
- `adapter/gates/orient.md` asks the machine to report addressed node, work name, target
  segments, work in flight, and open direction.
- `adapter/gates/frame.md` asks for problem, constraints, and decision surface for open
  routes.
- `adapter/loop.sh` currently treats any non-empty non-signoff file under a new
  `intent/frame/` directory as frame-complete.
- Current material has no `intent/changes` or `intent/history/change-folders`
  directories, so removing that compatibility path does not orphan active work or
  retained current history collections.

Required proof after implementation:

- `./check.sh` exits zero.
- A newly started work node receives a scaffolded frame template.
- `loop.sh frame <work-name>` rejects a new work frame when required common-ground fields
  are absent.
- The required frame fields are not tied to the retired change-folder path.
- The adapter prose and gate prompts plainly reject bypassing the loop because work is
  small or simple.
- Current intent, machine statements, adapter material, loop implementation, checks, and
  current user-facing prose no longer preserve the retired change-folder path.
- The sweep finds no contradiction with the active-work statement that frame content is
  recoverable under `intent/frame/`.

## sweep

Map:

- `hypercore.md` says the operator and machine keep common ground written, and that every
  work node needing adoption or shelving goes through orient, frame, implement, check,
  and archive.
- `intent/collaboration.md` already states the desired communication properties, but only
  one machine statement is settled: phase-two handoff state files.
- `intent/loop.md` states orient and frame are the design phase, and that open direction
  must surface problem, constraints, and decision surface before route settlement.
- `intent/adapter.md` states the rigid workflow blocks failed preconditions and that
  pointing alone is weaker than enforced agreement.
- `intent/structure.md`, `intent/active-work.md`, and `intent/endorsement.md` still name
  the retired change-folder path as readable or signable compatibility.
- `adapter/codex.md` tells Codex to read intent and use the loop, but its first-step
  behavior still depends on the machine treating the request as loop-worthy.
- `adapter/loop.sh` can currently sign off any new work frame with any non-empty
  non-signoff file under `intent/frame/` and still carries branches for the retired
  compatibility path.
- `check.sh` still checks readability for the retired compatibility path even though the
  current corpus no longer contains that path.

Read:

- Route A is coherent with current statements, but it does not materially close the
  rationalization gap.
- Route B is coherent if the required fields are described as a frame completeness
  contract under `intent/frame/`, not as a restored retired path.
- Route B strengthens existing collaboration intent by making common ground recoverable
  before sign-off, and it strengthens adapter intent by turning frame completeness into a
  real precondition.
- Removing the retired compatibility branch is coherent because no current directories
  depend on it, current work nodes now live directly under addressed nodes, and retained
  adopted history remains history rather than a current route.
- Route C is coherent but may violate fastness unless smaller checked frames first prove
  insufficient.

Sweep verdict for frame: coherent if adoption keeps the loop at five gates, validates
frame content without restoring the retired compatibility path, treats ordinary
conversation as outside governed work, forbids simplicity-based loop bypass for governed
work, and leaves adopted history as history unless separately authorized.

## open questions

Does the operator accept Route B as the implementation route, with current compatibility
references removed and adopted history left intact, or should this work be reframed
toward instruction-only hardening, a fuller collaboration ledger, or historical record
rewriting too?

## adoption claim

Adopt this work if governed work can no longer be framed or signed off without a written
common-ground record, the adapter rejects simplicity-based loop bypass, the loop validates
new frames mechanically, the retired compatibility branch is gone from current corpus
semantics, and `./check.sh` proves the material contract.

Shelve this work if the operator decides that checked frame completeness is too much
mechanism for the methodology's fastness property.
