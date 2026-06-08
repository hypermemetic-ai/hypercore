# adapter

the adapter is the binding between a harness and the methodology: it promises the harness
acts in agreement with the intent and the loop.
a harness begins each session memoryless, reaching the work only through what it loads;
absent the adapter, agreement is left to chance.
the adapter points the harness at the intent and the loop -- the single source of truth --
and drives it through them; pointing alone is a request, agreement is enforced.
the adapter's specifics are a rigid workflow over the loop's gates: each gate's
preconditions must hold before the next is allowed, and a gate whose preconditions fail
blocks rather than warns.
the rigid workflow restates no rule: the gates and their order are the loop, already
intent; the workflow operationalizes them, and where workflow and intent disagree, the
intent wins.
the rigid workflow is interactive through orient and frame as the design phase, and through
sign-off as the human gate: before a route is written, the machine surfaces understanding,
alternative framing, information-gain questions, reversibility, review where required, and
a decision surface for substantive operator direction; after sign-off, implement, check,
and archive run through cleared sessions that re-derive each unit and acceptance review
from the signed frame directory and lean phase-two handoff artifacts alone.
the phase-two orchestrator protects self-editing work by running execute from a snapshot
made at execute start; later edits to the live orchestrator material do not change the
already-running process.
phase two has a real supervisor-to-executor handoff: after sign-off, an outer supervisor
launches a fresh phase-two executor from the addressed node and supervises its recorded
progress, intervening only when the loop blocks on a real gate failure or operator need.
`start` creates a new work node for phase one; `execute` enters phase two for signed work,
and omitting the execute work name is only an inference convenience that succeeds when
exactly one signed, unarchived work node exists in the addressed node and blocks otherwise.
the implement and archive gate contracts live in re-read gate files, not in frozen inline
orchestrator strings; `adapter/loop.sh` supplies only dynamic unit or work context and the
archive decision line.
direction and review are phase-one acts or artifacts, not loop gates.
the review roster for one-way phase-one work has a base roster of
`contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`.
the implementation-acceptance reviewer for each phase-two unit is independent and read-only.
the tier-two implementation-acceptance panel for one-way work has required lenses
`whole-acceptance-conformance`, `proof-integrity`, `independent-coherence`,
`security-permissions`, and `red-team`.
the complete optional review roster is `implementation-maintainability`,
`security-permissions`, `operator-ergonomics`, `migration-compatibility`,
`domain-evidence`, and `performance-cost`.
optional reviewers are advisory additions and cannot override, outvote, average away, or
dilute unresolved base-roster or red-team flags.
the adapter classifies the request surface before changing material: ordinary
conversation and read-only inspection may proceed directly, while governed work starts or
continues a work node.
the adapter rejects perceived simplicity, file count, convenience, and low risk as waivers
for governed work.
on request the adapter renders a statement of the intent intelligible in plain language
without altering it.
the adapter carries only what the intent cannot yet reach the harness with -- the order to
read the intent first, and disciplines not yet written as statements; each is a debt,
folded into the intent by later work and then dropped.
an adapter is per harness; one node may be bound by more than one, each loaded by its own
harness.
an adapter binds a harness to a phase; phase one and phase two may bind different harnesses,
and the current materialization binds one harness to both phases.
the phase-one collaborator role defaults to the interactive harness that loaded the
adapter; no orchestrator routing knob is required until a materialization routes that role.
the adapter material is materialized only at the methodology root, with the prose it routes
to, and not in any nested node; a mounted external project may carry a target-local entry
point that links to root-managed adapter material and routes direct-path work back to the
root adapter and loop.
the adapter is not in the orient path; loading it is how orient begins, not part of the
intent it routes to.
the sweep reads the adapter against the intent, so a rule it has come to restate, or a debt
the intent has since absorbed, is caught as drift.

## machine
the current root harness adapter is materialized as `adapter/codex.md`.
the current materialization binds the same harness to phase one and phase two; the
phase-one collaborator is the interactive harness that loaded the adapter.
the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;
the root entry is the harness's mandated pointer, holding nothing, not where the adapter
lives.
a machine working in a nested node under the root is bound by the root `AGENTS.md` in the
project instruction chain from the project root to the current directory, so no node below
the root carries its own adapter material.
a mounted external project may carry a target-local `AGENTS.md` entry point for
direct-path openings; the entry point links to root-managed adapter material and routes
back to the root adapter and loop instead of copying root adapter material into the
mounted node.
the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
over the phase-two executor harness: each implementation unit opens a fresh builder
session from the signed frame, and acceptance reviewers and the archive actor are fresh
sessions rather than resumes of the builder.
`adapter/loop.sh` snapshots and re-execs itself at the start of `execute`, using the
original root adapter paths for gate files and the snapshot path for the running loop
version digest.
the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
`.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
final outputs, acceptance artifact paths, and current pointers for the addressed work and
root.
the loop streams inner executor JSON events into the phase-two run state while
printing concise progress, without changing the cleared-session contract.
the loop materializes separate builder and reviewer routing, structured acceptance
artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
one-way tier-two panel, and phase-one review subprocess crash diagnostics.
the materialized execute cache is non-fatal: a cache-record failure is logged as a soft
miss and affects only future resumability, not phase-two correctness or whether execute
continues.
`adapter/loop.sh` accepts one node-local work name in the addressed node for new work.
the root node is the default addressed node.
`loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node, including a
linked mounted child when `<node-path>` is its mount path.
`loop.sh start <work-name>` creates a work node directly under the addressed node.
`loop.sh execute` without `<work-name>` resolves the single signed, unarchived work node in
the addressed node and blocks when there are zero or more than one.
`loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work
and act only on that addressed work.
`loop.sh execute <work-name>` records only the addressed node-local work in that node's
history.
the orchestrator creates, signs, executes, and records only addressed node-local work
nodes.
the gate prompts use addressed-node and node-local work wording and point cleared sessions
at the addressed work frame.
the implement and archive gate prompts carry their contract in `adapter/gates/implement.md`
and `adapter/gates/archive.md`; `run_gate` reads those files for each invocation, so a
self-change to a gate prompt can affect the next gate invocation in the same execute run.
the orient gate prompt requires the machine to classify the request surface, name the
addressed node, node-local work name, target segments, work in flight, teach-back,
alternative framing, information-gain questions, reversibility classification, and any
open direction that needs an operator decision before the frame settles a route.
the orient gate prompt tells the machine not to write a route or operator direction.
the frame gate prompt requires addressed node, node-local work name, target segments, work
in flight, problem, constraints, decision surface or open direction, reversibility, route,
acceptance condition, observable acceptance, excluded interpretation, proof state, sweep,
and adoption or shelving claim in `intent/frame/frame.md`.
the frame gate prompt requires substantive `intent/frame/direction.md` before route
framing and requires `intent/frame/review.md` for one-way work.
the frame gate prompt tells the machine not to write operator direction, not to collect
direction retrospectively, and not to let optional reviewer verdicts clear base-roster or
red-team flags.
the adapter prose describes phase one as design-phase collaboration with direction
and review artifacts, while preserving phase two as cleared, heads-down execution from the
signed frame directory and lean phase-two handoff artifacts.
`check.sh` mechanically checks that the gate prompts, adapter prose, loop frame
validation, start scaffolding, direction/review helpers, operator-act gating through
`/dev/tty` with B-ready `operator-gate:` markers and numbered-option direction, review and
acceptance isolation settings, strict frame parsing, phase-two acceptance gating, structured
acceptance legibility, acceptance source markers and fake-source rejection, separate
builder/reviewer routing with bounded retry and strong escalation, resumable execute
caching including non-fatal cache-record soft misses, the concurrent tier-two panel, the
re-read implement/archive prompt contract and
absence of frozen inline implement/archive contract text, the new operator-act and
phase-two performance contract in the `collaboration`, `loop`, and `adapter` segments, and
current-material absence of the retired compatibility route still carry the contract.
each gate's instructions are held in a file in `adapter/gates/`; the harness path includes
them in the executor gate prompt; the orchestrator owns gate order and preconditions and
blocks a gate whose preconditions fail.
sign-off for new work records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty`
in the work-node frame's `intent/frame/signoff.md`; the orchestrator seals phase two until
sign-off is present, and the machine never writes it for itself.
the root `./direction` and `./signoff` helpers are terminal-gated operator-act helpers for
new work: direction selects a numbered option from `intent/frame/options.md` through
`/dev/tty`, and sign-off renders a frame-derived brief and reads the work number through
`/dev/tty`, each writing `operator-gate: tty`; the explicit argument forms are admin forms
that cannot record gated operator acts for new work.
`operator-gate: tty` records that the legitimate helper path crossed the current harness's
terminal-liveness check, which the default machine command path lacks; it does not prove
network isolation, cryptographic non-repudiation, tamper-evidence, file integrity, or that
an operator rather than a deliberately allocated terminal answered.
at the check gate the orchestrator records tier-one implementation acceptance for each
unit, records the concurrent one-way tier-two panel when required, and halts phase two
before archive when required acceptance flags remain unresolved.

---
endorsed by qqp-dev
