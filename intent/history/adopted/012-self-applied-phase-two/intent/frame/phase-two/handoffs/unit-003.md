# handoff - unit-003

unit: unit-003

proof obligation: Make the resumable cache non-fatal. In `adapter/loop.sh`, a failure at the per-unit cache-record step logs and degrades to a soft miss (the unit rebuilds next run); it never aborts phase two and never changes a correctness outcome. Record the non-fatality in the `loop` and `adapter` intent and machine statements, and add a `check.sh` self-test proving a poisoned or failing cache-record step yields a soft miss and the run proceeds (no fatal exit), through the existing dry-run / fake-dir self-test surface. `./check.sh` is green at the unit boundary.

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260608T035103Z-root-012-self-applied-phase-two-pid1848209/gates/implement-unit-003-fast-1.final.md

## builder final output

Implemented `unit-003`.

Changed files:
- [adapter/loop.sh](/home/qqp/projects/hypercore/adapter/loop.sh)
- [check.sh](/home/qqp/projects/hypercore/check.sh)
- [intent/loop.md](/home/qqp/projects/hypercore/intent/loop.md)
- [intent/adapter.md](/home/qqp/projects/hypercore/intent/adapter.md)
- [intent/machine-statements/loop.md](/home/qqp/projects/hypercore/intent/machine-statements/loop.md)
- [intent/machine-statements/adapter.md](/home/qqp/projects/hypercore/intent/machine-statements/adapter.md)

Unit delta: cache-record failure is now a logged soft miss. The accepted unit remains accepted, phase two continues, downstream cache state uses a nonempty accepted-state marker, and the soft-missed unit rebuilds on the next execute run instead of aborting.

Checks prepared and run:
- `bash -n adapter/loop.sh`
- `bash -n check.sh`
- `git diff --check -- adapter/loop.sh check.sh intent/loop.md intent/adapter.md intent/machine-statements/loop.md intent/machine-statements/adapter.md`
- `./check.sh` green

Proof gap: none.
