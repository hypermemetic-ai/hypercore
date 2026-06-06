# loop

every work node that needs adoption or shelving goes through five gates: orient, frame,
implement, check, archive.
orient and frame are the design phase: the operator and machine choose direction there
before sign-off closes the frame.
when a work node's direction is still open, especially multi-task or multi-phase work, the
machine states the problem, the constraints, and the decision surface before settling the
route; when operator direction is missing, the frame records the open decision and waits
rather than prescribing the sequence.
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
`material/`.
`loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work and
act only on that addressed work.
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

---
endorsed by qqp-dev
