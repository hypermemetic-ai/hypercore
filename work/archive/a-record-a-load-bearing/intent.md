---
kind: ask
state: done
owner: operator
created: 1782321971
---
A record a load-bearing mechanism is supposed to produce — a design-it-twice design-decision, a worker's RESULT/delta, an accepted-length record, a scenario verdict — is byte-indistinguishable from one a role hand-authored without running the mechanism. So a worker, architect, or agent can short-circuit the mechanism and leave a durable record that misrepresents how the judgment was made; the operator's source of truth cannot tell a mechanism's real output from a fake. Make a short-circuited or faked mechanism-output detectable, so the record cannot lie about its own provenance.

## the integrity stack (one of three composable nodes)
hypercore's self-verification rests on one claim — the description is the test, and the builder cannot
fake the verdict. It can fail three independent ways, each its own node; none subsumes another, and a
short-circuit at any layer defeats the whole:
- **proposer** — did the architect author the check (WHEN/THEN + verbs), or the builder? — `worker-builds-proposed-delta`
- **run** — did the mechanism actually run and leave a trail, or is the record hand-faked? — *this node*
- **adequacy** — when it ran, did the check test the property, or a builder-authored proxy? — `gate-vouches-for-the-new-verb`
This node owns the **run** layer: the *presence of the trail* the mechanism leaves, never the *adequacy*
of the check it ran — that is `gate-vouches-for-the-new-verb`'s. A real fenced build with a real red→green
leaves a real trail yet can still test nothing, so this gate proves the mechanism ran; it cannot certify
the scenario verdict.

This refutes a premise in this node's own already-resolved pass. That pass treats the scenario verdict as
the strongest, self-certifying trail ("the scenario gate re-derives it red→green … so no recorded verdict
is ever believed"). `gate-vouches-for-the-new-verb` shows the re-derivation can be hollow, so that premise
is wrong. The pass must be **re-derived** to drop the over-claim and defer check-adequacy to that node —
not hand-patched, because hand-editing a settled mechanism output is the exact short-circuit this node
exists to forbid.

The three touch shared seams (`spec/worker.md`, the scenario gate in `conditions`/`scenario`): each must
**ADD** its own requirement rather than co-MODIFY a shared one (two MODIFYs of one requirement clobber at
fold), or be sequenced on another's tip — so three concurrent fences compose.
