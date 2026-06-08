# handoff - unit-004

unit: unit-004

proof obligation: Make the handoff real. `loop.sh execute` resolves the single signed, unarchived work node in the addressed node when `<work-name>` is omitted (and blocks with a clear message when zero or more than one exist). Add the Opus->codex launch + supervise path and the `start`-versus- `execute` distinction to `adapter/codex.md` and the `adapter` intent and machine statements, and add a `check.sh` self-test for the auto-detect resolution. `./check.sh` is green at the unit boundary.

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260608T035103Z-root-012-self-applied-phase-two-pid1848209/gates/implement-unit-004-fast-1.final.md

## builder final output

Unit `unit-004` is built.

Changed files:
- [adapter/loop.sh](/home/qqp/projects/hypercore/adapter/loop.sh)
- [adapter/codex.md](/home/qqp/projects/hypercore/adapter/codex.md)
- [intent/adapter.md](/home/qqp/projects/hypercore/intent/adapter.md)
- [intent/machine-statements/adapter.md](/home/qqp/projects/hypercore/intent/machine-statements/adapter.md)
- [check.sh](/home/qqp/projects/hypercore/check.sh)
- [unit-004 handoff](/home/qqp/projects/hypercore/012-self-applied-phase-two/intent/frame/phase-two/handoffs/unit-004.md)

Built:
- `loop.sh execute [<work-name>] [--dry-run]` now infers the single signed, unarchived work node when omitted.
- Zero or multiple candidates now block with explicit messages.
- Adapter prose/intent now names the supervisor-to-executor handoff and distinguishes `start` from `execute`.
- `check.sh` now self-tests zero, single, and ambiguous auto-detect resolution.

Checks prepared and run:
- `bash -n adapter/loop.sh`
- `bash -n check.sh`
- `./check.sh`

Proof gap: none known; all checks passed.
