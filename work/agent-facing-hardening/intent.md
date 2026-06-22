---
kind: ask
state: standing
owner: operator
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

## ratified — operator decisions (2026-06-22)

Settled in session before the build opens; the arc is operator-owned from here.

- **Channel targeting → verify empirically first.** A fresh session probes what the architect's
  `claude -p` harness actually loads, then ships the derived bridge if the channels do not auto-load,
  or records native loading if they do — the `anchor.py` docstring fix lands either way.
- **The `architecture-review` overclaim → de-claim** (with `engine-hardening`'s depth call): depth is
  judgment-only, the model-driven verdict marked unbuilt. The spec edit is owned there; this arc
  confirms the rendered skill reads honestly once it folds.
- **Sequencing → parallel** with `engine-hardening`; the one cross-dependency (the de-claim → skill
  confirmation) is honored across the two concurrent sessions.

## P0 — defects the channels must not ship with

- **The channels may target the wrong harness — the highest-stakes finding.** Current Anthropic /
  Claude Code docs (verified 2026-06-22) say the harness reads `CLAUDE.md`, not `AGENTS.md`, and
  discovers skills under `.claude/skills/`, not a root `skills/`. `engine/anchor.py`'s docstring
  claims "Claude reads it directly when no `CLAUDE.md` is present" — false for stock Claude Code, in
  which the anchor and all five skills would load as **nothing**. The deciding variable is which
  harness the architect actually runs at runtime. **Ratified: verify first** — a fresh session
  empirically probes what the architect's `claude -p` harness actually loads, then ships either
  (a) a derived `CLAUDE.md` bridge (`@AGENTS.md`) plus skills mirrored to `.claude/skills/` in
  `channels.py` if the channels do not auto-load, or (b) a recorded note that they load natively if
  they do. The false docstring in `anchor.py` is corrected either way.
- **`architecture-review` overclaims a capability the engine does not have.** The skill advertises a
  model-driven shallow/leakage/deletion-test "depth verdict"; the engine ships only the length signal
  plus two mechanical AST rules (ADR 0020). The honest limit is currently buried at the end of a long
  bullet. **Resolved by `engine-hardening`'s depth-gate call — de-claim:** that arc rewrites
  `spec/architecture-review.md` (and `spec/depth.md`) so depth is judgment-only and the model-driven
  verdict is marked unbuilt, and the skill renders from that slice. This arc's job narrows to
  confirming the rendered skill reads honestly once the de-claim folds.
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

1. **Verify the harness first** (ratified): a fresh session probes what the architect's `claude -p`
   harness actually loads, which scopes the P0 targeting fix to shipping the bridge or recording a fact.
2. **Build the conformance gate to go red on a live defect, then green** as the P0/P1 source fixes
   land — a genuine feedback-loop record, the discipline applied to the channels themselves.
3. The prose fixes ride along; the `architecture-review` skill confirmation waits only on
   `engine-hardening`'s de-claim folding (the two arcs otherwise run in parallel).

## cross-arc coupling — `engine-hardening`

- The `architecture-review` de-claim wording is owned by `engine-hardening` (its depth-gate call); this
  arc only confirms the rendered skill once it folds. The arcs run in parallel; only that one
  confirmation waits.
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
overclaim wording folds with `engine-hardening`'s de-claim.

## result

Built in the fenced worktree on branch `agent-a5a7b08c674db6a18` (worktree
`.claude/worktrees/agent-a5a7b08c674db6a18`). `python3 -m engine --check` is **green — slices 1–17**.

### what landed

- **P0 targeting — the derived bridge.** Empirically confirmed against current Anthropic docs
  (verbatim *"Claude Code reads `CLAUDE.md`, not `AGENTS.md`"*; skills discovered under
  `.claude/skills/`, not a bare root `skills/`): the channels do **not** auto-load in stock Claude Code.
  Shipped the bridge as derived channels in `engine/channels.py` — a `CLAUDE.md` whose body is the
  `@AGENTS.md` import (`anchor.bridge`/`anchor.bridge_materialize`), and the five skills mirrored into
  `.claude/skills/<cap>/SKILL.md` alongside the harness-neutral `skills/` (`methodology.SKILL_DIRS`,
  `materializers()` now renders each cap into both). Both regenerated by the fold, never hand-copied.
  Corrected the false docstring in `engine/anchor.py` (and the matching line in `channels.py`).
- **P0 prose** (owned slices): positivized the compound negation in `spec/coherence.md` (×2,
  "never a silent veto and never a silent pass" → "surface as exactly one of two outcomes — a fold, or
  a decision/depth decision …"); moved every mid-clause `(ADR NNNN)` to line-end in `spec/coherence.md`,
  `spec/grilling.md`, `spec/design-it-twice.md` (incl. the bare-subject fix in design-it-twice's
  preamble). The fold re-rendered the skills; the rendered SKILL.md files carry the fixes.
- **P1 conformance gate** — `engine/check/slice17.py`, wired into `python3 -m engine --check` (appended
  to the imports and `SLICES` tuple in `engine/check/__init__.py`). Validates each rendered SKILL.md's
  frontmatter against the documented Claude Code schema (name regex/≤64/==dir; description non-empty/
  ≤1024), asserts the discovery-location invariant (skills in `.claude/skills/`, the `CLAUDE.md`
  `@AGENTS.md` bridge), and link-checks every rendered `spec/<cap>.md` and `@AGENTS.md` pointer against
  a seeded self-consistent tree.
- **P1 worker preamble** — retired the hand-frozen `WORKER` constant in `engine/worker.py` that restated
  `spec/worker.md` (the exact `worker.DEPTH`-constant drift-by-copy). The worker's discipline prose is
  now single-sourced from `spec/worker.md` through the `methodology` seam (`_worker_disciplines`). Only
  the genuinely non-inferable residue stays authored: a one-line `SALUTATION`, the JSON `ENVELOPE`, and
  a new `GROUNDING` block encoding the two facts the slice cannot carry — the **corrected single-writer
  invariant** (stage exact files, never `git add -A` over a shared parent; a repo-level lock spanning
  write→commit) and the machine-readable **gated-vs-watched register** (delta-applies / length-ratchet /
  mechanical scan / red→green-must-execute are gated; depth / coherence / grilling-floor /
  design-it-twice are watched, model judgment the harness cannot certify).
- **P1 vision binding** — added `<!-- vision: candidate, isolat, fence -->` to `spec/design-it-twice.md`;
  it binds 2 real intent statements (the isolation/fence concurrency model and the graph-of-candidates),
  exactly the vision design-it-twice realizes — not the noisy 10-statement `interface` match.
- **P2 citation** — strengthened the `arXiv:2602.11988` paraphrase in `engine/anchor.py` to the harsher,
  correct finding: context files *reduce* task success rates versus no repository context, while raising
  inference cost by over 20%.

### the red→green loop (dogfooded)

The conformance gate's discovery-location assertion **is the targeting defect, caught by construction** —
the gap research.md said the gate should close. slice17 drives both halves: it reconstructs the pre-fix
render (the five skills in root `skills/` only, no `CLAUDE.md` bridge) and asserts the gate goes **RED**
(`RED: the pre-fix render … fails the discovery gate`), then runs the live channels and asserts it goes
**GREEN** (`GREEN: the live channels land skills in .claude/skills/ and bridge the anchor via
@AGENTS.md`). Both halves run on every `--check`, so the loop is executed, not narrated. The schema and
link gates were separately shown to bite (bad name regex, name≠dir, missing/over-long description, broken
pointer all turn it RED).

### parked / surfaced

- **`folding-conditions` vision binding — decided: pure machinery, carries none (no edit).** It is the
  conditions a graph's material must meet to fold — engine machinery run at the archive gate; the vision
  it serves is realized through the *disciplines* it gates (depth, the loop), not as its own intent
  statement. `engine/view.py`'s docstring already names it the canonical pure-machinery example. So the
  bare slice is correct, intentionally — recorded here rather than touched.
- **Surfaced, not a defect:** `spec/worker.md:25` ("never raw code, and never the operator view") is a
  compound negation left as-is — it is a list of two prohibitions that *are* the whole point (style-guide
  rule 2: keep a negation when the prohibition is the point and no positive form exists), and it is
  outside the plan's named coherence idiom. Flagging for the operator in case a later pass wants it
  positivized; my read is it should stay.

### cross-arc dependency (engine-hardening)

- The **`architecture-review` skill must be re-confirmed honest after `engine-hardening`'s de-claim
  folds.** `spec/architecture-review.md` and `spec/depth.md` are the sibling's to edit; I did not touch
  them. The rendered `architecture-review/SKILL.md` still carries the 167-word overclaim statement and
  its mid-clause `(ADR 0020)` ref. Once the sibling's de-claim folds, re-run `channels.materialize` and
  confirm the rendered skill opens with the built things and marks the model-driven verdict unbuilt.
- The worker GROUNDING's single-writer invariant and gated-vs-watched register **fold together with**
  the sibling's engine fix (the repo-level lock / exact-path staging in `record.py`). The grounding the
  worker is *taught* lives here; the lock the engine *enforces* lives there.

### operator confirmation step (cannot be driven from a worktree)

The fold asserts the bridge lands *where* stock Claude Code reads and *conforms* to its schema. The final
live confirmation — that a real `claude -p` session actually loads the anchor and the skills — is the
operator's watched A/B evidence, not a thing a headless check can assert. **Operator step:** open a stock
Claude Code session on this repo (or the architect's `claude -p` harness) and run `/memory` (does the
anchor appear via `CLAUDE.md`?) and `/doctor` or "what skills are available?" (are the five listed?). If
the architect runs a custom harness that natively loads `AGENTS.md` + root `skills/`, the bridge is
harmless redundancy; if it runs stock Claude Code, the bridge is what makes the channels load at all.
