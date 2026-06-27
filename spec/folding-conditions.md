# folding-conditions

The conditions a tree's material must meet to fold — the engineering standards made into **guards**.
A guard is a pure predicate the system evaluates over a node's material and state to decide whether a
transition may fire; it decides, it never acts. The self-model owns the delta and the atomic merge;
this capability owns the guards on the `fold` transition — run over the material a worker produced, at
the archive stage before the merge — while readiness (`tree.ready()`) is their sibling on the
`dispatch` transition. One vocabulary, two transitions: a guard says when a node may move, never what
moving does. Advice can be ignored; a folding condition cannot, so the standards bite by construction
rather than by a reviewer remembering them.

The keystone condition is the **scenario gate**: a behavior change folds only when the
**architect-authored scenario** of the capability it touches goes red→green — failing at the fork
base (the behavior was not yet built) and passing at the tip. The oracle is the self-model's own
account of the behavior (`spec/<capability>.md`), not a command the worker records about its own
work; the builder can no longer author the check that judges it. The other conditions are the
**delta applies** (a non-negotiable fact — the spec never merges a delta that does not land cleanly)
and **depth**: a **judgment** where length is one signal of a deep module, never the criterion, so a
file past the length signal raises a **decision** — re-cut, deepen, or accept-with-reason — held on
the operator's queue, never an auto-refusal and never a silent pass.

### Requirement: a behavior change folds only when its capability's scenario goes red→green
A behavior-changing tree MUST fold only when the **architect-authored scenarios** of the capabilities
its delta touches go red→green: the scenarios, as they stand at the tip, are run in the fence at the
**fork base** (they MUST fail — the behavior was not yet built) and at the **tip** (they MUST pass),
and only the exit codes are trusted. A capability whose scenarios already pass at the base did not have
its behavior driven by this change; one whose scenarios fail at the tip is not green. The worker records
**no loop** — the check it must turn green is the self-model's own scenario, authored by the side that
does not build it, so a fabricated or self-serving oracle cannot fold. A capability the change touches
that carries **no** executable scenario is *watched*, not faked. The gate is itself engine machinery: it
cannot certify itself from inside a fold, so the acceptance harness exercises its red→green directly.

#### Scenario: a change whose scenario transitions red→green folds
- WHEN a tree's delta touches a capability whose scenarios fail at the fork base (the behavior absent)
  and pass at the tip (the behavior built)
- THEN the scenario gate is met for that capability and the fold may proceed

#### Scenario: a change whose scenario does not transition is held
- WHEN a touched capability's scenarios already pass at the fork base, or do not pass at the tip, or
  cannot run in the fence
- THEN the fold is refused — a scenario that did not go red→green did not prove the change drove the
  behavior, and narration is never the gate

### Requirement: length past the signal raises a decision, never a silent refusal
A source file a tree created or grew past the **length signal** trips the depth guard — the system's
**one escalating guard**. Where an ordinary guard that fails simply withholds its transition, this one
MUST **raise**: it neither passes silently nor refuses on its own, but escalates a **decision** —
re-cut, deepen, or accept-with-reason — held on the operator's queue, and holds the fold pending it. It
thus escalates rather than resolving length itself — neither auto-refusing nor silently passing. Length is a context-cost signal — every line
is context an agent must load — not a verdict on depth, and there is **no hard length ceiling**:
even a far-over-signal file raises a decision the operator can accept, never an outright
refusal (a number standing in for the judgment of depth is the error being removed). The fold
is held until the decision is settled, and an **accepted-length record**
accepting the file lets it fold. The condition is scoped to the files the tree itself touched.

#### Scenario: a tree grows a module past the signal
- WHEN a tree's material adds or grows a source file past the length signal and no
  accepted-length record accepts it
- THEN a decision (re-cut / deepen / accept-with-reason) is raised, the fold is held, and
  the spec is left untouched — never a silent refusal and never a silent pass

  ```check
  grow engine/giant.py past-signal
  gate held because depth names engine/giant.py
  spec untouched
  ```

#### Scenario: an accepted-length record accepts the length
- WHEN an accepted-length record names the file as accepted **at a stated length** and
  the file is still within that length
- THEN the depth condition is met for that file and the fold may proceed

  ```check
  grow engine/wide.py past-signal
  accept engine/wide.py @460
  gate folds
  ```

#### Scenario: a coincidental mention is not an exception
- WHEN a record accepts a *different* file whose path merely contains the name as a substring,
  with no accepted-length record accepting the file itself
- THEN the file is not cleared and the decision still stands — the exception is the
  decision matched on the path, not a spelling that coincidentally appears

  ```check
  grow engine/wide.py past-signal
  accept engine/wide-helper.py @900
  gate held because depth names engine/wide.py
  ```

### Requirement: an accepted length is bounded to the length it names, and ratchets
An accepted-length record MUST accept a file **at a stated length** (`@<N>`), and that
acceptance is bounded to it: it clears the gate only while the file stays within the accepted
length plus a small **materiality margin**, so a one-line edit past the bar does not re-open a
settled decision. A file that grows **materially past** the length it was accepted at MUST re-raise
the decision — acceptance ratchets, it does not silence later growth — and renewing the
acceptance at the new length raises the bar. A stable file stays cleared; the bar
lives in the record, so a shrink never lowers it. A record with **no stated length** (no `@<N>`)
names no bound and MUST NOT clear the gate — the exception is the decision *at a stated size*, not
the spelling. When several records name one file, the highest accepted length governs (the ratchet
only rises).

#### Scenario: an accepted file grows materially past its bar
- WHEN a file an accepted-length record accepted at length N grows materially past N (beyond the margin)
- THEN the decision is re-raised at the new length and the fold is held until it is renewed —
  the old acceptance does not silence the growth, and renewing it at the new length clears it

  ```check
  grow engine/grown.py 800
  accept engine/grown.py @460
  gate held because stale
  accept engine/grown.py @800
  gate folds
  ```

#### Scenario: the ratchet only rises
- WHEN a file accepted at length N is re-accepted at a *lower* length and then grown within N
- THEN it stays cleared — a re-acceptance at the same or a lower length writes nothing, so the bar
  only ever rises

  ```check
  grow engine/risen.py 850
  accept engine/risen.py @800
  accept engine/risen.py @400
  gate folds
  ```

#### Scenario: a record with no stated length names no bound
- WHEN an accepted-length record names the file with no `@<N>`
- THEN it does not clear the gate — an acceptance must name the length it is bounded to

  ```check
  grow engine/bare.py past-signal
  accept engine/bare.py none
  gate held because depth
  ```

### Requirement: the accepted-length record is durable authored state, written through one seam
The accepted-length record is the gate's one piece of **live authored state**, and it MUST outlive
the work that grew the file past the signal: the file stays long after its tree folds, so the record
cannot ride a node (a node archives with its work) and is not re-derived on fold like the channels.
It MUST therefore live in **one durable store**, read and written through a **single seam** — the
gate reads the accepted length, and one writer records it — so the store's location is a hidden
decision and the record can never be written two ways. The writer **ratchets**: it records a higher
length and is a no-op at an already-cleared one.

#### Scenario: the writer records an accepted length the reader then honors
- WHEN the one writer records a file accepted at a length the file is within
- THEN the gate reads that length back from the one durable store and clears the file — one seam over
  one store, the writer the only producer of the record the reader honors

  ```check
  grow engine/relocated.py past-signal
  accept engine/relocated.py @460
  gate folds
  ```

### Requirement: a standard is gated by carrying a scenario, watched without one
The system MUST carry an honest, **machine-readable** account of which standards are mechanically
gated and which are only watched — but it MUST NOT hand-maintain a separate register that can drift
from the gates it names. The classification is **derived**: a requirement is **gated** exactly when one
of its scenarios carries an executable `check` block (a scenario fails unless the behavior holds), and
**watched** when none does — model-side judgment no adversarial fixture can certify (depth as a module
judgment, coherence, the grilling floor's finding, the design-it-twice pick), honestly recorded as not
mechanically enforced. Because the block's **presence is the classification**, a regenerating author
cannot script a watched judgment and call it gated, and the register cannot disagree with reality —
there is no register, only the scenarios.

#### Scenario: the classification is read off the scenarios
- WHEN the gated/watched classification is read for a capability
- THEN each requirement is gated if one of its scenarios carries a check block and watched otherwise —
  derived from the scenarios themselves, never separately authored, so it cannot drift from what is gated

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
