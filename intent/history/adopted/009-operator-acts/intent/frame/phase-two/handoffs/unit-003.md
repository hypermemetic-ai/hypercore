# handoff - unit-003

unit: unit-003

proof obligation: Rework the primary sign-off helper to render the frame-derived attestation brief, require the work number confirmation through `/dev/tty`, write `signed-off-at:` and `operator-gate: tty`, and add checks that old bare sign-off artifacts cannot satisfy new-work signability.

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260607T185350Z-root-009-operator-acts-pid3509571/gates/implement-unit-003.final.md

## builder final output

Unit-003 is built and marked `check-ready`. I did not edit parent intent documents.

Changed files:
- [adapter/loop.sh](/home/qqp/projects/hypercore/adapter/loop.sh)
- [check.sh](/home/qqp/projects/hypercore/check.sh)
- [unit-003.md](/home/qqp/projects/hypercore/009-operator-acts/intent/frame/phase-two/units/unit-003.md)
- [handoffs/unit-003.md](/home/qqp/projects/hypercore/009-operator-acts/intent/frame/phase-two/handoffs/unit-003.md)
- [diffs/unit-003.diff](/home/qqp/projects/hypercore/009-operator-acts/intent/frame/phase-two/diffs/unit-003.diff)

Prepared checks passed:
- `bash -n adapter/loop.sh`
- `bash -n check.sh`
- `./check.sh`

Proof gap: none for this unit.
