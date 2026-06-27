---
kind: ask
state: standing
owner: operator
created: 1782532501
---
communication-mastery — reground the clarity standard on compression to a decoder the one reader already runs.

The communication clarity standard leans too hard on expertise and jargon — its spine is the "expert-reader inversion / removal of scaffolding." Reground it: **clarity is compression to a decoder the one reader already runs.** Mastery is the rare encoder whose short output the reader can re-run from what they already hold; jargon is the cheap encoder — the formally identical short string aimed at a private key the reader must already own, which is encryption wearing depth's clothes. The prior dive vindicated the cheap one and called it respect for the reader's expertise. Carry the four-test self-check, the make-the-caveat-land-as-hard-as-the-claim inversion, and the practical-not-literary register. Make the skill actually change the architect's voice (directives + a worked exemplar + a write-time self-check), not principles alone — stating the standard does not make the model obey it. Build the caveat-survival routing into the architect's render so a dropped load-bearing caveat is caught before it crosses, with the entailment verdict **watched** (model-driven) and the routing **gated**.

Filed to tackle at a better time. The findings live beside this intent:
- `synthesis.md` — the conclusions (the spine, the four-test gate, the hedge-lands inversion, the application apparatus, the scope decision).
- `research.md` — the eight-front provenance ledgers (four on the idea, four on application), with named sources.
- `draft-spec.md` — the authored draft: the regrounded preamble, the two reframed clarity requirements, and the proposed gated caveat-survival requirement + engine seam.

This supersedes the spine of the earlier dive in `work/archive/communication-clarity/` (which argued the now-demoted expert-reader inversion); that dive's type/color/surface findings are untouched and still stand.

## structural constraints — read before building
- **The fold cannot carry the spine.** `delta._apply` keeps a capability's PREAMBLE verbatim and edits only requirement blocks by name. The compression-spine reground lives in the preamble (what renders as the skill's overview via `methodology._overview`), so it is **authored directly** — architect authorship, the way preambles always change — never built by a fenced worker, whose preamble the fold discards.
- **The division of labor.** Author directly: the preamble spine, the two reframed clarity requirements (watched prose), and the `engine/check/scenarios.py` assertion that currently greps the skill for `"removal of scaffolding"` (line ~154) — flip it to the compression spine, or `--check` goes red. Build through a fenced codex worker: the one new BEHAVIOR — the gated caveat-survival requirement + its red→green scenario + the engine seam (`communication.py` caveat-survival on the `integrate` render path + `communication_world.py` verbs). The builder must not author the scenario that judges it; the architect authors the scenario, the worker turns it green.
- **The watched/gated line for the NLI check.** `--check` runs deterministic and in-process, so a live entailment model call can never be the gate — only its routing can. Build the caveat-survival *routing* gated (a dropped caveat is provably caught, tested against a scripted oracle in the world fixture); the entailment *verdict* stays watched/model-driven, exactly as `codex.py` treats the worker fence ("the gate proves the fence holds, not that the worker thrives").
- **Preserve the just-folded requirement.** "the defined vocabulary stays consistent — the vocabulary check" landed on `spec/communication.md` mid-session (commit 54a116b). Edit around it; do not overwrite it.

## folding condition
- `spec/communication.md` carries the regrounded preamble (compression-to-a-shared-decoder spine, the four-test gate, the caveat-lands inversion, the expert-reader inversion demoted to a conditioned corollary) and the two reframed clarity requirements;
- a new **gated** requirement — a dropped load-bearing caveat is caught before it reaches the operator — lands with its scenario and check block, the engine seam turning it red→green, the entailment verdict watched and the routing gated;
- the `communication` skill re-renders the new discipline; `engine/check/scenarios.py` asserts the new spine (not "removal of scaffolding"); `python3 -m engine --check` is green;
- the eight-front provenance is placed on the node.
