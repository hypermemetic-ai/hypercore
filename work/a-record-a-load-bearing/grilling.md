surfaced: 2

[Q] Whose dishonesty must the detector defeat: a *cooperating* role (architect or worker) that honestly short-circuits — skips the contest, the fenced worker, the `accept()` seam, or the red→green run — and emits a plausible record; or a role that *deliberately forges* the mechanism's trail, with full write access to the repo and to the detector itself?
lean: The cooperating short-circuit. Every role here is one of the system's own agents, each with write access to the repo, main, and the gate code; a role determined to forge can commit straight past the gate, fabricate a trail, or rewrite the detector — so cryptographic non-repudiation is unwinnable and isn't the failure we have. The failure we have is sitting in the repo right now: `work/worker-builds-proposed-delta/design-decision.md`, self-marked "⚠ RETRACTED — HAND-FABRICATED, NOT A REAL CONTEST … no isolated candidate designs, no machine-side selection." Detect the *absence of the mechanism's trail*; don't try to out-forge a forger.
flip: A role is ever untrusted — a remote or third-party worker the operator can't vouch for. Then forgery-resistance is the real requirement, and the design needs an external root of trust (a key only the operator or a trusted runner holds, signing the trail) rather than a trail-presence check — a different, much heavier mechanism.
answer: Accept the lean: the threat model is the cooperating short-circuit. Roles are trusted system agents with write access, so detect the ABSENCE of the mechanism's trail (no candidate fences, no red->green run, no accept() seam) rather than attempt forgery-resistance. Not the untrusted-role / external-signing path.

[Q] When the gate cannot establish a record's provenance — the mechanism's trail is missing — should the fold be **refused** (a fact, the way a mismatched delta or a scenario that didn't go red→green refuses), or should it **raise a decision** the operator settles (the way the depth and vocabulary conditions do, honoring "never a silent refusal")?
lean: Refuse. Under the cooperative threat model, trail-presence is a *fact*, not a fallible signal: depth and vocabulary *raise* precisely because length and term-novelty are judgments a human must make, whereas "did the worker's fence exist, did the contest leave its candidate worktrees, did this `accepted:` line come through the one `accept()` seam, did the scenario actually run red→green" are dispositive like delta-applies. The ask wants a record that *cannot lie*; a fact that refuses with a reason ("no trail — re-run the mechanism") is that guarantee. An operator-waveable decision would re-open the exact short-circuit — the operator approving a record on the agent's say-so that it ran.
flip: The trail-check carries false positives that would wedge legitimate work — a real record whose trail is ambiguous, or a mechanism that predates the witness. If the operator would rather adjudicate a *suspected* fabrication than have a heuristic edge case silently block a fold, provenance becomes a raised decision, not a hard gate.
answer: Accept the lean: refuse. Trail-presence is a dispositive fact like 'delta applies' or 'scenario went red->green', not a judgment like depth/length. A missing trail refuses with a reason ('no trail - re-run the mechanism'); it is never an operator-waveable decision, because waving it would re-open the exact short-circuit.

[Q] Should the contract cover all four record types now — scenario verdict, worker RESULT/delta, accepted-length record, design-it-twice decision — each attested at the strength its existing trail affords; or scope the first build to the proven holes and leave the rest honestly *watched*?
lean: All four, each at its affordable strength — the trails already mostly exist, so this is binding records to evidence that's already produced, not minting new machinery per record. A scenario verdict is *already* re-derived (the gate never trusts a stored verdict — it re-runs red→green in the fence and on merged main); an `accepted:` line can be bound to the single `accept()` seam it's meant to pass through; a worker RESULT to its fenced branch and commit; a design decision to the candidate worktrees a real contest leaves behind. A uniform "every mechanism-output record carries provenance" requirement is the deep version; a partial one leaves exactly the lie the ask names open in whichever records it skips.
flip: Attesting the *creative prose* — the design decision's reasoning, the worker's report — turns out to need machinery disproportionate to the structural records. Then gate the structurally-attestable ones first (the verdict, the accepted-length line, the worker delta, the contest's existence) and record the prose portions as honestly watched, never pretend-gated.
answer: Accept the lean: all four record types now, each attested at the strength its existing trail affords - scenario verdict (re-derived red->green), accepted-length record (the one accept() seam), worker RESULT/delta (its fenced branch and commit), and design-it-twice decision (the candidate worktrees a real contest leaves). The uniform 'every mechanism-output record carries provenance' version; do not leave the lie open in any skipped record. Where creative prose cannot be structurally attested, record it as honestly watched, never pretend-gated.

[CONTRACT]
Every durable record one of hypercore's load-bearing mechanisms is meant to produce — a scenario's red→green verdict, a worker's RESULT and delta, an accepted-length acceptance, a design-it-twice decision — will, at the fold, be checked for the trail the mechanism leaves when it actually runs: the red→green re-run that earns the verdict, the writer seam that records the acceptance, the fenced branch and commit a worker builds in, and the candidate contest a real design leaves behind. A record that claims to be a mechanism's output but carries no such trail — one a role hand-authored by skipping the mechanism — is refused at the fold with "no trail — re-run the mechanism," the same flat, factual way a delta that doesn't apply is refused, and never an operator decision to wave (waving it would only re-open the skip). The catch is honestly scoped: it detects the absence of the trail — the convenient short-circuit by a trusted role — not a determined forger who, with write access to the record and the gate itself, rewrites the trail too; closing the lazy lie, not sabotage, is the whole of it. Where a record's content is irreducibly creative — a decision's reasoning, a judgment's grounds — and no trail can attest its quality, the system records that part as honestly watched rather than dressing it as gated. The result is validated by trying to fold each of the four record kinds without running its mechanism and seeing the fold refused, by confirming each one folds once its mechanism actually ran, and by checking the creative residue is marked watched and not pretend-gated — so the operator's source of truth can no longer be made to show a hand-authored record as a real mechanism's output.

[DELTA]
## ADDED — folding-conditions

### Requirement: a mechanism-output record folds only when its mechanism's trail is present
A durable record a load-bearing mechanism is supposed to produce — a scenario's red→green **verdict**, a worker's **RESULT and delta**, an **accepted-length record**, a **design-it-twice decision** — MUST, at the fold, carry the **trail** the mechanism leaves when it actually runs, and the gate MUST refuse the fold when that trail is **absent**. The threat is the **cooperating short-circuit**: a trusted role with write access that honestly skips the mechanism — no contest, no fenced build, no writer seam, no red→green run — and emits a plausible record byte-indistinguishable from real output. The gate therefore detects the **absence** of the trail, not a forged one: with write access to the repo and to the gate itself a determined forger is out of scope, and the lie being closed is the convenient skip, not sabotage. Each kind is attested at the strength its existing trail affords — the **scenario verdict** is already the strongest, since the scenario gate re-derives it red→green in the fence and trusts only the exit codes, so no recorded verdict is ever believed; the **accepted-length record** by the writer seam's commit; the **worker RESULT** by its fence's branch and commit; the **design decision** by the candidate fences a real contest leaves. A missing trail is a **dispositive fact**, refused the way *delta applies* and the scenario gate are — with the reason `no trail — re-run the mechanism` — and is **never** an operator-waveable decision the way depth and vocabulary are: waving it would re-open the exact short-circuit, so the only path past the gate is to run the mechanism, never to author its record.

#### Scenario: a hand-authored record with no trail does not fold
- WHEN a record claims a mechanism's output but the mechanism left no trail — here a ledger line no writer seam wrote
- THEN the gate refuses the fold (`no trail — re-run the mechanism`), the spec is left untouched, and the refusal is a fact, not a decision the operator can wave

  ```check
  grow engine/forged.py past-signal
  forge accepted-length engine/forged.py @460
  gate held because provenance
  spec untouched
  ```

#### Scenario: re-running the mechanism leaves the trail and the record folds
- WHEN the same acceptance is instead recorded through the writer seam that actually ran
- THEN the trail is present and the gate clears — the only way past the gate is to run the mechanism, never to hand-author its record

  ```check
  grow engine/forged.py past-signal
  accept engine/forged.py @460
  gate folds
  ```

### Requirement: a record's irreducibly creative content is watched, not pretend-gated
The provenance gate attests a record's **structure** — that the mechanism ran and left a trail — never the **quality** of the judgment the record carries. A record's irreducibly creative content — a design decision's reason, a coherence judgment's grounds, the prose a role writes around a verdict — cannot be structurally attested, so the system MUST record it as honestly **watched**, and MUST NOT script a watched judgment as if it were gated. The provenance claim stays honest by saying exactly what it proves: the mechanism produced the record, not that the record's reasoning is sound.

#### Scenario: the creative residue is recorded watched
- WHEN a record carries both a structural trail (the mechanism ran) and irreducibly creative content (its reasoning)
- THEN the gate attests the trail and the creative content is recorded watched, not gated — no fixture certifies the quality of the judgment, and the classification says so rather than overclaiming

## ADDED — worker

### Requirement: a worker's RESULT carries the fence's provenance trail
A worker's RESULT and refined delta MUST carry the trail of the fence that produced them — the worker's own branch and the commit it made there (`a worker runs fenced in its own git worktree`) — and the provenance gate MUST check that trail is present before the fold. A RESULT handed back with **no** fence-and-commit behind it — a hand-off a role authored without ever running a fenced worker — has no trail and MUST NOT fold: it is refused with `no trail — re-run the mechanism`, never an operator-waveable decision. The fence's branch and commit are the trail the worker already leaves; this makes their **presence** load-bearing, so a short-circuited build is detectable at the gate rather than passing as real worker output.

#### Scenario: a hand-authored RESULT with no fence is refused
- WHEN a RESULT is handed back with no fenced branch-and-commit behind it, and when a RESULT is carried by its real fence commit
- THEN the trail-less RESULT is refused at the gate (`no trail`), while the fenced RESULT folds

  ```check
  build
  integrates
  forge result
  fold held because provenance
  ```

## ADDED — design-it-twice

### Requirement: a recorded design decision carries the contest's provenance trail
The architect's recorded design decision (`design-decision: <subject> → <chosen> — <reason>`) MUST carry the trail of the contest that produced it — the candidate fences a real design-it-twice leaves, each candidate committing its design on its own branch (`a load-bearing interface decision is designed twice, in isolation`) — and the provenance gate MUST check that trail. A decision recorded with **no** candidate contest behind it — a role that skipped the contest and authored the pick — has no trail and MUST NOT fold: it is refused with `no trail — run the contest`, never an operator-waveable decision. Only the **structural** trail (a contest ran, in isolated fences) is gated; the pick's **reason** is irreducibly creative and stays **watched**, never pretend-gated.

#### Scenario: a contest-less design decision is refused
- WHEN a design decision is recorded with no candidate fences behind it, and when one is left by a real contest
- THEN the contest-less decision is refused at the gate (`no trail`), while the contested decision folds, and the pick's reason is watched, not gated

  ```check
  contest 2
  recorded
  forge design-decision
  fold held because provenance
  ```
