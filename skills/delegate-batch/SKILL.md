---
name: delegate-batch
description: Composes complete work orders and dispatches aligned batches of bounded tickets through isolated worktrees and stateless qq engines while the accountable session retains judgment, gates, and delivery. Use for an approved ticket batch or when the operator asks the accountable session to work the to-do list.
---

# Delegate a bounded ticket batch

Use this skill only after intent and plan bounds are settled. For aligned new
work or board-driven dispatch, the operator talks to the accountable session;
it stays in the project home and owns batch judgment and delivery. Each writing
ticket runs in its own work session and worktree.

## Compose the work order

Write one complete work-order brief per delegated ticket under the OS temporary
directory. It is the delegate's complete orientation and plan bound. Include:

- the ticket, acceptance criteria, and necessary batch context;
- exact orientation paths and reconciliation facts already verified;
- hard constraints, including local-only work, no push or pull request, and no
  `backlog/` edits under the hybrid Task-truth convention;
- its commit protocol and exact Checks; and
- the required completion envelope.

Keep durable intent in the Task and complete orientation in the brief. The
runtime prompt is only the fixed file pointer carried by `qq-dispatch`.

## Select the work shape

- Couple tickets that share files or one invariant; work them sequentially in
  one isolated Change.
- Fan out independent read-only work through native read-only workers.
- Give independent writing tickets disjoint branches, worktrees, work
  sessions, and non-Git resources.
- Run only the unblocked frontier of a dependency chain.

Keep 3–5 writing tickets in flight at most. Operator review and decision
bandwidth sets the limit; serialize integration.

## Dispatch through the engines

From each ticket's worktree, call:

```sh
qq-dispatch implementer \
  --root <ticket-worktree-root> \
  --brief <work-order-path> \
  --output <envelope-path> \
  --events <events-path> \
  --stderr <stderr-path>
```

Substitute only the paths; never put ticket prose on the command line. Keep all
artifacts under the OS temporary directory. `qq-dispatch` owns the isolated
runner, containment, role configuration, completion wake, and artifacts. Opt
an implementer into external knowledge access only when its work order requires
it. Use a harness-native subagent only for harness-native tools or judgment
beyond the plan bound.

At every dispatcher-owned boundary call `qq-status` with one of its events:
`queued`, `dispatched`, `working`, `envelope-received`,
`envelope-verified`, `review`, `pr-open`, `blocked`, `failed`, or `terminal`.
Pass its required Repository, dispatcher-workspace, work-session, placeholder
pane, agent, ticket, and label identities plus the event details. The engine
owns atomic reporting, monotonic sequencing, notifications, cleanup, and all
Herdr degradation; the glass never gates dispatch or delivery.

After dispatch, inspect each non-terminal events file once at every natural
boundary. Publish `working` when `thread.started` supplies the steering handle.
If it is still absent ten minutes after dispatch, publish `blocked` with
`no thread after 10m`; do not poll. At the completion wake publish `failed` for
exit 124 or a missing envelope, otherwise `envelope-received`. Reconstruct
after dispatcher loss from Tasks, envelopes, and worktrees, never the glass.

## Verify the envelope and retain the gates

Require the final message to report per-ticket status, commits, files changed,
Checks with results, contestable decisions, open questions, unresolved risks,
and the branch and worktree. Verify every claim against the tree; an envelope
claim is not evidence. Publish `envelope-verified` only afterward.

The accountable owner may steer rework but never hands over the lifecycle.
Delegates do not align, review, deliver, or expand scope. A new consequential
decision or scope gap returns to the assigner.

The five gates remain: intent alignment, plan approval, review verdict,
acceptance, and merge. Each Change still passes `code-review` and
`deliver-change`.
