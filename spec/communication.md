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

Every word that crosses is held to a **clarity** standard — *watched*, judgment not metric. Clarity is
**compression to a decoder the one reader already runs**. Strip the redundancy from a message and what is
left is indistinguishable from noise — unless the reader holds the key; maximal compression and
encryption are one operation, parted only by whether the key is shared. So dense prose is not one thing.
The term that expands, *in this reader's head*, into all it stands for is mastery; the same short string
aimed at a key they do not hold is ciphertext wearing depth's clothes. The architect's burden is the
**rare encoder** — the word, image, or shape that builds the idea into a form the operator re-runs from
what they already know — never the cheap one that offloads the rebuild onto the reader and calls it
respect for their expertise. The reader is the system's: **one expert who reads all day and decides hard
things**, and one with a *job*, so the register is practical, not literary — show the thing, but never
stage the hard-won as effortless, because the effort that staging hides is the operator's risk register.

Stating this does not make it so, so the standard is **run, not only declared**: before the words cross,
the architect tests its own draft against this one reader on four counts — the reader can **re-derive**
the decision's cases and limits from what they already hold (else it is encryption, not insight); the
load-bearing **caveat survives** the compression and keeps its weight, the map never dropping the cliff;
the draft's felt-truth does not move when the **cadence is stripped**, because beauty may carry an idea
but never stand as its evidence; and the audience is **this reader on a tired afternoon**, never a
gallery. The rarest discipline is the one to hold hardest — **make the caveat land as hard as the
recommendation**: anyone can compress the headline, mastery compresses the limitation. The self-check
edits *expression only*, never the decision it carries. The **removal of scaffolding** an expert reader
rewards is a corollary of this, not its spine — right where the decoder is genuinely shared, and
elsewhere merely encryption with good manners. The readability literature behind all of it is
provenance, cited not inlined (`work/archive/communication-mastery-reground-the-clarity/`; the prior
dive's now-superseded spine and its still-standing type and surface findings are in
`work/archive/communication-clarity/`); the disciplines below distill it, and they render into the
architect's loaded `communication` skill so the voice carries them every episode.

A pair, since the move resists statement:
- *encrypts* — "Per the reversibility analysis, the migration is non-trivially load-bearing on the
  single-writer seam." Jargon to a key the reader may not hold, the caveat deleted under a clean line.
- *lands* — "The migration rides on the one-writer lock; if that lock isn't truly single-holder, every
  concurrent fold corrupts the record — that's the flip." The term expands, and the caveat is the
  payload, in the stress position.

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

### Requirement: the operator-facing voice is clear — compression to a shared decoder
The architect's words MUST compress to a decoder the one reader already runs — spend their **working
memory** on the *decision*, not on decoding, hunting, or re-reading. Clarity is that load, never a
readability metric: a length or syllable score is gameable and punishes precise, terse prose, so none
gates the fold; the standard is **watched**, held by judgment. Dense prose splits on one axis — whether
the key is shared. The compression the reader can re-run is mastery and earns its place; the same short
string aimed at a key they lack is encryption, however expert it looks; the cliché — a private key worn
smooth — is its decay. Removing the scaffolding a peer infers is right *where the decoder is shared*
(over-explaining a peer is the real failure there), and wrong everywhere else, where it is encryption with
good manners.

#### Scenario: the architect authors operator-facing words
- WHEN the architect renders a card, an answer, or an explanation for the operator
- THEN it is judged on whether this one reader can decompress it — re-derive the decision from what they
  already hold — never on a length or readability score, so a dense passage whose key the reader holds
  passes and a short one whose key they lack does not

### Requirement: the words carry the decision, and the caveat lands with it
The standard MUST police **structure and what the form builds**, never length. The floor is parse cost:
subject and verb kept close, shallow embedding, the core stated early with detail appended rightward, the
decision in the stress position, and the connectives **kept** — over-compression that strips cohesion
shifts load onto the reader, so telegraphic is a worse failure than long. Above the floor is the
generative bar: a word, term, or **figure** earns its density by what it lets the reader **regenerate**,
not by parsing cheaply. A figure passes only if cashing it into plain language yields a true,
decision-relevant inference the plain sentence would not, and none of its silent entailments is false on
the surface that bears the weight. **Reach for the shared symbol** is the positive of that bar: where a
relation or comparison *is* the point, prefer the non-letter symbol the one reader already runs — →, ≠, ≤,
the system's own glyphs — over the prose that spells it out, when it decompresses faster and stays at least
as faithful. The generative bar above judges it and the shared-decoder split classifies it, so a symbol
earns and loses its place exactly as a term of art does. A pair shows the line the rule alone cannot.
*Earns it* — `ready: open ∧ folding-condition named ∧ no open child` is the one predicate the reader
already runs, faster than the three spelled conjuncts and shedding nothing. *Decoration* — `the worker's
result ⟹ the fold ⟹ the record` wears the arrow as a vague "leads to," decoding to nothing the prose did
not carry while dropping that the fold is gated on coherence. **One term, one concept**: the ratified name is
repeated verbatim, synonym-variation of a defined term being a clarity bug the **vocabulary check** guards;
in-group jargon is the cheap encoder, admitted only where the reader truly holds the key and it still does
work, never a slot-filler. And the hardest discipline — the load-bearing **caveat lands as hard as the
claim**: the qualifier the decision turns on takes its own stress position, made as concrete and memorable
as the recommendation, never deleted under a clean line nor demoted beneath the headline. Hedge to the
evidence, not the nerves.

#### Scenario: a dense passage and its caveat are judged
- WHEN a passage is long or technical, or carries a load-bearing qualifier
- THEN it is weighed by whether the reader can regenerate it and whether the caveat keeps its weight —
  subject–verb distance, dropped connectives, a figure's or symbol's entailments, a symbol whose decoder
  this reader lacks, a qualifier buried beneath the headline — never by word count

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

### Requirement: a depth-gate trip raises a neighborhood-aware assessment; a flat refusal stays verbatim
When `integrate` meets a typed depth guard, the architect MUST raise a reasoned depth/length
assessment of the flagged file read in its neighborhood: callers, siblings, and cross-module
boundaries as seen through the standing architecture review's whole-tree read. It MUST consult the
shared `depth_scan` seam with the standing `review.review(root)` result, never run a second scan. The
assessment carries a lean and a flip in place of the bare re-cut / deepen / accept template; it informs
the operator's settlement and does not gate the fold or leave an extra watched trace. Flat refusals,
including a delta that does not apply and provenance no-trail, MUST be raised with their reason
verbatim, never dressed as negotiable prose.

#### Scenario: a depth-gate trip raises a neighborhood-aware assessment; a flat refusal stays verbatim
- WHEN the architect integrates a worker hand-off that trips the depth gate, and one that trips a flat
  refusal
- THEN the depth trip raises a neighborhood-aware assessment carrying a lean and a flip instead of the
  bare depth template, while the flat refusal's reason is raised verbatim

  ```check
  integrate depth-trip assessment-with-lean-flip
  integrate flat-refusal verbatim
  ```

### Requirement: a dropped caveat never reaches the operator
The architect MUST run the clarity self-check on its own draft before the words cross, and a load-bearing
**caveat dropped by the compression MUST be caught before it reaches the operator**. The four-count
self-check (re-derivable · caveat survives · truth survives form-strip · this reader, not the gallery) is
watched judgment and edits expression only, never the decision. The one count a tool holds without a
model — caveat-survival — is built into the architect's archive render: the operator-facing words are
checked against the load-bearing caveat the contract carries, and words that drop it do not cross as
drafted. The entailment verdict is model-driven and stays **watched** — live it is the architect's
judgment — so only the **routing** is mechanically **gated**: a dropped caveat is provably caught and
raises a decision, never silently passed.

#### Scenario: a dropped caveat is caught, a surviving one crosses
- WHEN the architect integrates a worker hand-off whose contract carries a load-bearing caveat
- THEN words that drop the caveat are caught before they cross — the routing gated on the survival verdict,
  raising a decision — while words that keep it cross and fold, the verdict itself the architect's watched
  judgment

  ```check
  contract-caveat
  drafts-without
  caught
  drafts-with
  crosses
  ```
