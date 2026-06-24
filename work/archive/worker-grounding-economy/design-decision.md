# design-it-twice — the worker's grounding interface

**Provenance of this contest (read first).** Authored by the architect **by hand**, not as fenced
candidate runs. The design-it-twice transport spawns each candidate in its own worktree fence — the
same `worker_transport` that just died at `E2BIG`; the fenced contest cannot run until this very
decision lands. So there are no candidate worktrees behind this record, and it does not claim any.
The candidates below are genuinely distinct designs developed on their own briefs, then compared — not
a winner dressed as a contest (the retracted `worker-builds-proposed-delta` decision is the failure
this avoids).

## The interface under contest
The worker's **grounding**: what reaches the worker, and through which channel — inlined in the
assembled prompt (`worker.prompt`/`worker.context`) versus read from the worker's fenced **checkout**,
where the whole repo already sits on disk. Today: the prompt inlines every capability in full (`scan` =
the untouched bodies, 70 %). The seam in question is the line between *prompt-inline* and
*checkout-read*, and what stands in for a body that is not inlined.

## Candidates

### C1 — minimize what's inlined (index + JIT bodies)
Inline: disciplines, ask, delta, the **touched** capabilities in full (plus `depth`, always), and a
high-signal **index** of every other capability — name + its `<!-- vision -->` line + its
`### Requirement:` titles. A full untouched body is **read JIT from `spec/<name>.md` in the fence**
when the rescan implicates it. *Hides:* the load policy ("full iff touched, else index + read"). *Seam:*
inline = touched-full + all-index; checkout = untouched bodies (already on disk). *Deletion test:* drop
the index → myopia returns (can't spot a mis-named/missed capability); drop the JIT read → can't verify
an implicated one — both load-bearing, so the pair is one deep module. *Cost:* the index must be
genuinely high-signal; a read round-trip per implicated body.

### C2 — maximize fidelity within budget (dependency neighborhood full + far index)
Inline touched **and their dependency neighborhood** (capabilities they cross-reference) in full; index
only the far rest. *Seam:* needs a spec-level dependency graph (architecture-review's cycle scan is the
seed). *Deletion test:* drop the neighborhood expansion → lose locality that catches a cross-capability
mis-mapping without a round-trip. *Cost:* more mechanism; and at the spec level nearly everything
references `tree`/`depth`/`communication`, so the neighborhood risks engulfing most of the spec —
undercutting the saving the whole contest exists for.

### C3 — keep whole-preload, cut the source
Leave the grounding seam unchanged; instead cut the spec+glossary's own **excess** (architecture-review
at the source) until the whole preload fits with margin. *Seam:* unchanged. *Cost:* does not address
the **structural** defect — even a trimmed whole-spec is still mostly untouched per task, so every token
keeps spending budget every episode; the saving is one-time and erodes as the spec grows. Loses on
signal-density, the axis the evidence names.

### C4 — pure JIT (no index)
Inline disciplines+ask+delta+touched; point the worker at `spec/` in its checkout, no index. *Deletion
test:* there is no index to delete — the worker is **blind** to capabilities it does not think to read.
*Cost:* smallest prompt, but sacrifices the myopia-defense `role-assembly` re-litigated twice to keep —
"the pull is gated on the worker realizing it needs to look." Loses on the settled constraint.

## Selection — depth, locality, seam placement
- **C4** is out: it sacrifices myopia-defense, the constraint the operator settled twice.
- **C3** is out: it makes the bad prompt smaller, not high-signal; the structural cost recurs every
  episode and erodes. Not deep — no new interface, the smell stays.
- **C2 vs C1:** C2 buys locality but at real mechanism cost, and its neighborhood plausibly engulfs the
  spec (universal `tree`/`depth` references), so it under-delivers the economy. C1 is the **deepest small
  interface**: one rule — *full iff touched, else index + read-on-demand* — hides the entire load policy,
  preserves myopia-defense through the **full index** (the worker still sees every capability and pulls
  the body it implicates), and places the seam where the bodies **already live** (the fenced checkout),
  so the JIT channel costs no new storage. Index machinery is nearly present (`grill._digest`).

**Pick: C1**, with one C2-flavored refinement folded in — the index carries each capability's **vision
line + requirement titles** (not just its name), so the worker has the dependency signal to decide what
to pull without inlining neighbors. Expected assembled prompt ≈ 73 KB (from 131 KB): the 92 KB of
untouched bodies collapse to a ~6 KB index; `disciplines`, `depth`, touched, and `glossary` stay full.
Bounded as the touched set grows, because the index of the rest shrinks in step.

design-decision: worker-grounding → index-plus-JIT-bodies (C1) — foreground touched in full, carry every other capability as a vision+requirements index, read a full body JIT from the fenced checkout; preserves the whole-picture myopia-defense at ~5–10% of the token cost and places the seam where the bodies already live.

## The stake-bearing difference → re-enters grilling
The pick **supersedes `role-assembly`'s whole-spec-preload** — a decision the operator personally
re-litigated twice. That is operator-stake by the design-it-twice floor, so it does not fold on
machine-side judgment alone: it carries to the operator as a ratification. The architect-authored stake:
*we stop inlining the 70 % of the spec a given change does not touch and hand the worker a full index it
reads from on demand — keeping the whole-picture defense role-assembly wanted, at a fraction of the
attention budget, and bringing the prompt back under our own context-engineering standard.*
