surfaced: 3

[Q] The gated (mechanical) floor is "a term used but undefined." To be gated it must compile to a deterministic check block, so "a term" has to be identifiable with no model. What is the mechanical signal?
lean: Glossary-set, no marking — the gated floor reads the glossary↔corpus set-difference in the deterministic direction (a defined term unused anywhere in the live corpus), and "used-but-undefined NEW term" detection moves to the watched/semantic half (the dedicated run, already provisioned, cheap because the corpus fits one context window). Why: bold is already overloaded for emphasis across the corpus, so making "marked = term" gated would be noisy and would punish the dense house voice — the exact gameable-metric failure clarity warns against.
flip: If the operator wants the gated floor to literally catch "used but undefined" at fold time without waiting on the watched run, adopt a marking convention and make a marked-as-coined term with no glossary.md entry the gated floor — at the cost of making a writing convention enforceable.
answer: Resolved on the communication-clarity evidence the operator pointed to (research.md §A2; synthesis.md). The evidence settles the scope and confirms the direction: "the rule binds the defined concept vocabulary, not every token" — so the term-set IS the glossary and no marking is made load-bearing; "No readability gate — judge cohesion, never length" (a metric "penalize[s] precise terms") — so the gated floor is glossary↔corpus closure (a defined term fallen out of use, a dispositive set-difference, never a metric); and the watched half is sharpened to guard the "chunk economy, not just tidiness" — a defined concept under a synonym (Fowler's "elegant variation" vice) or the language casually expanded by a term earning no distinct chunk. Not the marking path.

[Q] D19 requires the watched half to emit a trace the fold checks for presence. What is that trace, and who owns the fold-side check — given a-record-a-load-bearing (open) is building the general "a record folds only when its mechanism's trail is present" gate that would subsume it?
lean: Self-contained trace — the run commits its verdict over the named corpus snapshot on the node (clean, or the findings and their define/waive/dismiss settlement), and vocabulary-check builds its OWN fold-side presence check. Keeps the vehicle independent of a-record's unbuilt gate so the back-half run isn't blocked on it; a-record later generalizes and absorbs this one trace-check.
flip: If the operator would rather not build a trace-check a-record will immediately generalize, the watched half emits the trace only and defers the fold-side presence check to a-record — sequencing a-record first and giving up the vehicle's independence.
answer: Accept the lean: self-contained trace. The run commits its verdict on the node; vocabulary-check builds its own fold-side trace-presence check, independent of a-record's general gate, so the back-half run is not blocked on it; a-record later subsumes this one trace-check.
re-fired: a-record-a-load-bearing folded (f82eee1). The lean's whole reason was sequencing — keep the back-half run unblocked on a-record's *unbuilt* gate. That gate is now built, and depth-scan (the flagship) names this same model-run-leaves-a-trace pattern as its core. Re-surfaced to the operator as one choice — build the "did the model-run happen?" trail once and share it, or give vocab a throwaway copy. Operator chose **build it once, shared**. So the watched half no longer builds its own trace-presence check: it rides a new **watched-evidence trace** clause on a-record's provenance gate — the trail a watched model-run leaves (a verdict committed on the node), attested by presence, never re-derived. The gate gains its third trail type; vocab is its first consumer, depth-scan the next. The seam is load-bearing (two consumers), so the build runs design-it-twice on it.

[Q] (surfaced mid-build — the grilling floor is a standing guard) Building revealed that the watched half, as ratified ("a missing trace holds the fold"), halts the autonomous loop: `conditions._vocabulary` holds every fold until a vocab-run verdict is committed on the node, but nothing in the fold pipeline invokes that run (`commit_verdict` is called only by test worlds). So the guard blocks on a run that never happens — the harness is green only because the fixtures commit a verdict. How to resolve before folding?
lean: Ship the gated floor live-and-blocking; defer the watched model-run half to **non-blocking** until its run is built — the honest "not yet" posture the model-driven depth scan's watched half already takes (`DEPTH_NOT_YET`). The loop keeps folding, the deterministic floor (a defined term gone dead) guards now, and the provenance watched-evidence seam still ships for depth-scan to ride; the blocking re-arms automatically when the run lands.
flip: If the corpus-drift the node was filed against is mostly the synonym/conflict drift the model-run catches (not the dead-term floor), build the run-invocation now instead — wire `integrate` to run the vocab check and commit its verdict each fold — accepting the larger scope and a strong-model call on the fold hot path.
answer: Ship floor live, run-half deferred (operator). The gated floor holds the fold on a dead defined term; the watched half rides the provenance watched-evidence trail but does **not** hold the fold until the run mechanism exists, named honestly as not-yet the way depth's watched half is. The provenance seam ships and is tested at its own layer. Deferred from this fold's delta: the vocab "a missing trace holds the fold" scenario — it re-arms when the run lands.

[CONTRACT]
hypercore's shared language gains a standing guard so the corpus can no longer drift from its own glossary the way it silently drifted ~16 terms behind the built system. At every fold a **vocabulary check** runs over the whole live corpus — `glossary.md`, `intent.md`, and the spec — communication's **consistency** standard, the guard the one-term-one-concept rule already names but never had. It has two halves, at the two strengths a standard can take. A **gated** mechanical floor catches a dispositive fact: a term `glossary.md` defines that the live corpus no longer uses — the glossary and the language fallen out of step — read as a string set-difference, never a readability metric that would punish precise prose. A **watched** semantic half — a single dedicated run, cheap because the whole corpus fits one context window — reads the corpus for **new or conflicting** vocabulary: a defined concept reappearing under a synonym (elegant variation) or the shared language casually expanded by a term that earns no distinct chunk, guarding the chunk economy the ubiquitous language rests on. A gated finding — a defined term gone dead — raises a **define / waive / dismiss** decision on the operator's queue and **holds the fold** until it is settled, the length-signal pattern applied to words, and the architect never carries it. The system's one new mechanism is the **watched-evidence trace**: a capability-agnostic trail a-record's provenance gate gains — the verdict a watched model-run commits on its node, attested by presence and never re-derived (a watched judgment has no red→green to reproduce) — which the model-driven depth scan will ride next. Vocabulary-check's own watched half rides the same seam, but the dedicated run that would commit the verdict is **not yet built**, so that half is held **not-yet** — named honestly the way the depth scan's watched half is (`DEPTH_NOT_YET`), non-blocking until the run lands — and the gated floor is the live guard in the meantime. The result is validated by growing the corpus out of step with its glossary and watching the gated floor raise the decision and hold the merge, by the provenance gate attesting a committed watched verdict present and refusing an absent one, by a corpus consistent on its floor folding through, and by `python3 -m engine --check` carrying the acceptance and staying green.

[DELTA]
## ADDED — communication

### Requirement: the defined vocabulary stays consistent — the vocabulary check
The shared language MUST stay consistent across the live corpus: the **defined concept vocabulary** of
`glossary.md` is the ratified set, and the system holds the corpus to it. This is communication's
**consistency** standard, the **vocabulary check** the one-term-one-concept rule already names ("synonym-
variation of a defined term being a clarity bug the vocabulary check guards"). It binds the **defined
concept vocabulary, not every token** — ordinary words and pronouns are not terms. It has two halves at
the two strengths a standard takes. Its **mechanical floor is gated**: a dispositive, non-gameable fact —
a term `glossary.md` defines that the live corpus no longer uses (the glossary fallen out of step with the
language), read as a string set-difference, **never a readability metric** (a metric is gamed and punishes
precise terms — `communication`'s own "no readability gate"). Its **semantic half is watched**: a single
dedicated run reads the whole corpus for **new or conflicting** vocabulary — a defined concept reappearing
under a **synonym** (Fowler's "elegant variation" vice) or the language **casually expanded** by a term
that earns no distinct chunk — a judgment no fixture can certify, guarding the **chunk economy** the
ubiquitous language rests on, recorded as watched and never pretend-gated.

#### Scenario: a synonym for a defined concept is a watched finding
- WHEN the corpus names a defined concept under a synonym, or expands the shared language with a term that
  earns no distinct chunk
- THEN the watched run surfaces it as a finding for a define / waive / dismiss decision — a judgment no
  fixture certifies, recorded as watched, not pretend-gated

## ADDED — folding-conditions

### Requirement: the provenance gate attests a watched-evidence trace
The provenance gate MUST attest a third trail type beside the authored records it already reaches (the
accepted-length record, the design decision): a **watched-evidence trace** — the verdict a **watched**
mechanism commits on its node when it runs. A watched mechanism is a model-run whose judgment no fixture
can re-derive — it leaves no red→green to reproduce — so its only honest trail is **presence**: the gate
attests that the run's verdict trace is committed on the node, and refuses (`no trail — re-run the
mechanism`) when a fold carries a watched standard but no such trace. The attestation is
**capability-agnostic** — it reaches "a watched run committed its verdict on the node," never any one
capability's content — so the single seam serves every watched standard (the vocabulary check, the
model-driven depth scan). Like the gate's other trails it is **presence only** (`Attestation.adequacy`
deferred, `residue` watched): it proves the run happened, never that its judgment was sound.

#### Scenario: a watched run's committed verdict is a present trail
- WHEN a watched mechanism committed its verdict trace on the node
- THEN the provenance gate attests the trail present — presence only, the judgment's soundness still watched

  ```check
  watched-run committed-verdict
  provenance attests present
  ```

#### Scenario: a watched run with no committed verdict has no trail
- WHEN a fold carries a watched standard but no verdict trace is committed on the node — the run was skipped
- THEN the gate refuses with the flat reason: no trail, re-run the mechanism

  ```check
  watched-run no-verdict
  provenance refuses no-trail
  ```

### Requirement: the vocabulary check guards the fold — closure gated, the semantic half watched and deferred
A fold MUST run the **vocabulary check** over the whole live corpus before the merge, as a sibling of the
depth guard: it is the system's **second escalating guard**, and like the first it neither passes silently
nor refuses on its own. Its **gated** floor is a dispositive fact: a term `glossary.md` defines that the
corpus no longer uses raises a `define / waive / dismiss` decision naming that term and **holds the fold**,
the same flat way a length past the signal raises one. Its **watched** half is the dedicated run's semantic
judgment — a defined concept under a synonym, the language casually expanded — which no fixture can certify;
per the trace discipline its verdict is a **watched-evidence trace** the fold checks for presence on the
provenance gate's shared trail (it does **not** build its own presence check). But the dedicated run that
commits that verdict is **not yet built**, so this half is held **not-yet** — named honestly the way the
model-driven depth scan's watched half is, non-blocking until the run lands and re-arming through the shared
trail the moment it does. So today the live guard is the gated floor; a corpus consistent on its floor
folds. The check is scoped to the live corpus the fold would publish.

#### Scenario: a defined term fallen out of use raises a decision and holds the fold
- WHEN the live corpus no longer uses a term `glossary.md` defines and no decision has settled it
- THEN a `define / waive / dismiss` decision naming that term is raised, the fold is held, and the spec is
  left untouched — a dispositive fact, never a silent pass

  ```check
  orphan glossary-term widget
  gate held because vocabulary names widget
  spec untouched
  ```

#### Scenario: a corpus consistent on its floor folds, the watched half held not-yet
- WHEN the corpus uses every term its glossary defines — the gated floor is met — and the dedicated run is
  not yet built
- THEN the vocabulary guard clears on its live floor and the fold may proceed; the watched half is held
  not-yet and does not hold the fold

  ```check
  corpus consistent
  gate folds
  ```
