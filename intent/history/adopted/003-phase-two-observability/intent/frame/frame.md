# frame - 003-phase-two-observability

## work

Build phase-two observability for the Codex loop handoff.

Addressed node: root (`.`).
Node-local work name: `003-phase-two-observability`.
Target segments: `adapter`, `loop`, and `collaboration`.
Work in flight: this work node only. There are no other active work nodes under the root
or `home`; the worktree already carries uncommitted direct-path greenfield adapter changes
touching `adapter`, `home`, `check.sh`, and history, and this work must preserve them.
Open direction needing operator input: none. The operator asked for a clearer phase-two
handoff system and compatibility with future `codex-cockpit` tracking.

## problem

Two phase-two behaviors are not scrutable enough.

First, the outer Codex session often launches `adapter/loop.sh execute` from a filesystem
sandbox where the inner `codex exec` cannot initialize its own home/session state. The
operator sees a repeated handoff failure followed by a rerun with escalation. That is not
a work failure, but the loop does not distinguish it from an ordinary gate failure.

Second, once phase two starts, the launcher has little live information. `run_codex_gate`
captures the inner Codex JSON stream, waits for the command to finish, and only then prints
the final gate message. The outer process therefore polls blindly and cannot report which
gate is active, which Codex thread is running, or what the most recent inner action was.

## constraints

- Do not weaken the signed-frame boundary. Phase two still starts only after operator
  sign-off and still re-derives from the frame.
- Do not hide real Codex or check failures. The loop should label preflight, gate, check,
  sweep, and archive failures clearly.
- Do not depend on `codex-cockpit` being present. The loop should expose simple files that
  a cockpit can tail or poll later.
- Preserve current `codex exec` and `codex exec resume` semantics: one fresh implement
  thread, resumed for check and archive.
- Preserve existing dirty worktree changes not owned by this work.
- Keep the state format boring: line-oriented event history plus a small current state
  file that shell, jq, or a UI can read.

## proposed parent amendments

`adapter` should gain machine statements that the Codex loop records phase-two run state
and streams inner harness events while preserving the cleared-session contract.

`loop` should gain machine statements that `loop.sh execute` exposes phase-two state, and
that `loop.sh status` can report the addressed work's current gate/run state when a phase
two run is active or recently failed.

`collaboration` should gain a machine statement that phase-two handoff state is written as
common ground for the operator and later tooling.

## route

Implement these material changes:

1. Add loop-owned phase-two run state to `adapter/loop.sh`.
   - Add `HYPERCORE_LOOP_STATE_DIR`, defaulting to `.hypercore/loop-runs` under the root.
   - On `execute`, create a run id containing a timestamp, addressed node, work name, and
     process id, then create a run directory.
   - Write a stable current pointer for the addressed work and a root current pointer.
   - Record `state.json` with fields at least: `run_id`, `node`, `work_name`, `phase`,
     `gate`, `status`, `codex_thread_id`, `started_at`, `updated_at`, `message`, and
     paths to the run artifacts.
   - Append `events.jsonl` entries for preflight, gate start, Codex thread discovery,
     check start/pass/fail, sweep verdict, archive decision, completion, and failure.
   - Store each gate's final message in the run directory so the operator/cockpit can read
     the actual gate result after streaming progress.

2. Make `run_codex_gate` stream instead of buffer.
   - Keep the raw `codex exec --json` event stream in the run's `events-codex-<gate>.jsonl`.
   - Print concise progress lines while the inner Codex process runs.
   - Continue to parse the implement gate's Codex thread id from the JSON stream and keep
     using the final output file for `GATE_OUTPUT`.
   - Preserve non-zero exit behavior and final-output cleanup.

3. Add a preflight before launching the first phase-two Codex gate.
   - Check whether the Codex binary is present.
   - Check whether the outer environment appears unable to let Codex write its home/session
     state, using `CODEX_HOME` when set and otherwise `$HOME/.codex`.
   - If preflight fails, write a failed run state and stop before invoking `codex exec`.
     The message should name the missing permission and the exact loop command to rerun
     with outer escalation. It should not present this as a build/check failure.
   - Do not require network preflight; the inner harness owns its own model/API failures.

4. Teach `loop.sh status` to surface phase-two run state.
   - Existing status output stays valid.
   - Add a human-readable active/recent run line when state exists for the addressed work.
   - Add `--json` if convenient, but do not make cockpit compatibility depend on it; the
     state files are the stable interface.

5. Update checks.
   - `check.sh` should verify the loop defaults and requires the new state directory,
     event JSONL, current state, preflight, streaming behavior, and status reporting.
   - Checks should not require a live Codex call.

6. Update adopted intent/machine statements during archive.
   - Update `intent/adapter.md` and `intent/machine-statements/adapter.md`.
   - Update `intent/loop.md` and `intent/machine-statements/loop.md`.
   - Add the settled machine statement to `intent/machine-statements/collaboration.md`
     and copy it into the `## machine` section of `intent/collaboration.md` if the work
     leans on it.

## proof state

Known facts from orient:

- `adapter/loop.sh` currently captures `codex exec --json` output into a shell variable,
  then prints only the final gate response.
- `codex exec --help` in the current outer sandbox emits a read-only filesystem warning
  before doing useful work, so the handoff failure is plausibly a Codex home/session
  initialization permission issue rather than a loop-frame issue.
- `CODEX_THREAD_ID`, `CODEX_CI`, and `CODEX_SANDBOX_NETWORK_DISABLED` are present in the
  outer Codex environment, so the loop can label this as a nested Codex handoff without
  guessing about the operator's shell.
- `adapter/loop.sh` already parses the inner thread id from `thread.started`.
- `check.sh` already checks adapter/loop text without invoking live Codex.

Proof after implementation:

- `./check.sh` must be green.
- `./adapter/loop.sh execute 003-phase-two-observability --dry-run` or an equivalent
  signed dry-run target should show state setup without invoking live Codex.
- A manual status read should show the current work phase and any run state files created
  by dry-run or preflight.

## sweep

Concepts mapped: phase-two cleared session, Codex harness initialization, handoff state,
operator reliance, work in flight, and adapter materialization.

Likely clashes:

- The direct-path greenfield adapter changes currently dirty `intent/adapter.md`,
  `intent/machine-statements/adapter.md`, and `check.sh`. This work may touch those same
  files, so implementation must preserve and build on the dirty text instead of reverting
  it.
- The `adapter` segment says the adapter restates no rules. The telemetry must be stated
  as materialization of the loop/harness, not a new gate or an alternate phase-two rule.
- The `loop` segment says phase two stops only for incomplete frames, failed checks, or
  sweep incoherence. A Codex preflight failure is before the implement gate starts, so it
  should be reported as a sealed handoff/environment blocker, not as a new phase-two stop
  condition inside the gate sequence.

Sweep verdict for the frame: coherent if the implementation treats telemetry as adapter
materialization, preserves the sign-off boundary, and keeps Codex preflight separate from
work proof.

## adoption claim

Adopt this work if the loop exposes clear phase-two state without weakening the loop:
preflight blockers are labeled before `codex exec`, gate progress streams while running,
state files are durable enough for `codex-cockpit`, `status` reports the run, and checks
prove the material contract.
