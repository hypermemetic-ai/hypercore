surfaced: 2

[Q] The gated (mechanical) floor is "a term used but undefined." To be gated it must compile to a deterministic check block, so "a term" has to be identifiable with no model. What is the mechanical signal?
lean: Glossary-set, no marking — the gated floor reads the glossary↔corpus set-difference in the deterministic direction (a defined term unused anywhere in the live corpus), and "used-but-undefined NEW term" detection moves to the watched/semantic half (the dedicated run, already provisioned, cheap because the corpus fits one context window). Why: bold is already overloaded for emphasis across the corpus, so making "marked = term" gated would be noisy and would punish the dense house voice — the exact gameable-metric failure clarity warns against.
flip: If the operator wants the gated floor to literally catch "used but undefined" at fold time without waiting on the watched run, adopt a marking convention and make a marked-as-coined term with no glossary.md entry the gated floor — at the cost of making a writing convention enforceable.
answer: Resolved on the communication-clarity evidence the operator pointed to (research.md §A2; synthesis.md). The evidence settles the scope and confirms the direction: "the rule binds the defined concept vocabulary, not every token" — so the term-set IS the glossary and no marking is made load-bearing; "No readability gate — judge cohesion, never length" (a metric "penalize[s] precise terms") — so the gated floor is glossary↔corpus closure (a defined term fallen out of use, a dispositive set-difference, never a metric); and the watched half is sharpened to guard the "chunk economy, not just tidiness" — a defined concept under a synonym (Fowler's "elegant variation" vice) or the language casually expanded by a term earning no distinct chunk. Not the marking path.

[Q] D19 requires the watched half to emit a trace the fold checks for presence. What is that trace, and who owns the fold-side check — given a-record-a-load-bearing (open) is building the general "a record folds only when its mechanism's trail is present" gate that would subsume it?
lean: Self-contained trace — the run commits its verdict over the named corpus snapshot on the node (clean, or the findings and their define/waive/dismiss settlement), and vocabulary-check builds its OWN fold-side presence check. Keeps the vehicle independent of a-record's unbuilt gate so the back-half run isn't blocked on it; a-record later generalizes and absorbs this one trace-check.
flip: If the operator would rather not build a trace-check a-record will immediately generalize, the watched half emits the trace only and defers the fold-side presence check to a-record — sequencing a-record first and giving up the vehicle's independence.
answer: Accept the lean: self-contained trace. The run commits its verdict on the node; vocabulary-check builds its own fold-side trace-presence check, independent of a-record's general gate, so the back-half run is not blocked on it; a-record later subsumes this one trace-check.

[CONTRACT]
hypercore's shared language gains a standing guard so the corpus can no longer drift from its own glossary the way it silently drifted ~16 terms behind the built system. At every fold a **vocabulary check** runs over the whole live corpus — `glossary.md`, `intent.md`, and the spec — communication's **consistency** standard, the guard the one-term-one-concept rule already names but never had. It has two halves, at the two strengths a standard can take. A **gated** mechanical floor catches a dispositive fact: a term `glossary.md` defines that the live corpus no longer uses — the glossary and the language fallen out of step — read as a string set-difference, never a readability metric that would punish precise prose. A **watched** semantic half — a single dedicated run, cheap because the whole corpus fits one context window — reads the corpus for **new or conflicting** vocabulary: a defined concept reappearing under a synonym (elegant variation) or the shared language casually expanded by a term that earns no distinct chunk, guarding the chunk economy the ubiquitous language rests on. A finding of either half raises a **define / waive / dismiss** decision on the operator's queue and **holds the fold** until it is settled — the length-signal pattern applied to words, and the architect never carries it. The watched run leaves a **trace** of its verdict on the node, and the fold checks that trace is present, so a fold can never show the run as having happened when it did not — vocabulary-check building its own trace-presence check, independent of the general provenance gate that a-record will later generalize. The result is validated by growing the corpus out of step with its glossary and watching the fold raise the decision and hold the merge, by a clean corpus whose run left its trace folding through, by a missing trace holding the fold, and by `python3 -m engine --check` carrying the acceptance and staying green.

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

### Requirement: the vocabulary check guards the fold — closure gated, the judgment watched on a trace
A fold MUST run the **vocabulary check** over the whole live corpus before the merge, as a sibling of the
depth guard: it is the system's **second escalating guard**, and like the first it neither passes silently
nor refuses on its own but **raises a decision** — `define / waive / dismiss` — and holds the fold pending
it. Its **gated** floor is a dispositive fact: a term `glossary.md` defines that the corpus no longer uses
raises the decision naming that term and holds the fold, the same flat way a length past the signal raises
one. Its **watched** half is the dedicated run's semantic judgment, which cannot be checked — but per the
trace discipline the run MUST leave a **trace** of its verdict on the node, and the fold MUST check that
**trace is present** (its absence holds the fold the same way), so the fold's dependency on the watched
half is the deterministic presence of its trace while the judgment's quality stays watched. A clean corpus
whose run left its trace folds; an open finding holds the fold until the operator settles it. The check is
scoped to the live corpus the fold would publish.

#### Scenario: a defined term fallen out of use raises a decision and holds the fold
- WHEN the live corpus no longer uses a term `glossary.md` defines and no decision has settled it
- THEN a `define / waive / dismiss` decision naming that term is raised, the fold is held, and the spec is
  left untouched — a dispositive fact, never a silent pass

  ```check
  orphan glossary-term widget
  gate held because vocabulary names widget
  spec untouched
  ```

#### Scenario: a clean corpus whose run left its trace folds
- WHEN the corpus uses every term its glossary defines and the watched run committed its verdict trace on
  the node
- THEN the closure floor is met and the trace is present, so the vocabulary guard clears and the fold may
  proceed

  ```check
  corpus consistent
  run leaves-trace
  gate folds
  ```

#### Scenario: a missing watched trace holds the fold
- WHEN the corpus is consistent but the dedicated run left no verdict trace on the node — the run was
  skipped, not merely clean
- THEN the guard holds the fold (`no vocabulary trace`) — the fold cannot show the run as having happened
  when it did not, the same way the gated floor refuses on a fact

  ```check
  corpus consistent
  run no-trace
  gate held because vocabulary
  ```
