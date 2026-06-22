---
name: grilling
description: hypercore's grilling methodology — turn a filed ask into a ratified contract and spec delta by resolving what the spec and intent already settle and surfacing only the stake-bearing residue, one question at a time, each with a lean and a flip. Load when extracting intent from an ask or judging whether it is ready to become work.
---

# grilling

Intent extraction by grilling — how the architect turns a filed ask into ratified work
without authoring on the operator's behalf (ADR 0013, carved from `conversation`). Before an
ask that opens real choices becomes work, the architect runs a grilling pass: it resolves every
decision it can from the living spec and intent, and surfaces only the residue — the decisions
the operator has a stake in — as questions on the queue, **one at a time**, in dependency order,
each carrying the machine's **lean** (its recommended answer) and the one thing that would
**flip** it. The operator settles each by accepting the lean or answering in their own words, so
they ratify far more often than they author. An ask whose every decision is already determined
files straight to standing work, ungrilled; the floor is a **standing guard**, not a front gate —
the same test re-fires whenever a stake-bearing choice surfaces mid-work. A resolved pass yields
two products: the **contract** (the operator-view entry the result is later validated against)
and the **spec delta** the change will realize.

## The disciplines — what good looks like

- **a filed ask is grilled before it becomes work** — An ask that opens real choices MUST pass a grilling floor before spawning work: the architect resolves every decision it can from the living spec and intent, and only a residual decision the operator has a stake in keeps the ask above the floor. An ask whose every decision is already determined files straight to standing work, ungrilled. The floor is a standing guard, not a front gate — the same test re-fires whenever a stake-bearing choice surfaces mid-work.
- **grilling asks one question at a time, each carrying a lean** — A grilling pass MUST surface its residual decisions as questions on the queue one at a time, in dependency order, each carrying the machine's recommended answer (the lean) and the one thing that would flip it. The operator settles each by accepting the lean or answering in their own words, so they ratify far more often than they author.
- **a grilling pass yields the contract and the spec delta** — A resolved grilling pass MUST produce the operator-view entry — the contract the result is later validated against — and the spec delta the change will realize, authored by the architect against the concise specs its scan reaches.

## Going deeper

The full requirements and their scenarios are `spec/grilling.md`, this skill's single source.
