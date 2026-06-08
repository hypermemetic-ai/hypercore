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
new work that needs route selection carries `intent/frame/options.md` with neutral,
materially distinct numbered options, and the operator's direction is one option selected
through `/dev/tty` and recorded with `operator-gate: tty`.
direction and sign-off for new work are terminal-gated operator acts; the `operator-gate:`
token is `tty` today and the field stays open to a later keyed scheme such as `hmac:<...>`.
one-way work has `intent/frame/review.md` before route framing and sign-off; two-way work
skips review unless the operator requests it.
before sign-off, a new work frame carries lean recoverability fields: addressed node,
node-local work name, target segments, work in flight, problem, constraints, decision
surface or open direction, reversibility, route, acceptance condition, observable
acceptance, excluded interpretation, proof state, sweep, and adoption or shelving claim.
`observable acceptance` names the concrete command, state, check, or externally inspectable
condition that phase-two acceptance can test.
`excluded interpretation` names what the work must not mean.
implementation autonomy begins after sign-off: phase two builds from the signed frame in
green proof-advancing units, and stops when the frame is incomplete, a check fails, or
required implementation acceptance returns `FLAG`.
orient: read the intent documents, the work in flight across the node tree, and the
material's conventions; search the web for what you do not know; ask the operator what the
artifacts cannot tell you; do not guess.
frame: write enough of the addressed work node's intent and material to make the proposed
work scrutable, including proposed parent amendments where the work needs them, and run the
sweep over the whole corpus and work in flight across the node tree.
implement: build in proof-advancing units from the signed frame.
an implementation unit is the smallest proof-advancing delta that leaves `./check.sh`
green; units are vertical slices, so statements, material, and checks land together when
the work requires all three.
check: prove each statement with checks on the material, and run the phase-two acceptance
scrutiny required by the signed frame and reversibility.
`./check.sh` is green at every phase-two unit boundary and before any acceptance verdict
or archive fold is trusted.
after each implementation unit, a fresh independent read-only implementation-acceptance
reviewer reads the signed frame, unit proof obligation, unit diff, and lean unit handoff,
then returns a structured verdict: exactly one `PASS` or `FLAG` with required rationale and
concrete evidence.
for one-way work, a required tier-two implementation-acceptance panel runs before archive,
its lenses started concurrently after every required tier-one artifact is clean; two-way
work does not run that panel unless later intent explicitly requires it.
the one-way tier-two panel lenses are `whole-acceptance-conformance`, `proof-integrity`,
`independent-coherence`, `security-permissions`, and `red-team`.
the `independent-coherence` lens carries the semantic sweep judgement for one-way archive;
this does not solve the deeper semantic-indexing problem.
missing, malformed, nonzero, unsupported-source, evidence-free, or non-`PASS`/`FLAG`
acceptance reviewer output counts as `FLAG`.
acceptance artifacts record their source as real reviewer, dry-run/self-test, or
fake/self-test; real execute refuses fake acceptance, and real archive refuses dry-run or
fake-source required acceptance.
phase-one labor may be routed by role: the collaborator drives operator-facing orient and
frame work, corpus-throughput work may be delegated, and the collaborator may differ from
the phase-two executor harness while phase-one review stays on the strong review floor.
the collaborator role defaults to the interactive harness that loaded the adapter.
phase-two builders may be routed separately from reviewers through a fast-builder model
knob, while tier-one acceptance, tier-two acceptance, and phase-one review stay on the
strong review floor; the fast-builder default is held at the strong model until the
two-step plan/build work lands.
a unit build attempts the fast builder first, retries a failed unit up to three fast
attempts when `./check.sh` or tier-one acceptance fails, escalates that unit to the strong
builder after the fast budget, and returns to the operator if the strong attempt still
fails.
execute is resumable from the signed frame and on-disk artifacts: a passed unit's build and
tier-one evidence is reused only when its cache key still matches the signed frame, unit
proof obligation, relevant prior-unit state, loop implementation version, recorded diff, and
green mechanical-check evidence, and a cache miss rebuilds the unit and invalidates
downstream unit evidence.
unresolved required tier-one or tier-two `FLAG`s halt phase two before archive; the active
work node remains in flight for the operator.
the checks re-run for every statement, not only the ones a work node touched.
drift is a check that falls without work meaning to break it, and it surfaces wherever it
happens.
archive: adopt or shelve the work according to the signed frame.
one-way archive cannot fold or stamp until required implementation-acceptance artifacts
are present and clean.
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
runs and after recent failure or completion, including the active gate, status, harness
session id, latest message, event history, and run artifact paths.
before launching the first phase-two executor gate, `loop.sh execute <work-name>` checks
that the configured executor binary is present and that executor home/session state is
writable; a failed preflight records failed run state and stops before the executor
session starts.
`loop.sh status <work-name>` reports the addressed work's current phase and, for
non-historical work with phase-two state, the current or recent run's gate, status, state
path, event path, and latest message; `loop.sh status --json <work-name>` renders the same
run state for tooling.
from the root, `./signoff` invokes the root loop sign-off gate and preserves any explicit
arguments it receives.
`loop.sh signoff <work-name> <operator>` remains the explicit sign-off form, and for new
work it renders a concise frame-derived attestation brief through `/dev/tty`, requires the
work number as the confirming token, and writes `signed-off-by:`, `signed-off-at:`, and
`operator-gate: tty`.
`loop.sh signoff` infers the work name only when exactly one frame-complete unsigned work
node exists in the addressed node; otherwise it blocks and asks for `<work-name>`.
`loop.sh signoff` infers the operator from `HYPERCORE_OPERATOR` when set, otherwise from
the addressed node's current intent foot endorsements when exactly one operator is present;
otherwise it blocks and asks for `<operator>`.
from the root, `./direction` invokes `loop.sh direct` and preserves explicit arguments.
`loop.sh direct [<work-name> [<operator>]]` with no direction form renders the neutral
numbered options from `intent/frame/options.md` through `/dev/tty` and copies the operator's
selected option verbatim into `intent/frame/direction.md`, accepting a bare number, `n` for
none-of-these, or `q` for abort.
the explicit `loop.sh direct ... --route|--constraint|--delegate <text-or->` form is an
admin form that cannot record gated operator direction for new work; only the narrow
gate-introducing bootstrap work may record direction without the numbered selection.
`loop.sh direct` rejects empty or placeholder direction, multiple direction forms, an
existing valid direction artifact, a malformed existing direction artifact, and direction
after route content is already present.
`intent/frame/options.md` records numbered options with `kind`, `summary`, `reversibility`,
and `tradeoff`, plus `none` and `abort` rejection choices, and carries no recommendation
marker.
`direction.md` contains `direction-by:`, `direction-given-at:`, `operator-gate: tty`, and
exactly one non-placeholder `selected-route:`, `constraint:`, or `delegation:` copied from a
numbered option.
`operator-gate:` is a B-ready gate token, either `tty` or a reserved `<scheme>:<value>` such
as a later `hmac:<...>`, and only the `tty` liveness scheme is implemented.
from the root, `./review` invokes `loop.sh review` and preserves explicit arguments.
`loop.sh review <work-name> [--add <role>]...` seats the base review roster and any valid
optional complete-roster roles, then writes `intent/frame/review.md`.
new work frame completeness is checked from the canonical `intent/frame/frame.md` only;
`direction.md`, `review.md`, and `signoff.md` do not satisfy ordinary frame fields.
new work frame completeness requires these recoverable fields: addressed node,
node-local work name, target segments, work in flight, problem, constraints, decision
surface or open direction, reversibility, route, acceptance condition, observable
acceptance, excluded interpretation, proof state, sweep, and adoption or shelving claim.
`reversibility:` is parsed as exactly `one-way` or `two-way`.
`loop.sh start <work-name>` scaffolds `intent/frame/frame.md` with the lean fields.
`loop.sh frame` and `loop.sh signoff` block new work whose frame is incomplete, whose
direction is absent or malformed, whose direction appears retrospective, whose new-work
direction or sign-off lacks the `operator-gate: tty` marker, or whose one-way frame lacks a
review artifact.
one-way review artifacts record base-role verdicts, unresolved flags, and disposition;
optional reviewer verdicts cannot clear unresolved base-roster or red-team flags.
new work sign-off records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty` in
the work node's `intent/frame/signoff.md`.
`loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
fresh builder session for each unit, and records lean unit handoff, diff, and tier-one
verdict artifacts under the work frame.
`loop.sh execute <work-name>` routes builders through the builder-model knob, defaulting to
the strong model until the two-step plan/build work lands, separately from the strong
review route; it gives each unit a three-attempt fast-builder budget, escalates an
exhausted unit through the strong-builder model knob, and stops for the operator when the
strong builder fails.
`loop.sh execute <work-name>` runs implementation-acceptance reviewers with literal
approval `never` and literal sandbox `read-only`.
`loop.sh execute <work-name>` writes structured acceptance artifacts with a verdict,
rationale, evidence, and a `source:` marker, refuses `HYPERCORE_ACCEPTANCE_FAKE_DIR` outside
dry-run, and lets real archive accept only `source: real-reviewer` required acceptance.
`loop.sh execute <work-name>` caches per-unit build and tier-one evidence under a
signed-frame-derived key, skips unchanged accepted units on rerun, and rebuilds cache misses
while invalidating downstream evidence.
`loop.sh execute <work-name>` treats malformed, evidence-free, or unsupported-source
implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
concurrent one-way tier-two panel before archive.
`loop.sh execute <work-name>` records the addressed work in node-local history after archive.

---
endorsed by qqp-dev
