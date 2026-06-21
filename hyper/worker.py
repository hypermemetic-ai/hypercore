"""The worker: system-facing, fenced, grounded in the living spec.

The worker is the half of the split that never faces the operator. Its audience is
the conversationalist and the spec; its job ends at handing back a complete technical
result, written for the machine. Three properties define it, and each is structural,
not a discipline to remember:

- **It is grounded in its capability's spec slice, by construction.** Before a worker
  runs, the spec is sliced for it — the requirements and scenarios of the capabilities
  its change touches, the glossary, the system's decisions. `apply` builds its prompt
  only from that slice (`context`), so there is no path that runs a worker without it.
  It holds the spec, never raw code, and never the operator view.

- **It runs fenced in its own git worktree.** Its tree is a separate checkout on its
  own branch; it builds in isolation and its commits reach the one record without ever
  touching a sibling's tree or the main line. (intent.md's full fence — the rest of the
  host read-only — is the system's to enforce around this; the worktree is the seam.)

- **Its output cannot reach the operator.** `apply` returns a `WorkerResult`, written
  for the machine. It has no operator-facing field and is never rendered. The only
  thing that crosses to the operator is what the conversationalist *authors* from it
  (`conversation.integrate`) — so the old raw-worker-prose-on-a-card failure is not a
  bug to avoid but a path that does not exist.

Delta authorship crosses the seam (rebuild-spec §6.4): the conversationalist *proposes*
the delta during grilling; the worker *applies* — rescans the current spec to verify the
handed delta against present reality, builds, and refines the delta as the code reveals
what the spec could not; the conversationalist *archives* it.
"""
from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass, field

from . import conversation, delta, graph, grill, spec

WORKER = (
    "You are a hypercore worker — the system-facing half of the split. Your audience is "
    "the conversationalist and the spec, never the operator: write for the machine, in "
    "precise technical terms, no operator-facing prose. You are grounded in the spec "
    "slice below. Rescan it to verify the handed delta against current reality, do the "
    "work behind a feedback loop, and refine the delta to match what you built. Reply "
    "with ONLY a JSON object:\n"
    '{"report": <the technical result and all relevant facts, for the conversationalist>, '
    '"delta": <the refined spec delta — ADDED/MODIFIED/REMOVED markdown over the '
    'capabilities the change touches>, '
    '"loop": <the feedback loop you drove: how it went red on the behavior, then green>}'
)


@dataclass
class WorkerContext:
    """The spec slice a worker is grounded in — assembled from the model, never free-form.
    Its capabilities are exactly the ones the change touches; nothing of the operator
    view and nothing of the code is in here."""
    capabilities: list[tuple[str, str]] = field(default_factory=list)  # (name, spec text)
    glossary: str = ""
    decisions: str = ""
    delta: str = ""                                   # the handed delta, to verify + refine

    @property
    def names(self) -> list[str]:
        return [name for name, _text in self.capabilities]


@dataclass
class WorkerResult:
    """The worker's hand-off — written for the machine. No field of this is operator-facing
    and nothing renders it; the conversationalist authors every operator-facing word from
    it. The worker's words reach the operator through no path at all."""
    report: str                                       # the technical result, for the conversationalist
    delta: str                                        # the refined spec delta the change realizes
    loop: str                                         # the feedback-loop record (slice 5 enforces it)
    worktree: str                                     # the fenced tree the work ran in


# ── the spec slice (assembled by construction; no worker runs without it) ─────

def context(node: graph.Node, root: str | None = None) -> WorkerContext:
    """Slice the living spec for a node: the capabilities its handed delta touches (or a
    full scan when none is handed — a delta cannot be authored from one capability alone),
    their spec text, the glossary, and the system's decisions."""
    sp = spec.read_spec(root)
    handed = _handed_delta(node)
    touched = _touched(handed, sp)
    caps = [(c.name, _cap_text(c.name, root)) for c in sp.capabilities if c.name in touched]
    return WorkerContext(caps, sp.glossary, _decisions(root), handed)


def prompt(node: graph.Node, ctx: WorkerContext) -> str:
    """The worker's grounding, rendered to one prompt — spec slice, glossary, decisions,
    the handed delta, and the ask. This is the whole of what the worker is given."""
    sliced = "\n\n".join(f"### capability: {n}\n{t.strip()}" for n, t in ctx.capabilities)
    return (
        f"{WORKER}\n\n"
        f"The ask:\n{grill.contract_of(node) or node.text}\n\n"
        f"The handed delta (verify and refine it):\n{ctx.delta or '(none — author it from the scan)'}\n\n"
        f"The spec slice you are grounded in:\n{sliced or '(no capability matched)'}\n\n"
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
    ctx = context(node, root)                          # no apply without the slice
    obj = conversation._parse(transport(prompt(node, ctx)))
    report = (obj.get("report") or "").strip()
    refined = (obj.get("delta") or ctx.delta).strip()
    loop = (obj.get("loop") or "").strip()
    tree = _tree_path(node, root or graph._root())
    _record(tree, report, refined, loop)               # the worker's own commit, fenced
    return WorkerResult(report, refined, loop, tree)


def run(node: graph.Node, transport=None, root: str | None = None):
    """The whole crossing for one node: take it (it goes live), build it fenced, hand to
    the conversationalist to coherence-check and archive, then tear the fence down. The
    worker speaks only to the conversationalist; what reaches the operator is its reply."""
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


def _record(tree: str, report: str, refined: str, loop: str) -> None:
    """The worker commits its result inside its own tree — proof its commits reach the one
    record, fenced from the main line until the conversationalist integrates the delta."""
    body = f"# worker result\n\n## report\n{report}\n\n## delta\n{refined}\n\n## loop\n{loop}\n"
    graph.atomic_write(os.path.join(tree, "RESULT.md"), body)
    _git(tree, "add", "RESULT.md")
    _git(tree, "commit", "-m", "worker: result")


def _git(cwd: str, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
