---
name: code-review
description: Delegates review of a branch, pull request, or working tree to a fresh read-only reviewer, then verifies and returns material findings. Run once for every non-trivial Change after implementation and local verification, before the first commit or publication; review each in-scope fix delta. Also use when the operator asks for review.
---

# Review with fresh context

A review is independent judgment. The owning Actor resolves orientation once;
the fresh reviewer derives its verdict from the Change, its intent, and the
code around it without inheriting the author's conclusions.

## Own the orientation

1. Define the exact surface. Honor a supplied base; otherwise infer the branch
   and merge-base. Include committed, staged, unstaged, and untracked work.
2. Compare the actual Change with its reconciled Task or specification,
   ownership boundary, inclusions, and non-goals. Stop and align if intent is
   conflicting or unclear, or the Change crossed its boundary.
3. Write a complete review brief under the OS temporary directory containing:
   - Repository path, base, head, working-tree state, objective, and layer;
   - a changed-path map marking mechanical, generated, and historical material;
   - intent, acceptance criteria, inclusions, boundary, and non-goals;
   - the threat model, defended failure modes, and declined finding classes;
   - applicable unenforced Repository rules and standards;
   - consulted sources and the facts each supplied, plus Check results;
   - the reviewer's permission boundary; the required finding shape of file,
     line, concrete failure path, and supporting evidence; and the exact
     context-gap condition.

Give coordinates and distilled facts, not source dumps. Omit the author's
conclusions, suspected findings, and development transcript. Owned reviewer
rules ride `REVIEW.md`; the brief supplies only Change-specific facts, and its
declared scope wins.

## Delegate the judgment

4. Call one fresh reviewer:

   ```sh
   qq-dispatch reviewer \
     --root <repository-root> \
     --brief <brief-path> \
     --output <report-path>
   ```

   Substitute only the paths. The engine owns fresh-context isolation,
   read-only access, role configuration, containment, artifacts, and process
   retirement. The brief states that it completes orientation: no start-of-work
   sequence, broad intent search, or full-suite rerun.
5. The reviewer tests the Change's responsibilities against the brief, exact
   diff, surrounding callers and tests, and suspected failure paths. Review
   moves and deletions through their invariants.
6. A hole produces a context-gap report: the missing or contradictory fact,
   why the verdict depends on it, and evidence inspected. Amend only that fact
   and dispatch a new fresh reviewer. A context gap is neither finding nor pass.
7. Request only material introduced failures across correctness, security,
   reliability, intent, and unenforced standards. A smell needs concrete future
   cost and counterevidence; never prescribe refactoring from a label.

## Verify and close

8. Verify every finding against the Repository. Confirm a failure with a
   constructed input, state, or sequence observed to go wrong; confirm intent
   findings against scope and diff. Deduplicate and rank only confirmed
   findings. Clustered findings may expose a model problem; raise it instead of
   feeding a patch queue. Stop at review unless fixes were requested.
9. Fix only a Change-introduced failure reproduced in a supported state whose
   remedy stays inside agreed intent. Rerun affected Checks and review the exact
   fix delta. A new finding class already fixed in two prior rounds trips the
   convergence circuit-breaker: halt at the last green state and ask which
   layer owns the invariant.
10. A dispatch error, nonzero exit, missing report, or context gap is not a
    review. Rerun the unchanged or minimally completed brief fresh. Never
    narrow scope or soften intent to obtain a pass; repeated failure blocks.
