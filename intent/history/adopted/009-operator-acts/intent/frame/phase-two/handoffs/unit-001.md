# handoff - unit-001

unit: unit-001

proof obligation: Add the shared `/dev/tty` operator-gate primitive, add exact `operator-gate:` parsing, make non-interactive direction and sign-off attempts fail to satisfy new-work validation, and add focused `check.sh` coverage for `/dev/tty` refusal and marker validation.

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260607T185350Z-root-009-operator-acts-pid3509571/gates/implement-unit-001.final.md

## builder final output

Unit-001 handoff:

Changed files:
- [adapter/loop.sh](/home/qqp/projects/hypercore/adapter/loop.sh:1202): shared `/dev/tty` operator gate, exact `operator-gate: tty` parsing, direction/sign-off validation, and gated helper writes.
- [check.sh](/home/qqp/projects/hypercore/check.sh:447): focused coverage for `/dev/tty` refusal, no artifact writes on refusal, and invalid/missing marker rejection.

Checks prepared and run:
- `bash -n adapter/loop.sh`
- `bash -n check.sh`
- `./check.sh`

All passed. No parent intent documents were edited in this implement pass. Proof gap: none for unit-001.
