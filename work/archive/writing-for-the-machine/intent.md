---
kind: ask
state: standing
owner: operator
created: 2026-06-23
---
# writing-for-the-machine — materialize the parked machine-writing standard as a standing skill

The agent-facing-hardening audit (2026-06-22) produced a validated standard for writing the system's
own agent-facing channels — the skills, the anchor, the prompts, the worker's hand-backs — for their
real reader, the model that loads them. The findings were *applied* once (the `CLAUDE.md` bridge, the
`.claude/skills/` mirror, the conformance gate, the prose fixes all folded), but the standard itself
was never made a standing discipline. So when the `communication` skill landed — the operator-facing
clarity standard — its machine-facing mirror stayed in the archive. This arc closes that: it lands the
standard as its own capability and loaded skill, the pair to `communication`.

## ratified — operator decisions (2026-06-23)

Settled in a grilling pass before the build opened; the arc is operator-owned from here.

- **Scope → the full methodology**, A+B+C of the audit: the skill-vs-mechanism boundary (what earns a
  channel), the structural conformance (owned and gated by `channels`, cited not restated), and the
  machine-writing standard (Part C). Where it overlaps an existing home, the duplicate is removed there
  rather than copied — the one real overlap, `channels`' conformance gate, is single-sourced by pointer.
- **Name → `writing-for-the-machine`** — the machine-facing mirror of `communication`. A shared skill:
  it loads for either role, since both author machine-facing prose (the architect the slices and anchor,
  the worker its hand-backs).
- **Prose gate → watched, plus one non-blocking signal.** The discipline stays watched, held by
  judgment, like the clarity standard. Three mechanically-detectable constructs — a sentence past sixty
  words, a compound negation, a provenance reference off the line-end — raise a signal over the spec's
  own prose in the length tripwire's idiom: it flags candidates for judgment and never refuses a fold.
  A readability score never gates, for the reason `communication` gives; the only true verdict is the
  behavioural A/B eval.

## the spec delta this realizes

- A new slice `spec/writing-for-the-machine.md` — four watched requirements: the channel boundary,
  writing for the one-pass reader, density-is-signal, and the signal-not-a-gate discipline.
- `writing-for-the-machine` registered in `engine/methodology.METHODOLOGIES` (one line — the *when to
  load*), so the fold renders it into both skill locations and the anchor index gains its derived line.
- `engine/machine_writing.py` — the non-blocking signal: the three-construct detector over the spec's
  requirement statements, surfaced as an advisory in `python3 -m engine --check`, never gating.
- An acceptance block in `engine/check/scenarios.py` (the mirror of the communication §7b): the skill
  registers, carries the core discipline, classifies all-watched, and its signal fires on a planted
  construct yet never gates — asserted from outside, never a faked in-spec block.

## folding condition

The `writing-for-the-machine` capability and skill are registered and render on fold; the standard's
prose is watched (no gated readability metric); the non-blocking construct signal is built and its
detector is acceptance-checked; the one structural overlap with `channels` is single-sourced by
pointer, not duplicated; `python3 -m engine --check` carries the acceptance and is green.

## what this arc deliberately does NOT do

It does not re-derive the channel architecture or the conformance gate (the asset it builds on), does
not gate prose by a metric (watched, by ratified decision), and does not edit `spec/communication.md`
(its operator-facing mirror stands as folded — the new slice cites it, no restatement).

## provenance (cited, not depended on)

- `work/archive/agent-facing-hardening/research.md` — Report 1, the agent-facing-artifacts audit (four
  researcher seats synthesized): the tools inventory (A.5), the criteria set (A.3), the skill-vs-
  mechanism boundary (B.1–B.2), and the machine-writing standard with its evidence (Part C). The
  self-sufficient ask is above; the report is the line-precise source the build distils.
