# ADR 0008 — an accepted length is bounded, and ratchets

Status: machine-owned, awaiting ratification — the *direction* (acceptance must set a higher bar
for the next trip) is operator-settled (next-work.md, 2026-06-21); the machine-side shape below
awaits ratification. [machine]

## Context

Slice 7 (ADR 0006) made length a context-cost *signal* that raises a depth *decision* rather than
auto-refusing, and recorded the operator's accept-with-reason outcome as a structured
depth-decision — `depth-decision: <path> accepted — <reason>`. That record had a hole the operator
named after the slice: once written, it cleared the file **permanently and regardless of length**.
A file accepted at 450 lines could balloon to 2,000 in later changes and the gate would stay
silent — acceptance was *unbounded*. An accept-with-reason judged at one size silently licensed
unbounded later growth, which is exactly the dilution the folding conditions exist to stop.

The operator settled the direction: when a length signal is accepted, **set a higher bar for the
next trip** — do not silence the file forever, and do not nag on every touch. The acceptance is
bounded to the length it was accepted at; renewed growth past it re-opens the decision at the new,
higher level. What had to be settled to build it is machine-side (the operator's anchor is the
contract, not the machine-side design — rebuild-spec §6.4): where the accepted length is recorded,
how "materially past" is drawn, and how the standing review renders a stale acceptance.

## Decision

**An accepted length is bounded to the length it names, and ratchets up; it does not silence later
growth.**

- **The accepted length lives in the record, not in git history.** The structured depth-decision
  becomes `depth-decision: <path> accepted@<N> — <reason>`, where `<N>` is the line count the
  operator accepted. The bar is durable, version-controlled, and operator-legible where a computed
  high-water mark would be stateful and fragile — and recording it (rather than inferring it from
  history) makes **shrink-then-regrow** correct for free: a shrink never lowers the bar, so a file
  that shrinks and regrows back to its old size never re-nags.
- **`accepted` is bounded; it clears only within the bar plus a materiality margin.** A
  depth-decision `accepted@N` clears the gate while the file's current length is `≤ N + N·SLACK`
  (`SLACK = 0.1`, a starting value to tune, §11). The margin is so a one-line edit past the bar
  does not re-open a settled decision — only **material** growth does. Past it the depth decision
  re-fires and the acceptance must be **renewed** at the new length (`accepted@<new N>`), which
  ratchets the bar up. A stable or shrinking file stays quiet.
- **A bare `accepted` (no `@<N>`) no longer clears the gate.** An acceptance that names no length
  names no bound, so it is *incomplete* and the depth decision re-fires — the same by-construction
  closure slice 7 used for the substring hole: the exception is the decision *at a stated size*,
  not the spelling. This is the direct consequence of the settled direction (an unbounded
  `accepted` is the hole being closed), recorded machine-side rather than re-grilled.
- **The ratchet only rises: the highest recorded bar governs.** Each renewal writes a new
  depth-decision at a higher `N`; `accepted_at` takes the **max** across all records naming the
  file, so the live bar is order-independent and the most permissive recorded acceptance is the
  one in force.
- **The standing review distinguishes a stale acceptance from a never-decided over-signal file.**
  The review gains a third over-signal status, `exceeded`: a file past the signal that *was*
  accepted at a lower bar and has since outgrown it. It is rendered distinctly — the map marks it
  "grew past its accepted bar of N — decision re-opened" and it returns to the deepening backlog —
  so the operator reads a *stale* acceptance differently from a brand-new over-signal file. `over`
  is never accepted; `exceeded` is accepted-but-outgrown; `accepted` is within the bar.

## Grounds

The seam from slice 7 carries this with no re-cut: one criterion (depth, signalled by length) at
two scopes — the per-graph gate (`folding-conditions`) and the standing scan
(`architecture-review`) — both consult the same structured depth-decision through one predicate.
Bounding the acceptance changes only what that predicate reads: `accepted_at` (the recorded bar)
is the deep primitive, and the bounded `accepted` and the review's status both build on it, so the
margin logic lives in exactly one place. Recording the bar in the record rather than computing it
keeps durable state in version-controlled files (intent.md's own discipline) and makes the
shrink-then-regrow case fall out of the data model rather than needing special handling. The
structured-record idiom is the one slice 8 also uses for `design-decision`; only the
depth-decision carries a length, because only depth is signalled by one.

## Consequences

`conditions.SLACK`, `conditions.accepted_at`, a length-bearing `accepted(rel, lines, root)`, and a
`depth-decision: <path> accepted@<N>` record format. `review` gains the `exceeded` status, a
`Module.bar` field, and its mark/finding. The living spec carries deltas across
`folding-conditions` (acceptance is bounded and ratchets), `architecture-review` (the exceeded
rendering), and the glossary (accepted length / ratchet bar / exceeded acceptance). This ADR
**refines** ADR 0006: the structured depth-decision it introduced now names the length it accepts,
and a bare `accepted` no longer clears the gate. The boundary decisions of 0004/0005/0006 (the two
capabilities, one criterion at two scopes) stand unchanged. A future change that unbounds
acceptance again, or moves the bar out of the record, carries an ADR superseding this one.
