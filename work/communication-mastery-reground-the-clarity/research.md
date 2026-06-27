# communication-mastery — the research ledgers (provenance)

Eight parallel research fronts: four on the idea (what mastery of compression is), four on application
(how to make a model obey it). Provenance — mined, distilled into `synthesis.md`; nothing standing depends
on this. Sources are named for verification. A sourcing caveat: the load-bearing claims rest on
well-established work (cited below); several bleeding-edge 2025–26 arXiv ids are corroborative and were not
all independently verified.

---

## PART ONE — the idea

### Front 1 — Classic style / the positive craft tradition
- **Classic style is a window** (Thomas & Turner, *Clear and Simple as the Truth*, Princeton 1994): prose
  presents a truth the writer has seen; the reader looks *through* it. It bars three hedges — of process,
  of worth, and **of liability** — and stages the hard-won as effortless.
- **Practical vs classic is the load-bearing split.** Practical style = the reader *has a job*, info for
  use. Classic = "neither writer nor reader has a job." **A decision surface lives in practical style's
  scene.** Classic's own concession: "clarity everywhere is not accuracy everywhere"; it "simplifies away
  complicated qualifications" — and on a decision surface the suppressed qualification is the payload.
- **Pinker's positive program** (*The Sense of Style*, 2014): good prose = "seeing the world"; orient the
  reader's gaze. Borrow the *window* and *arcs of coherence* (given-new); discard the "let the equal
  connect the dots" license on any load-bearing step.
- **Williams's GRACE** (the half the prior dive skipped): "a flash of elegance can fix a thought in our
  minds." Borrow **end-weight** (the load-bearing term in the stress position — what is elaborated is
  retained, Craik & Lockhart 1972 levels-of-processing). Refuse *suspension* (anti-BLUF) and ornament that
  bends the true claim to fit a rhythm.
- **Transmit vs land** (Heath & Heath, *Made to Stick*; Craik & Lockhart): most prose transmits a thought
  the reader forgets; good prose builds it into a form they keep. Stickiness is orthogonal to truth — slave
  every stickiness device to accuracy; never make a hedge less sticky than the headline.
- **Synthesis:** mastery here = the *practical* register raised by classic concreteness + graceful
  end-weight, with the inversion the genre forces: make the uncertainty itself land.

### Front 2 — Understanding as compression (the keystone)
- **MDL / Kolmogorov** (Rissanen 1978; Grünwald 2007; arXiv:1908.08484): the best model is the shortest
  description; regularity = compressibility; compression and explanation are one act. Limit: "shortest" is
  uncomputable and **code-relative** — the codebook (the reader) is part of the spec.
- **Simplicity principle** (Chater & Vitányi, *TICS* 2003; Feldman PMC5125387): the mind seeks the shortest
  encoding (efficient coding, Barlow). Contested as *the* primitive (may be a Bayesian likelihood drive).
- **Compression progress = beauty/insight** (Schmidhuber, arXiv:0812.4360): the "aha" is the first
  derivative — discovering a better encoding. Explains why an elegant line *feels* like insight; but it
  tracks novelty, **not truth**.
- **Compression ≈ intelligence, critically** (Hutter Prize; Huang et al. arXiv:2404.09937, bpc vs
  benchmark r≈−0.95). Counter (Chollet, arXiv:1911.01547): intelligence = generalization to novel tasks,
  not succinctness over seen data; compression is **necessary, not sufficient**.
- **THE CRUX — decompressible vs encrypted.** The relevant quantity is `K(x | y)` — shortest *given the
  reader's prior knowledge y*. **The encryption identity:** an optimal compressor's output is
  indistinguishable from random *unless the decoder is shared* (Slepian–Wolf / Wyner–Ziv side information;
  arXiv:1511.03602; MDPI *Information* 11(4):196). Jargon = compression to a private table (ciphertext to
  outsiders). Insight = compression to structure the reader already runs. Named on the decoder side: Clark
  & Brennan "Grounding in Communication" (1991, common ground); Sperber & Wilson Relevance Theory; Pinker's
  curse of knowledge (assuming a shared decoder that isn't there). Limit: decompressibility is
  reader-relative and testable only behaviorally; short+decompressible can still be lossy or false (Kelly,
  "Ockham's Razor, Truth, and Information").
- **Operational test:** (1) regeneration — can this reader re-derive the cases? (2) fidelity — does the
  re-run include the exception? Pass both = earned brevity; fail either = well-typeset ciphertext.

### Front 3 — Metaphor & the aphorism as understanding-mechanisms
- **Conceptual metaphor** (Lakoff & Johnson, *Metaphors We Live By*, 1980): metaphor imports the source
  domain's inferential structure — understanding, not ornament. Counter: it highlights-and-hides; it
  smuggles entailments faster than the reader audits them.
- **Structure-mapping** (Gentner, *Cognitive Science* 1983): a generative analogy transfers *relational
  structure* and yields **candidate inferences**; systematicity governs quality. Surface match is
  decoration and the main vector for false mapping (experts reject misleading surface remindings faster).
- **Aristotle** (*Poetics* 22; *Rhetoric* III.10–11): mastery of metaphor is "the mark of genius"; it
  delivers a fresh idea at minimal cost (energeia, bringing-before-the-eyes). Fenced: too far = riddle, too
  near = trivial; it persuades by ease, which can substitute for proof.
- **The aphorism** (Bacon: "Aphorisms, representing a knowledge broken, do invite men to inquire
  further"; La Rochefoucauld; Gracián; Lichtenberg): a whole model in one portable sentence; its
  incompleteness is generative. Counter (Karl Kraus): "in an aphorism, aptness counts for more than truth"
  — memorability is bought by dropping the qualifier.
- **The live/dead line** (Orwell, "Politics and the English Language", 1946): the prefab phrase is the
  death of thought — "a term is a retrieved chunk" is his failure mode named approvingly. But Orwell
  over-reaches: a precise *frozen* term ("iron resolution," genuine jargon) compresses real meaning. So
  the axis is **not** live-vs-dead novelty but **does the figure still do cognitive work for *this*
  reader**.
- **The discriminator — the entailment audit:** a figure earns its place only if (a) cashing it into plain
  language yields a true, decision-relevant inference the plain sentence would not, and (b) none of its
  silent entailments is false on the weight-bearing surface. Vividness is the anesthetic that suppresses
  the audit.

### Front 4 — Memorability, and the counter-case
- **Memorability is load-bearing for a daily reader** (not "irrelevant to a same-session tool," as the
  prior dive dismissed): the reader re-retrieves a gist-handle, not the sentence (Brainerd & Reyna,
  fuzzy-trace; Miller/Chase & Simon chunking). The handle is a higher-fidelity, lower-cost cue, paid for
  once via the **generation effect** (Slamecka & Graf 1978) and **desirable difficulties** (Bjork) — a
  compression the reader can *just barely* unpack outperforms spoon-fed prose; one they cannot is strictly
  worse than plain.
- **The Keats heuristic** (McGlone & Tofighbakhsh, *Poetics* 1999; *Psych Science* 2000): fluent/rhyming
  form is judged truer and sticks — same effect that biases. **Form-strip defuses it:** told to judge the
  claim not the poetry, the rhyme-truth advantage collapsed.
- **Fluency → false confidence** (Alter & Oppenheimer 2009; Fazio et al. 2015, "knowledge does not protect
  against illusory truth"). **Erudite-vernacular penalty** (Oppenheimer 2006): needless complexity is
  judged *less* intelligent — preciousness ≠ mastery.
- **Where the genius lean must be forbidden:** (1) where beauty carries the truth-claim — force a
  form-stripped accuracy check; (2) where the qualifier is the payload — demand plain, evidence-tight prose
  (gist drops a caveat that sits beside the handle); (3) where the audience is the peer gallery.
- **The operational guardrail:** compress only to a handle this reader can unpack alone; put the caveat
  *inside* the handle. Admissible iff (a) it sits in Bjork's desirable band, (b) it survives the McGlone
  form-strip, (c) its qualifier survives in the gist.

---

## PART TWO — application

### Front A — What actually changes an LLM's prose
- **Directives beat exemplars and persist across turns** (Bohr, arXiv:2511.13972: instructions −56% vs
  examples −20% tokens; examples expand back to baseline on the next turn). A stated positive directive is
  the strongest, most durable single lever for the *stateable* part.
- **The slop register is a trained-in attractor** (Kobak et al., *Science Advances* 2025 / arXiv:2406.07016
  — excess style vocabulary; RLHF length/sycophancy bias, arXiv:2403.19159). A one-time instruction fights
  a standing gradient.
- **Negation backfires** (pink-elephant, arXiv:2404.15154): state what TO do, never ban-lists.
- **Instruction-following decays with count and over long context** (arXiv:2507.11538; lost-in-the-middle;
  "style amnesia" → periodic reinforcement). Re-invoke the standard at write-time, not only at load.
- **Form:** a few positive directives (durable spine) + 1–2 contrastive before→after pairs (the
  un-stateable moves) + a short self-applied write-time checklist (Self-Refine ~20% gain).

### Front B — Critique-and-revise, LLM-as-judge
- **Constitutional AI** (Bai et al., arXiv:2212.08073): a written principle → critique → revise loop
  measurably moves output; apply our four tests as an ensemble, not one sampled at a time.
- **The editing/reasoning asymmetry** (Self-Refine, Madaan arXiv:2303.17651: +14–49 on style, ~0 on math;
  Huang arXiv:2310.01798: LLMs cannot self-correct *reasoning* unaided). Clarity-revision is editing — the
  favorable side — so a self-check works, **bounded to editing expression, never the truth-claims**.
- **Verbosity/length bias** (Zheng et al. MT-Bench, arXiv:2306.05685: repetitive-list attack fools weak
  judges 91%, GPT-4 8.7%) — points exactly opposite a dense-prose goal. Self-enhancement bias inflates a
  model's grade of its own prose ~10–25%; a fresh-context critic decorrelates it. Feedback must be
  **binary and located**, not a score (G-Eval drifts pro-fluency).

### Front C — The four tests as computable checks
- **Regeneration → Round-Trip Correctness** (RTC, Allamanis et al. arXiv:2402.08699): compress → reader-
  model re-derives → score equivalence (aim at consequences, not words). Backed by ICAE reconstruction
  (arXiv:2307.06945), LLMLingua/Gist task-retention, the Information Bottleneck (Tishby).
- **The exception survives → NLI entailment** (SummaC arXiv:2111.09525; FactCC arXiv:1910.12840): premise =
  the compressed line, hypothesis = the load-bearing caveat; not entailed → the cliff was dropped. Cheap,
  binary, off-the-shelf. Coverage via QA-generation (QuestEval, QAFactEval) with a mandatory question about
  the qualifier.
- **Calibrated hedging** (IPCC calibrated language; Kent's Words of Estimative Probability; Budescu 2009/14
  — verbal hedges regress toward 50%): a load-bearing qualifier must be a banded term, with the number
  attached.
- **Form-strip → paraphrase-invariance** (ParaRel arXiv:2102.01017; metamorphic testing): re-render in N
  neutral paraphrases; if judged truth shifts, form carried the persuasion. Semi-soft (needs a truth
  oracle).
- **Prompt-compression cousins** (LLMLingua arXiv:2310.05736; LongLLMLingua arXiv:2310.06839; LLMLingua-2):
  admissible = the dropped material was low-information *given the consequences*; lossy = you removed
  something the answer is conditioned on. "Question-aware perplexity drop" ≈ "is this clause load-bearing."
- **Verdict:** two tests buildable (RTC, NLI); the single most decisive is **NLI caveat-survival**.

### Front D — Deployed reality / the skeptic
- **A loaded skill is the floor, not the mechanism.** Instruction drift within ~8 turns (Li et al., COLM
  2024, arXiv:2402.10962); Intercom's content agent: "guidelines alone proved insufficient"; even the lab
  that publishes its prose system prompt moves voice into post-training.
- **The readability-tool trap** (Liberman, Language Log: same sentence 4.4/8.5/12.5 by punctuation;
  gibberish grade 3.9; Hemingway's own "Technical mode" admits it strips nuance). Confirms the no-metric
  stance: a numeric gate would punish the compressed-expert register.
- **The editor seam** (Self-Refine; Huang reconciled — style is self-verifiable, reasoning is not): a
  draft→critique→revise pass against an explicit rubric is the highest-leverage add-on.
- **Minimum apparatus, ranked:** (1) principles as concrete positive directives; (2) a self-critique pass
  against the checklist; (3) 3–5 before/after exemplars; (4) optional fresh-context editor pass; (5) one
  non-scoring mechanical tripwire that *summons* judgment, never a gate.
- **Verdict for the operator:** stating the principles is not enough; the realistic ceiling of prompt-only
  is a noticeable-but-unreliable shift. The minimum that reliably changes the voice is directives +
  exemplar + write-time self-check; the deepest "what to cut, what altitude to hold" stays the residue a
  human/architect gate keeps earning.
