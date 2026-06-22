---
name: design-it-twice
description: hypercore's design-it-twice methodology — design a load-bearing interface as a contest of isolated candidates, then pick or hybridize on depth, locality, and seam placement. Load when designing or judging a load-bearing interface decision.
---

# design-it-twice

The judgment use of the worktree concurrency. The fence that isolates a
worker for throughput also isolates several candidates for design quality: for an interface the
architect judges load-bearing, the decision is **designed twice** — several candidates, each in
its own fence, each briefed to design the *same* interface radically differently — and the
architect picks or hybridizes on **depth, locality, and seam placement**. The first shape
committed is rarely the deepest, so design-it-twice applies hypercore's existing isolation where
first-draft commitment hurts most: the shape of a deep module. *(ADR 0007.)* It rests on the worker's fence composing —
several candidates advancing one decision at once, isolated, exactly as concurrent workers
advance the graph at once.

## The disciplines — what good looks like

- **a load-bearing interface decision is designed twice, in isolation** — A load-bearing interface decision MUST be designable as a contest of several candidates, one per brief (minimize the interface / maximize flexibility / optimize the common caller / ports-and-adapters), each running in its own fence — the worker's worktree, tagged per candidate — so the candidates advance the same decision at once, isolated from each other and the main line. The architect judges an interface load-bearing; the depth gate's "cannot deepen in place" is the second entry. *(Load-bearing judgment: ADR 0007. Depth's second entry: ADR 0006.)*
- **candidates design, they do not implement** — A candidate MUST produce an interface **design** — the interface, what it hides, where the seam falls, and the deletion-test argument for its depth — not a built-out implementation. Depth, locality, and seam placement are judgable from the design; building each candidate out would throw most of the work away. The winning design carries forward as the contract for one ordinary worker apply.
- **the architect selects machine-side and records an ADR** — The architect MUST compare the candidates on **depth, locality, and seam placement**, pick one or hybridize, and record the pick as a **structured design-decision ADR** — a parseable `design-decision: <subject> → <chosen> — <reason>` line, the same structured-record idiom the depth-decision uses. The selection is machine-side design judgment: the operator's trust anchor is the contract, not the machine-side design, so the pick does not spend the operator's go. The candidate designs and the reasoning stay machine-side — in the fences and the ADR — never on a card. *(Trust anchor is the contract: ADR 0007.)*
- **a stake-bearing difference re-enters grilling** — WHEN the comparison reveals a difference the operator has a stake in — operator-visible behavior, hard to reverse, or real cost — the architect MUST raise it as a decision card parented to the decision node (the standing-guard floor), carrying only the architect-authored stake. The interface shape stays machine-side; only a stake-bearing behavioral difference crosses to the operator.

## Going deeper

The full requirements and their scenarios are `spec/design-it-twice.md`, this skill's single source.
