---
kind: ask
state: standing
owner: machine
created: 2026-06-22
---
# agent-facing-hardening — make the derived channels bulletproof (structure) and correct (content)

The agent-facing channels — `AGENTS.md` (the always-on anchor) and the five `skills/<name>/SKILL.md` —
were put to a panel of independent researchers on 2026-06-22 (full audit: `research.md`, this folder).
The verdict: above field median on craft and content, but carrying real, fixable defects the operator
was right to suspect. This arc closes them. A fresh session reads this file top to bottom, then the
report for line-precise loci; the conversation that produced both is disposable.

## the load-bearing reframe — read before touching anything

These artifacts are **derived**, never hand-authored. `AGENTS.md` is rendered by `engine/anchor.py`
(an authored operational residue plus a skills index derived from the registries); each skill is
rendered by `engine/methodology.py` from its `spec/<cap>.md` slice (`depth` from `spec/depth.md`);
`engine/channels.py` is the registry whose `materialize` re-renders all of them on every fold. So a
hand-edit of any `.md` is overwritten by the next fold. **Every fix in this arc lands in a spec slice
or a generator — never in the rendered file.** This is the discipline that already gives these
channels zero drift (the one anti-drift mechanism the repo proved); the work is to point it at what
it does not yet reach, not to bypass it.

## P0 — defects the channels must not ship with

- **The channels may target the wrong harness — the highest-stakes finding.** Current Anthropic /
  Claude Code docs (verified 2026-06-22) say the harness reads `CLAUDE.md`, not `AGENTS.md`, and
  discovers skills under `.claude/skills/`, not a root `skills/`. `engine/anchor.py`'s docstring
  claims "Claude reads it directly when no `CLAUDE.md` is present" — false for stock Claude Code, in
  which the anchor and all five skills would load as **nothing**. The deciding variable is which
  harness the architect actually runs at runtime; this is the open question below. Fix: confirm the
  harness, then either (a) materialize a `CLAUDE.md` bridge (`@AGENTS.md`) and mirror skills to
  `.claude/skills/` as derived channels in `channels.py`, or (b) record that the architect's harness
  loads `AGENTS.md` + root skills natively. Either way, correct the false docstring in `anchor.py`.
- **`architecture-review` overclaims a capability the engine does not have.** The skill advertises a
  model-driven shallow/leakage/deletion-test "depth verdict"; the engine ships only the length signal
  plus two mechanical AST rules (ADR 0020). The honest limit is currently buried at the end of a long
  bullet. Fix in `spec/architecture-review.md`: lead the requirement with what is built, relegate the
  verdict to a marked roadmap line; the faithful render fixes the skill automatically. **Coupled to
  `engine-hardening`'s depth-gate call** — if that arc ships a mechanical depth proxy, the claim
  narrows rather than disappears; sequence the wording after that decision.
- **Machine-costly prose — the writing the channels are made of.** The research tied specific
  constructions to measured instruction-following degradation: a single ~167-word requirement
  statement (`spec/architecture-review.md`), compound negation (`spec/coherence.md` —
  "never a silent veto and never a silent pass", ×2), and ADR cross-refs wedged mid-clause between
  verb and predicate. Fix at the source: split the over-packed statement into one-instruction
  sentences, positivize the compound negations, move every `(ADR NNNN)` to line-end. The dense house
  style is an asset — the cut is the ~15% of excess, not the voice. (Full before→after set and a short
  style guide encodable in the generators: `research.md`, Part C.)

## P1 — structural and content hardening

- **Add an external-conformance gate to `python3 -m engine --check`.** The engine guarantees "the
  rendered artifact matches my spec" but never "it matches the field standard" or "its links resolve."
  Add a check that validates SKILL.md frontmatter against a schema, runs a skills reference/validator,
  and link-checks the rendered artifacts. This is itself a red→green opportunity — let it go red on a
  current defect first (see sequencing).
- **Retire the hand-frozen worker preamble — the same drift the system already outlawed.** The
  `WORKER` constant in `engine/worker.py` hand-restates `spec/worker.md` — a frozen second copy, the
  exact smell that retired `worker.DEPTH`. Single-source the worker's discipline prose into the worker
  prompt from `spec/worker.md`, leaving only the genuinely non-inferable envelope authored. This is
  also where `engine-hardening`'s grounding implications land (the gated-vs-watched register and the
  corrected single-writer invariant the worker must be taught — see cross-arc coupling).
- **Add the missing per-capability vision bindings.** Three discipline slices (`depth`,
  `design-it-twice`, `architecture-review`) lack the `<!-- vision: ... -->` binding ADR 0020
  introduced, so the operator view shows no authored vision beside the capabilities that most embody
  it. Add them at the slice; decide explicitly whether `folding-conditions` is pure machinery (and so
  correctly shows none).

## P2 — quality

- Strengthen the load-bearing `arXiv:2602.11988` citation in `anchor.py`: the paper is real and its
  finding is harsher than the paraphrase (context files can *reduce* task success). The "keep the
  anchor minimal" decision is well-grounded; cite the stronger result.

## the number-of-skills call — keep five

The operator's boundary is correct: a methodology a **role** runs becomes a skill (`design-it-twice`,
`grilling`, `coherence`, `architecture-review`, `depth`); a mechanism the **engine** runs (graph,
queue, interface, self-model, schedule, worker, folding-conditions) does not. ADR 0022's scheduler
independently confirms it — a capability slice, no skill question. The one genuine coverage gap is the
worker's own discipline, and it is correctly **not** a sixth skill: it is always-on, so it belongs in
the worker prompt (the P1 single-sourcing above), not in the on-demand routing. Net: five skills,
unchanged in count; the defects are in their content and targeting, not their number.

## recommended sequencing — verify, then dogfood the red→green

1. **Resolve the deciding variable first** (the open question below): confirm the architect's runtime
   harness. The harness answer scopes the P0 targeting fix from "ship a bridge" to "record a fact."
2. **Build the conformance gate to go red on a live defect, then green** as the P0/P1 source fixes
   land — a genuine feedback-loop record, the discipline applied to the channels themselves.
3. The prose and overclaim fixes ride along; the overclaim wording waits on `engine-hardening`'s
   depth-gate decision.

## cross-arc coupling — `engine-hardening`

- The `architecture-review` overclaim resolves differently depending on whether the engine ships a
  mechanical depth proxy; sequence the wording after that call.
- The worker grounding (P1) must encode what `engine-hardening` finds the harness does **not** gate —
  a machine-readable gated-vs-watched register — and must teach the corrected single-writer invariant
  (stage exact files, lock spanning write→commit) rather than the current false one. The grounding
  change lives here; the engine fix lives there; they fold together.

## what this arc deliberately does NOT do

It does not add or remove skills, rewrite the house style, or re-derive the channel architecture (the
derive-on-fold mechanism is the asset it builds on). It does not fix the engine bugs that motivate the
grounding changes — those are `engine-hardening`; this arc only encodes what the worker must be told.

## provenance (this folder)

- `research.md` — Report 1, the agent-facing-artifacts audit (four independent researcher seats
  synthesized; structure, content, and machine-writing parts; full sources). Material, cited not
  depended on: the self-sufficient ask is above.

## folding condition

Every P0 defect is closed by a spec-slice or generator delta — or consciously deferred with a recorded
reason on its node, none silently dropped; the external-conformance gate runs in
`python3 -m engine --check` and is green; the architect's runtime harness is confirmed to load the
channels, or a derived bridge makes it so; the five-skill roster stands as ratified. The depth-related
overclaim wording folds with `engine-hardening`'s depth call. [machine]
