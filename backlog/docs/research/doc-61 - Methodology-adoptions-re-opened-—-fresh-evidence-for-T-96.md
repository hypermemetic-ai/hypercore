---
id: doc-61
title: Methodology adoptions re-opened — fresh evidence for T-96
type: other
created_date: '2026-07-19 17:52'
updated_date: '2026-07-19 17:53'
tags:
  - research
---
# Methodology adoptions re-opened — fresh evidence for T-96

**Owning task:** T-96. **Research date:** 2026-07-19 (fresh researcher, operator's brief).
**Overall confidence:** HIGH on the debugging adoption and the keep-current findings; MEDIUM on the negative pushback finding (absence searches cannot be exhaustive).
**Settles:** T-96 is respecified. Only one external methodology clears the combined bar of sharpness, independent evidence of use, maintenance, Pi 0.80.10 compatibility, and piecemeal adoption: `obra/superpowers`'s `systematic-debugging`, filtered. qq's `grilling`, `research`, and `code-review` bodies stay as-is. Warranted pushback remains an explicit gap. Waza `think`/`hunt` are not adopted.
**Context:** commissioned after the operator could not find independent attestation for waza and declined to be bound by doc-59's claims; this report re-opened the question with fresh sources rather than re-fact-checking doc-59. Raw findings: researcher artifact reconciled here.

## Verdict table

| Surface | Verdict | Sharper than qq? | Proven-use evidence | Confidence |
|---|---|---|---|---|
| Intent extraction → plans | KEEP qq `grilling`; reject waza `think`; hard-reject Superpowers planning chain | Marginal (waza attacks plans better, weakens intent ownership) | waza v3.32.0 released *same day* — no use record for current text | HIGH / MEDIUM on negative |
| Warranted pushback | NO admissible package; gap preserved (closest: gstack `plan-ceo-review`, cockpit-bound) | Yes vs qq's absence, but inadmissible | Real users, inseparable from gstack cockpit (Claude/Bun, ~2,200 lines, phone-home reports) | MEDIUM |
| Independent research | KEEP qq `research` | No | qq's corroboration/confidence model materially stronger | HIGH |
| Independent review | KEEP qq `code-review` | No | Candidates weaker on independence/verification or cockpit-bound | HIGH |
| Debugging | ADOPT `obra/superpowers` `systematic-debugging` only, filtered; keep thin qq wrapper | **Yes** | Thoughtworks Radar Vol. 34; six-month practitioner account; method-specific reports | HIGH |

## Debugging adoption (the one positive)

The [methodology text](https://raw.githubusercontent.com/obra/superpowers/main/skills/systematic-debugging/SKILL.md) is sharper than qq's diagnosing-bugs generic mechanics: instrument every component boundary before choosing a fix; trace bad data backward to origin; compare against working reference implementations; one falsifiable hypothesis at a time; stop after three failed fixes and question the architecture; name rationalizations that force return to evidence. Numerical fix-rate claims in the skill were *not* credited; adoption rests on method + independent reports.

Admissible install (manifest verified: v6.1.1, 2026-07-02, declares pi extension + skills):

```json
{ "source": "git:github.com/obra/superpowers@v6.1.1",
  "extensions": [], "skills": ["skills/systematic-debugging"],
  "prompts": [], "themes": [] }
```

End-to-end smoke install was NOT run (read-only research sandbox); a temporary `pi -e` smoke test remains the final pre-adoption Check.

Local qq deltas that must survive in a thin wrapper (superpowers' Phase 4 proceeds into implementation and references unselected skills): diagnosis-vs-fix authorization; artifact-based route when no live reproducer exists; evidence/inference labeling; qq's regression and completion requirements when a fix is authorized.

## Negative findings that respecify T-96

- **Waza `think`/`hunt` rejected:** v3.32.0 released 2026-07-19 (same day as research); external material is author interviews or AI-generated explainers, not independent outcomes; embeds an unrelated update check. Reassess only when method-specific independent outcome reports exist for current-generation text.
- **Superpowers planning chain hard-rejected:** `brainstorming`/`writing-plans` mandate foreign artifact hierarchies and handoff into Superpowers' execution lifecycle.
- **Pushback gap recorded:** no package passes the fit constraints; importing a cockpit to fill one method violates the agreed architecture. Not forced.
- Waza `write` was outside the research brief (prose methodology unevaluated); rpiv-ask-user-question was doc-59's QoL pick, not re-evaluated. Both revert to trial status, not adoption.

## Sources

Primary: [superpowers manifest](https://raw.githubusercontent.com/obra/superpowers/main/package.json), [v6.1.1 release](https://github.com/obra/superpowers/releases/tag/v6.1.1), [systematic-debugging text](https://raw.githubusercontent.com/obra/superpowers/main/skills/systematic-debugging/SKILL.md), [waza releases](https://github.com/tw93/Waza/releases), [gstack plan-ceo-review](https://github.com/garrytan/gstack/blob/main/plan-ceo-review/SKILL.md), qq skill bodies (grilling, research, code-review, diagnosing-bugs). Independent attestation: [Thoughtworks Technology Radar Vol. 34](https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2026/04/tr_technology_radar_vol_34_en.pdf), [six-month practitioner account](https://gautamkhorana.com/blog/claude-code-superpowers-how-i-actually-use-it/), [debugging practice discussion](https://www.reddit.com/r/ClaudeCode/comments/1u0piw9/how_do_you_handle_debugging_code/), [gstack user reports](https://news.ycombinator.com/item?id=47355173). Owning-agent spot-checks 2026-07-19: manifest/release dates/waza same-day release/practitioner mention/radar PDF all verified.

## Gaps

- Smoke installation of the filtered superpowers package on pi 0.80.10 not yet performed (pre-adoption Check).
- Pushback negative finding is MEDIUM — catalog absence cannot be proven.
- Waza `write` and prose methodology unevaluated by this round.
