# adapter -- machine statements

the current root harness adapter is materialized as `adapter/codex.md`.
the Codex harness loads its adapter through a root `AGENTS.md` symlinked to
`adapter/codex.md`; the root entry is the harness's mandated pointer, holding nothing, not
where the adapter lives.
a machine working in a nested node is bound by Codex including the root `AGENTS.md` in the
project instruction chain from the project root to the current directory, so no node below
the root carries its own adapter.
the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
over the Codex phase-two harness: `codex exec` opens a fresh thread at implement and
`codex exec resume` resumes it across check and archive; the path carries no phase-one
context.
`adapter/loop.sh` accepts a node-local work name in the addressed node, not a
slash-separated child path, for new work.
the root node is the default addressed node.
`loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node, including a
linked mounted child when `<node-path>` is its mount path.
`loop.sh start <work-name>` creates a work node directly under the addressed node.
`loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work
and act only on that addressed work.
`loop.sh execute <work-name>` records only the addressed node-local work in that node's
history.
the orchestrator no longer creates or relies on child change collections inside work or
legacy change folders.
legacy nested child-change archives may be read if present, but they are not the structure
for new work and are not required retained history.
the gate prompts use addressed-node and node-local work wording and point cleared sessions
at the addressed work frame.
the orient gate prompt requires the machine to name the addressed node, the node-local work
name, the target segments, the work in flight, and any open direction that needs an
operator decision before the frame settles a route.
the frame gate prompt requires a problem, constraints, and decision surface before
prescribing an open multi-task or multi-phase route; when operator direction is missing, it
tells the machine to stop at the decision surface and wait for sign-off or direction rather
than filling the gap.
the Codex adapter prose describes phase one as design-phase collaboration, while preserving
phase two as a cleared, heads-down execution from the written frame.
`check.sh` mechanically checks that the gate prompts and Codex adapter prose still carry
the design-phase collaboration language.
each gate's instructions are held in a file in `adapter/gates/`; the Codex path includes them in
the `codex exec` gate prompt; the orchestrator owns gate order and preconditions and
blocks a gate whose preconditions fail.
sign-off is a `signed-off-by` line in the work-node frame's `intent/frame/signoff.md`, or
in legacy `endorsement.md` for old signed frames; the orchestrator seals phase two until
sign-off is present, and the machine never writes it for itself.
at the check gate the orchestrator reads the sweep's verdict, and when the sweep flags the
corpus incoherent it halts phase two and surfaces the flag to the operator rather than
proceeding to archive.
