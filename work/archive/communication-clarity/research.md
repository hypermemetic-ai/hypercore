# communication — the deep dive (living research / provenance)

Working material for the clarity standard and the (re-opened) communication+interface surface.
Research is **provenance**: it folds with the work; the standing artifacts are the **clarity intent**
and the rendered **`communication` skill** (`spec/communication.md` → `engine/methodology.py`). Nothing
standing depends on this file — it is mined, distilled, and left as a footnote.

## The target

Clarity and ease for a **single expert operator who reads a lot and makes hard decisions all day**,
daily, at stake. Reduce the friction of taking the system in; preserve the operator's mental budget
for the deciding. Fatigue across long sessions is a first-class adversary.

Operator profile (from `intent.md`): one expert; reads system state at a glance; the queue is their
decision surface; commits real resources; knows the ubiquitous language (`glossary.md`); uses the
system continuously.

## The governing lens — Cognitive Load Theory, made our own

Spend the operator's working memory on the **decision**, never on the **interface**.

- **Intrinsic load** — the decision's own difficulty. Irreducible, sacred.
- **Extraneous load** — load from *presentation* (ambiguity, hunting, inconsistent naming, noise).
  **The enemy.** Every choice exists to drive it toward zero.
- **Germane load** — the deciding itself. Protect the budget; fatigue drains it.

Working memory ≈ **4 chunks** (Cowan; "7±2" is folklore). `one-name-one-concept` is a chunking
optimization — a settled term retrieves as one chunk.

**Per-finding test:** *Does this choice convert extraneous load into signal, or just add density?*
Keep the first; cut the second, even when it's pretty.

This dissolves the house-voice question: density is good when **intrinsic** (signal an expert can
decode), bad when **extraneous** (ornament, allusion-for-its-own-sake, ambiguity that forces a re-read).

## The map (dimensions)

- **A — Verbal craft:** sentence structure, diction, chunking, information ordering (given-new,
  inverted pyramid), concision, parallelism, the architect's single voice.
- **B — Visual / typographic:** typeface, weight/size, measure & leading, contrast, hierarchy,
  whitespace. (TTY-bound today; surface re-opened.)
- **C — Diagrams / illustration:** when a picture beats prose; terminal-renderable diagram grammar.
- **D — Accessibility & cognitive science:** dyslexia, low-vision, color vision deficiency, dual
  coding — mined for *universally* helpful patterns, not a disability floor.
- **E — Make-it-our-own:** single-operator reader, the queue/decision surface, the watched (non-metric)
  standard, the architect's voice, ubiquitous language.

## Open tensions against endorsed intent (surface as decisions, never silent edits)

1. **Color.** Intent: *"color spent only where it earns its place."* Proposed sharpening: *earns its
   place = carries a second, redundant encoding of meaning that speeds retrieval.* Candidate ratifiable
   refinement, not a contradiction.
2. **Beyond the TTY.** `spec/interface.md`: *"pure-frame render off a TTY."* Surface re-opening is a
   real architectural direction — machine-owned proposal until ratified.
3. **High-contrast.** Intent: *"high-contrast."* Evidence: maximal 21:1 fatigues an all-day reader;
   soft high contrast (~7–15:1), warm dark-on-off-white, is the better target. Candidate refinement.

## Findings ledger

Each finding: **Claim → Evidence (with source) → Cost/contest → hypercore verdict** (earns its place /
conflicts → decision / banked provenance).

### D/B — Color (full pass, sourced)
The evidence *vindicates restraint* rather than overturning it — the steer below honors "color helps
process complex info" via mechanism, not volume.

- **Pre-attentive pop-out is the big win — and it allows only ONE code at a time.** Treisman's Feature
  Integration Theory: a single-feature color difference (one red among the rest) is found in *flat*
  reaction time regardless of how much text surrounds it. The instant a second simultaneous color code
  is added it becomes a *conjunction* search → slow serial scan. → Spend the pre-attentive budget on the
  one thing that must be *found* (e.g. needs-attention), not on coloring everything.
- **Decorative/duplicative color measurably *lowers* comprehension.** Mayer's redundancy effect and
  seductive-details effect: color that doesn't carry non-redundant meaning taxes the same working memory
  the operator needs for the decision. This is empirical backing for intent's *"every element earns its
  place."*
- **Dual coding (Paivio)** gives a smaller retrieval benefit — but dense text is already verbal-
  saturated, so color only pays as a *second channel carrying what the words don't*.
- **Redundant coding (WCAG 1.4.1).** CVD ≈ 8% of men / 0.5% of women, almost all red-green — the exact
  axis "good/bad" uses, and the first to wash out under glare/fatigue/age. Color is the *fast* channel;
  a glyph/label/weight/position is the *certain* channel. Never color alone.
- **Categorical budget ≈ 6–7 hues** (Ware 5–10; hard cap ~10–12 nameable categories). Past that,
  pop-out is lost. Reserve one saturated "alarm" hue used nowhere else.
- **Semantic color:** red = *attend/abnormal* is near-universal (arousal); red = *bad/down* is cultural
  (Western finance) and brittle. Use red for attention; be deliberate before using it for valence.
- **Palette type → data structure:** hue for categories, monotonic lightness for sequential, two-hue
  divergence for above/below-normal. Use **viridis / ColorBrewer** (perceptually uniform, grayscale- and
  colorblind-safe); never jet/rainbow — it invents false boundaries and has *measured* clinical error.
  *(Banked for any future diagram/data surface.)*
- **Verdict.** *Earns its place* refined and now evidence-backed: **one pre-attentive code, ≤6–7
  load-bearing hues + one alarm, always doubled by a non-color cue, carrying meaning the words don't.**

### B — Contrast for the all-day reader  →  NEW tension against intent
- **Claim.** Maximal contrast (#000/#FFF = 21:1) is the *wrong ceiling* for an 8-hour reader — drives
  excess pupil work and (on dark bg) halation. Soft high contrast (~7–15:1) reads as well and fatigues
  less. WCAG 7:1 (AAA) is the floor, not the target.
- **Polarity.** Dark-on-light (positive) wins for small-text acuity and is the safer default; light-on-
  dark helps cataract/glare cases but triggers halation for the ~30–50% with astigmatism. Polarity is
  eye-dependent → a soft dark toggle, not a fixed choice.
- **Verdict → decision.** Intent says *"high-contrast."* Evidence says **soft high contrast (~7–15:1),
  warm dark-on-off-white default, not maximal.** Surface as a candidate intent refinement (tension #3).

### D — Legibility, and the expert-reader inversion
The pivotal finding: most legibility/dyslexia research is calibrated to *struggling* readers, and some
of it **penalizes an expert**. So we don't import accessibility advice wholesale — we take the variables
that help *everyone* and reject the ones that only help slow readers.

- **Dyslexia fonts (OpenDyslexic/Dyslexie): debunked.** No speed/accuracy benefit (Wery & Diliberto
  2017; Kuster 2018, n=170/147 preferred Arial); letterforms contribute *nothing* (Galliussi 2020) —
  any gain is a spacing effect, gettable from any face.
- **Widened letter-spacing *slows fast readers* — the inversion in one finding.** Helps dyslexic
  children (Zorzi 2012) but disrupts the parallel chunk-processing skilled readers rely on; fast readers
  slowed the *most* (Galliussi/Masulli, Frontiers 2020). → **Normal tracking; never widen.** Adequate
  word-spacing only.
- **Universal wins (help everyone, our reader included):**
  - **Measure ≈ 55–66 CPL** (Bringhurst 66; Dyson & Haselgrove ~55 supports fast reading) — the
    highest-leverage, most-violated variable; controls return-sweep cost over long sessions.
  - **Leading ≈ 1.4–1.5×** (Butterick 120–145%; BDA 150%), more as the line widens.
  - **Size** toward the upper band, user-adjustable; **weight 400–500**, bold for emphasis only.
  - **Character disambiguation** (l/I/1, rn/m, O/0, B/8) — the *real* grain of truth in the dyslexia-
    font idea, isolated: a high-stakes accuracy win for a reader scanning identifiers/numbers (Atkinson
    Hyperlegible engineered for exactly this).
  - **No ALL-CAPS runs** (10–20% slower, Tinker; destroys word-shape) — caps for short labels only.
    **No long italic runs.**
  - **Serif vs sans = folklore** — no reliable speed/comprehension difference; choose on letterform
    quality + disambiguation, not the axis.
  - **Left-align ragged-right;** justify *only* with TeX-grade hyphenation (browser `justify` = rivers).

### B — Screen typography & the terminal scorecard
- **Measure/rhythm/whitespace:** 66-col body (cap 45–80), ragged; whitespace is functional chunking
  (reduces working-memory load), one-idea paragraphs, space-between *or* indent (never both).
- **Hierarchy by signal-to-noise (highest first):** **space › modest size › bold › small-caps ›
  indentation › color.** "Change one parameter at a time." Limit to 2–3 heading levels.
- **Terminal scorecard.** *Native-excellent* at: exact measure, perfect vertical rhythm, whitespace
  chunking, box-drawing structure, a disciplined one-color-one-meaning map. *Genuinely loses:* sustained-
  prose **reading speed** (proportional packs more per fixation — the big one), fractional leading,
  subtle color-free hierarchy.

### Synthesis — two rules that fell out, and the beyond-TTY seam
1. **Color and hierarchy do different jobs — don't cross them.** Color is the #1 *pre-attentive search*
   cue (find the one card that needs attention) but the *worst* hierarchy cue for prose (low SNR). Space
   + size + weight carry *structure*; one redundant color code carries *state / what-to-look-at*. This
   reconciles the color agent (color = biggest find-speedup) with the typography agent (color = lowest
   hierarchy SNR): different jobs, not a conflict.
2. **The expert-reader rule.** Take only legibility variables that help everyone (measure, leading,
   size, contrast, disambiguation, no all-caps); reject struggling-reader fixes that slow an expert
   (widened tracking). Our reader's expertise is a *design input*, not a deficit to accommodate.
3. **Beyond-TTY reframed — it maps onto a seam intent already has.** The terminal is *excellent* for a
   structured, scannable **decision surface** (cards, tree, queue) and *loses* mainly on **sustained-
   prose** speed/fatigue. Intent already splits these: *"the main screen"* (queue + work, scanned) vs.
   *"the views built for reading"* (reference detail). So the real fork isn't "leave the terminal?" but
   **"does a richer *read-view* earn its place for the long prose, while the grid keeps the decision
   surface?"** — a hybrid, grounded in hypercore's own structure.

### A — Verbal craft
Three agents: (1) sentence architecture; (2) diction/concision/jargon; (3) information ordering & the
decision brief. Distills into the clarity-standard spec prose the `communication` skill renders.

#### A1 — Sentence architecture (the crux for the house voice)
The unifying finding: **sentence difficulty for a skilled reader is working-memory load *during
parsing* — dependency length + held-open structure — NOT length, formality, or density.** The expert
decodes vocabulary cheaply; what they can't cheat is holding an unresolved dependency open while
material piles up. This is the evidence that settles the house-voice question.

- **Dependency locality (Gibson, DLT).** Keep grammatically-linked pairs close — above all **subject
  and verb**. *Distance is the tax,* not word count. Object-relative clauses, long subject–verb gaps,
  and dependencies spanning many referents are the costly structures.
- **Given-new contract (Haviland & Clark 1974).** Open each sentence with a link to something the
  reader already holds; never smuggle a new entity in as if given (forces a bridging inference). The
  reaction-time foundation under "old before new."
- **Topic & stress positions (Gopen & Swan).** Link/old info at the **start** (topic position); the one
  piece of payload at the **syntactic close** (stress position), where the reader auto-assigns emphasis.
  One new thing per stress position. → **hypercore verdict:** engineer every card and sentence so *the
  decision* lands in the stress position; spend no stress position on hedges.
- **Passive & nominalization — folklore debunked.** "Never passive" is false: passive is correct for
  given-before-new flow, **light-before-heavy** ordering (postpone a long/new agent to the end), and
  unknown/irrelevant agents (Pinker, Williams). Default active + strong verbs; reach for passive as a
  *flow tool* to shorten a dependency or fix topic/stress.
- **No length ceiling — structure sets load (THE finding).** A long **right-branching** sentence (core
  stated early, elaboration appended rightward) stays nearly flat in working memory; a short
  **center-embedded** one can be brutal. Center-embedding ceiling ≈ **2** (fMRI/branching evidence,
  Matchin 2023). Readability-formula length penalties are **proxies for embedding, not causes** — more
  backing for the no-metrics decision.
- **Em-dashes (the house habit, adjudicated).** Punctuation is a real parsing aid (implicit-prosody
  brain response; commas eliminate garden-paths). A **trailing** em-dash opening end-elaboration is
  essentially *free* — right-branching, clean boundary, payload in stress position. A **paired** em-dash
  interruption *is* a center-embedding: cheap only if the bracketed span is **short** and doesn't split
  subject from verb.
- **hypercore verdict (made our own).** Density is **vindicated conditionally.** The sentence standard
  is not "shorter/simpler" — it is: **right-branching · short dependencies (esp. subject–verb) · given-
  then-new · the decision in the stress position · paired-dash interruptions kept short · no local
  garden-path ambiguity.** A precise, testable craft bar that *honors* the dense voice instead of
  flattening it. The thing to police is never word count — it's subject–verb distance, embedding depth,
  and any dependency held open across many referents.

#### A2 — Diction, concision & jargon (hypercore vindicating itself, now sourced)
Through-line: the standard is a **cohesion-and-decision-load** standard, not a readability gate —
exactly the existing decision, now with the primary sources behind it.

- **One-term-one-concept is evidence-backed.** "Elegant variation" — swapping synonyms for a defined
  term — is a named *vice* (Fowler); technical-writing consensus says repeat terms of art verbatim. →
  direct support for hypercore's **ubiquitous language**. Nuance: the rule binds the *defined concept
  vocabulary*, not every token (pronouns/ordinary repetition are fine).
- **In-group jargon IS the plain version** for the one expert reader — a precise term is a retrieved
  *chunk* (working-memory economy). Plain-language gains are real but accrue to *novices*; for a genuine
  expert in-group, simplifying only sheds precision. **But:** jargon harms outsiders *even when defined*
  (Bullock/Shulman 2019 — the cost is metacognitive, not lexical). → **keep the shared language tight,
  don't expand it casually** — which is exactly what the `vocabulary-check` consistency standard
  protects. (New link: vocabulary-check guards the chunk economy, not just tidiness.)
- **Concision has a hard floor — keep the connectives.** Cut metadiscourse, redundant pairs,
  nominalize-plus-"is" (Williams); **never** cut the cohesive ties, referents, or scope qualifiers that
  carry the logic. Shortening that strips cohesion did **not** improve comprehension (Duffy & Kabance) —
  it shifts load back onto the reader. → **"Density is high signal-per-token, not fewest tokens."** The
  house voice's real failure mode is *over-compression* (dropped "because"/antecedent), not length.
- **Curse of knowledge, defused — with one live residue.** For a single shared-schema reader the curse
  largely lifts (jargon is safe), and the danger inverts toward condescension. What still bites even one
  expert: **skipped intermediate *steps* and unstated *scene/state*** (Pinker). → police elided steps,
  not vocabulary.
- **Hedge to the evidence, not the nerves.** Keep qualifiers that change truth conditions or the
  decision (scope, real uncertainty); cut throat-clearing and intensifiers; never stack them. *Test:
  delete and reread — if truth conditions / the decision are unchanged, it was noise.*
- **No-metrics decision fully vindicated.** Readability formulas measure two surface proxies (word/
  sentence length), not meaning; are gameable; reward cohesion-destroying edits; and penalize precise
  terms of art — a triple mismatch with this register (UXmatters; DuBay; Flesch-Kincaid critique). If
  any signal is wanted, prefer **cohesion/decision-load**, never a length formula.
- **Strunk & White:** keep its concision/concreteness instincts; discard its grammar prohibitions
  (Pullum: 3 of its 4 "passive" examples aren't passive). Don't cargo-cult rules-as-law.

#### A3 — Information ordering & the decision brief
- **Answer-first (BLUF) is the right default for *this* reader** — an expert who must *act*, not be
  persuaded or taught (scanning behavior + the levels effect, Kintsch; Army AR 25-50; Completed Staff
  Work: "answers, not questions"). The contested case where answer-first is wrong — *earning a surprising
  claim* — maps cleanly: the card face is BLUF; **`explain` is the reasoning-first surface.** Correctly split.
- **Minto's Pyramid:** answer at the apex, MECE grouped support, **every parent node a *synthesis*, never
  a topic label.** → maps onto the **fold**: a folded node's material must summarize its subtree, not
  label it (a depth/coherence link).
- **Decidability = five things, front-loaded:** framed question · MECE options each with what-it-entails
  (unblocks / breaks / **reversibility-cost**) · the lean · **the one assumption that, if wrong, flips
  it** — reproduced by staff-work + decision science (DQ chain; Bezos two-way door = reversibility) +
  tradecraft (CIA **Key Assumptions Check**; Martin "what would have to be true"; Klein **pre-mortem**).
- **THE convergence:** that list *is* hypercore's existing decision-card intent ("what it changes · a
  worked example · where the machine leans · the one thing that would flip it") and **grilling's
  lean+flip** — reproduced from scratch by three independent traditions. The **"flip" is the Key
  Assumptions Check.** External validation of the queue/grilling design.
- **Discourse cohesion:** chain old→new (zig-zag: end each sentence on the word the next opens with),
  stable topic strings (Williams: old-to-new = "the single most important principle of cohesion").
- **Signposting:** descriptive, front-loaded headings as scan anchors — but **don't over-bullet**;
  bullets strip connective reasoning, and the **reverse-cohesion effect** (McNamara) shows gaps make
  *high-knowledge* readers process actively, so over-explaining an expert *hurts*. Reasoning in prose.
- **Progressive disclosure:** Shneiderman "overview first… details-on-demand" — card face = overview +
  crux, detail one keystroke away (→ read-view seam, B). Never hide critical info or disclosure-hide
  options that must be *compared*.

#### A — synthesis (what distills into the standard)
**The one test (whole dive):** does a choice spend the operator's working memory on the *decision*, or on
decoding / hunting / re-reading? Keep what saves it; cut what spends it.

Three testable craft bars, by altitude:
- **Sentence:** right-branching · short dependencies (subject–verb adjacent) · given→new with the
  decision in the **stress position** · paired-dash interruptions short · no garden-path.
- **Flow:** chain old→new · stable topic strings · **keep the connectives** (don't telegraph) · reasoning
  in prose not bullets · don't over-explain an expert (reverse-cohesion).
- **Card/document:** answer-first (the lean) · MECE options + what-each-entails + reversibility · **the
  explicit flip** · every parent a synthesis not a label · detail one keystroke away.

**House voice — a corridor, not a cap.** Density is vindicated *between two guardrails*: never center-
embed / split subject–verb (A1), never over-compress / drop connectives (A2); and some gaps are *good*
for an expert (A3), so don't over-explain. Dense, allusive, em-dash prose is fine **inside** the corridor.
The thing to police is never word count.

**New internal links:** vocabulary-check guards the chunk economy · Minto-parent-summary ↔ the fold ·
`explain` = the reasoning-first surface · details-on-demand ↔ the read-view seam.

### C — Diagrams & illustration  *(research round in flight)*
Three agents: (1) when a picture beats prose + the grammar of a good diagram (Larkin & Simon, Tufte,
Cleveland & McGill graphical perception, Bertin); (2) diagrams on a character grid (box-drawing, text
sparklines, tables, the Monospace Web, the grid's hard limits); (3) tree/graph visualization & making
reasoning visible (the tree-is-the-model, focus+context for "the front of the tree stays legible," and
the "live visual of a model's reasoning, seen from several angles, in real time" intent statement).
Then everything distills into the clarity-standard spec prose + the candidate intent refinements.

#### C2 — Diagrams on a character grid (sharpens the beyond-TTY fork)
The grid renders **axis-aligned structure** cleanly and **free routing** (diagonals, crossings) badly —
so the terminal's native diagram set is exactly what hypercore shows.

- **Tables are the terminal's strongest diagram — the workhorse.** Decimal-aligned numbers +
  tabular-nums = instant magnitude comparison; "a single expert reading a dense decision surface wants
  the *number*" (Tufte: tables beat charts for small data sets). Add one **sparkline column** for shape
  without surrendering the digits. → default the decision surface to well-set tables.
- **Indented `├/└/│` trees beat node-link on a grid** (no crossings) and **operationalize "the front of
  the tree stays legible":** spend columns on the path being read, **elide interior depth**, keep 2-col
  indentation. → the **fold** *is* that elision mechanism. `git log --graph` on a busy repo is the
  cautionary tale (auto-laid-out node-link breaks). Don't render the whole tree as node-link.
- **Sparklines:** block `▁▂▃▄▅▆▇█` (8 buckets) for in-row trend; braille for a live series pane; **never
  where the exact number is the decision** (pair with the number). Block glyphs render *wider* — keep
  out of strictly-aligned tables unless the font is verified.
- **A third surface tier appears — the "rich grid" (Monospace Web).** Between pure-TTY and full-pixel
  sits a **still-monospace** read-view (Wickström): the `ch`-unit cell grid kept, but with a *chosen*
  font (JetBrains Mono holds box-drawing at 120%), **fractional leading 1.4–1.5** (B's win), truecolor,
  whole-character responsive steps. → buys B's typography wins **without losing grid discipline.**
- **Every TUI source independently lands on our color rule** — 16-color usable, truecolor only as
  redundant enhancement, color defined by function (btop/k9s/lazygit). Corroboration the rule generalizes.
- **Hard limits → pixels only for a narrow set.** Leave the grid **only** when the decision rides on
  *continuous 2-D position or continuous tone*: smooth curves, dense scatter, large topology w/
  crossings, gradients/heatmaps (→ sixel / Kitty graphics protocol). For everything structural & numeric
  the grid is **cheaper on working memory, not a compromise.**
- **hypercore verdict — three surface tiers, not two.** (1) pure TTY today; (2) **rich grid** read-view
  (font + leading + truecolor, grid kept) — the cheap, high-value upgrade that captures B's wins; (3) a
  **pixel pane** (Kitty/sixel) reserved for X = {smooth curve, dense scatter, gradient, large topology}.
  The decision surface stays on the grid; tier-3 is a narrow escape hatch. This is a far more defensible
  "beyond-TTY" step than "rebuild as a GUI."

#### C1 — When a picture beats prose, and the grammar of a good diagram
- **A diagram earns its place *computationally*, not informationally** (Larkin & Simon). It pays off only
  when it (a) co-locates what's used together (cuts search), (b) uses position to replace label-matching,
  or (c) lets a conclusion be read off perceptually. If it does none of these better than a clear
  sentence, **keep the sentence.** The "earns its place" test, for diagrams.
- **Encoding ranking — all three foundations agree, position first.** Quantitative → position, then
  length (bars/dots; never pies for magnitude). Categorical → position, then **hue**. Ordinal → position,
  then value/density (Cleveland & McGill; Mackinlay; Bertin). Only **position and size** are truly
  quantitative; **hue/shape are categorical only** → reinforces the color rule: **hue carries *kind/
  state*, never magnitude.**
- **Integrate or delete, never split** (split-attention vs. redundancy; Sweller/Kalyuga). Diagram
  unintelligible alone → put the label *on* the figure, not a distant legend. Self-sufficient → cut the
  restating prose.
- **Expertise reversal (Kalyuga) — the THIRD appearance of the expert-reader inversion.** Scaffolding,
  labels, and cues that help novices *burden* an expert; post-expertise "the best designs eliminated the
  text." → strip scaffolding to the bare self-sufficient artifact; signal sparingly (signaling is the
  weakest multimedia principle, and over-cueing *hurts* experts).
- **Micro-visuals: shape from a glyph, value from a number** (Radecki & Medow — sparkline wins trend,
  table wins exact value). A status glyph pops out in <250 ms, but only one *unique* cue per channel
  against a uniform field (conjunction search isn't pre-attentive). Matches C2 + the color round.
- **Tufte, adjudicated:** data-ink is an *optimum* ("within reason"), not a literal maximum; "chartjunk
  always harmful" is contested (Bateman/Borkin) — but the embellishment win is *memorability over weeks*,
  "largely irrelevant to a same-session decision tool," so **minimalism stays the default** here. Small
  multiples + sparklines sit on the firmest ground.

### ★ The spine of the whole dive — the expert-reader inversion (appears 4×)
The single deepest finding, now independently confirmed in four separate literatures:
- **D (legibility):** struggling-reader fixes (widened tracking) *slow* a fast expert.
- **A2 (diction):** the curse of knowledge lifts for a shared-schema reader; the danger inverts to
  **condescension / over-explaining**.
- **A3 (cohesion):** the **reverse-cohesion effect** — explicit connectives that help low-knowledge
  readers *hurt* high-knowledge ones (gaps make them process actively).
- **C1 (diagrams):** **expertise reversal** — labels/cues/scaffolding that help novices burden experts;
  the best expert design *eliminates* the text.

→ **The make-it-our-own principle:** hypercore's reader is an expert, so the universal clarity move is
**removal of scaffolding**, not addition — across words, type, *and* diagrams. This is *why* the dense,
allusive, low-scaffolding house voice is correct, not a liability. It earns first-class billing in the
clarity standard.

#### C3 — Tree viz & making reasoning visible
- **Indented outline is the right tree viz — and the fold is its superpower.** Depth = column position
  (the most accurate channel); it's the only natively-terminal layout and **the only one that folds
  without re-flowing the screen** (treemap/sunburst re-flow every sibling on collapse). "That stability
  *is* 'the front of the tree stays legible.'" Strong vindication of hypercore's existing design.
- **The fold = focus+context by elision** (Furnas fisheye / Card & Nation DOI trees) — and it sidesteps
  every distortion pathology of *warping* focus+context. Evidence-backed refinements:
  - drive the fold by a **degree-of-interest threshold**: keep active node + ancestors-to-root +
    immediate children full-size; fold the rest;
  - **never fold to an opaque node — fold to an aggregate *scent* cue** (child count + rough shape +
    pass/fail rollup) so the front advertises what's worth opening;
  - **multiple pinned foci** — single-focus DOI is fragile under concurrency, and hypercore runs work
    *concurrently*, so the tree view must hold a few active foci at once.
- **State by glyph FIRST, color SECOND** (Nothelfer: glyph+color 88% vs color-alone 66%). Each state
  unique in glyph *and* hue; reserve one slow, gentle motion for **"running" only**. ≤7 hues backed by
  Healey 1996 (the "7±2→Miller" attribution is a myth — the basis is color-search).
- **Lay out for path-following** (Ware 2002): path length → **continuity** (straight, un-jogged paths —
  the underrated aesthetic) → crossings → branching. Zero crossings is *free* for a tree; skip symmetry/
  orthogonality/curved edges (empirically inert).
- **Reasoning-viz — the honest finding.** CoT traces and attention maps are documented **unfaithful** to
  the computation (Turpin 2023; Anthropic 2025 — hint mentioned 25% of the time; Jain & Wallace 2019);
  attention heatmaps are seductive and largely non-actionable. The *only* positive evidence is **steering
  by acting on structure** — prune a branch, edit a step, reset-and-rerun (Vis-CoT +24 pts; AGDebugger).
  → **Build an intervention *loop*, not a window;** every view is a hypothesis surface tested by acting.
  **"Several angles in real time" is currently aspirational** — novel work, not assembly of proven parts.
  Be loudest about faithfulness exactly where the viz is most beautiful.
  - → **candidate intent refinement (touches a `[machine]` statement):** reframe intent's "live visual of
    a model's reasoning… tune in to what a model is thinking" around **intervention** (steer by acting on
    structure) + an honest **faithfulness caveat**. Mechanics if built: orthogonal coordinated views,
    brushing-and-linking, ~100 ms sync, visible decoupling when a view lags (Roberts; Baldonado).

#### C — synthesis
- **A diagram obeys the same "earns its place" test** as a word and a color: it pays only when it cuts
  search, replaces labels with position, or yields a perceptual read-off; else keep the sentence.
  Encoding rule: **position for magnitude, hue for kind** (never the reverse).
- **The surface settles into three tiers** (C2): grid is *native-excellent* for cards/tree/tables;
  a rich-grid read-view buys B's type wins cheaply; a pixel pane only for {smooth curve, dense scatter,
  gradient, large topology}.
- **hypercore's tree + fold is the evidence-backed right design** (C3) — indented outline + fold = the
  *good* focus+context; refine the fold to carry aggregate scent cues and hold multiple foci.
- **The reasoning view is an intervention loop, honestly faithfulness-bounded** — the one place the
  research says the *beautiful* thing (passive "see the mind") is the *wrong* thing.

---

## STATUS: research phase complete (lens · A · B · C · D all in). Next: distill into spec prose + the
## candidate intent-refinement stack. See "Distillation map" below.

## Distillation map — what this dive produces
**Two tracks.**
1. **The clarity standard (the filed ask, `communication-clarity`) — words.** A watched **clarity
   intent** + the **expert-reader-inversion** principle, carried as expanded `spec/communication.md`
   prose (preamble + a clarity requirement) that the **`communication` skill** renders from; register
   `communication` in `engine/methodology.py`'s `METHODOLOGIES`. No gated metrics (evidence-backed).
2. **The surface refinements — type/color/diagrams/tree/reasoning.** A stack of **candidate intent
   refinements** for the operator to ratify, several touching endorsed or `[machine]` intent:
   - **color** — "earns its place" = one redundant, pre-attentive, semantic cue; hue=kind not magnitude;
   - **contrast** — soft high contrast (~7–15:1), not maximal 21:1;
   - **surface tiers** — keep the grid for the decision surface; a rich-grid read-view; pixel pane only
     for the narrow continuous-field set;
   - **decision card** — sharpen toward the decidable-brief five (already largely present);
   - **tree fold** — fold to an aggregate scent cue; multiple foci under concurrency;
   - **state encoding** — glyph-first, color-redundant, motion only for "running";
   - **reasoning view** — intervention loop + faithfulness caveat (reframes a `[machine]` statement).
