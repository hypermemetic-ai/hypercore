surfaced: 2

[Q] The four records split on the spec's authored/derived line: the worker delta and the scenario verdict are *derived*, so the gate can re-run the fence and re-derive their red→green trail; the design-it-twice design-decision and the accepted-length record are *authored*, with no run to reproduce — their only possible trail is structural reachability to a real artifact (a ratified candidate-set tree; an operator-approved length card written through the one seam). Do we accept this asymmetry — the two authored records get reachability-only provenance, structurally weaker than re-execution — or force a single uniform trail across all four?
lean: Accept the asymmetry: bind each record to the artifact its own mechanism necessarily leaves — re-derived red→green for the derived pair, reachability-to-a-ratified-card for the authored pair. This follows the spec directly ("computed, never stored" for derived state; "authored… written through one seam" for the length record), and forcing uniformity means inventing a synthetic "run" for records that have none.
flip: If a role can author a fake candidate-set tree or a fake length card as cheaply as the record itself, reachability proves nothing and the authored pair is effectively unprotected — then collapse to one substrate where only the gate's seam can write the record (prevention, not detection), so a hand-authored copy is structurally impossible rather than merely caught.
answer: Accept the asymmetry — bind each record to the artifact its own mechanism necessarily leaves: re-derived red-green for the derived pair (worker delta, scenario verdict), reachability-to-a-ratified-card for the authored pair (design-decision, accepted-length). This is consistent with the already-ratified threat model — detect the ABSENCE of the trail under a cooperating short-circuit, not out-forge a forger — so detection-by-reachability is correct and the single-write-seam prevention path stays out of scope. Critically, even for the derived pair the re-derived trail proves only that the mechanism RAN, never that the check it ran was ADEQUATE: a real red-green can still test nothing (a vacuous fixture). So this node attests trail-PRESENCE only; check-adequacy is explicitly deferred to gate-vouches-for-the-new-verb and must not be claimed here. Drop the over-claim that the scenario verdict self-certifies or that no recorded verdict is ever believed.

[Q] When a record's trail can't be verified at the fold gate, is that an absolute bar — the tree cannot fold, full stop — or is there a sanctioned path through it: an operator-endorsed override card, and/or a marked genesis exemption for the root records that necessarily predate the gate (chicken-and-egg)?
lean: Absolute bar by default — an unverifiable trail is a mismatched delta, and "a missing or mismatched delta cannot fold" — surfaced with its reason ("never a silent refusal"). Carve exactly one explicit exemption: a minimal, named set of genesis/bootstrap records that are authored-trust roots, like the minimal shared anchor — nothing else folds without a trail.
flip: If legitimate trail-less records arise in normal operation (not just at bootstrap), the absolute bar deadlocks them, and you need a general operator-override card — approve/cut/explain with a durable recorded reason — instead of a one-time genesis carve-out.
answer: Absolute bar by default, re-affirming the ratified position: an unverifiable trail refuses the fold the way a mismatched delta does, surfaced with its reason (no trail — re-run the mechanism), and is never an operator-waveable decision — waving re-opens the exact short-circuit this node forbids. Carve exactly one explicit, named, minimal exemption: the genesis/bootstrap records that necessarily predate the gate, the authored-trust roots like the minimal shared anchor. No general operator-override card, since that would reverse the ratified never-waveable. Nothing but the named genesis set folds without a trail.

[Q] Does the gate apply forward-only — only records produced after it lands must carry a verifiable trail, with existing records grandfathered — or retroactively, treating every record already in the source of truth as suspect until it re-derives?
lean: Forward-only. Re-deriving the entire existing source of truth is large cost, many legitimate records predate the trail mechanism and can't be reconstructed, and a retroactive sweep combined with the hard bar from the previous question would freeze the whole tree. Grandfather what exists; gate everything new.
flip: If the threat model includes fakes already planted before the gate existed — the short-circuit this node exists to forbid may have already happened — forward-only leaves those lies sitting in the operator's source of truth, forcing at least a one-time retroactive sweep to establish a clean baseline.
answer: Forward-only — the gate binds only records folded after it lands; existing records are grandfathered. Rationale: the run-derived trails are torn down at fold by design (the worker fence branch and worktree are removed on every exit, and the fold re-applies the delta as a fresh commit on main rather than merging the fence, so the worker commit is not even in main lineage; the design-it-twice candidate worktrees are likewise removed), so a retroactive bar cannot distinguish a fake from a legitimately-swept trail and would refuse to fold essentially the entire existing corpus while catching only one fake that is already self-marked retracted. Specify the trail as what durably survives, never the ephemeral fence: for the derived pair (scenario verdict, worker RESULT) the trail is RE-DERIVATION — the gate recomputes red-green from the spec at fold and on merged main and stores nothing; for the authored pair the trail is REACHABILITY to the artifact the mechanism already commits — the accepted-length line written through the one accept seam, and the recorded candidate set in design-decision.md (N briefed candidates plus the comparison). Persist no new self-asserted flag (no ran-true boolean, which is the forgeable record this node defeats) and never the torn-down fence branch or candidate worktrees. The authored pair is reachability-only, structurally weaker than re-execution, acceptable under the ratified threat model (the lazy short-circuit, not a forger). Check-adequacy of a re-derived run is deferred to gate-vouches-for-the-new-verb; this node attests trail-presence only.

[CONTRACT]
Every durable record one of hypercore's load-bearing mechanisms is meant to produce — a scenario's red→green verdict, a worker's RESULT and delta, an accepted-length acceptance, and a design-it-twice decision — will, at the fold, have to show the trail that mechanism leaves when it actually runs, and a record that shows none is refused the fold with a flat reason (`no trail — re-run the mechanism`), the same factual way a delta that doesn't apply is refused, never a decision the operator can wave through. Because the running fence is torn down on every exit, the trail is never the fence itself but what durably survives it: for the two *derived* records — the worker's delta and the scenario verdict — the gate re-derives the red→green from the spec at the fold and again on merged main and stores nothing (no "it ran" flag, since a stored flag is the exact forgeable record being closed); for the two *authored* records — the design decision and the accepted-length acceptance — which have no run to reproduce, the trail is reachability to the real artifact the mechanism necessarily commits: the recorded candidate set behind a real contest, and the accepted length written through the one accept seam. This proves only that the mechanism ran, never that the check it ran was adequate — a real red→green can still test nothing — so the guarantee is deliberately narrow: trail-presence only, with check-adequacy left to `gate-vouches-for-the-new-verb` and the irreducibly creative content (a pick's reasoning) recorded honestly as watched, not dressed up as gated; the old claim that the scenario verdict self-certifies, that no recorded verdict is ever believed, is dropped. The catch is scoped to the cooperating short-circuit — a trusted role that conveniently skips the mechanism — not a determined forger who rewrites the trail too. It binds forward only: records folded after the gate lands must carry a trail, existing records are grandfathered, and exactly one named, minimal set is exempt — the genesis/bootstrap authored-trust roots that necessarily predate the gate, like the minimal shared anchor — with no general operator-override. The result is validated by folding each record kind without running its mechanism and seeing the fold refused, by confirming each folds once its mechanism actually ran or its committed artifact is reachable, by confirming the named genesis set folds trail-less while nothing else does, and by confirming no new "ran" flag is persisted and no adequacy is claimed — so the operator's source of truth can no longer be made to show a hand-authored record as a real mechanism's output.

[DELTA]
## ADDED — folding-conditions

### Requirement: a mechanism-output record folds only when its mechanism's trail is present
A durable record a load-bearing mechanism is supposed to produce — a scenario's red→green **verdict**, a worker's **RESULT and delta**, an **accepted-length record**, a **design-it-twice decision** — MUST, at the fold, carry the **trail** the mechanism leaves when it actually runs, and the gate MUST refuse the fold when that trail is **absent**. The threat is the **cooperating short-circuit**: a trusted role with write access that honestly skips the mechanism — no contest, no fenced build, no accept seam, no red→green run — and emits a plausible record byte-indistinguishable from real output. The gate therefore detects the **absence** of the trail, not a forged one: with write access to the repo and to the gate itself a determined forger is out of scope, and the lie being closed is the convenient skip, not sabotage. The records split on the spec's authored/derived line and are attested **asymmetrically**, each bound to the artifact its own mechanism necessarily leaves: the **derived** pair (the worker delta and the scenario verdict) by **re-derivation** — the gate re-runs the touched capability's scenarios red→green and trusts only that transition; the **authored** pair (the design decision and the accepted-length record), which have no run to reproduce, by **reachability** to the durable artifact the mechanism commits. A missing trail is a **dispositive fact**, refused the way `a missing or mismatched delta cannot fold` and `a behavior change folds only when its capability's scenario goes red→green` are — with the reason `no trail — re-run the mechanism` — and is **never** an operator-waveable decision the way depth and vocabulary are: waving it would re-open the exact short-circuit, so the only path past the gate is to run the mechanism, never to author its record.

#### Scenario: a hand-authored authored-record with no seam trail does not fold
- WHEN an accepted-length line claims the accept mechanism's output but no accept seam ever wrote it — a ledger line a role hand-authored to clear the depth gate
- THEN the provenance gate refuses the fold (`no trail — re-run the mechanism`), the spec is left untouched, and the refusal is a fact, not a decision the operator can wave

  ```check
  grow engine/forged.py past-signal
  forge accepted-length engine/forged.py @460
  gate held because provenance
  spec untouched
  ```

#### Scenario: running the mechanism leaves the trail and the record folds
- WHEN the same acceptance is instead recorded through the one accept seam that actually ran
- THEN the trail is reachable and the gate clears — the only way past the gate is to run the mechanism, never to hand-author its record

  ```check
  grow engine/forged.py past-signal
  accept engine/forged.py @460
  gate folds
  ```

### Requirement: the provenance trail is what durably survives the torn-down fence, never the fence and never a self-asserted flag
The trail the gate checks MUST be what **durably survives** the mechanism, never the **ephemeral fence**, because the run substrate is swept on every exit by design: the worker fence branch and worktree are removed and the fold re-applies the delta as a fresh commit on main rather than merging the fence, so the worker commit is not even in main lineage; the design-it-twice candidate worktrees are likewise removed. So for the **derived** pair the trail is **re-derivation** — the gate recomputes red→green from the spec at the fold and again on the merged tree (`folding lands the verified build's code on the merged tree, not only its spec`) and **stores nothing** — and for the **authored** pair the trail is **reachability** to the artifact the mechanism already commits: the accepted length written through the one accept seam (`the accepted-length record is durable authored state, written through one seam`), and the recorded candidate set in `design-decision.md`. The gate MUST persist **no new self-asserted flag** — no `ran:true` boolean, no recorded "the mechanism ran" — because such a flag is precisely the forgeable, hand-authorable record this node exists to defeat: a record that asserts its own provenance is no trail at all. It MUST NOT rely on the torn-down fence branch or candidate worktrees, which no longer exist at fold time.

#### Scenario: a persisted "it ran" flag is never the trail
- WHEN a record carries a self-asserted provenance flag (a hand-written `ran:true` or a stored verdict) but the derived red→green does not re-derive and no authored artifact is reachable
- THEN the gate ignores the flag and refuses the fold (`no trail`) — a record's own assertion that its mechanism ran is not a trail, only re-derivation or reachability to a committed artifact is

  ```check
  build
  integrates
  forge ran-flag
  fold held because provenance
  ```

### Requirement: the provenance gate attests trail-presence, never check-adequacy
The provenance gate MUST attest only that the mechanism **ran and left a trail**, never that the **check it ran was adequate**. Even for the derived pair a re-derived red→green proves the mechanism **ran**, never that it tested the property: a real fenced build with a real red→green can still test nothing — a vacuous fixture. Check-adequacy is the distinct **adequacy** layer, owned by `gate-vouches-for-the-new-verb`, and MUST NOT be claimed here. This **corrects the over-claim** that the scenario verdict is self-certifying or that no recorded verdict is ever believed: the gate does decline to trust a *stored* verdict and re-derives instead, but re-derivation certifies the run, not the judgment. A record's irreducibly creative content — a design decision's reason, a coherence judgment's grounds, the prose a role writes around a verdict — cannot be structurally attested, so it MUST be recorded honestly as **watched**, never scripted as if it were gated.

#### Scenario: a real red→green with a vacuous check is attested for presence only
- WHEN a record carries a real re-derived red→green whose check tests nothing (a vacuous fixture)
- THEN the provenance gate attests the trail is present and makes **no adequacy claim** — whether the check tested the property is deferred to `gate-vouches-for-the-new-verb` and the residue is recorded watched, never certified here

  ```check
  build
  integrates
  provenance attests-presence
  adequacy deferred
  ```

#### Scenario: the creative residue is recorded watched
- WHEN a record carries both a structural trail (the mechanism ran) and irreducibly creative content (its reasoning)
- THEN the gate attests the trail and the creative content is recorded watched, not gated — no fixture certifies the quality of the judgment, and the classification says so rather than overclaiming

  ```check
  contest 2
  recorded
  reason watched
  ```

### Requirement: the provenance gate binds forward-only, with exactly one named genesis exemption
The provenance gate MUST bind **forward-only**: only records folded **after** the gate lands must carry a verifiable trail; records already in the source of truth are **grandfathered**. A retroactive bar is impossible by construction — the run trails are torn down at fold by design, so a retroactive sweep cannot distinguish a fake from a legitimately-swept trail and would refuse essentially the entire existing corpus while catching only one fake that is already self-marked retracted. Exactly **one** explicit, named, minimal **exemption** is carved: the **genesis/bootstrap** records that necessarily predate the gate — the authored-trust roots, like the minimal shared anchor — which fold trail-less because there was no gate to leave a trail for. **Nothing but** the named genesis set folds without a trail: there is **no general operator-override card**, since waving the bar would reverse the never-waveable refusal and re-open the exact short-circuit this node forbids.

#### Scenario: a record folded before the gate landed is grandfathered
- WHEN a record already in the source of truth, folded before the provenance gate landed, is read
- THEN it is grandfathered — the gate does not retroactively refuse it for lacking a trail, binding only records folded after it lands

  ```check
  grandfathered pre-gate
  gate folds
  ```

#### Scenario: a named genesis record folds trail-less and nothing else does
- WHEN a record in the named genesis set (an authored-trust root, the minimal shared anchor) folds with no trail, and, separately, a non-genesis record folds with no trail
- THEN the genesis record folds under its named exemption while the non-genesis trail-less record is refused (`no trail — re-run the mechanism`), and no operator-override clears it

  ```check
  genesis anchor trail-less
  gate folds
  forge accepted-length engine/forged.py @460
  gate held because provenance
  ```

## ADDED — worker

### Requirement: a worker's RESULT is trusted only by re-derivation, never by the fence the fold tears down
A worker's RESULT and refined delta are a **derived** record, so the provenance gate MUST attest them by **re-deriving** the touched capability's scenarios red→green — failing at the fork base and passing at the tip in the fence, and re-verified on the merged tree — and MUST NOT rely on the worker's fence branch or commit as the trail: that fence is removed on every exit and the fold re-applies the delta as a fresh commit on main, so the worker commit is not even in main lineage (`a worker runs fenced in its own git worktree`; `folding lands the verified build's code on the merged tree, not only its spec`). A RESULT hand-authored without ever running a fenced worker leaves no red→green to re-derive — its scenarios do not transition — so it has **no trail** and MUST NOT fold: it is refused with `no trail — re-run the mechanism`, never an operator-waveable decision. This attests that the build **ran**; whether its scenarios test the property is deferred to `gate-vouches-for-the-new-verb`.

#### Scenario: a hand-authored RESULT does not re-derive red→green and is refused
- WHEN a RESULT is handed back that a role authored without a fenced build, and, separately, a RESULT carried by a real fenced build
- THEN the hand-authored one fails to re-derive the touched scenarios red→green and is refused at the gate (`no trail`), while the real build re-derives and folds

  ```check
  build
  integrates
  forge result
  fold held because provenance
  ```

## ADDED — design-it-twice

### Requirement: a recorded design decision carries reachability to its contest's candidate set
The architect's recorded design decision (`design-decision: <subject> → <chosen> — <reason>`) is an **authored** record with no run to reproduce, so the provenance gate MUST attest it by **reachability** to the durable artifact a real contest commits — the **recorded candidate set** (the N briefed candidates and the comparison) in `design-decision.md` (`the architect selects machine-side and records the design decision`) — and MUST NOT rely on the candidate worktrees, which a real `design-it-twice` removes on exit (`a load-bearing interface decision is designed twice, in isolation`). A decision recorded with **no** candidate set reachable behind it — a role that skipped the contest and authored the pick, the byte-indistinguishable fabrication already sitting retracted in `work/worker-builds-proposed-delta/design-decision.md` — has **no trail** and MUST NOT fold: it is refused with `no trail — run the contest`, never an operator-waveable decision. Only the **structural** reachability (a contest's candidate set exists) is gated; the pick's **reason** is irreducibly creative and stays **watched**, never pretend-gated.

#### Scenario: a contest-less design decision is refused
- WHEN a design decision is recorded with no candidate set reachable behind it, and, separately, one whose candidate set a real contest committed
- THEN the contest-less decision is refused at the gate (`no trail — run the contest`), while the one with a reachable candidate set folds, and the pick's reason is watched, not gated

  ```check
  contest 2
  recorded
  forge design-decision
  fold held because provenance
  ```
