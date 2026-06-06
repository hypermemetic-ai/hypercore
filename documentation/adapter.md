# adapter

the adapter is the binding between a harness and the methodology: it promises the harness acts in agreement with the intent and the loop.
a harness begins each session memoryless, reaching the work only through what it loads; absent the adapter, agreement is left to chance.
the adapter points the harness at the intent and the loop — the single source of truth — and drives it through them; pointing alone is a request, agreement is enforced.
the adapter's specifics are a rigid workflow over the loop's gates: each gate's preconditions must hold before the next is allowed, and a gate whose preconditions fail blocks rather than warns.
the rigid workflow restates no rule: the gates and their order are the loop, already intent; the workflow operationalizes them, and where workflow and intent disagree, the intent wins.
the rigid workflow is interactive through orient, frame, and the operator's sign-off, then runs implement, check, and archive on a cleared session that re-derives the change from its written frame alone.
on request the adapter renders a statement of the intent intelligible in plain language without altering it.
the adapter carries only what the intent cannot yet reach the harness with — the order to read the intent first, and disciplines not yet written as statements; each is a debt, folded into the intent by a later change and then dropped.
an adapter is per harness; one node may be bound by more than one, each loaded by its own harness.
the adapter is materialized only at the methodology root, with the prose it routes to, and not in any nested node.
the adapter is not in the orient path; loading it is how orient begins, not part of the intent it routes to.
the sweep reads the adapter against the intent, so a rule it has come to restate, or a debt the intent has since absorbed, is caught as drift.

## machine
each harness's adapter is materialized in implementation/adapter/, the router prose in <harness>.md — implementation/adapter/claude-code.md for Claude Code.
the Claude Code harness loads its adapter through a root CLAUDE.md symlinked to implementation/adapter/claude-code.md; the root entry is the harness's mandated pointer, holding nothing, not where the adapter lives.
a machine working in a nested node is bound by Claude Code loading the root CLAUDE.md from the launch directory and its parents, so no node below the root carries its own adapter.
the rigid workflow is materialized as an orchestrator, implementation/adapter/loop.sh, realizing the two-phase shape over claude -p: phase one interactive; phase two one cleared claude -p session — a fresh session id opened by implement and resumed across check and archive — carrying no phase-one context.
each gate's instructions are a file in implementation/adapter/gates/, appended to the phase-two claude -p call as a system prompt; the orchestrator owns gate order and preconditions and blocks a gate whose preconditions fail.
sign-off is a signed-off-by line in the change's endorsement.md; the orchestrator seals phase two until it is present, and the machine never writes it for itself.
at the check gate the orchestrator reads the sweep's verdict, and when the sweep flags the corpus incoherent it halts phase two and surfaces the flag to the operator rather than proceeding to archive; the halt hands the graded flag to the operator to settle — it does not let the archive decision rest on the sweep.

---
endorsed by surlej
