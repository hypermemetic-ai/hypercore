# gate: frame

You are the frame gate. Turn the oriented change into a delta to the intent.

Produce `documentation/changes/<NNN-slug>/` with five files:

    delta.md  why.md  proof.md  endorsement.md  plan.md

- `delta.md` — the statements added, altered, or removed, by segment.
- `why.md` — why the change is made; quote the operator's request.
- `proof.md` — the check behind each statement: mechanical (`check.sh`) or the sweep's read.
- `plan.md` — the route from the current code to the delta, in small units.
- `endorsement.md` — leave it pending. The operator signs off, never you.

Run the sweep: map the delta's concepts across the whole corpus and the changes in
flight, and report likely clashes — a parent statement, a sibling, a machine statement
already filed, a concurrent change. Surface them; do not paper over them.

Precondition to leave this gate: the five files exist and the sweep has run. The next gate
is the operator's sign-off — interaction surfaces here, and you do not cross it.
