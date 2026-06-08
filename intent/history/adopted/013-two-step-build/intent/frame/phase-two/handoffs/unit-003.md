# handoff - unit-003

unit: unit-003

proof obligation: Non-decomposable units route to the strong builder. Let the planner emit an explicit non-decomposable signal that a check confirms; execute routes such a unit's build to the strong builder directly, as the proactive complement to 010's reactive three-fail escalation, without forcing a mechanical carve. Add the loop and adapter statements and keep them composed with the existing retry/escalate ladder. Proof: check.sh asserts the non-decomposable signal routes to the strong builder and does not break the existing ladder.

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260608T062609Z-root-013-two-step-build-pid3177438/gates/implement-unit-003-fast-1.final.md

## builder final output

unit-003 is built.

Changed files: `adapter/loop.sh`, `adapter/gates/plan.md`, `check.sh`, `intent/loop.md`, `intent/machine-statements/loop.md`, `intent/adapter.md`, `intent/machine-statements/adapter.md`.

Handoff and diff written:
- `013-two-step-build/intent/frame/phase-two/handoffs/unit-003.md`
- `013-two-step-build/intent/frame/phase-two/diffs/unit-003.diff`

Prepared checks:
- `bash -n adapter/loop.sh`
- `bash -n check.sh`
- `git diff --check -- ...`
- `./check.sh` passed

Proof gap: none found.
