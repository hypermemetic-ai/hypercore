# loop

every change goes through five steps: orient, frame, implement, check, archive.
orient: read the intent documents, the changes in flight under changes/, and the code's conventions; search the web for what you do not know; ask the operator what the artifacts cannot tell you; do not guess.
frame: state the change as a delta to the intent, break it into tasks, and run the sweep over the whole corpus and the changes in flight to flag clashes before code rests on them.
implement: build in small units.
check: prove each statement with a check on the code, and run the sweep for coherence, idiom, and security.
the checks re-run for every statement, not only the ones a change touched.
drift is a check that falls without a change meaning to break it, and it surfaces wherever it happens.
archive: fold the delta into the intent documents, stamp each touched segment's foot with this operator, and move the change to the archive.
a large change breaks into tasks at frame, and a task may itself be a change running this same loop.
a task that materializes or alters a child node is a change run in that child's corpus; the composition tree and the change tree are one tree.
two changes touching the same intent document is a smell, caused by concurrency or orthogonality.
concurrent changes are sequenced by the loop's gates, not by hand: first to archive wins, and a later change builds on the in-flight delta it read in changes/.
an orthogonal collision is fixed in the taxonomy, preferring more documents over more mechanism.

## machine
_none settled yet._

---
endorsed by abacus-git
