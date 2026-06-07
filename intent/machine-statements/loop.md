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
from the root, `./direction` invokes `loop.sh direct` and preserves explicit arguments.
`loop.sh direct [<work-name> [<operator>]] --route|--constraint|--delegate <text-or->`
records substantive operator direction in `intent/frame/direction.md`; `-` reads the
direction text from stdin.
`loop.sh direct` rejects empty or placeholder direction, multiple direction forms, an
existing valid direction artifact, a malformed existing direction artifact, and direction
after route content is already present.
`direction.md` contains `direction-by:`, `direction-given-at:`, and exactly one
non-placeholder `selected-route:`, `constraint:`, or `delegation:`.
from the root, `./review` invokes `loop.sh review` and preserves explicit arguments.
`loop.sh review <work-name> [--add <role>]...` seats the base review roster and any valid
optional complete-roster roles, then writes `intent/frame/review.md`.
new work frame completeness is checked from the canonical `intent/frame/frame.md` only;
`direction.md`, `review.md`, and `signoff.md` do not satisfy ordinary frame fields.
new work frame completeness requires these recoverable fields: addressed node,
node-local work name, target segments, work in flight, problem, constraints, decision
surface or open direction, reversibility, route, acceptance condition, proof state, sweep,
and adoption or shelving claim.
`reversibility:` is parsed as exactly `one-way` or `two-way`.
`loop.sh start <work-name>` scaffolds `intent/frame/frame.md` with the lean fields.
`loop.sh frame` and `loop.sh signoff` block new work whose frame is incomplete, whose
direction is absent or malformed, whose direction appears retrospective, or whose one-way
frame lacks a review artifact.
one-way review artifacts record base-role verdicts, unresolved flags, and disposition;
optional reviewer verdicts cannot clear unresolved base-roster or red-team flags.
new work sign-off is a `signed-off-by` line in the work node's `intent/frame/signoff.md`.
`loop.sh execute <work-name>` records the addressed work in node-local history after archive.
