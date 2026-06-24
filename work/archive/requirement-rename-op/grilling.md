surfaced: 1

[Q] How should a requirement's title change be expressible in the delta grammar — the gap the live crossing hit?
lean: Add a RENAMED operation — a fourth verb mirroring OpenSpec (old title → new)
flip: if adding a fourth verb to the grammar costs more than the footgun it removes
answer: Add a RENAMED operation

[Q] How much should one RENAMED operation do — just change the title, or also carry the requirement's new body?
lean: Retitle and carry the new body in one op
flip: if each op should do exactly one concern (identity vs content)
answer: Title only; the body lands via a paired MODIFIED keyed on the new title

[CONTRACT]
A delta can rename a requirement in place. RENAMED is a fourth verb beside ADDED / MODIFIED / REMOVED, written `## RENAMED — <capability>` with a `### Requirement: <old title>` block carrying a `→ <new title>` line. It changes only the requirement's title — its identity — the body and scenarios untouched. A scope-broadening retitle is a RENAMED paired with a MODIFIED keyed on the new title; within one delta the renames resolve first, so the modify finds its target and check validates it against the post-rename names. Refusals follow the existing discipline: a rename of an absent old title, or onto a title that already exists, cannot fold and leaves the spec untouched; a re-applied rename (old gone, new present) is the idempotent retry. The rename lands in the fold's one atomic act with the spec change and the node archive, on the single-writer line, like every other op. The worker-facing delta grammar (`worker.ENVELOPE` and `spec/worker.md`) must name RENAMED so a worker writes a retitle correctly instead of the MODIFIED-with-new-title the gate refused on the live run.

[DELTA]
# delta — a RENAMED operation changes a requirement's title in place

## MODIFIED — self-model

### Requirement: every behavior-changing tree carries a delta
A tree that changes behavior MUST carry a delta of ADDED / MODIFIED / REMOVED / RENAMED
requirements matching what it built. ADDED introduces a requirement; MODIFIED replaces the body and
scenarios of a requirement matched by its title; REMOVED drops one matched by its title; **RENAMED
changes a requirement's title — its identity — leaving the body and scenarios untouched**, written
`## RENAMED — <capability>` with a `### Requirement: <old title>` block carrying a `→ <new title>`
line. Because a requirement's identity *is* its title, a scope-broadening retitle is a RENAMED
(old → new) **paired with** a MODIFIED keyed on the **new** title; within one delta the renames
resolve first, so the paired MODIFIED finds its target and `check` validates it against the
post-rename names. A tree that makes no behavior change carries an empty delta and says so.

#### Scenario: a trivial tree
- WHEN a tree changes no behavior
- THEN it carries a delta that declares itself trivial, and folding it applies nothing

  ```check
  fold trivial
  unchanged
  ```

#### Scenario: a requirement is renamed in place
- WHEN a delta RENAMES a requirement (old title → new title)
- THEN the requirement is present under the new title with its body and scenarios intact, the old
  title is gone, and the node is archived — all in the same one atomic act

  ```check
  fold renamed
  retitled
  archived
  atomic
  ```

#### Scenario: a rename paired with a modify
- WHEN a delta RENAMES a requirement and, in the same delta, MODIFIES it keyed on the new title
- THEN the renames resolve first so the modify finds its target, and the requirement lands under the
  new title carrying the modified body

  ```check
  fold renamed-modified
  retitled
  remodeled
  ```

### Requirement: a missing or mismatched delta cannot fold
Folding MUST refuse a behavior-changing tree that carries no delta, and refuse a delta that does not
apply cleanly to the current spec. A MODIFIED or REMOVED of an absent requirement, an ADDED of one
that already exists with different content, a **RENAMED of an absent old title**, and a **RENAMED
onto a title that already exists** all fail to apply and leave the spec untouched. A re-applied
RENAMED — its old title already gone and its new title already present — is the idempotent retry, not
a conflict, so a crash-interrupted fold completes on retry rather than wedging.

#### Scenario: missing delta
- WHEN a behavior-changing tree carries no delta file
- THEN the fold is refused

  ```check
  fold missing
  refused
  ```

#### Scenario: mismatched delta
- WHEN a delta MODIFIES or REMOVES a requirement that is absent, or ADDS one that already exists
- THEN the fold is refused and the spec is left untouched

  ```check
  fold mismatched
  refused
  untouched
  ```

#### Scenario: an unfoldable rename
- WHEN a delta RENAMES a requirement whose old title is absent, or onto a title that already exists
- THEN the fold is refused and the spec is left untouched

  ```check
  fold rename-absent
  refused
  untouched
  fold rename-collision
  refused
  untouched
  ```
