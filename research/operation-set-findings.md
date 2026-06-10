# Operation set — research panel findings

A synthesis of an independent, six-panelist literature review answering
`research/operation-set.md`: *what is the enumerated set of primitive
problem-solving operations, derived from the science of problem solving?*

**How this was produced.** Six blind panelists each worked one distinct
scholarly tradition, in parallel, without seeing each other's output and
**without** being shown hypercore's prior vocabulary or the suspect draft — so
none could anchor on the idiomatic answer that triggered the brief. Each was
required to cite real, specific sources (author, year, work, concept), verify
them by web search/fetch, and flag anything it could not source. The six:

- **A — Cognitive science of problem solving** (Newell & Simon, Polya, Gestalt, ACT-R)
- **B — AI planning & formal action representation** (STRIPS, HTN/PDDL, least-commitment)
- **C — Theory of inquiry, logic & argumentation** (Peirce, Dewey, Toulmin, IBIS, Walton)
- **D — Sensemaking & information foraging** (Pirolli & Card, Klein data/frame, Russell et al.)
- **E — Decision analysis & decision theory** (Simon's phases, Howard, Raiffa, Kahneman & Tversky)
- **F — Collaboration: CSCW & distributed cognition** (Clark, Hutchins, Schmidt & Bannon, Roschelle & Teasley, Wegner)

The result below is the orchestrator's cross-reading of the six. Where it makes
a claim no single author makes (e.g. merging two traditions' grains), it says so.

---

## 0. Headline result

Six traditions that do not cite one another converge on the **same grain** and a
**small overlapping set of irreducible moves**. The convergent core is six
primitives:

> **FRAME · GATHER · DERIVE · GENERATE · TEST · COMMIT**

with a beautiful spine running through them: Peirce's claimed-exhaustive,
formally-defended inferential triad — **abduce / deduce / induce** — *is*
GENERATE / DERIVE / TEST, bracketed at the front by **FRAME** (institute the
problem) and at the back by **COMMIT** (settle it), and fed throughout by
**GATHER** (bring in external information). Collaboration is confirmed as a
**role-property on each operation**, not a separate operation — with two
amendments the literature forces. Two further moves (**SYNTHESIZE**, **REPAIR**)
are genuinely contested between "primitive" and "compound"; they are recorded as
open, not adopted.

The single most reassuring finding for the project is architectural: the bet
"small fixed alphabet + freely-growing named compounds" is **independently
proven or attested in four traditions** (HTN method/primitive split is *sound,
complete, and strictly more expressive than flat planning*; ACT-R knowledge
compilation; IBIS's frozen node vocabulary; Walton's argumentation schemes).
That is the most defensible part of the whole design.

---

## 1. The grain — defended, with the test applied

The brief's grain test was kept as "the one piece of prior reasoning." The panel
**vindicates it as not idiomatic at all** — it restates two of the most rigorous
constructs in the literature:

- **Test clause (1) — pre/post stated on the problem, not on world side-effects**
  is *exactly* the STRIPS operator criterion. Fikes & Nilsson (1971) define an
  operator entirely by a precondition and add/delete effects on an abstract
  *state description*, and **explicitly separate the operator from its "action
  routine,"** the thing that actually touches the world: "Execution of action
  routines actually causes the robot to take actions. Application of operators to
  world models occurs during the planning phase." That is precisely "moves on the
  problem, not tool-calls on the filesystem." Newell & Simon (1972) carve at the
  same grain: an operator transforms a *knowledge state* — "what the problem
  solver knows about the problem at a particular moment."

- **Test clause (2) — worth an independent, checkable handoff** is *exactly* the
  commitment-store / locution machinery of formal dialectic (Hamblin 1970): a
  move is a checkable, attributable update to a public ledger of who is committed
  to what. IBIS makes the handoff structural (an Issue is a question another
  party answers with a Position).

Every tradition's primitive is a transition on the problem's **knowledge or
commitment state**, and all six independently pass the test:

| Tradition | Its "state" | Its "move" | Grain test |
|---|---|---|---|
| Cogsci (A) | knowledge state | operator (legal move) | both clauses ✓ |
| Planning (B) | state description / knowledge fluent | action (pre→effect) | clause 1 ✓✓ (sharpest); clause 2 ✓ |
| Inquiry (C) | (in)determinate situation; commitment store | inference / locution | clause 1 ✓ (Peirce); clause 2 ✓ (Hamblin) |
| Sensemaking (D) | shoebox→evidence→schema→hypothesis | representation transition | both ✓ |
| Decision (E) | decision basis (alternatives/info/preferences) | phase (intelligence/design/choice) | both ✓ |
| Collaboration (F) | shared knowledge / common ground | contribution (present+accept) | clause 1 ✓; clause 2 partial |

**One sharp grain caveat, from E.** Howard *defines a decision by its world side
effect* — "an irrevocable allocation of resources." To keep COMMIT at operator
grain, we take the primitive to be the **commitment-state flip** ("this candidate
is now the binding one"), and treat the resource allocation as its downstream
tool-call. That separation is the panel's reading, not Howard's — flagged in §6.

---

## 2. The enumerated alphabet

Each primitive is given with its signature (pre→post on problem state, default
roles) and the traditions that independently surface it. Roles use the brief's
four-role schema: **P**ropose / **E**xecute / **J**udge / **D**ecide.

The alphabet maps cleanly onto the brief's own KNOWN / PROPOSED / COMMITTED
trichotomy, with FRAME as the one meta-level move that acts on the representation
itself.

### FRAME — institute or restructure the problem
- **Signature.** Pre: an indeterminate or mis-framed situation. Post: an explicit
  (re)framed problem — its terms, scope, and what would count as a solution.
  Acts on the *representation*, i.e. the state space itself.
- **Roles.** P: framer. D: problem-owner ratifies.
- **Sources (5-tradition convergence).** Dewey (1938): problematization — "problems
  do not preexist inquiry"; inquiry "converts an indeterminate situation into a
  determinate one." Tversky & Kahneman (1981): the "decision frame" is
  consequential and *preference-reversing* (Asian-disease problem) — framing is
  not free bookkeeping. Howard's "appropriate frame" (Decision Quality). Gestalt
  *restructuring* (Duncker 1945; Wertheimer 1945), operationalized by Ohlsson
  (1992) into elaboration / constraint-relaxation / re-encoding. Newell & Simon:
  "set up the problem space." Klein's data/frame **Reframe**; Russell et al.
  "search for a representation."
- **Note.** FRAME subsumes both *initial* framing and *reframing/restructuring*
  (changing an existing frame). Panels A and D both flag this as the most
  load-bearing yet least-theorized move — see §6.

### GATHER — acquire information that resolves an unknown  *(changes KNOWN, by input)*
- **Signature.** Pre: a stated unknown about the problem. Post: that unknown's
  value is now held.
- **Roles.** P: questioner. E: forager/holder. J: relevance check.
- **Sources (4-tradition convergence).** Scherl & Levesque (1997) **sensing /
  knowledge-producing action** — the planning primitive whose effect is on the
  *knowledge* fluent, not a physical one (the formal bridge to "what is KNOWN").
  Pirolli & Card (2005) foraging loop: *search & filter*, *read & extract*.
  Howard's *information* leg + **value of information** as the gate on whether to
  gather more before committing. Wegner (1986) *transactive retrieval* (locate
  knowledge held by another mind).

### DERIVE — draw out the necessary consequences of what is held  *(changes KNOWN, by inference)*
- **Signature.** Pre: held premises/hypothesis. Post: their explicit, *checkable*
  consequences/predictions, adding no new external content.
- **Roles.** E: anyone; the result is mechanically checkable (the ideal handoff unit).
- **Sources (4-tradition convergence).** Peirce: **deduction** — "proves that
  something *must be*"; explicates consequences. STRIPS: projecting an operator's
  effects to predict the resulting state *is* deductive. Toulmin (1958): the
  *warrant* licenses the step from grounds to claim. Klein data/frame:
  *elaborate the frame*. Decision-tree roll-back (Raiffa 1968).
- **Why distinct from GATHER and GENERATE.** Peirce's triad makes deduction
  irreducible to the other two; it adds no *new* content (unlike GENERATE) and
  imports no *external* fact (unlike GATHER). It makes the implicit explicit.

### GENERATE — put forward a new candidate  *(changes PROPOSED)*
- **Signature.** Pre: a frame with a gap/surprise and no candidate. Post: a
  candidate (hypothesis, option, alternative, design) is on the table, held
  provisionally.
- **Roles.** P: anyone.
- **Sources (6-tradition convergence — the most universally attested move).**
  Peirce: **abduction** — "the only logical operation which introduces any new
  idea." IBIS *Position*. Pirolli & Card *build case / generate hypotheses*.
  Simon's *Design* phase — "inventing, developing… courses of action." Roschelle
  & Teasley *introduce into the joint problem space*. Newell & Simon: the
  *generate* process in rule/model space.

### TEST — assess a candidate against evidence, criteria, or internal validity  *(changes STANDING)*
- **Signature.** Pre: a candidate/claim with unsettled standing. Post: a verdict,
  with grounds, that raises or lowers its warrant.
- **Roles.** J.
- **Sources (6-tradition convergence).** Peirce: **induction** — "shows that
  something *actually is* operative" (tests predictions against observation).
  Polya's *look back*, which usefully splits **check the result** from **check
  the argument**. Pirolli & Card *search for support* / *reevaluate*; Klein
  *question the frame* and *residue* (data that does not fit). Decision
  *evaluate/rank* and *review*. Toulmin *rebuttal*. Roschelle & Teasley *monitor
  for divergence*.
- **Note.** TEST bundles *opening* a question/challenge (the propose-side: IBIS
  *Issue*, Klein *question*) with *rendering* the verdict. Whether to split these
  is an open question (§6).

### COMMIT — bind one candidate as the settled commitment (or retract one)  *(changes COMMITTED)*
- **Signature.** Pre: candidates, some evaluated; an open question. Post: one is
  the *binding* commitment — or a prior commitment is withdrawn (RETRACT).
- **Roles.** D — and per E, possibly **non-delegable** (bound to the authority /
  resource owner).
- **Sources (5-tradition convergence).** Howard: a decision is "an irrevocable
  allocation of resources," **explicitly distinct from evaluation** — evaluation
  produces a *ranking*; commitment makes one *binding*. Simon's *Choice* phase.
  McBurney et al. (2007) deliberation *recommend→confirm→close*. Searle's
  *commissives/declarations*. Walton & Krabbe (1995) *concede / retract*. Klein
  *Preserve* (hold) / *Reframe* (withdraw). Roschelle & Teasley *accept into the
  JPS*. Newell & Simon: *select*.

### The spine, in one line
> **FRAME** the problem → **GATHER** external information → run the Peircean
> engine { **GENERATE** candidates · **DERIVE** their consequences · **TEST**
> them } as a loop → **COMMIT** to a settlement.

### Convergence matrix (which traditions independently surface each move)

| Primitive | A cogsci | B planning | C inquiry | D sensemaking | E decision | F collab |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| **FRAME**     | ● | ○ | ● | ● | ● | · |
| **GATHER**    | ○ | ● | · | ● | ● | ● |
| **DERIVE**    | ○ | ● | ● | ● | ● | · |
| **GENERATE**  | ● | · | ● | ● | ● | ● |
| **TEST**      | ● | ○ | ● | ● | ● | ● |
| **COMMIT**    | ○ | ○ | ● | ● | ● | ● |

● = first-class in that tradition · ○ = present but partial/implicit · · = silent

### Collaboration: not a primitive, a property (verdict on the working hypothesis)
The hypothesis — *collaboration is a property of each operation (who proposes /
executes / judges / decides), not its own operation* — is **substantially
confirmed**, most decisively by Panel F:

- **Clark's contribution model *is* the hypothesis.** A contribution = a
  *presentation* phase + an *acceptance* phase; grounding is defined as the
  collective acceptance riding on a contribution, never a free-standing act.
  Presentation/acceptance maps one-to-one onto the propose-vs-judge role split on
  a single operation.
- **It provably terminates.** Clark & Brennan's *relevant-next-turn* evidence
  shows acceptance of move *N* can be discharged *by performing move N+1* — so
  collaboration needs no infinite stack of "accept" operations. This is the
  formal answer to "won't roles cause regress?": no.
- **Independent corroboration.** C: commitment attribution is a *field on every
  move* (whose store updates; IBIS records who contributed). D: direction/trigger
  decorate each transition. E: role assignment differs per move (only the
  stakeholder owns preferences; only the resource-owner commits). Hutchins: the
  *medium* (person A, person B, an artifact) is a parameter of an operation.

**Two amendments the literature forces:**
1. **Some roles are not free.** E's sharpest prediction: the **D-role on COMMIT
   is non-delegable** (Howard: no decision without the resource-owner's
   commitment). Roles are a per-move property, but the property has constraints.
2. **Defaults come from the surrounding frame.** Walton & Krabbe's *dialogue
   types* (inquiry vs deliberation) set the default role distribution — so the
   role-property's defaults are a function of FRAME, not of the bare move.

### Two contested candidates — recorded, not adopted
- **SYNTHESIZE / STRUCTURE** (≈ the draft's "integrate"). Panel D insists that
  *schematizing* — turning a flat evidence file into a structure — is irreducible
  and distinct from gathering (Pirolli & Card; Russell et al.'s "search for a
  representation" + "encode" + "residue"). The other traditions treat structuring
  as a **compound** of FRAME (build the schema) + GATHER/DERIVE (populate it) +
  TEST (residue check). Genuinely underdetermined.
- **REPAIR** (restore shared understanding after a detected divergence). Panel F's
  one concession to the hypothesis: monitor-divergence + repair has **no solo
  analogue**, so it may be the single collaboration-native operation. F itself
  flags this as the weakest joint — it may decompose into re-GENERATE + re-TEST +
  re-COMMIT on the *shared-understanding* problem. If it does, the hypothesis is
  ~100% role-based; if not, the alphabet needs this one extra primitive.

---

## 3. The combinator set

The brief asks for "the small number of ways primitives compose." The traditions
converge on these:

1. **Partial order with dependency links.** Not strict sequence — Weld's (1994)
   least-commitment plan is `⟨actions, ordering constraints, causal links⟩`: a
   *causal link* records that one operation's output is consumed by another, and
   only the orderings that are *forced* are committed. (Generalizes "sequence":
   STRIPS plans, Peirce's inquiry chain, sensemaking's loop arrows.)
2. **Hierarchical decomposition (method expansion).** A compound expands into a
   network of sub-operations via a named method, bottoming out at primitives.
   This is the **primary explosion-control mechanism** — see §4. (HTN methods;
   GPS subgoaling; Simon's "wheels within wheels"; Clark's nested contributions.)
   **This is where the draft's "decompose" actually belongs** — it is a
   combinator, not a primitive.
3. **Gated iteration.** Repeat a sub-sequence until a condition; the gate is a
   TEST. The cleanest instance is Howard's **value-of-information as the loop
   condition** — keep gathering/analysing until learning more is no longer worth
   it. (Also: Peirce's induction→new-abduction cycle; sensemaking *reevaluate*;
   data/frame *question→reframe*.)
4. **Conditional branching on a verdict.** Choose the next operation from a TEST
   outcome (means-ends difference-reduction; data/frame *question → {elaborate |
   preserve | reframe}*; decision-tree branches).
5. **Role-binding (the collaboration combinator).** Assign P/E/J/D of an
   operation to particular parties — composition along the *who* axis rather than
   the *what* axis. (Clark's present+accept pairing; commitment-store attribution.)

---

## 4. How compounds (clusters) avoid combinatorial explosion

The answer is **proven**, and it is the strongest external support the project
has. In Hierarchical Task Network planning (Erol, Hendler & Nau 1994, *UMCP*),
there are exactly three task kinds — **primitive** (`do[…]`, directly
executable), **goal**, and **compound** — and a **method** `(α, d)` names *one way
to decompose* a compound task α into a network d of sub-tasks. Crucially:

- A method is **not a new primitive**; it is a stored *composition* that bottoms
  out in the fixed primitive alphabet.
- Methods are **domain knowledge that constrains search** — the planner only
  explores method-licensed decompositions, instead of all primitive sequences.
  That is what prevents explosion.
- UMCP proves this scheme **sound, complete, and strictly more expressive than
  STRIPS-style flat planning** — so the discipline costs *no* expressive power.

Two more traditions attest the same shape: ACT-R **knowledge compilation**
(Anderson) merges chains of primitive productions into compiled macro-operators —
expertise is *bigger compiled chunks, not new primitives* (Chase & Simon 1973
show chess mastery is larger chunks); and IBIS deliberately froze a tiny node
vocabulary while letting arbitrarily large maps grow, and Walton's ~25+
argumentation schemes are named compounds over assert/ground/challenge.

**Mapping to hypercore:** a **cluster** (a named set of relations = a repeatable
meta-operation) *is* an HTN method / a compiled chunk / an argumentation scheme.
The primitive alphabet (6 node kinds) never grows; the **dictionary of named
clusters grows freely**. This is exactly the "small alphabet, freely-growing
compounds" requirement — and it is the part the literature most strongly backs.

---

## 5. Mapping onto operations-only nodes in the existing schema

The substrate (nodes / relations / clusters / material) carries the alphabet
with no schema change:

- **Node = one operation instance.** Its `kind` is one of the six primitives:
  `frame · gather · derive · generate · test · commit`. (If SYNTHESIZE or REPAIR
  are later adopted, they become additional kinds — but only if the contest in
  §2 resolves toward "primitive.")
- **Material on a node = the operation's content and product** — the gathered
  facts, the generated candidate, the derived consequences, the verdict, the
  committed decision text. This is how the *operations-only* decision works:
  problem state lives in operations + their material + their relations, with no
  second node flavour for goals/claims/options. A GENERATE node's material *is*
  the proposed option; a COMMIT node's material *is* the decision; the "problem
  state" is the readout of the operation graph, never a parallel object graph.
- **Relations = the combinators.** A `feeds` / `depends-on` relation is a causal
  link (partial order, §3.1); a `tests` relation runs from a TEST node to its
  target; a `commits` / `selects` relation runs from a COMMIT node to the
  GENERATE node it binds; a `reframes` relation runs from a FRAME node to a prior
  FRAME; a `decomposes-into` relation runs from a parent compound to its children
  (§3.2). The relation `type` encodes which combinator and the dependency.
- **Cluster = a named composition** (an HTN method / scheme / compiled chunk): a
  reusable subgraph of operations+relations standing for a meta-operation (§4).
- **Collaboration roles = node props, not node kinds.** P/E/J/D-who lives in each
  operation node's `props` — matching C's "commitment attribution as a field on
  every move" and F's contribution model. There is deliberately **no `collaborate`
  node kind**. (The one possible exception is REPAIR, iff §2 resolves that way.)

This keeps the model genuinely operations-only: every load-bearing thing is an
operation, a relation between operations, a named cluster of them, or material
hanging off one.

---

## 6. Honest open questions — where the literature underdetermines the answer

1. **Alphabet size: 6, 7, or 8?** The core five (FRAME, GATHER, GENERATE, TEST,
   COMMIT) are unanimous. DERIVE (6th) is well-attested and anchored by Peirce's
   irreducibility argument, but a skeptic could fold projection/elaboration into
   GATHER or TEST. SYNTHESIZE and REPAIR (§2) are genuinely contested between
   primitive and compound. The literature does not settle this; a deliberate
   choice is required.
2. **FRAME is the most load-bearing yet least-theorized move.** A and D both flag
   that *how a representation is set up or changed* is exactly where the science
   is weakest — Simon's own admission that his theory "says little about how the
   solver constructs the problem space"; Schunn & Klahr: "we understand least
   about model space." The Gestalt insight-vs-search debate is still open. This is
   the biggest research risk in the whole set: the one operation you most need is
   the one the science specifies least.
3. **Is TEST one move or two?** IBIS makes *raising an Issue* (challenge) a
   first-class node distinct from answering it; Polya splits *check the result*
   from *check the argument*. TEST may want to split into challenge-vs-verdict, or
   evidence-check-vs-argument-check.
4. **Does GENERATE conflate invent vs adopt-on-probation?** C notes Peirce's
   abduction schema presupposes the hypothesis already conceived — so "invent a
   candidate" and "adopt a candidate provisionally" may differ (the latter is
   arguably a weak COMMIT).
5. **COMMIT's world-coupling and non-delegable role.** Treating the primitive as
   the commitment-state *flip* (with resource allocation as a downstream
   tool-call) is the panel's reading, not Howard's, who defines a decision *by*
   its side effect. And the D-role on COMMIT may be non-delegable — the "roles are
   free per-move properties" hypothesis must accommodate this constraint.
6. **The collaboration hypothesis is ~80% confirmed, and entirely on
   human–human data.** Every collaboration source studies human dyads/teams (or
   human + passive artifact); none treats an AI as a full collaborative party that
   proposes/judges/decides. Whether grounding's positive-evidence ladder, repair,
   and transactive allocation transfer to a human–AI pair is *open*. This is the
   gap most specific to the project's actual setting.
7. **Two grains were merged by the synthesizer, not by any author.** The inquiry
   and sensemaking traditions each carry *two* grains — an epistemic-content grain
   (Peirce's inferences; Pirolli-Card's KNOWN-axis transitions) and a
   commitment-ledger/handoff grain (Hamblin's stores; Klein's commitment moves).
   Folding both into one six-primitive alphabet is this report's inference. No
   single source endorses the merged set — though, per §0, the *components* are
   each well-sourced.
8. **Weick dissents on directionality.** Organizational sensemaking holds that
   sense is made *retrospectively* (you act, then make sense via enactment),
   which would put pressure on any clean precondition→postcondition framing for
   some moves. A minority view, but a real one.

---

## Sources

Consolidated from the six panels; each was independently verified by its
panelist. Page/quote-level grounding is in the panel records.

**A — Cognitive science.** Newell & Simon, *Human Problem Solving* (1972);
Simon, "Information-Processing Theory of Human Problem Solving"; Simon & Lea
(1974), dual-space search; Schunn & Klahr, instance/rule/model spaces; Polya,
*How to Solve It* (1945); Duncker, *On Problem-Solving* (1945); Wertheimer,
*Productive Thinking* (1945); Ohlsson (1992), representational change; Anderson,
ACT-R (knowledge compilation); Chase & Simon (1973), chess chunks; Chi,
Feltovich & Glaser (1981), expert vs novice representation.

**B — AI planning.** Fikes & Nilsson (1971), STRIPS; Pednault (1989), ADL;
McDermott et al. (1998), PDDL; Sacerdoti (1974), ABSTRIPS / abstraction;
Sacerdoti (1975/77), NOAH / procedural net; Tate (1977), NONLIN / causal links;
Weld (1994), least-commitment planning; Erol, Hendler & Nau (1994), UMCP / HTN;
Nau et al. (2003), SHOP2; Georgievski & Aiello (2015), HTN overview; Scherl &
Levesque (1997), knowledge-producing actions; Moore (1985), knowledge and action.

**C — Inquiry & argumentation.** Peirce, *Collected Papers* (abduction/deduction/
induction; 5.171, 5.172, 5.189); Dewey (1938), *Logic: The Theory of Inquiry*;
Toulmin (1958), *The Uses of Argument*; Kunz & Rittel (1970), IBIS; Conklin,
gIBIS; Walton (1996), argumentation schemes; Walton & Krabbe (1995), *Commitment
in Dialogue*; Hamblin (1970), *Fallacies*; McBurney, Hitchcock & Parsons (2007),
deliberation dialogue; Searle (1969/1976), speech acts.

**D — Sensemaking.** Pirolli & Card (2005), the sensemaking process; Klein, Moon
& Hoffman (2006) / Klein et al. (2007), data/frame theory; Russell, Stefik,
Pirolli & Card (1993), the cost structure of sensemaking; Weick (1995),
*Sensemaking in Organizations*.

**E — Decision analysis.** Simon (1960), *The New Science of Management
Decision* (intelligence/design/choice); Howard (1966), information value theory;
Howard (1968), foundations of decision analysis; Howard ("irrevocable allocation
of resources"); Raiffa (1968), *Decision Analysis*; Raiffa & Schlaifer (1961);
Tversky & Kahneman (1981), the framing of decisions; Keeney (1992),
value-focused thinking; Howard & Abbas (2014) / Decision Quality.

**F — Collaboration.** Clark & Brennan (1991), grounding; Clark (1996), *Using
Language*; Roschelle & Teasley (1995), joint problem space; Dillenbourg (1999),
collaboration as graded property; Wegner (1986/87), transactive memory; Schmidt
& Bannon (1992), articulation work; Hutchins (1995), *Cognition in the Wild*;
Schegloff, Jefferson & Sacks (1977), repair.

---

## The suspect draft, reckoned against the literature

The brief recorded an earlier **unsourced** alphabet to interrogate, not adopt:
*frame, decompose, research, generate, review, verify, decide, integrate.* The
research lands *near* it on several items — which, per the brief, is "a result
with citations" rather than a starting assumption — and **corrects** it on
several others:

| Draft term | Verdict | Why |
|---|---|---|
| **frame** | ✅ kept → **FRAME** | Now derived (Dewey, Kahneman & Tversky, Howard, Gestalt), not asserted. |
| **decompose** | ⚠️ **relocated** | Not a primitive — it is the primary *combinator* (HTN method expansion, §3.2). |
| **research** | ✅ kept → **GATHER** | The information-acquisition primitive (sensing actions, foraging, value-of-information). Better named for the *move*, not the activity. |
| **generate** | ✅ kept → **GENERATE** | The most universally attested move (abduction; six traditions). |
| **review** + **verify** | ⚠️ **merged** → **TEST** | The draft over-split judging into two; the literature treats it as one primitive (with possible modes: check-evidence vs check-argument). |
| **decide** | ✅ kept → **COMMIT** | Vindicated and sharpened — distinct from evaluation (Howard), D-role possibly non-delegable. |
| **integrate** | ❓ **contested** → SYNTHESIZE | Real per sensemaking (schematize), but the other traditions treat it as a compound. Open. |
| *(absent)* | ➕ **added** → **DERIVE** | The draft *missed* deduction — Peirce's irreducible third inference; distinct from GATHER (no external input) and GENERATE (no new content). |

Net: the literature-derived alphabet is **FRAME · GATHER · DERIVE · GENERATE ·
TEST · COMMIT**, with decomposition moved to the combinators, judging unified,
and DERIVE added — a result that overlaps the intuition but is now grounded, and
corrected where intuition over- or under-counted.
