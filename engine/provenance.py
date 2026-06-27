"""The provenance gate — a mechanism-output record folds only when its mechanism's trail is present.

A record one of hypercore's load-bearing mechanisms is meant to produce — a scenario's red→green
**verdict**, a worker's **RESULT and delta**, an **accepted-length record**, a **design-it-twice
decision** — is byte-indistinguishable from one a role hand-authored without running the mechanism. So a
trusted role with write access can *conveniently skip* the mechanism and leave a durable record that
misrepresents how the judgment was made. This gate makes the skip detectable: at the fold it demands the
**trail** the mechanism leaves when it actually runs, and refuses a record that shows none with a flat,
never-waveable reason. It catches the **absence** of the trail under a *cooperating short-circuit*, not a
forged one — a determined forger with write access to the repo and the gate is out of scope by design.

Because the running fence is torn down on every exit, the trail is never the fence itself but what
**durably survives** it. The records split on the spec's authored/derived line and are attested
**asymmetrically**, each bound to the artifact its own mechanism necessarily leaves:

- **derived** (the worker delta, the scenario verdict) — by **re-derivation**: the gate re-runs the
  touched capability's scenarios red→green (`derived`, over the `scenario` gate) and trusts only that
  transition. It stores **no "it ran" flag** — a record that asserts its own provenance is no trail at
  all, and a stored flag is precisely the forgeable record this node closes.
- **authored** (the design decision, the accepted-length record), which have no run to reproduce — by
  **reachability** to the durable artifact the mechanism commits (`reachability`): the accepted length
  written through the one accept seam (durable = committed, not a line hand-appended to the working-tree
  ledger), and the recorded candidate set in `design-decision.md` (a real contest's N briefed candidates
  and their comparison, not a bare hand-authored pick).
- **watched** (the vocabulary check's verdict, the model-driven depth scan's verdict) — a third trail
  type, a model-run whose judgment **no fixture can re-derive**, so it leaves no red→green and has no
  durable artifact to reach into for content. Its only honest trail is **presence**: the run commits a
  verdict trace on its node, and the gate attests that trace is committed (`watched_trace`), never
  re-deriving the verdict. It is **capability-agnostic** — it reaches "a watched run committed its
  verdict on this node," never any one capability's content — so the single seam serves every watched
  standard, each naming its own mechanism; the consumer that knows its standard ran asks for the
  attestation, so a fold carrying no watched standard demands nothing.

The guarantee is deliberately narrow: **trail-presence only**. Even a real re-derived red→green proves
the mechanism *ran*, never that the check it ran was **adequate** — a real fence can still test nothing.
Check-adequacy is the distinct layer owned by `gate-vouches-for-the-new-verb` and is **never claimed
here** (`Attestation.adequacy`). A record's irreducibly creative content — a pick's reason, a coherence
judgment's grounds — cannot be structurally attested, so it is recorded honestly **watched**, never
pretend-gated (`Attestation.residue`).

It binds **forward only**: records already durable in the source of truth are grandfathered (a committed
record predates this fold), because the run trails are torn down at fold by design and a retroactive bar
could not tell a fake from a legitimately-swept trail. Exactly one named, minimal **genesis** set is
exempt — the authored-trust roots that necessarily predate the gate, like the minimal shared anchor —
with **no** general operator-override, since waving the bar would re-open the exact short-circuit.
"""
from __future__ import annotations

from dataclasses import dataclass

# The genesis/bootstrap authored-trust roots — the one named, minimal exemption. These records
# necessarily predate the gate (there was no gate to leave a trail for) and the system rests on them as
# trust anchors. Nothing but this set folds trail-less; there is no general operator-override.
GENESIS = frozenset({"AGENTS.md", "CLAUDE.md", "README.md", "intent.md", "glossary.md"})

# The flat refusals — facts the way a delta that does not apply is a fact, never an operator-waveable
# decision. The only path past the gate is to run the mechanism, never to author its record.
NO_TRAIL = "no trail — re-run the mechanism"
NO_CONTEST = "no trail — run the contest"
FENCED_RUN = "fenced-run"


@dataclass(frozen=True)
class Attestation:
    """What the gate can honestly say about a record. `present` is the only structural verdict — the
    trail is there or it is not. `adequacy` and `residue` are **standing honesty**, not per-call
    judgments: this gate **never** claims the check was adequate (deferred to
    `gate-vouches-for-the-new-verb`) and **always** records a record's creative content as watched, so a
    caller can read the boundary of what trail-presence does and does not buy."""
    present: bool
    reason: str = ""
    adequacy: str = "deferred"   # check-adequacy is never claimed here
    residue: str = "watched"     # the creative residue (a pick's reason) is watched, never pretend-gated


# ── the gate ───────────────────────────────────────────────────────────────────

def gate(result, root: str | None = None, node=None) -> str | None:
    """The whole provenance verdict over a fold's records, or None when every trail is present (or the
    record is grandfathered / genesis-exempt). The authored pair is judged in-process by `reachability`;
    the derived pair by `derived` (re-derivation). First-absent-wins, like the other folding conditions."""
    return reachability(result, root, node) or derived(result, root)


def attest(result, root: str | None = None, node=None) -> Attestation:
    """Attest a record for **presence only**. `present` is the gate's structural verdict; the
    `adequacy`/`residue` honesty rides every attestation unchanged — the gate proves the mechanism ran,
    never that its check was adequate or its reasoning sound."""
    reason = gate(result, root, node)
    return Attestation(present=reason is None, reason=reason or "")


# ── the authored pair: reachability to the durable artifact (in-process) ─────────

def reachability(result, root: str | None = None, node=None) -> str | None:
    """The authored pair's trail, judged in-process without any base/tip re-derivation — so a scenario
    can read this verdict without recursing into the scenario gate. An accepted-length record is reachable
    when it is **committed** through the one accept seam (the seam writes-and-commits in one act; a
    hand-appended working-tree line is not committed and has no trail); a design decision is reachable
    when its contest's **candidate set** survives in `design-decision.md`."""
    return _accepted_length(root) or _design_decision(result, node, root)


def _accepted_length(root: str | None) -> str | None:
    """An accepted-length record folds only when it is reachable — committed through the accept seam, not
    a line hand-appended to the working-tree ledger this fold. The seam (`conditions.accept`) writes and
    commits in one held act, so a real acceptance is in the committed ledger; a forge that edits only the
    working tree is not, and is the short-circuit caught. A record already committed is **grandfathered**
    (it predates this fold) and a record naming a **genesis** root is exempt — nothing else folds new and
    uncommitted."""
    from . import conditions
    new = conditions.working_accepted(root) - conditions.committed_accepted(root)
    forged = sorted(p for p, _n in new if p not in GENESIS)
    return NO_TRAIL if forged else None


def _design_decision(result, node, root: str | None) -> str | None:
    """A recorded design decision folds only when its contest's candidate set is reachable behind it —
    the N briefed candidates and the comparison a real `design.record` commits to `design-decision.md`. A
    decision recorded with no candidate set is a skipped contest with no trail (`run the contest`); only
    the structural reachability is gated, the pick's reason stays watched."""
    import os
    path = _node_path(result, node)
    if not path:
        return None                                        # this fold carries no design decision
    md = os.path.join(path, "design-decision.md")
    if not os.path.isfile(md):
        return None
    text = open(md, encoding="utf-8").read()
    if "design-decision:" not in text:
        return None                                        # not a decision record
    return None if _candidate_set_reachable(text) else NO_CONTEST


def _candidate_set_reachable(text: str) -> bool:
    """True when a real contest's candidate set survives in the design-decision: the comparison's
    per-candidate grounds (`- **<brief>**: <note>`). A real `design.record` writes one bullet per
    briefed candidate (≥2 — a contest is several candidates); a hand-authored pick that skipped the
    contest carries the decision line alone, no candidate set. (A design decision is produced by the
    contest mechanism, never a genesis root, so the genesis exemption — path-scoped — does not reach
    here.)"""
    return sum(1 for ln in text.splitlines() if ln.lstrip().startswith("- **")) >= 2


def _node_path(result, node) -> str:
    if node is not None:
        return getattr(node, "path", "")
    return getattr(result, "node_path", "") or ""


# ── the watched-evidence trail: a committed verdict's presence (capability-agnostic) ──

def watched_trace(node, mechanism: str, root: str | None = None) -> str | None:
    """The third trail type — a **watched-evidence trace**: the verdict a watched mechanism commits on
    its node when it runs. A watched mechanism is a model-run whose judgment no fixture can re-derive, so
    its only honest trail is **presence**: this attests the run's verdict trace is **committed** on the
    node, and refuses with the flat `NO_TRAIL` when it is absent (the run was skipped, not merely clean).
    It is **capability-agnostic** — `mechanism` is a label that forms the trace's path, never inspected
    for content — so the one seam serves the vocabulary check, the depth scan, and every later watched
    standard, each naming its own mechanism. Presence only: the verdict's soundness is never claimed
    (`Attestation.adequacy` deferred, `residue` watched)."""
    import os
    path = _node_path(None, node)
    if not path:
        return None                                        # no node to carry a trace — nothing to attest
    rel = os.path.relpath(_verdict_path(path, mechanism), _resolve_root(root))
    return None if _committed(rel, root) else NO_TRAIL


def commit_verdict(node, mechanism: str, verdict: str, root: str | None = None) -> str:
    """The writer side of `watched_trace`: commit a watched mechanism's verdict trace on its node — the
    durable artifact a watched run leaves. Like the accept seam it writes **and commits** in one held
    act, so the trail is what survives the torn-down fence, never a working-tree scratch. Production's
    watched run (the vocabulary check, the depth scan) calls this; the gate later attests its presence,
    never re-derives the verdict. Returns the trace file's path."""
    from . import tree
    path = _verdict_path(node.path, mechanism)
    tree.atomic_write(path, f"# {mechanism} — watched verdict [machine]\n\n{verdict.strip()}\n")
    tree.commit([path], f"{mechanism}: verdict committed on the node")
    return path


def verdict_present(node, mechanism: str) -> bool:
    """True when a mechanism's verdict trace is present in a node folder. This is the read side for
    live renders that need a trace's presence in the current tree, while `watched_trace` stays the fold
    gate's committed-presence attestation."""
    import os
    path = _node_path(None, node)
    return bool(path and os.path.isfile(_verdict_path(path, mechanism)))


def _verdict_path(node_path: str, mechanism: str) -> str:
    import os
    return os.path.join(node_path, f"{mechanism}.verdict.md")


def _committed(rel: str, root: str | None) -> bool:
    """True when `rel` is committed at HEAD — the trace durably survived, read through git so what counts
    is what a commit left, the same discipline the accepted-length trail uses (`_committed_ledger`)."""
    import os
    import subprocess
    r = subprocess.run(["git", "cat-file", "-e", f"HEAD:{rel.replace(os.sep, '/')}"],
                       cwd=_resolve_root(root), capture_output=True)
    return r.returncode == 0


def _resolve_root(root: str | None) -> str:
    from .record import _root
    return root or _root()


# ── the derived pair: re-derivation, reframed as a trail (the scenario gate) ─────

def derived(result, root: str | None = None) -> str | None:
    """The derived pair's trail: the touched capability's scenarios must re-derive red→green. The gate
    delegates to the `scenario` gate — which re-runs the scenarios in the fence and **trusts only the
    transition**, never a stored verdict — and reframes its absence as the flat provenance reason. A
    RESULT hand-authored without a fenced build leaves no red→green to re-derive, so it has no trail and
    is refused. This attests the build **ran**; whether its scenarios test the property is deferred."""
    from . import scenario
    return NO_TRAIL if scenario.gate(result, root) else None


# ── the negative space: what a trail-less record looks like (forge fixtures) ─────
# A mechanism's real output and a hand-faked one are byte-indistinguishable, so the only way a fixture
# can prove the gate refuses the fake is to *be* the fake. These build the trail-less records the gate
# must catch — defined beside the gate so the real-vs-forged contrast is one source. They are fixture
# support for the scenario worlds (which lazy-import them), never reached on a live fold.


class _Forged:
    """A hand-authored hand-off the gate reads exactly as it reads a worker's — its delta, its
    'worktree', and (for an authored record) the node it reaches. Duck-typed, not a `WorkerResult`, so
    a fixture can hand one to the gate without the fence a real result carries."""
    def __init__(self, delta: str, worktree: str, report: str = "", node_path: str = ""):
        self.delta, self.worktree, self.report, self.node_path = delta, worktree, report, node_path


_PROBE_DELTA = ("## ADDED — folding-conditions\n### Requirement: a hand-authored provenance probe\n"
                "A probe MUST hold.\n#### Scenario: s\n- WHEN it runs\n- THEN it holds\n")


def forged_result(root: str | None, flag: bool = False) -> _Forged:
    """A worker RESULT hand-authored with **no fenced build**. Its delta names a scenario-carrying
    capability, but its 'worktree' is a bare spec copy — not a git fence — so the scenario gate finds
    scenarios to re-derive yet cannot run them (no fork base): the red→green cannot re-derive, the record
    has no trail. With `flag` it also carries a self-asserted `ran: true` the gate must **ignore** — a
    record that asserts its own provenance is no trail at all. (A design decision's negative space — the
    contest-skipped pick — is forged inline by the `design-it-twice` world, which holds the node.)"""
    import os
    import shutil
    import tempfile
    d = tempfile.mkdtemp(prefix="forged-result-")
    src = os.path.join(root or "", "spec")
    if os.path.isdir(src):
        shutil.copytree(src, os.path.join(d, "spec"), ignore=shutil.ignore_patterns("__pycache__"))
    report = "ran: true (self-asserted, no fenced build)" if flag else "hand-authored, no fenced build"
    return _Forged(_PROBE_DELTA, d, report)
