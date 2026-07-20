---
name: deliver-change
description: Owns the judgment and one-PR GitHub Flow delivery for every authorized Repository modification intended to land, from an aligned assignment through Task completion, a green pull-request handoff, verified disposition, and safe engine-driven retirement. Use only in the operator-facing accountable agent; not for read-only work, local experiments, or delegated work within another Actor's Change.
---

# Deliver a Change

Retain responsibility for scope, decisions, evidence, and delivery state. Give
delegates bounded assignments; never hand them this lifecycle.

`pi-hunk` is the operator's local diff-review checkpoint (`/hunk review`, submit
notes, empty submit approves). GitHub's web UI is for Checks and merge.

Call qq engines unconditionally. They own containment, degradation, and rails;
their fixed exit vocabulary is 0 done, 2 rail refusal, and 1 error.

1. Bind the Change to the agreed outcome and current Repository state. Before
   Repository mutation, require the owning Task Description to carry a
   **decision ledger**: every consequential decision the Change embeds cites
   the Backlog decision record, approved Task, asked-and-answered alignment
   exchange, or explicit operator opt-out recorded verbatim that settled it,
   or the ledger says `none`. Dispositions do not transfer. An uncited decision
   is open and returns to alignment. Mint a decision record for a disposition
   whose reach extends beyond this Change and cite it. Confirm that the branch
   and worktree isolate the Change.
2. Resolve the Repository root and call `qq-herdr-home inspect --repo <root>`.
   Best-effort attach an existing Change checkout to the project home, or
   create a work session from the explicitly agreed base when no checkout
   exists. Cockpit attachment never blocks delivery. The accountable session
   dispatches from the project home; run every Change command in its checkout.
3. Implement coherent units through one complete work order and
   `delegate-batch`, then verify its completion envelope against the tree.
   Delegate decision-grade investigation through `research`; retain the
   judgment. Keep the Task aligned through Backlog's CLI in the primary `main`
   checkout under the hybrid Task-truth convention, and run local Checks that
   observe the changed behavior.
4. After implementation and local verification, run `code-review` with fresh
   context for every non-trivial Change. Verify returned findings, resolve only
   confirmed in-scope failures, rerun affected Checks, and review each fix
   delta. Present the resulting local diff through `pi-hunk`.
5. Commit only green units, push them, and open one pull request carrying the
   Task intent and Check evidence. Pass the Repository's final GitHub Checks.
6. Before final handoff, move the Task record from the primary checkout into
   the Change checkout, then use Backlog's finalization procedure there:
   verify acceptance criteria, record the summary, mark the Task Done, and
   push that commit through the same pull request. Rerun affected Checks.
7. If a Check or operator feedback shows an acceptance criterion unmet,
   return the same Task to active and correct this Change. If it is closed or
   unavailable, align its branch disposition without replacing the Task. A
   later intent change is new work and needs approval; do not absorb it.
8. Confirm the open pull request is reviewed, finalized, and green; resolve
   its URL from GitHub. Open that URL in the operator's browser, send a Herdr
   notification containing it, and report it. Browser and cockpit behavior are
   best-effort and never block the green handoff.
9. Never merge; the operator merges. Arm the `qq_pr_watch` Pi-extension tool
   for the pull request. Its terminal wake is convenient, not load-bearing:
   on a wake, later resume, or operator message, call the idempotent
   `qq-change land <pr> --repo <checkout>`.
10. `qq-change land` owns merged-state and ancestry verification plus safe,
    fast-forward synchronization of the sole primary `main` checkout. On exit
    2, report its observed state and stop; on exit 1, report the error and
    retain the Change. A repeated call is safe. A closed or rejected Change
    follows step 7 and leaves the completed Task unchanged.
11. After landing succeeds, leave operator focus untouched and call
    `qq-change retire <work-session-id> --repo <checkout> --branch <branch>`.
    The idempotent engine owns clean-checkout, merged-branch, ownership,
    topology, and focus rails and never forces removal. On refusal or error,
    report its state and leave the work session, checkout, panes, and branch
    intact. Never merge, force-delete, stash, clean, reset, switch, or repair
    checkout state as part of delivery.
12. Keep all five gates with the accountable owner: intent alignment, plan
    approval, review verdict, acceptance, and merge.
