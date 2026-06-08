# handoff - unit-002

unit: unit-002

proof obligation: Plan-matches-frame check gating each plan. Add a dedicated independent strong read-only plan-faithfulness reviewer that checks each plan against the signed frame and returns a structured PASS or FLAG; execute requires a clean plan-match result before that unit's build is trusted, and an unresolved plan-match FLAG blocks the unit. Add the loop and adapter statements. Proof: check.sh asserts the plan-match check is required per unit and that a missing or failed plan-match blocks the build.

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260608T062609Z-root-013-two-step-build-pid3177438/gates/implement-unit-002-fast-2.final.md

## builder final output

unit-002 is built.

Changed files:
- [adapter/loop.sh](/home/qqp/projects/hypercore/adapter/loop.sh)
- [check.sh](/home/qqp/projects/hypercore/check.sh)
- [intent/loop.md](/home/qqp/projects/hypercore/intent/loop.md)
- [intent/machine-statements/loop.md](/home/qqp/projects/hypercore/intent/machine-statements/loop.md)
- [intent/adapter.md](/home/qqp/projects/hypercore/intent/adapter.md)
- [intent/machine-statements/adapter.md](/home/qqp/projects/hypercore/intent/machine-statements/adapter.md)

Prepared check: `./check.sh` exits 0.

Proof gap: none found.
