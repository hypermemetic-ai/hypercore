# session handoff - 009-operator-acts

Saved because the 2026-06-07 session was interrupted after a long phase-two run.

## operator question answered

This took about an hour because the signed frame drove four implementation units, and each
unit spawned a fresh Codex builder plus a fresh tier-one acceptance reviewer. After the
four units passed, one-way work also spawned the five-lens tier-two panel. The loop was
doing exactly the expensive thing `008-phase-two-acceptance` requires for one-way archive.

The restart happened because the tier-two panel found a real proof-integrity/security
problem:

- A read-only acceptance reviewer appears to have run `execute 009-operator-acts
  --dry-run`.
- Before the latest fix, dry-run execution wrote phase-two artifacts into the active work
  frame (`009-operator-acts/intent/frame/phase-two`) instead of a run-local dry-run
  directory.
- That overwrote real handoffs and tier-one verdict artifacts with `dry-run: yes`
  artifacts.
- The panel then returned `FLAG` for `proof-integrity`, `independent-coherence`,
  `security-permissions`, and `red-team`. `whole-acceptance-conformance` passed, but was
  also marked `dry-run: yes`, which would have blocked archive anyway.

The bug was fixed after the panel failure:

- `adapter/loop.sh`: `execute --dry-run` now writes phase-two artifacts under
  `$LOOP_RUN_DIR/phase-two-dry-run` instead of the active work frame.
- `adapter/loop.sh`: dry-run state no longer updates the current root/work run pointers.
- `check.sh`: self-tests now verify dry-run tier-one and tier-two artifacts stay out of the
  active work frame and are found in the run-local dry-run directory.
- `./check.sh` passed after this fix.

## current state

Work node: `009-operator-acts`

Frame/sign-off state:

- `./adapter/loop.sh status 009-operator-acts` reported `frame_complete=yes
  signed_off=yes`.
- The work remains active, not archived.

Important: the user interrupted a fresh rerun:

- Run id: `20260607T171202Z-root-009-operator-acts-pid3025173`
- Loop state reported: `gate=implement-unit-001`, `unit=unit-001`, `status=running`
- Before continuing, verify whether that process is still alive. If it is, stop it or wait
  for it intentionally before starting another `execute`.

Current modified files observed before the handoff:

- `adapter/loop.sh`
- `check.sh`
- `hypercore.md`
- `adapter/codex.md`
- `adapter/gates/orient.md`
- `adapter/gates/frame.md`
- `009-operator-acts/`

Other untracked files/directories observed:

- `WORK-NODE-COLLAPSE-FINDINGS.md` existed before this work and appears unrelated.
- `999-check-loop-frame-contract-3041236/` was left behind by a check/self-test run and
  should be inspected before removal.

Deleted by the implementation:

- `OPERATOR-ACTS-FINDINGS.md`

## commands already run

- `./adapter/loop.sh start 009-operator-acts`
- operator ran `./direction 009-operator-acts qqp-dev --route "...Route A..."`
- `./review 009-operator-acts` wrote a phase-one review artifact with all base roles
  `FLAG` because reviewer subprocesses exited `1`; the frame records this limitation.
- `./adapter/loop.sh frame 009-operator-acts` passed.
- operator ran `./signoff`
- `./adapter/loop.sh execute 009-operator-acts` was run multiple times.
- `./check.sh` was green after the dry-run artifact fix.

## what changed

High-level implemented behavior:

- Shared `/dev/tty` operator gate.
- Exact `operator-gate: tty` parsing.
- Direction options contract via `intent/frame/options.md`.
- Primary `./direction` path renders neutral numbered options and copies the selected
  option text into `direction.md`.
- Primary `./signoff` path renders a frame-derived attestation brief and requires the
  work number as confirmation.
- Narrow bootstrap exemption for this already-signed `009-operator-acts` work, because
  its own direction/sign-off were recorded before the new gate existed and the frame
  explicitly excludes a retroactive gate claim.
- Prose and checks updated for the new operator-gate contract.
- Dry-run `execute` isolation hardened after the tier-two panel found it could overwrite
  active phase-two artifacts.

## recommended next session steps

1. Check lingering process state:

   ```bash
   ./adapter/loop.sh status 009-operator-acts
   ps -ef | rg '3025173|adapter/loop.sh execute 009-operator-acts|codex exec'
   ```

2. If the interrupted run is still alive, stop it deliberately before continuing.

3. Inspect the leftover self-test directory:

   ```bash
   find 999-check-loop-frame-contract-3041236 -maxdepth 3 -type f -print
   ```

   Remove it only if it is confirmed to be a stale check artifact.

4. Run:

   ```bash
   bash -n adapter/loop.sh
   bash -n check.sh
   ./check.sh
   ./adapter/loop.sh status 009-operator-acts
   ```

5. Rerun phase two only after the old run is not active:

   ```bash
   ./adapter/loop.sh execute 009-operator-acts
   ```

6. Expect the rerun to be expensive unless the frame is reframed into fewer units or the
   acceptance reviewer behavior is changed. If the operator wants speed over the full
   one-way proof path, that requires new operator direction or a new work node; do not
   bypass the signed frame silently.

