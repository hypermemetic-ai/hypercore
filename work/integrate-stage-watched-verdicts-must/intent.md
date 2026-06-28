---
kind: ask
state: standing
owner: operator
created: 1782641995
---
Integrate-stage watched verdicts must not discard a gate-proven build — preserve-and-decide, one discipline for a failure type now patched four times.

A **watched** judgment on the integrate path (a model call no fixture certifies) can throw away a build the **deterministic** gate already proved sound. By the time `communication.integrate` runs its model judgments, the build has cleared both halves of the gate — its capability's scenarios went red->green (`conditions.verdict` / `scenario.gate`) and the whole system re-verified green on the merged tree (`scenario.reverify`). Yet a watched verdict that refuses sends `worker.run` down `tree.recover` and tears the fence down (`worker.run`'s `finally: teardown`): the ~20-minute verified build is gone, the node re-readies to rebuild from scratch, and only the verified bytes dangling in git let a human rescue it by hand. The deterministic gate is authoritative for **soundness**; a watched verdict discarding what the gate proved is the defect.

This is **one failure type**, seen four times and patched one seam at a time — the whack-a-mole this ask ends:
- `the-fold-s-re-verification` (folded): a re-verify timeout silently reclassified as a broken build.
- `worker-run-is-not-total` (folded): a raised crossing loses its decision card, re-readies, invites a blind retry.
- `the-integrate-stage-coherence-judgment` (folded 2026-06-28): an unreadable coherence reply (the `coherent` flag absent) collapsed into explicit incoherence and refused.
- the **caveat-survival entailment verdict** (`communication.caveat_survives`): over-fired on the very crossing that built the coherence fix (2026-06-28), false-refusing a gate-proven build over a caveat that was not dropped. Crucially this was an **adverse** verdict (`survives: false`), not an *unobtainable* one — so the coherence fix's "unreadable != veto" shape does NOT catch it. Each of the four folded only because a human took the architect seat and hand-re-integrated the gate-proven build, keeping every gated check and the whole-system re-verify intact. That human-in-the-loop is the live blocker between the watchably-driven dispatch and hands-off autonomy.

**Ratified spine (operator, 2026-06-28): preserve-and-decide.** The deterministic gate is authoritative for soundness. A watched verdict at integrate MAY **raise a decision** — the operator-altitude contract miss the gate cannot mechanize, which is why the coherence judgment exists — but MUST NEVER **discard** the verified build. The build is **held**, so settling the decision (or overriding a flake) folds the **same** artifact with no rebuild. An **unobtainable** verdict (absent / unreadable / malformed / errored / timed-out) is retried a bounded number of times, then surfaced as a distinct outcome — never collapsed into a refusal. This is ONE discipline that subsumes the four one-off fixes, not a fifth patch: a watched verdict's worst case is a held build plus a decision the operator settles, never lost work.

To surface in grilling (residue, not pre-resolved):
- **The decided-against disposition.** When the operator settles the decision AGAINST the held build (a genuine contract miss / dropped caveat they confirm), what happens to the preserved artifact: **re-cut** (rebuild from scratch), or **modify the build** (a targeted amend on the verified artifact, cheaper than a rebuild), or a card that offers the operator both. Operator leans toward *offering modify*; unsettled.
- **The load-bearing seam (design-it-twice): where the held build lives across the operator's decision** — the fence persists past integrate; or the verified `WorkerResult` (the captured `CodeFile` bytes + refined delta + base) rides on the decision card and is re-applied at settle; or the build is reconstructed on demand from its commit. Whichever seam wins MUST keep the deterministic gate AND the whole-system re-verify intact at the eventual fold — a held build still re-verifies on merged main, since main may have moved under it (the staleness path `delta.fold` already guards).
- **Scope.** Whether this folds the three landed integrate-family fixes (timeout, lost-card, unreadable) into the one shared seam, or only binds watched verdicts going forward and leaves the landed fixes as instances.

Folding condition: a watched integrate-stage verdict, over a build whose deterministic gate is green, never discards the verified build — it retries an unobtainable verdict, and for an adverse one raises a decision with the build held for a no-rebuild fold; a red->green scenario proves that a flaky OR over-firing watched verdict no longer discards a gate-proven, re-verified build (covering both the unreadable and the caveat-survival shapes); the disposition-on-decided-against and the preservation seam are settled; `python3 -m engine --check` is green.

---

**Update — 2026-06-28 (dispatch grilling settled the design; revert re-grounded the ask). NOT built.**
The hand-cranked dispatch grilled this node to a settled design before the approach was wound down; the
crossing was not built. The settled contract, seam, scope, and disposition are recorded in
`design-decision.md` beside this file. Two things the next build must read first:

- **The design is settled.** Seam **B** (the verified `WorkerResult` held as material on the decision
  node, re-folded at settle), scope **subsume**, and the decided-against disposition **offer modify
  (both)** — operator-settled directly 2026-06-28, so this node builds the seed-fence-from-held-artifact
  "modify" seam. No open forks remain.
- **The ask re-grounded smaller.** `worker-run-is-not-total` was **reverted** as a manual-path-only
  guarantee (and is a different shape — a raise, not an adverse verdict) and is **no longer an instance**
  of this ask. The timeout and coherence-unreadable instances are each already individually folded. So
  the genuinely-open core is the **adverse** watched verdict (caveat-survival, `survives: false`) still
  discarding a gate-proven build — see `design-decision.md` for the full re-grounding. The "seen four
  times" framing above is the original filing; the operator owns the narrowed scope when this is built.

---

**Update — 2026-06-28 (the CORE landed, architect-direct; this node stays open for the modify slice).**
Built directly in the architect seat (not a fenced crossing — the fix IS the machinery that makes a
crossing safe, so a fence would risk the very discard it cures; operator-settled). Landed in `f511b7b`,
`--check` green:

- **preserve-and-decide core (done).** An adverse watched verdict (incoherence / dropped-caveat) over a
  gate-proven build now **holds** the verified `WorkerResult` as durable material on the node
  (`communication.hold_build`), surviving the fence teardown; settling by **override**
  (`communication.settle_held`) re-folds the **same** artifact through the unchanged `delta.fold` with
  **no rebuild**. Gated red→green in `spec/coherence.md` ("a watched verdict never discards a gate-proven
  build"), staged through real apply + integrate + teardown in `coherence_world`. The window wires the
  operator's override (watched). This **removes the blocker** — a flaky/over-firing watched verdict can
  no longer throw away a gate-proven build.
- **still open (the second slice).** The **modify** disposition — `seed-fence-from-held-artifact` for a
  targeted amend when the operator confirms the verdict was *right* — and **subsuming** the already-folded
  timeout / coherence-unreadable fixes under the one shared seam. Seam B and "offer modify (both)" stay
  the settled design in `design-decision.md`. The folding condition is met for the core but not for the
  modify seam, so this node does not fold yet.

---

**Update — 2026-06-28 (two findings from dogfooding the core on interface slice 2).**
The first fenced crossing since the core landed (interface slice 2) exercised preserve-and-decide
end-to-end: the `caveat_survives` watched verdict over-fired on a gate-proven, coherence-passed build; the
build was **held** (not discarded), the operator settled by **override**, and `settle_held` re-folded the
same artifact with no rebuild (`177d34e`). The core worked as designed. Two residues surfaced for the
modify slice to subsume:

- **`caveat_survives` over-fires systematically — the verdict itself is miscalibrated, not just its
  discard behavior.** It has now false-refused **3/3** gate-proven interface/engine builds it has seen (the
  coherence-fix crossing, interface slice 1, interface slice 2). The core fix made each survivable (held +
  override), but a watched check that is wrong every time it fires is noise the operator pays a decision
  for. The modify slice (or a sibling) should narrow the `caveat_survives` entailment prompt/seam so it
  stops firing on builds whose contract caveat is already carried — the held-build path is the safety net,
  not the cure for a bad verdict.
- **`settle_held` leaves the held-build.json in the archive (~92K of base+tip bytes per overridden
  build).** A successful override-fold archives the node with its `held-build.json` intact — honest
  provenance, but it grows the archive by the full size of the touched files on every override, against the
  legible-minimal-tree bar. The modify seam should drop (or decline to archive) the held artifact once the
  fold lands, keeping only the verdict record.

---

**Update — 2026-06-28 (finding 1 was misdiagnosed; the real defect found and fixed from recovered evidence).**
Finding 1 above — "`caveat_survives` over-fires, the verdict is miscalibrated, false-refusing over a caveat
that was not dropped" — is **wrong**, and acting on it (loosening the entailment bar) would have **broken
the safety property**, silently crossing dropped caveats to the operator. The three over-fire `(say,
caveat)` pairs, believed lost with the torn-down fences, were **recovered** from Claude Code's per-call
session logs (`~/.claude/projects/-home-qqp-projects-hypercore/`, the live `claude -p` coherence/entailment
calls). Reading them settles it: in **all 3**, the architect's `say` was a confident headline and the
load-bearing caveat — each a *"this part is watched, not gate-proven"* hedge — was **genuinely dropped**
from the words that cross. The verdict fired **correctly 3/3**. It is not miscalibrated; it is a working
alarm.

The true defect is the one this node's filing already half-named: a misinterpretation **baked in at
construction**. `spec/communication.md` intends caveat-survival as the architect's **clarity self-check on
its own draft** — "edits expression only, never the decision." It was *built* as an operator-escalation
gate: a dropped caveat raised a **re-cut/abandon decision** on the operator's queue. A wording self-repair
became a decision the operator pays for — which is exactly why the alarm read as noise. Fixed by realigning
the build to the spec's intent (architect-direct, same rationale as the core — the fix is the caveat
machinery itself):

- **A dropped caveat is now redrafted, not raised.** `communication.carry_caveat` re-asks the architect to
  rewrite its own operator-facing words to carry the caveat in its stress position (`communication.REDRAFT`),
  re-runs the watched entailment verdict over the revision, bounded `CAVEAT_ATTEMPTS` times, then crosses the
  corrected words. The `ENTAILMENT` verdict is **unchanged** — it was always right.
- **Only a caveat the wording cannot carry escalates** — after the bound, a held-build decision (the rare
  contract-level miss past the render), preserving preserve-and-decide. Spec requirement + scenario rewritten
  (`a dropped caveat is redrafted to carry it`); the `communication` skill re-rendered; gated red→green with
  `redrafted-crosses` / `escalates-held` in `communication_world`; `python3 -m engine --check` green.
- **Residue 2 (`settle_held` archive cruft) is untouched** — still open for the modify slice.
