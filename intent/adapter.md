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
sign-off as the human gate: before the machine settles open direction it surfaces the
problem, constraints, and decision surface for operator direction; after sign-off,
implement, check, and archive run on a cleared session that re-derives the work from its
written frame alone.
on request the adapter renders a statement of the intent intelligible in plain language
without altering it.
the adapter carries only what the intent cannot yet reach the harness with -- the order to
read the intent first, and disciplines not yet written as statements; each is a debt,
folded into the intent by later work and then dropped.
an adapter is per harness; one node may be bound by more than one, each loaded by its own
harness.
the adapter is materialized only at the methodology root, with the prose it routes to, and
not in any nested node.
the adapter is not in the orient path; loading it is how orient begins, not part of the
intent it routes to.
the sweep reads the adapter against the intent, so a rule it has come to restate, or a debt
the intent has since absorbed, is caught as drift.

## machine
each harness's adapter is materialized in `material/adapter/`, the router prose in
`<harness>.md` -- `material/adapter/claude-code.md` for Claude Code and
`material/adapter/codex.md` for Codex.
the Claude Code harness loads its adapter through a root `CLAUDE.md` symlinked to
`material/adapter/claude-code.md`; the root entry is the harness's mandated pointer,
holding nothing, not where the adapter lives.
the Codex harness loads its adapter through a root `AGENTS.md` symlinked to
`material/adapter/codex.md`; the root entry is the harness's mandated pointer, holding
nothing, not where the adapter lives.
a machine working in a nested node is bound by Claude Code loading the root `CLAUDE.md`
from the launch directory and its parents, and by Codex including the root `AGENTS.md` in
the project instruction chain from the project root to the current directory, so no node
below the root carries its own adapter.
the rigid workflow is materialized as `material/adapter/loop.sh`, realizing the two-phase
shape over the selected phase-two harness: Claude Code uses `claude -p` with a fresh
session id opened by implement and resumed across check and archive; Codex uses
`codex exec` to open a fresh thread and `codex exec resume` across check and archive;
either path carries no phase-one context.
`material/adapter/loop.sh` accepts a node-local work name in the addressed node, not a
slash-separated child path, for new work.
the root node is the default addressed node.
`loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node.
`loop.sh start <work-name>` creates a work node directly under the addressed node's
`material/`.
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
the Codex and Claude Code adapter prose describe phase one as design-phase collaboration,
while preserving phase two as a cleared, heads-down execution from the written frame.
`material/check.sh` mechanically checks that the gate prompts and harness adapter prose
still carry the design-phase collaboration language.
each gate's instructions are a file in `material/adapter/gates/`; the Claude Code path
appends them to `claude -p` as a system prompt, and the Codex path includes them in the
`codex exec` gate prompt; the orchestrator owns gate order and preconditions and blocks a
gate whose preconditions fail.
sign-off is a `signed-off-by` line in the work-node frame's `intent/frame/signoff.md`, or
in legacy `endorsement.md` for old signed frames; the orchestrator seals phase two until
sign-off is present, and the machine never writes it for itself.
at the check gate the orchestrator reads the sweep's verdict, and when the sweep flags the
corpus incoherent it halts phase two and surfaces the flag to the operator rather than
proceeding to archive.

---
endorsed by qqp-dev
