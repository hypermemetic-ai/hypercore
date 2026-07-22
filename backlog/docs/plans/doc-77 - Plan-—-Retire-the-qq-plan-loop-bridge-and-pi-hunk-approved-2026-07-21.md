---
id: doc-77
title: Plan — Retire the qq-plan-loop bridge and pi-hunk (approved 2026-07-21)
type: other
created_date: '2026-07-21 22:57'
---
# Plan — Retire the qq-plan-loop bridge and pi-hunk

**Owning Task:** T-130. **Approved:** operator, explicit approval in the
accountable project-home session, 2026-07-21 ("proceed", after ruling "the
plan stuff points to the solution being weak... radically simplify it back
down to essentially just the grilling step we already had... we can probably
retire hunk too"). Captured per grilling.

## Intended outcome

The planning interaction returns to the conversation under grilling
governance; the 746-line `qq-plan-loop` bridge and the pi-hunk dependency
are deleted rather than patched. Smallest resulting system.

## Boundary and non-goals

In: delete `cockpit/pi/qq-plan-loop.ts` and `tests/test-plan-loop.sh`;
re-own the interaction in grilling (partial revert of T-119's slimming);
deliver-change diff review goes vendor-neutral; ratchet baselines
re-measured (lowered); operator-machine removals at land.

Out: adopting any replacement planning software; openwiki refresh
(maintainer Actor); changes to T-122's plans-doc capture; the
`qq_pr_watch` and `qq-backlog-guard` extensions, which are unaffected.

## Decisions and dispositions

1. **Delete, don't patch.** The T-130 incident (review tab with no
   call-to-action, approval select gated on tab close, aborted submit
   silently idling) is a property of the tab choreography itself —
   operator ruling, 2026-07-21 exchange.
2. **Grilling re-owns the interaction.** Structured questions ride the
   native question tool; the plan is drafted under `.pi/plans/` and
   presented inline; the operator's explicit conversational approval is
   the gate; "enactment cannot precede approval" is unchanged — operator
   ruling, same exchange.
3. **pi-hunk retired.** Its only consumers were the plan-loop review tab
   and deliver-change step 4's diff review; the latter becomes
   vendor-neutral ("present the diff inline") — operator ruling, same
   exchange.
4. **Option B (external software owns planning) rejected without a
   search:** the loop was already the in-house bet on that direction
   (T-117/T-118); no pi-native plan mode exists in 0.80.10;
   `plan_loop_submit` was qq's own registered tool — recorded in the
   same exchange.

## Success evidence

Main carries no `qq-plan-loop` reference outside historical backlog
records; grilling and deliver-change read as above; tests/test-ratchet.sh
green at re-measured (lowered) baselines; the full tests/ suite green in
CI; the operator's next planning session runs entirely in the pi tab.
