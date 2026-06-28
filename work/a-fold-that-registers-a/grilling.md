surfaced: 0

[CONTRACT]
When one fold both registers a new methodology and lands its spec, that fold now writes the new methodology's skill files (both skill locations) and its line in the anchor's skills index in the same act — instead of leaving them for a manual re-run in a fresh process, the reconciliation the worker-disciplines fold needed (commit c699304). The fold re-derives the channels from the merged tree in a fresh process that imports the just-landed code, so it materializes whatever that code registered — any module-level registry, not only the methodology one; a spec-only fold is unchanged and pays nothing new. A new acceptance scenario gates it: a methodology-registering fold materializes the skill in both locations and the anchor-index line, and leaves no post-fold drift.

[DELTA]
# delta — a fold materializes the methodology it registers, in the same act

## ADDED — channels
### Requirement: a fold materializes a methodology it registers in the same act
A code-bearing fold whose replayed code registers a new methodology in a module-level registry MUST
materialize that methodology's channels in the SAME fold act: its `SKILL.md` in both skill locations and
its line in the anchor's derived skills index. The render MUST reflect the just-replayed registry, never
the registry frozen in the folding process at import. The fold re-derives the channels from the merged
tree in a fresh process that imports the replayed code, so ANY module-level registry the replayed code
mutates is seen, not only the methodology registry. A spec-only fold carries no replayed code and renders
in-process unchanged. A methodology-registering fold therefore leaves no post-fold drift: a fresh render of
the merged tree matches every committed channel, with no manual re-materialize in a second process.

#### Scenario: a methodology-registering fold materializes its skill in the same act
- WHEN a code-bearing fold's replayed engine code registers a new methodology, the new methodology's slice
  added by the same delta
- THEN the fold materializes that methodology's SKILL.md in both skill locations and its anchor
  skills-index line in the same act, each a faithful render of the new registry, and a fresh-process audit
  of the merged tree reports no channel drift

  ```check
  register-methodology
  skill-materialized
  index-lists-new
  no-post-fold-drift
  ```
