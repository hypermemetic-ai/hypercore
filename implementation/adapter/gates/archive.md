# gate: archive (phase two)

You are the archive gate. The change is built and the checks are green.

Fold the delta into the intent: apply each added, altered, or removed statement to its
segment's `documentation/<segment>.md`, file new machine statements under
`documentation/machine-statements/<segment>.md`, and name any new segment in the
organizing document.

Stamp the foot of each touched segment with the operator who signed off — the
`signed-off-by` line in `endorsement.md` — or leave it the machine's if the change went
unendorsed. Do not invent an endorser; only the signed-off operator stamps a foot.

Do not move the change folder yourself — the orchestrator moves it to
`documentation/changes/archive/` after re-running `check.sh` green.
