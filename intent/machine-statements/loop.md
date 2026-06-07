# loop -- machine statements

a work address names the addressed node and one node-local work name in that node.
when no node is named, the root node is assumed.
`loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node.
`loop.sh start <work-name>` creates a work node directly under the addressed node's
corpus.
`loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work and
act only on that addressed work.
`loop.sh execute <work-name>` exposes phase-two run state for the addressed work while it
runs and after recent failure or completion, including the active gate, status, Codex
thread id, latest message, event history, and run artifact paths.
before launching the first phase-two Codex gate, `loop.sh execute <work-name>` checks that
the Codex binary is present and that Codex home/session state is writable; a failed
preflight records failed run state and stops before `codex exec`.
`loop.sh status <work-name>` reports the addressed work's current phase and, when phase-two
state exists, the current or recent run's gate, status, state path, event path, and latest
message; `loop.sh status --json <work-name>` renders the same run state for tooling.
from the root, `./signoff` invokes the root loop sign-off gate and preserves any explicit
arguments it receives.
`loop.sh signoff <work-name> <operator>` remains the explicit sign-off form.
`loop.sh signoff` infers the work name only when exactly one frame-complete unsigned work
node exists in the addressed node; otherwise it blocks and asks for `<work-name>`.
`loop.sh signoff` infers the operator from `HYPERCORE_OPERATOR` when set, otherwise from
the addressed node's current intent foot endorsements when exactly one operator is present;
otherwise it blocks and asks for `<operator>`.
new work sign-off is a `signed-off-by` line in the work node's `intent/frame/signoff.md`.
legacy signed frames under `intent/changes/<work-name>/` use their existing
`endorsement.md` sign-off line.
`loop.sh execute <work-name>` records the addressed work in node-local history after archive.
legacy nested child-change archives may be read if present, but the orchestrator does not
scaffold them for new work.
