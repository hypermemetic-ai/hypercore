# change

a change is a delta to the intent, the steps to materialize it, and its why and proof.
a change is a folder, not a file, because the plan and tasks need room to grow and a task may itself be a change.
a change holds four things: the delta, the why and the proof, the endorsement, and the plan with its tasks.
the delta is the statements the change adds, alters, or removes, by segment.
on archive, the delta folds into the intent documents.
the why says why the change was made and stays in the archive.
the proof is the check behind every statement; it becomes a check on the code and outlives the change.
a change lives in documentation/changes/ while in flight and moves to documentation/changes/archive/ when done.
the choices the machine settles on the way are machine statements, filed by segment in documentation/machine-statements/.
a task may itself be a change that runs the same loop.

## machine
a change folder is named NNN-slug, with NNN a zero-padded ordinal.
archive is a reserved name under changes/, so no change folder may take it.
the change's four things are the files delta.md, why.md, proof.md, endorsement.md, and plan.md.

---
endorsed by abacus-git
