# handoff - unit-002

unit: unit-002

proof obligation: Add and validate the neutral `options.md` contract, rework the primary direction helper to render numbered options and copy the selected option text into `direction.md`, and add checks for selection, none/abort handling, neutrality-relevant structure, and non-retrospective direction.

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260607T185350Z-root-009-operator-acts-pid3509571/gates/implement-unit-002.final.md

## builder final output

Unit-002 is built and checked.

Changed files for this unit:
- [adapter/loop.sh](/home/qqp/projects/hypercore/adapter/loop.sh): neutral `options.md` validation, primary numbered direction selection via `/dev/tty`, selected option copying into `direction.md`, none/abort handling, direction/options match checks, and non-retrospective direction enforcement.
- [check.sh](/home/qqp/projects/hypercore/check.sh): coverage for options scaffolding, selection, none/abort non-writes, neutrality structure, option mismatch, and retrospective direction rejection.

Prepared check: `./check.sh` passed.

Proof gap: none for unit-002. Parent intent documents were not edited.
