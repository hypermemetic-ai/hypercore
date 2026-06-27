# communication-mastery — the synthesis

The conclusions of a re-run over the communication clarity standard, leaning toward the rare mastery of
language rather than the prior dive's expertise-license. Provenance: `research.md` (the eight ledgers).
This is the overview layer; nothing standing depends on it.

## The diagnosis (why the prior standard was confused)

The prior dive's spine was the **expert-reader inversion**: scaffolding that helps novices slows experts,
so "for an expert, clarity is the removal of scaffolding." From there it blessed the dense house voice,
and — the buried error — it **conflated two different things that both produce dense prose**:

- **Compression by shared lookup table (jargon).** "A term is a retrieved chunk, so in-group jargon *is*
  the plain version." Compresses by *referring* to code the reader already owns; saves the reader nothing
  and the writer the work of thinking. Its degenerate case is the cliché (Orwell's worn-out metaphor).
- **Compression by craft (mastery).** The load-bearing word, the live metaphor, the sentence whose shape
  is its argument — compression that *builds* the idea into a form the reader can decompress and keep,
  even a reader who did not already share the code.

These look identical on the page and are opposite in what they do to the reader. The prior dive built a
rigorous theory of **friction-removal** (don't make the expert re-parse) and mistook it for a theory of
writing. Worse, "removal of scaffolding" as the spine hands every obscure or lazy passage an alibi: *I'm
not unclear, I'm respecting your expertise.* That is the failure mode to kill.

## The spine (the reground)

> **Maximal compression and encryption are the same operation. They differ only in whether the decoder is
> shared.**

The recoverable length of a message is conditional on what the reader already holds (`K(x | reader)`, not
`K(x)`); the output of an optimal compressor is indistinguishable from noise *unless you hold the key*.
So dense prose splits on one axis — is the key shared:

- **Mastery** — short string whose decoder is structure the reader already runs; expands faithfully in
  their head. Rare encoder, wide output. The cost is paid by the **writer** (the architect).
- **Jargon** — the formally identical short string whose decoder is a private lookup table; ciphertext to
  anyone without it. Cheap encoder, narrow output. The cost is offloaded onto the **reader**.
- **Obscurity / preciousness** — short string with no shared decoder at all; encryption wearing depth's
  clothes.
- **Telegraphic** — lossy compression; joints dropped, the decoder cannot reconstruct.

The expert-reader inversion survives **as a conditioned corollary, not the spine**: remove scaffolding
*where the decoder is genuinely shared*; remove it anywhere else and you have merely encrypted. The burden
lands on the writer, which is the system's own ethic — operator attention is the scarcest resource, so the
architect pays the rare-encoder cost to spare it.

The register is **practical, not classic** (Thomas & Turner): the operator has a *job*. Classic style's
defining act is suppressing the hedge and staging the hard-won as effortless — and on a decision surface
the suppressed qualification is usually the payload. So the one inversion classic style cannot make:
**make the caveat land as hard as the recommendation.** Anyone can compress the headline; mastery
compresses the limitation. (This is grilling's flip and the decision card's reversibility, generalized
from the card to the voice.)

## The gate — four tests, run against the one reader

Each test arrived independently from a different literature; they converge. A compression is admissible
only if it passes all four:

1. **Regeneration.** The reader can re-derive the cases and limits from what they already hold (re-run,
   not merely assent). Fail → encryption. *(Round-Trip Correctness is the mechanical analogue.)*
2. **The exception survives.** The load-bearing caveat keeps its weight; the caveat rides *inside* the
   handle, not beside it, because the daily reader retrieves a gist-handle and memory drops what sits
   next to it. The map must not omit the cliff. *(NLI entailment is the mechanical analogue.)*
3. **Form-strip.** The felt-truth does not move when the cadence is stripped — beauty may carry an idea
   but never stand as its evidence (the rhyme-as-reason / fluency-as-truth bias). *(Paraphrase-invariance
   is the mechanical analogue; the softest of the four.)*
4. **This reader, not the gallery.** Audience is the operator on a tired afternoon, never peer admiration.
   Preciousness fails regeneration; showing-off is encryption with good PR.

Honest limit kept loud: compression is **necessary, not sufficient, for truth** (Chollet; Kelly; Kraus).
Short and decompressible can still be confidently wrong, so the gate is two-sided — decompressibility
*and* fidelity (the exception). The prior dive optimized neither; it optimized parse-cost.

## Application — making a model actually obey it

Stating principles in a skill does **not** reliably change an LLM's voice; the verdict from the four
application fronts:

- **Directives beat exemplars and re-fire across turns** (Bohr 2511.13972: instructions −56% vs examples
  −20% tokens; examples decay to baseline by the next turn). The skill's spine should be **3–6
  positive operational directives** — positive, never a ban-list (negation backfires — the pink-elephant
  effect), and *few* (instruction-following degrades with instruction count).
- **The un-stateable moves need a worked exemplar.** "Make the caveat land," "density the reader can
  decompress" resist statement; 1–2 tight **before→after pairs** carry the boundary a rule cannot.
- **A write-time self-check is the biggest multiplier.** Style is self-verifiable from the text (Self-
  Refine's favorable regime; *not* Huang's reasoning-correction failure), so the architect running the
  four tests over its own draft converts the standard from declared-at-load to executed-on-the-draft.
  Constraint: it edits **expression only, never the truth-claims** it has no oracle for.
- **Verbosity bias is the existential threat — and it vindicates the no-metric stance.** LLM judges reward
  padding (a "repetitive-list attack" fools weak judges 91%); readability formulas score artifacts
  (Liberman: one sentence swings five grade levels on punctuation; gibberish scores grade 3.9). So the
  final gate stays **human/architect judgment**; any loop must be counter-loaded (binary, located
  feedback; an explicit short-when-equal preference; a fresh-context critic to beat self-enhancement
  bias).

Two of the four tests are buildable as real checks: **Round-Trip Correctness** (regeneration) and **NLI
caveat-survival** (the exception). Form-strip is semi-soft; this-reader stays judgment.

## The scope decided (with the operator)

Maximal: **skill rewrite + enforced critique seam + built NLI check.** But a structural constraint then
narrowed *how* it lands (see below): the spine is authored, only the caveat-survival behavior is built.

## What changes, and the structural constraint

- **Authored directly (not foldable):** the preamble spine reground, the two reframed clarity requirements
  (watched prose), the `engine/check/scenarios.py` skill-content assertion. The fold (`delta._apply`)
  keeps the preamble verbatim and edits only requirements, so the spine *cannot* be built by a fenced
  worker — preamble change is architect authorship, the way preambles always change.
- **Built through a fenced codex worker (gated):** the one new behavior — a gated requirement that a
  dropped load-bearing caveat is caught before it crosses, its red→green scenario, and the engine seam on
  `communication.integrate`'s render path (caveat-survival routing) plus `communication_world.py` verbs.
  The entailment verdict is watched (model-driven); the routing is gated (a dropped caveat provably
  caught against a scripted oracle).

## Status

Filed, not built. The session also surfaced a live operational fact: the standing system folds its own
work — "the defined vocabulary stays consistent — the vocabulary check" landed on `spec/communication.md`
mid-session (54a116b), so the build must edit around it.
