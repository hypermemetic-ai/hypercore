# frame - remove Claude adapter and ease sign-off

## orient

work: remove the Claude Code adapter from the root tracked corpus and make operator
sign-off easier to invoke.

addressed node: root (`.`).

node-local work name: `001-remove-claude-adapter`.

target segments: `adapter` and `loop`, plus the root `intent/organizing-document.md`
because it names the harness adapters that materialize the adapter segment.

work in flight: this work node only. No sibling root work nodes are active, `work-home`
has no mounted work folders, and no legacy change records are present.

external unknowns: none. The current corpus and harness files are enough to frame the
work.

## purpose

The root should be governed by the Codex adapter only. The Claude Code adapter is retired
as a live harness binding, so the tracked corpus must not expose a root `CLAUDE.md`
entry point, a `material/adapter/claude-code.md` adapter, a Claude phase-two execution
path in `material/adapter/loop.sh`, or live intent/check statements that still require
Claude support.

The sign-off gate should preserve operator agency without making the operator do
mechanical command assembly. The operator still signs; the machine still never signs for
them. The common case should be short: from the root, `./signoff` signs the only
frame-complete, unsigned active work in the addressed node, using a grounded operator
identity. Ambiguous cases should block and say what argument is needed.

## scope

Adopted changes should remove or update these tracked live artifacts:

- delete root `CLAUDE.md`;
- delete `material/adapter/claude-code.md`;
- remove Claude harness support from `material/adapter/loop.sh`, making Codex the only
  valid `LOOP_HARNESS` and the default;
- update `material/check.sh` so it proves the Codex adapter remains present and the
  retired Claude adapter entry points are absent;
- update `intent/adapter.md` and `intent/machine-statements/adapter.md` so the machine
  statements describe Codex-only adapter materialization and Codex-only phase-two
  execution;
- update `intent/organizing-document.md` so the adapter segment is materialized by
  `AGENTS.md` for Codex, not by both `CLAUDE.md` and `AGENTS.md`;
- add an operator-facing root sign-off entry point, expected as `./signoff`, that
  dispatches to the loop sign-off gate;
- make `loop.sh signoff` accept the common no-argument path by inferring:
  - the work name when exactly one active work node in the addressed node is
    frame-complete and unsigned;
  - the operator from `HYPERCORE_OPERATOR` when set, otherwise from the addressed node's
    current intent foot endorsements when exactly one operator is present;
  - neither value when inference is ambiguous, so the gate blocks rather than guessing;
- update `intent/loop.md` and `intent/machine-statements/loop.md` to record the inferred
  sign-off behavior;
- remove tracked ignore material that exists only to hide Claude Code local state, if it
  has no remaining purpose after the Claude adapter is retired.

The ignored local `.claude/` directory is not tracked corpus history and is not removed
by this work. Deleting it is a separate destructive filesystem action that needs explicit
operator direction.

## route

1. Read the current adapter intent, organizing document, `material/adapter/loop.sh`,
   `material/check.sh`, and both harness adapter prose files.
2. Remove the Claude adapter entry point and adapter prose file from the tracked corpus.
3. Simplify the loop's harness selection:
   - default `LOOP_HARNESS` to `codex`;
   - remove `CLAUDE_BIN`, `LOOP_BUDGET_USD`, `run_claude_gate`, and the Claude branches in
     `run_gate` and phase-two session id creation;
   - keep the Codex execution path and the existing node-local work behavior intact.
4. Simplify sign-off invocation:
   - allow `loop.sh signoff` to infer the single signable work node and the unique
     current operator when the addressed node makes both unambiguous;
   - allow explicit `loop.sh signoff <work-name> <operator>` to keep working;
   - add a root `signoff` helper or symlink that invokes the loop's sign-off gate, so the
     operator-facing command is `./signoff` in the root common case.
5. Replace Claude-positive structural checks with absence checks for the retired Claude
   artifacts and keep the Codex-positive checks.
6. Rewrite the adapter machine statements in both the live intent and
   `machine-statements/adapter.md` so no live statement claims Claude is materialized or
   executable.
7. Update the organizing document's adapter bullet to name `AGENTS.md` for Codex as the
   live harness adapter.
8. Update loop intent machine statements and structural checks to cover the easier
   sign-off path and its ambiguity blockers.
9. Run `./material/check.sh`.
10. Search the live tracked corpus for `Claude`, `CLAUDE`, and `claude`. Historical adopted
   work and untracked local state may mention the retired harness, but live parent intent,
   live material, and live checks should not.

## proposed parent amendments

`intent/adapter.md` and `intent/machine-statements/adapter.md` should retain the operator
statements that define adapters generally, but their machine statements should change from
multi-harness materialization to current Codex-only materialization.

The organizing document should continue to say the `adapter` segment is materialized at
the root by methodology prose, the harness adapter, and `material/adapter/`; it should no
longer name `CLAUDE.md` or Claude Code as a live harness adapter.

`intent/loop.md` and `intent/machine-statements/loop.md` should keep the explicit sign-off
form but add the inferred common case: when the addressed node has exactly one
frame-complete unsigned work node and one current operator endorsement, sign-off can infer
both. `HYPERCORE_OPERATOR` can provide the operator explicitly without putting it in the
command line. Ambiguity blocks.

## proof state

Baseline `./material/check.sh` is green before implementation.

Required proof after implementation:

- `./material/check.sh` exits zero;
- `git ls-files` no longer lists `CLAUDE.md` or `material/adapter/claude-code.md`;
- live files `intent/adapter.md`, `intent/machine-statements/adapter.md`,
  `intent/organizing-document.md`, `intent/loop.md`,
  `intent/machine-statements/loop.md`, `material/adapter/loop.sh`,
  `material/check.sh`, and `material/adapter/codex.md` carry no retired Claude support;
- `material/adapter/loop.sh` still executes Codex phase two for signed work nodes.
- `./signoff` exists at the root and signs the single frame-complete unsigned root work
  node when the operator identity is unambiguous;
- `./material/adapter/loop.sh signoff` keeps the old explicit
  `<work-name> <operator>` form working;
- ambiguous sign-off inference exits non-zero with a concrete message rather than
  guessing.

## frame sweep

Map:

- `adapter` intent names harness bindings, root adapter materialization, the rigid
  workflow, and phase-two cleared sessions.
- `organizing-document` names the adapter segment's materialization and currently names
  both root harness adapters.
- `material/check.sh` currently proves both Codex and Claude Code adapter prose exist.
- `material/adapter/loop.sh` currently defaults to Claude Code and dispatches both Claude
  and Codex phase two.
- `loop` intent and machine statements currently require a sign-off line in
  `intent/frame/signoff.md`, and the orchestrator currently requires the operator to pass
  both work name and operator on the command line.
- no other active work node proposes a conflicting adapter change.

Read:

- The current machine statements conflict with the requested retirement because they
  still claim Claude Code is materialized and executable.
- The check script conflicts with the requested retirement until its Claude-positive
  checks become absence checks.
- The general operator statement that an adapter is per harness does not conflict with
  retiring one current harness adapter; it remains true as a general methodology rule.
- The endorsement rule that the machine never endorses does not conflict with a shorter
  sign-off command because the operator still invokes the sign-off gate and ambiguity
  blocks rather than being settled by the machine.
- No sibling work or child-node contract likely contradicts this route.

Sweep verdict for frame: coherent if the adopted delta removes the live Claude adapter
material, updates the adapter machine statements and checks together, and makes sign-off
shorter without letting the machine decide endorsement.

## adoption claim

Adopt this work if the tracked root corpus is Codex-only for live adapter materialization,
the root has an easier operator sign-off command, and `./material/check.sh` is green.
Shelve it if the implementation cannot remove Claude support or ease sign-off without
breaking the loop or leaving the intent/checks contradictory.
