"""The worker: system-facing, fenced, grounded in the living spec.

The worker is the half of the split that never faces the operator. Its audience is
the architect and the spec; its job ends at handing back a complete technical
result, written for the machine. Three properties define it, and each is structural,
not a discipline to remember:

- **It is grounded in its capability's spec slice, with full scan of the whole spec.**
  Before a worker runs, `context` assembles the living spec for it — the capabilities its
  change touches marked as its *grounding*, the rest of the spec carried beside them for
  scan, plus the glossary and the system's decisions — so there is no path that runs a
  worker without it. A worker is *not* slice-confined (rebuild-spec §4.1, §6.4): a delta
  cannot be authored or verified from one capability in isolation, so the worker rescans
  the whole spec and its rescan catches a capability the handed delta mis-named or missed.
  It holds the spec, never raw code, and never the operator view.

- **It runs fenced in its own git worktree.** Its tree is a separate checkout on its
  own branch; it builds in isolation and its commits reach the one record without ever
  touching a sibling's tree or the main line. (intent.md's full fence — the rest of the
  host read-only — is the system's to enforce around this; the worktree is the seam.)

- **Its output cannot reach the operator.** `apply` returns a `WorkerResult`, written
  for the machine. It has no operator-facing field and is never rendered. The only
  thing that crosses to the operator is what the architect *authors* from it
  (`conversation.integrate`) — so the old raw-worker-prose-on-a-card failure is not a
  bug to avoid but a path that does not exist.

- **It is grounded in the depth disciplines, every episode.** The prompt carries the
  deep-module framework and the red flags (`DEPTH`, from `research/aposd.md`, rebuild-spec
  §7.1) so the worker builds **deep up front** — strategic, not tactical. This is the
  *proactive* primary defense against complexity (re-grounding §3): a worker that shares
  the long-term-health concern produces deep modules, so the folding-conditions depth gate
  stays a rarely-tripped backstop rather than an operator-load generator. Design awareness
  is the first anti-complexity mechanism; the gate is the second.

Delta authorship crosses the seam (rebuild-spec §6.4): the architect *proposes*
the delta during grilling; the worker *applies* — rescans the current spec to verify the
handed delta against present reality, builds, and refines the delta as the code reveals
what the spec could not; the architect *archives* it.
"""
from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass, field

from . import conversation, delta, graph, grill, spec

WORKER = (
    "You are a hypercore worker — the system-facing half of the split. Your audience is "
    "the architect and the spec, never the operator: write for the machine, in "
    "precise technical terms, no operator-facing prose. You are grounded in the capabilities "
    "marked below and hold the whole spec beside them. Rescan the WHOLE spec to verify the "
    "handed delta against current reality — catch any capability it mis-named or missed, "
    "because a delta cannot be authored from one capability in isolation — do the work behind "
    "a feedback loop, and refine the delta to match what you built. BUILD DEEP UP FRONT: "
    "honor the depth disciplines below — a lot of behavior behind a small interface, no "
    "shallow modules, no red flags — so your work folds without tripping the depth gate. "
    "Reply with ONLY a JSON "
    "object:\n"
    '{"report": <the technical result and all relevant facts, for the architect>, '
    '"delta": <the refined spec delta — ADDED/MODIFIED/REMOVED markdown over the '
    'capabilities the change touches>, '
    '"loop": {"command": <how to run the feedback loop>, '
    '"red": <its failing verdict on the behavior before the fix>, '
    '"green": <its passing verdict after the fix>}}'
)

# The depth disciplines the worker is grounded in every episode (rebuild-spec §7.1,
# re-grounded in Ousterhout — `research/aposd.md`). Compressed to fit the window: the
# criterion, the signal, and the red flags it learns to *not* build. This is the proactive
# anti-complexity defense — the worker builds deep so the gate rarely has to raise a decision.
DEPTH = (
    "The depth disciplines (you are held to these — build deep up front):\n"
    "- DEEP MODULES are the criterion: a lot of behavior behind a small interface. A simple "
    "interface matters more than a simple implementation — interface cost is paid by every "
    "caller forever, implementation cost is paid once. PULL COMPLEXITY DOWNWARD: when "
    "something must be hard, make it hard inside the module.\n"
    "- STRATEGIC, not tactical: working code is not enough; invest in the design that keeps "
    "the system cheap to change. The increments are abstractions, not features.\n"
    "- LENGTH is a signal, not the criterion: every line is context an agent must load, so a "
    "long module costs the window — but a deep module may be long and a heap of shallow "
    "fragments is worse. Do not over-decompose into shallow, entangled pieces (classitis).\n"
    "- RED FLAGS — symptoms of shallowness to avoid: shallow module; information leakage (the "
    "same knowledge in two places); temporal decomposition (structure by execution order, not "
    "knowledge); pass-through method (only forwards its arguments); special-general mixture; "
    "conjoined methods (you must read one to understand the other); repetition; a comment that "
    "repeats the code; a vague or hard-to-pick name; nonobvious code.\n"
    "- DEFINE ERRORS OUT OF EXISTENCE where you can, and COMMENT what the code cannot say "
    "(the why, the invariants) — an interface comment is what makes a module deep from outside."
)


@dataclass
class WorkerContext:
    """The spec a worker is grounded in — assembled from the model, never free-form. It
    carries the *whole* spec (the worker is not slice-confined): `capabilities` is every
    capability, and `touched` marks the ones the change names as its grounding/focus. The
    rest is carried for the rescan that catches a mis-named or missed capability. Nothing of
    the operator view and nothing of the code is in here."""
    capabilities: list[tuple[str, str]] = field(default_factory=list)  # (name, spec text) — all
    glossary: str = ""
    decisions: str = ""
    delta: str = ""                                   # the handed delta, to verify + refine
    touched: set[str] = field(default_factory=set)    # the grounding: capabilities the delta names

    @property
    def names(self) -> list[str]:
        return [name for name, _text in self.capabilities]


@dataclass
class WorkerResult:
    """The worker's hand-off — written for the machine. No field of this is operator-facing
    and nothing renders it; the architect authors every operator-facing word from
    it. The worker's words reach the operator through no path at all."""
    report: str                                       # the technical result, for the architect
    delta: str                                        # the refined spec delta the change realizes
    loop: dict                                         # the recorded red→green loop (folding-conditions enforces it)
    worktree: str                                     # the fenced tree the work ran in


# ── the spec slice (assembled by construction; no worker runs without it) ─────

def context(node: graph.Node, root: str | None = None) -> WorkerContext:
    """Assemble the living spec for a node: the *whole* spec — every capability's text, the
    glossary, the decisions — with the capabilities the handed delta names marked as the
    worker's grounding (`touched`). The worker is not slice-confined: it holds full scan
    access so its rescan can verify the handed delta against the whole spec, not trust its
    list (rebuild-spec §4.1, §6.4)."""
    sp = spec.read_spec(root)
    handed = _handed_delta(node)
    touched = _touched(handed, sp)
    caps = [(c.name, _cap_text(c.name, root)) for c in sp.capabilities]   # all — full scan
    return WorkerContext(caps, sp.glossary, _decisions(root), handed, touched)


def prompt(node: graph.Node, ctx: WorkerContext) -> str:
    """The worker's grounding, rendered to one prompt — the depth disciplines first (the
    proactive defense), then the touched capabilities foregrounded as the grounding, the rest
    of the spec carried for the rescan, then the glossary, decisions, the handed delta, and the
    ask. This is the whole of what the worker is given."""
    def render(items):
        return "\n\n".join(f"### capability: {n}\n{t.strip()}" for n, t in items)
    grounding = render([(n, t) for n, t in ctx.capabilities if n in ctx.touched])
    scan = render([(n, t) for n, t in ctx.capabilities if n not in ctx.touched])
    return (
        f"{WORKER}\n\n"
        f"{DEPTH}\n\n"
        f"The ask:\n{grill.contract_of(node) or node.text}\n\n"
        f"The handed delta (verify and refine it against the WHOLE spec):\n"
        f"{ctx.delta or '(none — author it from the full scan)'}\n\n"
        f"Your grounding — the capabilities the delta names:\n"
        f"{grounding or '(none named — author the delta from the full scan)'}\n\n"
        f"The rest of the spec, for your rescan (catch any capability the delta mis-named or "
        f"missed):\n{scan or '(none — this is the whole spec)'}\n\n"
        f"The glossary:\n{ctx.glossary}\n\n"
        f"The decisions:\n{ctx.decisions or '(none)'}\n\n"
        "Reply with the JSON object now."
    )


# ── the fence (a real, separate git worktree on its own branch) ──────────────

def worktree(node: graph.Node, root: str | None = None) -> str:
    """Cut the worker a fenced tree: a separate checkout on branch worker/<id>. It builds
    here in isolation; its commits land in the shared object store without touching the
    main line or a sibling's tree."""
    base = root or graph._root()
    path = _tree_path(node, base)
    if os.path.isdir(path):
        return path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    _git(base, "worktree", "add", "-b", f"worker/{node.id}", path, "HEAD")
    return path


def teardown(node: graph.Node, root: str | None = None) -> None:
    """Tear the fence down once the result has integrated: remove the worktree and its
    branch. The work has reached the one record through the fold, not through this branch."""
    base = root or graph._root()
    path = _tree_path(node, base)
    _git(base, "worktree", "remove", "--force", path)
    _git(base, "branch", "-D", f"worker/{node.id}")


# ── apply: the worker builds, fenced and grounded, and hands back ────────────

def apply(node: graph.Node, transport=None, root: str | None = None) -> WorkerResult:
    """Run the worker on a node: assemble its spec slice (the grounding, by construction),
    summon it, and take its machine-facing result. The result is committed inside the
    worker's own tree — its commit reaching the record in isolation — and handed back."""
    transport = transport or conversation._claude
    ctx = context(node, root)                          # no apply without the grounding
    obj = conversation._parse(transport(prompt(node, ctx)))
    report = (obj.get("report") or "").strip()
    refined = (obj.get("delta") or ctx.delta).strip()
    loop = obj.get("loop") if isinstance(obj.get("loop"), dict) else {}
    tree = _tree_path(node, root or graph._root())
    _record(tree, report, refined, loop)               # the worker's own commit, fenced
    return WorkerResult(report, refined, loop, tree)


def run(node: graph.Node, transport=None, root: str | None = None):
    """The whole crossing for one node: take it (it goes live), build it fenced, hand to
    the architect to coherence-check and archive, then tear the fence down. The
    worker speaks only to the architect; what reaches the operator is its reply."""
    graph.delegate(node)
    worktree(node, root)
    result = apply(node, transport, root)
    reply = conversation.integrate(node, result, root=root)
    if reply.done:                                     # archived: the result integrated
        teardown(node, root)
    return reply


# ── internals ────────────────────────────────────────────────────────────────

def _handed_delta(node: graph.Node) -> str:
    entry = grill.entry_of(node)
    return grill.delta_of(entry) if entry else ""


def _touched(handed: str, sp: spec.Spec) -> set[str]:
    """The capabilities a delta touches; with no handed delta, every capability — the
    worker must scan flat to author one (you cannot tell what a change touches from a
    single capability in isolation)."""
    if not handed.strip():
        return {c.name for c in sp.capabilities}
    return {op.capability for op in delta.parse(handed).ops}


def _cap_text(name: str, root: str | None) -> str:
    path = spec.cap_path(name, root)
    return open(path).read() if os.path.isfile(path) else ""


def _decisions(root: str | None) -> str:
    d = os.path.join(spec.spec_dir(root), "decisions")
    if not os.path.isdir(d):
        return ""
    return "\n\n".join(open(os.path.join(d, n)).read()
                       for n in sorted(os.listdir(d)) if n.endswith(".md"))


def _tree_path(node: graph.Node, base: str) -> str:
    return os.path.join(base, "work", "worktrees", node.id)


def _record(tree: str, report: str, refined: str, loop: dict) -> None:
    """The worker commits everything it built inside its own tree — RESULT.md beside any
    source it produced — proof its commits reach the one record, fenced from the main line
    until the architect integrates the delta. The whole tree is committed (not just
    RESULT.md) so the material the folding conditions read — the source it grew, the loop it
    ran — is in the record."""
    loop_md = "\n".join(f"- {k}: {loop.get(k, '')}" for k in ("command", "red", "green"))
    body = f"# worker result\n\n## report\n{report}\n\n## delta\n{refined}\n\n## loop\n{loop_md}\n"
    graph.atomic_write(os.path.join(tree, "RESULT.md"), body)
    _git(tree, "add", "-A")
    _git(tree, "commit", "-m", "worker: result")


def _git(cwd: str, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
