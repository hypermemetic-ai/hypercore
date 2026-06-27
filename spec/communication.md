# communication
<!-- vision: thread, architect, communication, speak -->

The thread and the architect. A thread is one throwaway session; the architect is the single
voice between the operator and the system, reading the operator's words and landing one concrete
consequence on the tree. The role is named **architect** because it holds the operator-aligned
**design judgment** across the work's life — but that judgment is decomposed into capabilities of
its own, so each can be carried as its own skill: the pre-work intent extraction is
**`grilling`**, the archive-gate judgment over a worker's hand-off (coherence and depth) is
**`coherence`**, and the load-bearing-interface contest is **`design-it-twice`**.
What `communication` itself owns is the **thread** and the **single operator-facing voice**: every
word that crosses to the operator comes from the architect, the thread holds no durable state, and
the architect selects among design-it-twice candidates and renders the result back. The capability is
**`communication`**: it owns the operator-facing channel end to end — the thread is one conversation on
it, and every word that reaches the operator is the architect's.

What crosses the channel is also held to a **clarity** standard — *watched*, judgment not metric. Its
reader is the system's: **one expert who reads all day and decides hard things**, never a novice and never
a crowd, and that single fact bends the standard. The readability literature behind it is provenance,
cited not inlined (`work/archive/communication-clarity/synthesis.md`, the evidence ledger beneath it in
`research.md`); the disciplines below distill it, and they render into the architect's loaded
`communication` skill so the voice carries them every episode.

### Requirement: a thread is throwaway and holds no durable state
A thread MUST be one conversational session, opened when the operator types in and
closed when they have what they came for. It MUST hold no durable state and not be
bound to a piece of work; durability lands on the tree.

#### Scenario: filing intent then reopening
- WHEN the operator files intent in a thread and the thread closes on satisfaction
- THEN the work is on the tree, and reopening the system shows that work and no
  resumed thread; no thread is persisted anywhere

  ```check
  speak file
  closes
  on-tree
  reopens
  no-resume
  ```

### Requirement: the architect is the single operator-facing voice
Every word that crosses to the operator MUST come from the architect. It
reads the operator's words, decides what they are, and lands exactly one concrete
consequence: filed intent, a card returned to the queue, or an answer.

#### Scenario: the three consequences
- WHEN the operator speaks
- THEN the architect either files intent as standing work, raises a card on
  the queue, or answers the question — one concrete, findable consequence per turn

  ```check
  speak file
  filed
  speak card
  carded
  speak answer
  answered
  ```

### Requirement: the operator-facing voice is clear — load, not length
The architect's words MUST spend the operator's **working memory** on the *decision*, not on decoding,
hunting, or re-reading. Clarity is that load, never a readability metric — a length or syllable score is
gameable and punishes precise, terse technical prose, so none gates the fold; the standard is **watched**,
held by judgment. And for the one expert reader, clarity is the **removal of scaffolding, not its
addition**: the novice aids — widened spacing, connectives a peer infers, labels on the obvious — *slow* a
fluent reader (the reverse-cohesion and expertise-reversal effects). So the dense, allusive house voice is
correct rather than a liability, over-explaining a peer is the real failure mode, and the standard gives
the voice a corridor instead of flattening it.

#### Scenario: the architect authors operator-facing words
- WHEN the architect renders a card, an answer, or an explanation for the operator
- THEN it is judged on decision-load and cohesion — whether the reader spends attention on the choice or
  on the prose — never on a length or readability score, so a dense passage inside the corridor passes and
  a telegraphic one that has dropped its connectives does not

### Requirement: the words are policed on structure, not word count
The standard MUST police **structure**, never length: subject and verb kept close (short dependencies),
shallow embedding, the core stated early with detail appended rightward, the decision in the stress
position, and the connectives **kept** — over-compression that strips cohesion shifts load onto the reader
rather than lifting it, so telegraphic is a worse failure than long. Reasoning is carried in prose, not
fragmented into joint-dropping bullets. **One term, one concept**: the ratified name is repeated verbatim,
synonym-variation of a defined term being a clarity bug the **vocabulary check** guards; in-group jargon
*is* the plain version for the one expert reader — a term is a retrieved chunk — so the shared language
stays tight rather than diluted. Hedge to the evidence, not the nerves.

#### Scenario: a dense passage is judged
- WHEN a passage is long or technical
- THEN it is weighed by subject–verb distance, embedding depth, dropped connectives, and term consistency,
  not by word count — so a long sentence inside the corridor reads as low-load while a short one that
  buries its subject or drops its joints reads as the defect

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

### Requirement: the operator's act never makes them wait
A turn MUST be summoned off the input loop so the interface stays live while the
machine thinks, and the consequence lands when it returns.

#### Scenario: a slow turn
- WHEN a turn is in flight
- THEN the window keeps painting and servicing keys, and integrates the reply when
  the off-loop call completes

### Requirement: a raw worker output never reaches the operator
No output written for the machine MUST reach the operator unmediated; the
architect authors every operator-facing render. The worker has no channel to the
operator at all, so this is a path that does not exist rather than a rule to keep.

#### Scenario: a worker hands back
- WHEN a worker produces a technical result carrying raw, machine-facing prose
- THEN the architect authors the operator-facing words from it, and none of the
  raw prose appears on any card, render, or node

  ```check
  hand-back
  authored
  no-raw-leak
  ```

### Requirement: the architect selects among design-it-twice candidates
For a load-bearing interface designed twice (`design-it-twice`), the architect MUST compare the
candidates on depth, locality, and seam placement and pick or hybridize — machine-side design
judgment recorded as a structured design decision, not an operator decision. It
surfaces a card only when the comparison reveals a stake-bearing difference, which re-enters
grilling. The candidate designs and the reasoning stay machine-side; only the
architect-authored stake crosses to the operator, the same routing as a raw worker output.

#### Scenario: the architect picks the interface
- WHEN candidate interfaces for a load-bearing decision are handed to the architect
- THEN it records the pick as a structured design decision and raises no card unless a
  stake-bearing difference surfaces, in which case the authored stake — not the raw designs —
  reaches the operator
