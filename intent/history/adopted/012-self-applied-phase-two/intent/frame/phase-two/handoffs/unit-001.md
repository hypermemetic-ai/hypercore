# handoff - unit-001

unit: unit-001

proof obligation: Add orchestrator self-edit safety. Make `adapter/loop.sh` run phase two from an immutable snapshot of itself (re-exec from a copy at execute start) so a unit that edits `loop.sh` mid-run cannot corrupt the live orchestrator. Record it in the `loop` and `adapter` intent and machine statements, and add a self-test proving a mid-run `loop.sh` edit does not corrupt the active run. `./check.sh` is green at the unit boundary. (First so no later unit edits `loop.sh` before the safety exists; 012's own bootstrap run is launched from a manual snapshot by the supervisor.)

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260608T035103Z-root-012-self-applied-phase-two-pid1848209/gates/implement-unit-001-fast-1.final.md

## builder final output

Built `unit-001` and left the unit boundary green.

Changed files:
- [adapter/loop.sh](/home/qqp/projects/hypercore/adapter/loop.sh)
- [check.sh](/home/qqp/projects/hypercore/check.sh)
- [intent/loop.md](/home/qqp/projects/hypercore/intent/loop.md)
- [intent/machine-statements/loop.md](/home/qqp/projects/hypercore/intent/machine-statements/loop.md)
- [intent/adapter.md](/home/qqp/projects/hypercore/intent/adapter.md)
- [intent/machine-statements/adapter.md](/home/qqp/projects/hypercore/intent/machine-statements/adapter.md)
- [unit-001.md handoff](/home/qqp/projects/hypercore/012-self-applied-phase-two/intent/frame/phase-two/handoffs/unit-001.md)
- [unit-001.diff](/home/qqp/projects/hypercore/012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-001.diff)

Prepared checks, all passing:
- `bash -n adapter/loop.sh`
- `bash -n check.sh`
- `./check.sh`

Proof gap: none for this unit.
