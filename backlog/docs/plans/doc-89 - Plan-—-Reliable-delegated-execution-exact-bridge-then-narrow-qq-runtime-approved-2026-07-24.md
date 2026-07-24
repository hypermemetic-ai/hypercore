---
id: doc-89
title: >-
  Plan — Reliable delegated execution: exact bridge, then narrow qq runtime
  (approved 2026-07-24)
type: specification
created_date: '2026-07-24 07:13'
updated_date: '2026-07-24 07:17'
tags:
  - plan
  - delegation
  - pi-subagents
  - qq-runtime
---
# Plan — Reliable delegated execution: exact bridge, then narrow qq runtime

- **Approved:** 2026-07-24, operator-facing asked-and-answered alignment exchange
- **Roadmap Task:** T-154
- **Immediate Change:** T-154.1
- **Replacement Change:** T-154.2
- **Durable decision:** decision-12

## Outcome

Restore strict delegated completion and resume immediately, then replace the
general-purpose dependency with the smaller runtime qq actually needs.

The first Change creates and installs one immutable qq-controlled
`pi-subagents` bridge, migrates production one-step workflows to true single
runs, and proves the existing completion contract on the exact installed
versions. The second Change extracts that contract into implementation-neutral
Checks, builds a narrow qq-owned delegate runtime on Pi's documented process
surfaces and the existing `qq-dispatch` boundary, migrates production and
observer assembly, and removes the bridge.

The bridge is a delivery tactic, not a product direction. The resulting system
must keep qq-owned intent, roles, policy, supervision, completion, timeout,
cleanup, and observation semantics above a replaceable Landstrip driver.

## Settled decisions and boundaries

- **Bridge base:** upstream `pi-subagents` commit
  `f1540b09283a1c176a0c721878453c6382ecd399`. This snapshot includes upstream
  acceptance-safe async recovery and true single-run `outputSchema` support.
- **Bridge ownership:** create `hypermemetic-ai/pi-subagents`; carry one bounded
  qq behavioral delta for terminal structured-output recovery; install from an
  immutable fork commit. Never install from a branch, mutable tag, unpinned npm
  range, or machine-local path.
- **Production call shape:** one-step reviewer and implementer workflows become
  true single runs. A one-element chain is not the stable qq interface.
- **Destination:** a qq-owned, single-child delegate runtime implementing only
  the production contract named below. It does not become a generic agent
  framework.
- **Containment:** decision-8 remains unchanged. `bin/qq-dispatch`, the pinned
  Landstrip CLI/policy identity, timeout, and process-tree supervisor remain the
  confinement and cleanup composition. Network egress remains open.
- **Observation:** decision-10 remains unchanged. Native persisted Pi session
  JSONL is the sole agent-content observation seam. Lifecycle metadata and
  completion notification may be live; no parallel transcript/content capture
  is introduced. Observer Change attribution remains separate and undisposed.
- **Role/compute policy:** T-152/doc-88 remains authoritative. qq owns canonical
  role occupancy and execution-profile policy; a delegate package, same-name
  project agent, invocation override, or fallback router may not claim that
  authority.
- **Delivery:** T-154.1 and T-154.2 are separate Changes with separate fresh
  review. A new security boundary, observation seam, public workflow, or
  orchestration mode requires realignment.

## Evidence establishing the plan

The installed `pi-subagents` 0.35.1 has two reproduced contract failures:

1. A child can receive a tool error, recover, successfully call terminal
   `structured_output`, and produce a schema-valid completion envelope. The
   child and capture succeed, but `detectSubagentError` scans past the last
   non-empty assistant text, rediscovers the earlier tool error, and causes the
   parent to fail the completed run. The recorded example is the former run
   `923f44ae`; its session was under
   `/tmp/pi-subagent-sessions/923f44ae/run-0/session.jsonl` when investigated.
2. Async recovery can reject legacy resolved acceptance metadata or revive a
   run without the original structured-output contract. The recorded examples
   were the former runs `c689a6ef` and `e2d76888` under the ordinary
   `pi-subagents-uid-*` runtime tree.

A disposable prototype based on the chosen upstream snapshot added successful
`structured_output` tool results as recovery evidence, kept failed structured
output terminal, and passed 278 targeted execution tests plus 20 async-resume
unit tests. Prototype directories under `/tmp/pi-subagents-f154` and
`/tmp/pi-subagents-fix` are hints only; the implementing Actor must reconstruct
and verify the patch from the exact upstream commit rather than trust volatile
state.

The architecture is narrow because qq's production Skills each use one role,
one task, one cwd, one completion schema, and one async lifecycle. Generic
chains, parallel graphs, scheduling, agent discovery, watchdogs, sharing, and
model fallback are unused. Pi's official subprocess subagent example proves
that isolated child execution is available through documented `pi --mode json`
surfaces, while `bin/qq-dispatch` already owns worktree validation, Landstrip
policy rendering, timeout, descendant cleanup, isolated runtime/config/session
directories, and observation spans.

## Change 1 — T-154.1: exact bridge

### 1. Establish immutable fork provenance

1. Fork the upstream Repository into `hypermemetic-ai/pi-subagents` as an
   externally visible side effect already authorized by decision-12.
2. Create the bridge branch from the exact base SHA above. Preserve the upstream
   history; do not copy source into qq or synthesize a release tarball.
3. Record the upstream base and fork patch commit in the fork and in qq's install
   documentation. Give the fork package a distinguishable qq bridge identity
   where the package's existing version/provenance surfaces permit it without
   changing Pi package resolution semantics.
4. Pin the Pi installation through Pi's documented Git-package source syntax to
   the exact fork commit. Verify the resolved package list and installed source;
   a settings string alone is not evidence that the running extension changed.

### 2. Apply the one behavioral delta

Change error recovery classification so the last trusted recovery watermark is
either:

- a non-empty assistant text response, as today; or
- a successful `toolResult` for the child-only `structured_output` tool.

Only messages after that watermark may terminalize the run. A failed
`structured_output` result is never recovery evidence. A tool call without a
successful result is never recovery evidence. A later tool/provider error after
successful structured output remains terminal. Parent-side schema validation
continues to decide whether the captured value is valid; the patch must not
turn arbitrary prose or a model-authored JSON claim into completion evidence.

Keep the delta local to this contract. Do not add retries, fallback models,
acceptance inference, chain behavior, or unrelated upstream-main changes.

### 3. Add reproduce-before-fix package regressions

At minimum, prove all of these against the exact fork source:

- earlier `bash`/tool error + successful terminal structured output + valid
  captured value => success;
- earlier error + failed structured-output tool result => failure;
- earlier error + absent capture => failure;
- earlier error + schema-invalid captured value => failure;
- successful structured output + later terminal tool/provider error => failure;
- ordinary recovered prose remains success and an unrecovered tool error remains
  failure;
- foreground single and background single paths agree;
- a persisted single-run recovery descriptor contains the raw output schema and
  explicit `{level:"none", reason:...}` acceptance contract;
- resume passes the original schema, acceptance, role, cwd, session, timeout,
  context, and output settings to the revived child;
- malformed, stopped, ambiguous, cross-run, wrong-agent, and legacy descriptors
  retain their intended refusal/compatibility behavior.

Demonstrate that the primary regression fails before the qq patch and passes
after it. Run the full applicable upstream test suite, not only the new tests.

### 4. Migrate qq production calls

Update `skills/code-review/SKILL.md` and `skills/delegate-batch/SKILL.md` so each
example invokes single mode directly:

- top-level `agent`, `task`, `outputSchema`, and explicit acceptance-none;
- absolute assigned `cwd`;
- `context:"fresh"`;
- `async:true`;
- the existing hard timeout.

Preserve one complete brief per child, canonical manifest selection, completion
envelope verification by the accountable owner, natural-boundary status
inspection, and the existing `status.json`, `events.jsonl`, session, output, and
notification expectations where single mode already supplies them. Update tests
that intentionally lock the call shape. Do not preserve one-step chain syntax
for compatibility inside qq.

Inspect `bin/qq-dispatch` and `bin/qq-observe` against actual single-run status
and session artifacts. Make only compatibility changes required by the
migration. Do not use this Change to redesign observer attribution or artifact
formats.

### 5. Verify the exact installed composition

Run fresh Checks on the fork commit, the qq Change checkout, and the installed
Pi composition:

- upstream package typecheck/lint/test/build commands applicable at the pinned
  snapshot;
- focused structured-output and async-resume regressions;
- `tests/test-qq-delegate-enforcement.sh` and every Repository Check affected by
  Skill, dispatch, package, or observer changes;
- a foreground single-run structured completion probe;
- a background single-run completion probe with lifecycle/status artifacts;
- a background recovery/resume probe proving schema and acceptance preservation;
- a failure probe proving malformed or missing completion remains terminal;
- confinement probes for assigned-worktree access, forbidden writes, reviewer
  scratch, timeout, and descendant cleanup on the exact installed Landstrip and
  Pi versions;
- observer assembly against a real single-run status/session mapping if that
  surface changed.

Read complete output and verify the running package provenance. Then invoke
fresh-context `code-review` over the fork delta and the qq Change. Any additional
required fork behavior is a scope gap and returns to the operator.

### 6. Document maintenance and retirement

Document:

- exact upstream base and exact fork commit;
- the one carried delta and its regression;
- how to reconstruct, test, and deliberately update the fork;
- why automatic package updates and moving refs are forbidden;
- the fork's bridge status;
- retirement condition: T-154.2 passes the shared contract suite, production
  Skills and observer assembly use the qq runtime, and the installed fork pin is
  removed.

An upstream issue or pull request is useful but is not required and is not
implicitly authorized by this plan.

## Change 2 — T-154.2: narrow qq runtime

Start only after T-154.1 is landed and its exact contract is green. Create a new
Change from fresh `origin/main`; do not continue developing the replacement in
the bridge checkout.

### 1. Extract implementation-neutral contract Checks

Turn the bridge verification matrix into black-box qq Checks whose subject is
the delegate contract rather than `pi-subagents` internals. Run them against the
bridge first to establish the baseline. Fixtures must cover success, every
terminal failure class, lifecycle transitions, timeout/cleanup, confinement,
notification, crash residue, and exact resume.

### 2. Build only the required surfaces

Provide one qq-owned root tool with a deliberately small parameter contract:
trusted canonical role, task/brief pointer, assigned worktree, exact output
schema, explicit timeout/output settings, and fresh context. Provide only the
management actions required by production: status/fleet visibility, wait or
completion wake, stop, and resume.

The implementation should:

1. Resolve canonical role configuration only from qq's trusted manifest source
   and persist a dedicated trusted role assertion. Refuse unknown, conflicting,
   or same-name project occupancy before spawning.
2. Validate the same-Repository worktree and request, then write an immutable,
   mode-0600 launch/recovery descriptor before child launch.
3. Start a detached supervised runner that invokes Pi through
   `bin/qq-dispatch`, using Pi's documented JSON or RPC/session surfaces. Avoid
   private Pi APIs unless a separately aligned gap proves unavoidable.
4. Load one child-only structured-completion extension. The trusted tool writes
   one schema-validated capture; parent validation repeats before terminal
   success. Prose is never a substitute completion envelope.
5. Materialize atomic lifecycle state and bounded event/status diagnostics,
   maintain process identity, and deliver one completion/attention wake without
   requiring polling. Preserve enough evidence to distinguish not-started,
   running, paused, timed-out, failed, completed, stopped, and orphaned/crashed
   states.
6. Forward cancellation, enforce the declared hard deadline, terminate the
   complete descendant tree, and prove cleanup. `qq-dispatch` and Landstrip
   remain the enforcement driver rather than being reimplemented in TypeScript.
7. Resume only from the immutable descriptor and exact persisted Pi session.
   A follow-up message may vary; role, worktree, schema, timeout, output,
   execution profile, context, and policy identity may not drift. Refuse
   malformed, foreign, ambiguous, stopped, or unverifiable recovery state.
8. Expose the canonical Pi session path to observer assembly while keeping
   lifecycle metadata separate from agent-content observation. During migration,
   assembly may understand both bridge and qq artifacts; remove bridge-specific
   logic once no delivered Change can emit it.

### 3. Keep the non-goals absent

Do not implement chains, generic/dynamic fan-out, generic agent discovery,
scheduling, best-of-N, sharing, watchdogs, model fallback/routing, acceptance
inference, a new TUI, or a broader security boundary. Independent ticket fan-out
continues to be composed by the accountable owner through separate single-run
calls and separate worktrees, not inside the runtime.

### 4. Migrate and retire

Run the black-box contract suite unchanged against the qq runtime. Migrate
`code-review`, `delegate-batch`, observer launch, and any other production caller
only after it is green. Verify a real Change review and a bounded implementer
run end to end. Remove the fork from Pi settings/install documentation and
remove pi-subagents-specific production coupling only in the same green Change.
Leave historical sessions readable; do not rewrite or delete evidence.

T-154 completes only when both child Tasks are green and landed and no moving or
forked delegate dependency remains authoritative.

## Fresh-session handoff

The immediate implementation checkout is:

- **Task:** T-154.1
- **Branch:** `fix/delegate-runtime-bridge`
- **Checkout:** `/home/qqp/.herdr/worktrees/qq/delegate-runtime`
- **Base:** fresh `origin/main` at Change creation

This checkout currently contains only decision-12, T-154/T-154.1/T-154.2, and
this approved plan. The fresh accountable session should begin with T-154.1,
re-read current source and Pi package documentation, verify the exact upstream
commit independently, inspect the working tree, and continue the ordinary
`deliver-change` flow. It must not implement T-154.2 in the bridge Change.
