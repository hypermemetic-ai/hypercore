# handoff - unit-001

unit: unit-001

proof obligation: Strong-model plan step plus a readable per-unit plan artifact. Add a planner model knob to adapter/loop.sh (defaulting to the strong model) and make execute run a strong-model plan sub-step at the head of each unit that writes a human-readable plan under the unit's phase-two tree before the build runs. Add the loop and adapter intent statements for the per-unit plan step and the readable plan artifact. Proof: check.sh asserts the planner knob exists and defaults to the strong model, the new statements are present, and a dry-run execute records a plan artifact before that unit's build artifact.

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260608T062609Z-root-013-two-step-build-pid3177438/gates/implement-unit-001-fast-2.final.md

## builder final output

Unit `unit-001` is built.

Changed files:
- [adapter/loop.sh](/home/qqp/projects/hypercore/adapter/loop.sh)
- [adapter/gates/plan.md](/home/qqp/projects/hypercore/adapter/gates/plan.md)
- [check.sh](/home/qqp/projects/hypercore/check.sh)
- [intent/loop.md](/home/qqp/projects/hypercore/intent/loop.md)
- [intent/machine-statements/loop.md](/home/qqp/projects/hypercore/intent/machine-statements/loop.md)
- [intent/adapter.md](/home/qqp/projects/hypercore/intent/adapter.md)
- [intent/machine-statements/adapter.md](/home/qqp/projects/hypercore/intent/machine-statements/adapter.md)

Prepared checks:
- `./check.sh` passed.
- `bash -n adapter/loop.sh && bash -n check.sh` passed.
- `git diff --check -- ...` passed.

Proof gap: none found for this unit.
