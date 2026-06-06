# adapter — machine statements

each harness's adapter is materialized in implementation/adapter/, the router prose in <harness>.md — implementation/adapter/claude-code.md for Claude Code.
the Claude Code harness loads its adapter through a root CLAUDE.md symlinked to implementation/adapter/claude-code.md; the root entry is the harness's mandated pointer, holding nothing, not where the adapter lives.
a machine working in a nested node is bound by Claude Code loading the root CLAUDE.md from the launch directory and its parents, so no node below the root carries its own adapter.
the rigid workflow is materialized as an orchestrator, implementation/adapter/loop.sh, realizing the two-phase shape over claude -p: phase one interactive; phase two one cleared claude -p session — a fresh session id opened by implement and resumed across check and archive — carrying no phase-one context.
each gate's instructions are a file in implementation/adapter/gates/, appended to the phase-two claude -p call as a system prompt; the orchestrator owns gate order and preconditions and blocks a gate whose preconditions fail.
sign-off is a signed-off-by line in the change's endorsement.md; the orchestrator seals phase two until it is present, and the machine never writes it for itself.
at the check gate the orchestrator reads the sweep's verdict, and when the sweep flags the corpus incoherent it halts phase two and surfaces the flag to the operator rather than proceeding to archive; the halt hands the graded flag to the operator to settle — it does not let the archive decision rest on the sweep.
