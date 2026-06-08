# adapter -- machine statements

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
the current handoff path is that an outer supervisor launches a fresh phase-two executor
from the addressed node and supervises the loop's recorded progress, intervening only when
the loop blocks on a real gate failure or operator need.
the loop materializes separate builder and reviewer routing, structured acceptance
artifacts with source markers and fake-source rejection, the per-unit non-decomposable
signal and direct strong-builder route, the per-unit fast-builder retry then
strong-builder escalation ladder, the shipped two-step builder default where the default builder is the cheap fast model behind the plan step and plan-match check, on-disk resumable execute that skips a unit already carrying a clean plan-match and tier-one PASS for the signed frame, the
concurrent one-way tier-two panel, and phase-one review subprocess crash diagnostics.
the loop materializes a per-unit planner route and writes readable plan artifacts before
builder sessions while keeping the plan as read-only build scaffolding.
the loop materializes exactly one normalized `non-decomposable: true` or
`non-decomposable: false` signal in each plan artifact before plan-match or build can
proceed.
the loop materializes a dedicated independent strong read-only plan-faithfulness review after
each per-unit plan, writes plan-match artifacts before builder sessions, and blocks a unit
whose plan-match artifact is missing, malformed, or not `PASS`.
the loop routes a confirmed `non-decomposable: true` unit directly to the strong builder
and leaves `non-decomposable: false` units on the fast-builder retry and reactive
strong-builder escalation ladder.
the loop keeps the contract-bearing implement and archive prompt text in
`adapter/gates/implement.md` and `adapter/gates/archive.md`, while inline execute prompts
carry only dynamic unit or work context and the archive decision line.
`adapter/loop.sh` accepts one node-local work name in the addressed node for new work.
the root node is the default addressed node.
`loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node, including a
linked mounted child when `<node-path>` is its mount path.
`loop.sh start <work-name>` creates a work node directly under the addressed node.
`loop.sh execute` without `<work-name>` resolves the single signed, unarchived work node in
the addressed node and blocks when there are zero or more than one.
`start` is the new-work phase-one entry point, while `execute` is the signed-work phase-two
entry point.
`loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work
and act only on that addressed work.
`loop.sh execute <work-name>` records only the addressed node-local work in that node's
history.
`loop.sh execute <work-name>` writes each unit's readable plan artifact under
`phase-two/plans/` before it starts that unit's builder session.
`loop.sh execute <work-name>` writes each unit's plan-match artifact under
`phase-two/plan-match/` and blocks before the builder session unless that artifact records
a clean `PASS`.
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
builder/reviewer routing with bounded retry, the short-but-judgeable frame altitude,
direct strong routing for confirmed
non-decomposable units, and strong escalation, the per-unit planner route with readable
plan artifacts before build artifacts, on-disk resumable execute that skips units already
carrying a clean plan-match and tier-one PASS, the concurrent tier-two panel, the re-read
implement/archive prompt contract and
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
