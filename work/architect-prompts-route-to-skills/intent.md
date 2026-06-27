---
kind: ask
state: in flight
owner: operator
created: 1782536400
---
# architect-prompts-route-to-skills — the per-episode prompt loads the skill, never restates it

The architect's per-episode prompts are hand-authored string constants that restate, in compressed
and less-faithful form, disciplines that already live single-sourced in `spec/<cap>.md` and render to
the materialized skills: `communication.SYSTEM` / `COHERENCE` / `EXPLAIN`, `grill.FLOOR` / `PRODUCTS`,
and `design.SELECT`. Two costs follow, and they are the same cost seen twice:

- **the skills channel has no demand path** — the anchor advertises skills as "the specialization,
  loaded on demand", but no architect prompt points at a skill, so the on-demand specialization is
  never loaded. The architect runs as a one-shot `claude -p` completion: it has neither a cue nor a
  need to read `skills/<cap>/SKILL.md` while the discipline already sits paraphrased in its prompt.
- **the inline paraphrase is a second copy that can drift** — the prompt constants are never checked
  against the spec (the `audit` gate covers the derived channels, not these literals), so they are
  free to drift from `spec/<cap>.md` the way every hand-tended restatement in the coherence audit did.

The architect is Claude Code, which discovers `.claude/skills/` natively, so routing is safe to lean
on **today** — unlike the worker, whose skill-load is still watched evidence
(`work/worker-disciplines-become-a-loadable-skill`).

The intent: each architect per-episode prompt **instructs the model to load its skill** for the
method, and carries only the live task and material inline (the digest, the contract, the report, the
ask, the reply envelope). No architect prompt restates a discipline its skill single-sources, so the
skill becomes the one source and there is no second copy to drift.

## folding condition
- each architect per-episode prompt names and instructs loading its corresponding skill, and carries
  no hand-authored restatement of the methodology that skill single-sources;
- the architect still produces the same structured reply envelope each prompt declares;
- `python3 -m engine --check` is green.
