# loop

every work node that needs adoption or shelving goes through five gates: orient, frame,
implement, check, archive.
governed work is not optional by perceived simplicity, file count, risk, or convenience
when it changes governed material or needs adoption or shelving.
orient and frame are the design phase: understanding, scrutiny, operator direction, route
framing, and sign-off happen there before phase two begins.
direction and review are phase-one acts or artifacts inside orient and frame, not new loop
gates.
when a work node's direction is still open, the machine states the problem, constraints,
decision surface, reversibility, and information needed from the operator before settling
the route.
before a route is written, governed work has substantive operator direction recorded in
`intent/frame/direction.md`.
one-way work has `intent/frame/review.md` before route framing and sign-off; two-way work
skips review unless the operator requests it.
before sign-off, a new work frame carries lean recoverability fields: addressed node,
node-local work name, target segments, work in flight, problem, constraints, decision
surface or open direction, reversibility, route, acceptance condition, proof state, sweep,
and adoption or shelving claim.
implementation autonomy begins after sign-off: phase two builds from the signed frame, and
stops only when the frame is incomplete, a check fails, or the sweep flags incoherence.
orient: read the intent documents, the work in flight across the node tree, and the
material's conventions; search the web for what you do not know; ask the operator what the
artifacts cannot tell you; do not guess.
frame: write enough of the addressed work node's intent and material to make the proposed
work scrutable, including proposed parent amendments where the work needs them, and run the
sweep over the whole corpus and work in flight across the node tree.
implement: build in small units from the signed frame.
check: prove each statement with a check on the material, and run the sweep for coherence,
idiom, and security.
the checks re-run for every statement, not only the ones a work node touched.
drift is a check that falls without work meaning to break it, and it surfaces wherever it
happens.
archive: adopt or shelve the work according to the signed frame.
adoption folds accepted child statements and material into the parent, stamps each touched
segment's foot with this operator, and records the work node as adopted history.
shelving records the work node as shelved history without changing parent truth.
large work breaks into related work at frame, and related work is an ordinary work node in
the node it alters.
a coordinating work node remains responsible for its plan: before it adopts or shelves,
related unfinished work is either resolved in its own node or carried as explicit debt.
two work nodes touching the same intent document is a smell, caused by concurrency or
orthogonality.
concurrent work is sequenced by the loop's gates: first to adopt wins, and later work builds
on the in-flight or adopted material it reads across the node tree.
an orthogonal collision is fixed in the taxonomy, preferring more documents over more
mechanism.

## machine
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

---
endorsed by qqp-dev
