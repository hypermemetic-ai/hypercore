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
first-draft commitment hurts most: the shape of a deep module. It rests on the worker's fence composing —
several candidates advancing one decision at once, isolated, exactly as concurrent workers
advance the tree at once.

## The disciplines — what good looks like

- **a load-bearing interface decision is designed twice, in isolation** — A load-bearing interface decision MUST be designable as a contest of several candidates, one per brief (minimize the interface / maximize flexibility / optimize the common caller / ports-and-adapters), each running in its own fence — the worker's worktree, tagged per candidate — so the candidates advance the same decision at once, isolated from each other and the main line. The architect judges an interface load-bearing; the depth gate's "cannot deepen in place" is the second entry.
- **candidates design, they do not implement** — A candidate MUST produce an interface **design** — the interface, what it hides, where the seam falls, and the deletion-test argument for its depth — not a built-out implementation. Depth, locality, and seam placement are judgable from the design; building each candidate out would throw most of the work away. The winning design carries forward as the contract for one ordinary worker apply.
- **the architect selects machine-side and records the design decision** — The architect MUST compare the candidates on **depth, locality, and seam placement**, pick one or hybridize, and record the pick as a **structured design decision** — a parseable `design-decision: <subject> → <chosen> — <reason>` line, the same structured-record idiom the accepted-length record uses. The selection is machine-side design judgment: the operator's trust anchor is the contract, not the machine-side design, so the pick does not spend the operator's go. The candidate designs and the reasoning stay machine-side — in the fences and the recorded design decision — never on a card.
- **a stake-bearing difference re-enters grilling** — WHEN the comparison reveals a difference the operator has a stake in — operator-visible behavior, hard to reverse, or real cost — the architect MUST raise it as a decision card parented to the decision node (the standing-guard floor), carrying only the architect-authored stake. The interface shape stays machine-side; only a stake-bearing behavioral difference crosses to the operator.
- **a recorded design decision carries reachability to its contest's candidate set** — The architect's recorded design decision (`design-decision: <subject> → <chosen> — <reason>`) is an **authored** record with no run to reproduce, so the provenance gate MUST attest it by **reachability** to the durable artifact a real contest commits — the **recorded candidate set** (the N briefed candidates and the comparison) in `design-decision.md` (`the architect selects machine-side and records the design decision`) — and MUST NOT rely on the candidate worktrees, which a real `design-it-twice` removes on exit (`a load-bearing interface decision is designed twice, in isolation`). A decision recorded with **no** candidate set reachable behind it — a role that skipped the contest and authored the pick, the byte-indistinguishable fabrication already sitting retracted in `work/worker-builds-proposed-delta/design-decision.md` — has **no trail** and MUST NOT fold: it is refused with `no trail — run the contest`, never an operator-waveable decision. Only the **structural** reachability (a contest's candidate set exists) is gated; the pick's **reason** is irreducibly creative and stays **watched**, never pretend-gated.

## Going deeper

The full requirements and their scenarios are `spec/design-it-twice.md`, this skill's single source.
