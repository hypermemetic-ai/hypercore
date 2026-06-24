# communication — what the dive concluded

The distilled conclusions of the communication deep dive. This is the **overview layer**; the evidence,
the contested magnitudes, and the inline sources live one layer down in `research.md`. Both are
**provenance** — they informed the standard and the refinements; nothing standing depends on them.

The target throughout: **one expert reader who reads a lot and makes hard decisions all day.** Not a
novice, not a crowd. That single fact bends almost every finding.

---

## The one test

> **Does this choice spend the operator's working memory on the *decision*, or on decoding, hunting, or
> re-reading?** Keep what saves it; cut what spends it.

This is the whole standard in one line (Cognitive Load Theory, made ours). It is also *why* we refuse
readability metrics: they measure length; this measures load. Intrinsic difficulty — a hard decision —
is sacred and irreducible. Extraneous load — presentation friction — is the only enemy.

## The spine — the expert-reader inversion

The deepest finding, confirmed independently in **four separate literatures**:

| Literature | The inversion |
|---|---|
| Legibility (D) | Struggling-reader fixes (widened letter-spacing) **slow** a fast expert. |
| Diction (A2) | The curse of knowledge lifts for a shared-schema reader; the danger becomes **condescension**. |
| Cohesion (A3) | The **reverse-cohesion effect** — explicit connectives that help novices **hurt** experts. |
| Diagrams (C1) | **Expertise reversal** — labels and scaffolding that help novices **burden** experts. |

> **The make-it-our-own principle: for an expert, clarity is the *removal* of scaffolding, not its
> addition — across words, type, and diagrams.**

This resolves the question the dive opened with. hypercore's prose is dense, allusive, low-scaffolding —
and that is **correct**, not a liability. The standard does not flatten the house voice; it gives the
voice a corridor.

---

## The clarity standard — words, three altitudes

**Sentence.** Difficulty for a skilled reader is working-memory load *during parsing* — dependency
length and held-open structure — **not** length, formality, or density (Gibson). So the bar is not
"shorter":

- right-branching (state the core early, append rightward);
- subject and verb adjacent (short dependencies);
- given→new, with **the decision in the stress position** (the syntactic close);
- paired em-dash interruptions kept short; a *trailing* dash is free;
- no local garden-path ambiguity.

A long sentence is low-load inside that corridor. **Police structure — subject–verb distance, embedding
depth, dropped connectives — never word count.**

**Flow.** Chain old→new across sentences (end each on the word the next opens with); hold a stable cast
of subjects; **keep the connectives** — over-compression that strips cohesion does not aid comprehension,
it shifts load onto the reader (Duffy & Kabance). Carry reasoning in prose, not fragmented bullets. The
house voice's real failure mode is *telegraphic*, not *long*.

**Card / the decision brief.** A brief is *decidable at a glance* when it carries, front-loaded:

- the recommendation first (the lean);
- a MECE set of options, each with what it entails — what it unblocks, what it breaks, and the **cost to
  reverse** it;
- **the flip** — the one assumption that, if wrong, changes the recommendation;
- every parent node a *synthesis*, never a topic label;
- detail one keystroke away, never hidden behind a hunt.

**Diction.** One term, one concept — repeat the ratified name verbatim; synonym-variation of a defined
term is a clarity bug (Fowler). In-group jargon **is** the plain version for the one expert reader (a
term is a retrieved chunk), so keep the shared language tight rather than diluting it. A hard word earns
its place only by naming a distinct chunk. Hedge to the evidence, not the nerves. Police elided *steps
and state*, not vocabulary. **No readability gate** — judge cohesion and decision-load, never length.

---

## The surface — type, color, diagrams, tree, reasoning

**Type (B/D).** Measure 55–66 characters; leading 1.4–1.5; left-aligned ragged; weight 400–500 with bold
for emphasis only; a face chosen for **character disambiguation** (l/I/1, rn/m, O/0); no all-caps runs;
no long italic runs. Serif-vs-sans is folklore. **Never widen tracking** — it slows an expert.

**Color.** One redundant, pre-attentive, semantic cue — ≤6–7 load-bearing hues plus one reserved alarm,
**never the sole carrier** (always doubled by a glyph), carrying meaning the words don't. **Hue = kind,
not magnitude.** And the division of labor that resolved the apparent conflict in the research:

> **Color carries *state* (what to look at). Space, size, and weight carry *structure* (hierarchy).
> Never cross them.**

**Contrast.** Soft high contrast (~7–15:1), warm dark-on-off-white default — **not** maximal 21:1, which
fatigues an all-day reader. A soft dark toggle, because polarity is eye-dependent.

**Diagrams.** A picture earns its place only when it cuts search, replaces label-matching with position,
or yields a perceptual read-off (Larkin & Simon); else keep the sentence. **Position for magnitude, hue
for kind.** Integrate labels into the figure or delete redundant prose — never strand them in a distant
legend. For a same-session decision surface, **minimalism is the default** (the "useful junk" evidence is
about week-later *memorability*, which we don't need). **Tables are the workhorse** — decimal-aligned
numbers plus a sparkline column for shape; the expert wants the number.

**The surface, in three tiers** (this is the answer to "beyond the TTY?"):

1. **Pure TTY** — today.
2. **Rich grid** (the "Monospace Web") — *still the cell grid*, but a chosen font, real 1.4–1.5 leading,
   truecolor, character-stepped layout. Captures the type wins **without losing grid discipline.** The
   cheap, high-value upgrade.
3. **Pixel pane** (sixel / Kitty graphics) — reserved for the narrow set the grid genuinely can't render:
   smooth curves, dense scatter, gradients, large crossing topology.

The decision surface — cards, tree, queue, tables — stays on the grid, where it is *cheaper* on working
memory, not compromised.

**Tree + fold.** The indented outline is the right tree visualization and the only one that **folds
without re-flowing the screen** — and the fold *is* focus-plus-context by elision, the good kind. Refine
it: **fold to an aggregate scent cue** (child count + shape + pass/fail rollup), never to an opaque node;
**hold multiple foci**, since hypercore runs work concurrently. Lay out for path-following (continuity —
straight, un-jogged paths).

**State.** Glyph first (survives no-color, piped output, color-blindness), color second as the redundant
amplifier; one slow, gentle motion for "running" only.

**The reasoning view.** The honest finding: CoT traces and attention maps are documented **unfaithful**
to the computation, and visualizing them can mean visualizing a confabulation. The only positive evidence
is **steering by acting on structure** — prune a branch, edit a step, reset-and-rerun. So the reasoning
view is an **intervention loop, not a passive window**, and "several angles in real time" is currently
*aspirational* — novel work, faithfulness-bounded, not the assembly of proven parts.

---

## What this validates in hypercore

The dive's surprise: it mostly **handed hypercore its own decisions back, with sources attached.**

- The **decision-card** intent was reproduced, independently, by military staff-work doctrine, decision
  science, and analytic tradecraft.
- **Grilling's "flip" is the CIA's Key Assumptions Check** — the same move, named three ways.
- The **tree + fold** is the evidence-backed right design (indented outline + focus-plus-context).
- The **color rule** is where every serious TUI independently lands.
- **One-term-one-concept** is Fowler's "elegant variation" vice plus the technical-writing consensus.
- The **dense house voice** is vindicated by the expert-reader inversion.
- **vocabulary-check** turns out to guard the *chunk economy*, not just tidiness.
- The **no-metrics** decision is fully backed by the evidence.

## What changes — candidate intent refinements (for ratification)

Each is **machine-owned** until the operator ratifies it. Several touch endorsed or `[machine]` intent.

| # | Statement today | Proposed refinement | Touches |
|---|---|---|---|
| 1 | "color spent only where it earns its place" | "earns its place" = one redundant, pre-attentive, semantic cue; hue=kind not magnitude; color=state, space/weight=hierarchy | endorsed |
| 2 | "high-contrast" | soft high contrast (~7–15:1), warm dark-on-off-white; not maximal 21:1; soft dark toggle | endorsed |
| 3 | "a pure-frame render off a TTY" | three surface tiers; decision surface stays on the grid; rich-grid read-view; pixel pane for the narrow continuous-field set | endorsed |
| 4 | decision-card contents | sharpen toward the decidable-brief five (lean · options+reversibility · the flip · synthesis-not-label · detail one keystroke away) | endorsed (mostly present) |
| 5 | the fold / tree view | fold to an aggregate scent cue, not an opaque node; multiple foci under concurrency | endorsed |
| 6 | node/state rendering | glyph-first, color-redundant; motion only for "running" | (new) |
| 7 | "a live visual of a model's reasoning… tune in to what a model is thinking" `[machine]` | an **intervention loop** (steer by acting on structure) + an honest faithfulness caveat | `[machine]` |

## What we deliberately rejected (debunked / folklore)

- **Readability formulas as a gate** — measure two surface proxies, gameable, reward cohesion-destroying
  edits, penalize precise terms.
- **Dyslexia fonts** (OpenDyslexic/Dyslexie) — no measured benefit; the letterforms contribute nothing.
- **"Never use the passive"** — Strunk & White couldn't even identify passives (Pullum); passive is a
  flow tool.
- **Widened letter-spacing** — helps struggling readers, **slows** an expert.
- **"Chartjunk is always harmful / maximize data-ink"** — aesthetic doctrine; data-ink is an optimum,
  not a maximum.
- **Attention maps as explanation** — seductive, largely non-actionable, and unfaithful.
- **Maximal 21:1 contrast** — the wrong ceiling for an all-day reader.
- **Over-cueing / over-explaining an expert** — the inversion; scaffolding burdens.

## Open and aspirational

- The **reasoning cockpit** (intervention loop, several orthogonal coordinated views, brushing-and-
  linking, ~100 ms sync) is real but **novel work**, and faithfulness-bounded — be loudest about
  faithfulness exactly where the view is most beautiful.
- The **surface-tier move** is an architectural direction the operator owns.
- Evidence is **real but modest** in places (graph-aesthetic and tree-navigation samples n≈12–32; the
  sparkline base is thin) — directionally trustworthy, exact magnitudes not measured for our case.

---

*Provenance: `research.md` (the ledger — full findings, contested magnitudes, inline sources). The dive
ran as parallel research rounds across the governing lens and dimensions A (verbal craft), B (typography),
C (diagrams/tree/reasoning), and D (accessibility & cognition).*
