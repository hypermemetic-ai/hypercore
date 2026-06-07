# adapter -- machine statements

the current root harness adapter is materialized as `adapter/codex.md`.
the Codex harness loads its adapter through a root `AGENTS.md` symlinked to
`adapter/codex.md`; the root entry is the harness's mandated pointer, holding nothing, not
where the adapter lives.
a machine working in a nested node under the root is bound by Codex including the root
`AGENTS.md` in the project instruction chain from the project root to the current
directory, so no node below the root carries its own adapter material.
a mounted external project may carry a target-local `AGENTS.md` entry point for
direct-path openings; the entry point links to root-managed adapter material and routes
back to the root adapter and loop instead of copying root adapter material into the
mounted node.
the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
over the Codex phase-two harness: `codex exec` opens a fresh thread at implement and
`codex exec resume` resumes it across check and archive; the path carries no phase-one
context.
the Codex loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
`.hypercore/loop-runs`, with run-local state, event history, raw Codex gate streams, gate
final outputs, and current pointers for the addressed work and root.
the Codex loop streams inner `codex exec --json` events into the phase-two run state while
printing concise progress, without changing the cleared-session contract: implement opens
one fresh thread and check and archive resume it.
`adapter/loop.sh` accepts one node-local work name in the addressed node for new work.
the root node is the default addressed node.
`loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node, including a
linked mounted child when `<node-path>` is its mount path.
`loop.sh start <work-name>` creates a work node directly under the addressed node.
`loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work
and act only on that addressed work.
`loop.sh execute <work-name>` records only the addressed node-local work in that node's
history.
the orchestrator creates, signs, executes, and records only addressed node-local work
nodes.
the gate prompts use addressed-node and node-local work wording and point cleared sessions
at the addressed work frame.
the orient gate prompt requires the machine to classify the request surface, name the
addressed node, node-local work name, target segments, work in flight, durable
common-ground state, and any open direction that needs an operator decision before the
frame settles a route.
the frame gate prompt requires addressed node, node-local work name, target segments, work
in flight, problem, constraints, decision surface or open direction, route, methodology
adherence, proof state, sweep, adoption or shelving claim, and written common ground before
sign-off.
the frame gate prompt requires pre-sign-off operator deliberation before settling a route:
problem/domain map, evidence standard, evidence basis, options and tradeoffs, operator
expectation, rejection conditions, and unresolved discomfort or open judgement.
the frame gate prompt states that evidence depth is problem-relative and rejects
superficial research when good literature is unavailable or irrelevant.
the frame gate prompt requires a problem, constraints, and decision surface before
prescribing an open multi-task or multi-phase route; when operator direction is missing, it
tells the machine to stop at the decision surface and wait for sign-off or direction rather
than filling the gap.
the Codex adapter prose describes phase one as design-phase collaboration, while preserving
phase two as a cleared, heads-down execution from the written frame.
`check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
validation, start scaffolding, current intent, and current-material absence of the retired
compatibility route still carry the contract.
each gate's instructions are held in a file in `adapter/gates/`; the Codex path includes them in
the `codex exec` gate prompt; the orchestrator owns gate order and preconditions and
blocks a gate whose preconditions fail.
sign-off is a `signed-off-by` line in the work-node frame's `intent/frame/signoff.md`; the
orchestrator seals phase two until sign-off is present, and the machine never writes it for
itself.
at the check gate the orchestrator reads the sweep's verdict, and when the sweep flags the
corpus incoherent it halts phase two and surfaces the flag to the operator rather than
proceeding to archive.
