"""The worker: system-facing, fenced, grounded in the living spec.

The worker is the half of the split that never faces the operator. Its audience is
the architect and the spec; its job ends at handing back a complete technical
result, written for the machine. Three properties define it, and each is structural,
not a discipline to remember:

- **It is grounded in its capability's spec slice, with full scan of the whole spec.**
  Before a worker runs, `context` assembles the living spec for it — the capabilities its
  change touches marked as its *grounding*, the rest of the spec carried beside them for
  scan, plus the glossary — so there is no path that runs a worker without it. The spec is
  **preloaded whole** (the small, scannable high-signal core); the long history and grounds of
  past decisions are *not* inlined — they carry no whole-picture stake, so the worker runs at its
  fence and greps `work/archive/` in its own checkout **just-in-time** as the change needs
  (role-assembly step 5). A worker is *not* slice-confined: a delta
  cannot be authored or verified from one capability in isolation, so the worker rescans
  the whole spec and its rescan catches a capability the handed delta mis-named or missed.
  It holds the spec, never raw code, and never the operator view.

- **It runs fenced in its own git worktree.** Its tree is a separate checkout on its
  own branch; it builds in isolation and its commits reach the one record without ever
  touching a sibling's tree or the main line. Its model transport runs with its working
  directory set to that worktree (`transport.worker_transport`), so the checkout — its source,
  the archived grounds, and the derived channel files (the anchor and skills) — is what it reads,
  and the harness auto-loads the fence's anchor and discovers its skills. (intent.md's full
  fence — the rest of the host read-only — is the system's to enforce around this; the worktree
  is the seam.)

- **Its output cannot reach the operator.** `apply` returns a `WorkerResult`, written
  for the machine. It has no operator-facing field and is never rendered. The only
  thing that crosses to the operator is what the architect *authors* from it
  (`communication.integrate`) — so the old raw-worker-prose-on-a-card failure is not a
  bug to avoid but a path that does not exist.

- **It is grounded in the depth standards, every episode.** The prompt foregrounds the `depth`
  capability — the deep-module framework and the red flags — ahead of the ask, so the worker builds
  **deep up front**, strategic, not tactical. This is the *proactive* primary defense against
  complexity: a worker that shares the long-term-health concern produces deep
  modules, so the folding-conditions depth gate stays a rarely-tripped backstop rather than an
  operator-load generator. Design awareness is the first anti-complexity mechanism; the gate is
  the second. Depth is a capability like any other, single-sourced from `spec/depth.md`,
  so a sharpened slice reaches the next worker with no second copy to drift — the old `worker.DEPTH`
  constant's smell, retired.

Delta authorship crosses the seam: the architect *proposes*
the delta during grilling; the worker *applies* — rescans the current spec to verify the
handed delta against present reality, builds, and refines the delta as the code reveals
what the spec could not; the architect *archives* it.

The worker's **discipline prose is single-sourced from `spec/worker.md`**, not hand-frozen in this
module. The old `WORKER` constant restated the slice by hand — the exact `worker.DEPTH`-constant
drift-by-copy retired for depth, left unretired here. Now the prompt renders the worker's
own requirement statements through the same `methodology` seam the skills use, so a sharpened
`spec/worker.md` reaches the next worker with no second copy to drift. Only the genuinely
non-inferable envelope stays authored in this module: the JSON reply shape, and two grounding facts
the slice does not carry — the **corrected single-writer invariant** (stage the exact files a change
touches, never `-A` over a shared parent; a repo-level lock spans write→commit) and the **scenario
gate** (you author no loop; build to turn the architect's scenario red→green, and a requirement is
gated exactly when one of its scenarios carries an executable check block, watched otherwise). The
worker is taught the gate it builds toward; the lock the engine enforces folds alongside it.
"""
from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass, field

from . import communication, delta, tree, grill, methodology, spec
from .transport import parse_object, worker_transport

# The salutation — who the worker is, in one line; the disciplines that follow are single-sourced from
# spec/worker.md (the methodology seam), not restated here, so they cannot drift from the slice.
SALUTATION = (
    "You are a hypercore worker — the system-facing half of the split. Your audience is the architect "
    "and the spec, never the operator. The disciplines below are the standing ones you are held to; "
    "honor them, then build."
)

# The genuinely non-inferable grounding the slice does not carry — two engine facts the worker must be
# told because it cannot read them off the spec. They land here with engine-hardening's engine fix.
GROUNDING = (
    "Two facts about the shared record you cannot infer from the spec, and must respect:\n"
    "- **The single-writer record.** The one git record is shared across concurrent fences. Stage the "
    "*exact* files your change touches — never `git add -A` over a shared parent, which can sweep a "
    "sibling worker's uncommitted material into your commit. A repo-level lock spans write→commit, so "
    "your write and your commit are one indivisible act on the record; do nothing that reaches outside "
    "your own worktree between them.\n"
    "- **The scenario gate, and gated versus watched.** You do not author the check that judges you. A "
    "behavior change folds only when the **architect-authored scenarios** of the capabilities it "
    "touches go red→green — failing at the fork base (the behavior absent), passing at your tip. Build "
    "to turn those scenarios green; you record **no loop**. A capability requirement is *gated* exactly "
    "when one of its scenarios carries an executable `check` block (the **delta applies**, the **length "
    "ratchet**, and the **mechanical red-flag scan** are gated this way); it is *watched* — model "
    "judgment no adversarial fixture can certify (**depth** as a module judgment, **coherence**, the "
    "**grilling floor**, the **design-it-twice** pick) — when none does. Do not mistake a watched "
    "discipline for a gated one; hold it yourself, because no gate will."
)

# The one authored residue that is neither discipline nor grounding: the reply shape the transport parses.
ENVELOPE = (
    "Reply with ONLY a JSON object:\n"
    '{"report": <the technical result and all relevant facts, for the architect>, '
    '"delta": <the refined spec delta — ADDED/MODIFIED/REMOVED/RENAMED markdown over the '
    'capabilities the change touches, including any new or sharpened scenario (with its check '
    'block) the behavior needs>}'
)


def _worker_disciplines(root: str | None = None) -> str:
    """The worker's standing disciplines, rendered from `spec/worker.md`'s requirement statements through
    the same `methodology` seam the skills use — single-sourced, so a sharpened slice reaches the next
    worker with no second copy to drift (the retired `WORKER`-constant restatement). The depth standards
    are foregrounded separately by `prompt`; these are the worker's own."""
    text = methodology._read_slice("worker", root)
    return methodology._bullets(methodology._disciplines(text))

@dataclass
class WorkerContext:
    """The grounding a worker runs on — assembled from the model, never free-form. It carries
    the *whole* spec (the worker is not slice-confined): `capabilities` is every capability, and
    `touched` marks the ones the change names as its grounding/focus; the rest is carried for the
    rescan that catches a mis-named or missed capability. The `depth` capability is among them, and
    the prompt foregrounds it every episode. The long history and grounds of past decisions are *not*
    here — the worker greps `work/archive/` in its fence checkout just-in-time (step 5). Nothing of
    the operator view and nothing of the code is in here."""
    capabilities: list[tuple[str, str]] = field(default_factory=list)  # (name, spec text) — all
    glossary: str = ""
    delta: str = ""                                   # the handed delta, to verify + refine
    touched: set[str] = field(default_factory=set)    # the grounding: capabilities the delta names

    @property
    def names(self) -> list[str]:
        return [name for name, _text in self.capabilities]


@dataclass
class CodeFile:
    """One engine path the worker's build touched, captured as a self-contained pair: the byte-image it
    forked from (`base`, the fence's HEAD~1) and the verified bytes it hands back (`tip`, the fence's
    working tree). The fold content-replays the `tip` onto main and reads the `base` for its staleness
    pre-check; either is `None` for a path absent at that end (an added file has no base, a removed one
    no tip). Content, not a diff — the verified bytes themselves, so the fold consumes a flat artifact
    and never reaches a live fence."""
    base: str | None
    tip: str | None


@dataclass
class WorkerResult:
    """The worker's hand-off — written for the machine. No field of this is operator-facing
    and nothing renders it; the architect authors every operator-facing word from
    it. The worker's words reach the operator through no path at all."""
    report: str                                       # the technical result, for the architect
    delta: str                                        # the refined spec delta the change realizes
    worktree: str                                     # the fenced tree the work ran in (the gate runs its scenarios red→green here)
    code: dict[str, CodeFile] = field(default_factory=dict)  # the verified engine code the build touched, for the fold to land on main


# ── the spec slice (assembled by construction; no worker runs without it) ─────

def context(node: tree.Node, root: str | None = None) -> WorkerContext:
    """Assemble the grounding for a node: the *whole* spec — every capability's text and the
    glossary — with the capabilities the handed delta names marked as the worker's grounding
    (`touched`); the `depth` capability is among them and the prompt foregrounds it every episode.
    The long history and grounds of past decisions are left out by design: the worker greps
    `work/archive/` in its fence checkout just-in-time (step 5), so the preloaded grounding stays the
    small, scannable spec. The worker is not slice-confined: it holds full scan access so its rescan
    can verify the handed delta against the whole spec, not trust its list."""
    sp = spec.read_spec(root)
    handed = _handed_delta(node)
    touched = _touched(handed, sp)
    caps = [(c.name, _cap_text(c.name, root)) for c in sp.capabilities]   # all — full scan, incl. depth
    return WorkerContext(caps, sp.glossary, handed, touched)


def prompt(node: tree.Node, ctx: WorkerContext, root: str | None = None) -> str:
    """The worker's grounding, rendered to one prompt — the salutation, then the worker's own
    disciplines single-sourced from `spec/worker.md`, the non-inferable record grounding, and the JSON
    envelope; then the depth standards (the proactive defense), the touched capabilities foregrounded
    as the grounding, the rest of the spec carried for the rescan, the glossary, the handed delta, and
    the ask. The long history and grounds of past decisions are *not* inlined: the prompt points the
    worker at `work/archive/` in its fence checkout to grep just-in-time (step 5). This is the whole of
    what the worker is given."""
    def render(items):
        return "\n\n".join(f"### capability: {n}\n{t.strip()}" for n, t in items)
    depth_text = next((t.strip() for n, t in ctx.capabilities if n == "depth"), "")
    grounding = render([(n, t) for n, t in ctx.capabilities if n in ctx.touched and n != "depth"])
    scan = render([(n, t) for n, t in ctx.capabilities if n not in ctx.touched and n != "depth"])
    return (
        f"{SALUTATION}\n\n"
        f"Your standing disciplines (single-sourced from spec/worker.md — what good looks like):\n"
        f"{_worker_disciplines(root)}\n\n"
        f"{GROUNDING}\n\n"
        f"{ENVELOPE}\n\n"
        f"The depth standards — you are held to these every episode; build deep up front:\n"
        f"{depth_text}\n\n"
        f"The ask:\n{grill.contract_of(node) or node.text}\n\n"
        f"The handed delta (verify and refine it against the WHOLE spec):\n"
        f"{ctx.delta or '(none — author it from the full scan)'}\n\n"
        f"Your grounding — the capabilities the delta names:\n"
        f"{grounding or '(none named — author the delta from the full scan)'}\n\n"
        f"The rest of the spec, for your rescan (catch any capability the delta mis-named or "
        f"missed):\n{scan or '(none — this is the whole spec)'}\n\n"
        f"The glossary:\n{ctx.glossary}\n\n"
        f"The long history and grounds of past decisions are not inlined here — they carry no "
        f"whole-picture stake, so you pull them just-in-time from your own checkout: the archived "
        f"nodes are in `work/archive/` at your worktree root; grep them for a past decision's grounds "
        f"as the change needs. The spec capabilities above are preloaded whole — your scannable "
        f"high-signal core.\n\n"
        "Reply with the JSON object now."
    )


# ── the fence (a real, separate git worktree on its own branch) ──────────────

def worktree(node: tree.Node, root: str | None = None, tag: str = "") -> str:
    """Cut the worker a fenced tree: a separate checkout on branch worker/<id>. It builds
    here in isolation; its commits land in the shared object store without touching the
    main line or a sibling's tree. `tag` distinguishes sibling fences on one node — the
    design-it-twice contest cuts one per candidate (branch worker/<id>-<tag>), so several
    candidates advance the same decision in isolation from each other."""
    base = root or tree._root()
    path = _tree_path(node, base, tag)
    if os.path.isdir(path):
        return path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    _git(base, "worktree", "add", "-b", _branch(node, tag), path, "HEAD")
    return path


def teardown(node: tree.Node, root: str | None = None, tag: str = "") -> None:
    """Tear the fence down — remove the worktree and its branch — on *every* path out of a worker
    crossing, not only the integrating one (C2). The work reaches the one record through the fold, not
    through this branch, so the fence is always disposable once the crossing ends. Best-effort and
    idempotent: a fence never cut, already torn down, or half-removed leaves no part standing and
    raises nothing, so `run`'s `finally` can call it unconditionally without a refusal or an error
    leaking a worktree or branch."""
    base = root or tree._root()
    path = _tree_path(node, base, tag)
    _git_quiet(base, "worktree", "remove", "--force", path)
    _git_quiet(base, "worktree", "prune")               # clear any stale administrative entry
    _git_quiet(base, "branch", "-D", _branch(node, tag))


def commit_tree(tree: str, message: str) -> None:
    """Commit everything in a fence to the one record — the in-fence commit primitive, kept
    in one place because the fence is the worker's concern. Both the worker's result and a
    design-it-twice candidate's design land through it, fenced from the main line until they
    integrate."""
    _git(tree, "add", "-A")
    _git(tree, "commit", "-m", message)


# ── apply: the worker builds, fenced and grounded, and hands back ────────────

def apply(node: tree.Node, transport=None, root: str | None = None) -> WorkerResult:
    """Run the worker on a node: assemble its spec slice (the grounding, by construction),
    summon it at its fence, and take its machine-facing result. With no injected transport the live
    worker runs via `worker_transport(tree)` — cwd = its worktree (step 5), so it reads the archived
    grounds and its skills from its own checkout; the harness injects a scripted fake instead. The result
    is committed inside the worker's own tree — its commit reaching the record in isolation."""
    ctx = context(node, root)                          # no apply without the grounding
    fence = _tree_path(node, root or tree._root())
    transport = transport or worker_transport(fence)   # the live worker runs at its fence (step 5)
    obj = parse_object(transport(prompt(node, ctx, root)))  # strict: a malformed reply is a failure, not a no-op (H3)
    report = (obj.get("report") or "").strip()
    refined = (obj.get("delta") or ctx.delta).strip()
    _record(fence, report, refined)                    # the worker's own commit, fenced
    return WorkerResult(report, refined, fence, _capture_code(fence))  # the verified code, captured before teardown


def run(node: tree.Node, transport=None, root: str | None = None):
    """The whole crossing for one node: take it (it goes live), build it fenced, hand to the architect
    to coherence-check and archive, then tear the fence down — on *every* exit, not only the
    integrating one. The worker speaks only to the architect; what reaches the operator is its reply.

    Refusal is the steady-state path, not an edge: a folding-condition block, a failed coherence
    judgment, or a malformed model reply returns not-done, and an error mid-build raises. On any of
    these the fence must not leak and the node must not strand `IN_FLIGHT` with no live worker (C2).
    So the fence is torn down in a `finally`, and a non-integrating crossing recovers the node to
    standing (its decision card, parented to it, blocks re-dispatch until the operator settles it). The
    error path recovers the node too, then re-raises so the scheduler raises its own decision card."""
    tree.dispatch(node)
    try:
        worktree(node, root)
        result = apply(node, transport, root)
        reply = communication.integrate(node, result, transport, root=root)  # one transport, build → archive
        if not reply.done:                             # refused or judged incoherent — recover, don't strand
            tree.recover(node)
        return reply
    except Exception:
        tree.recover(node)                            # an error mid-build must not leave the node in flight
        raise                                          # the scheduler turns it into a decision card
    finally:
        teardown(node, root)                           # the fence never leaks, on any path out of the crossing


# ── internals ────────────────────────────────────────────────────────────────

def _handed_delta(node: tree.Node) -> str:
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


def _tree_path(node: tree.Node, base: str, tag: str = "") -> str:
    name = node.id + (f"-{tag}" if tag else "")
    return os.path.join(base, "work", "worktrees", name)


def _branch(node: tree.Node, tag: str = "") -> str:
    return f"worker/{node.id}" + (f"-{tag}" if tag else "")


def _capture_code(fence: str) -> dict[str, CodeFile]:
    """Capture the engine code the worker built in its fence as a self-contained artifact — per engine
    path its one commit touched, the byte-image it forked from (`base`, HEAD~1) and the verified bytes
    it hands back (`tip`, the working tree). The fold content-replays the tip onto main and reads the
    base for its staleness pre-check; no live fence is reached at fold time. Scoped to `engine/*.py` —
    where hypercore's code lives — so the spec (folded via the delta), the derived channels
    (re-rendered on fold), the node's own folder, and the `RESULT.md` scratch never cross as code. A
    **read** of the fence, run unlocked: the verified bytes are taken into the hand-off, not the fence."""
    names = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], cwd=fence,
                           capture_output=True, text=True).stdout.split()
    code: dict[str, CodeFile] = {}
    for rel in names:
        if not (rel.startswith("engine/") and rel.endswith(".py")):
            continue
        tip_path = os.path.join(fence, rel)
        tip = open(tip_path, encoding="utf-8").read() if os.path.isfile(tip_path) else None
        shown = subprocess.run(["git", "show", f"HEAD~1:{rel}"], cwd=fence,
                               capture_output=True, text=True)
        base = shown.stdout if shown.returncode == 0 else None
        code[rel] = CodeFile(base, tip)
    return code


def _record(fence: str, report: str, refined: str) -> None:
    """The worker commits everything it built inside its own fence — RESULT.md beside any
    source it produced — proof its commits reach the one record, fenced from the main line
    until the architect integrates the delta. The whole fence is committed (not just
    RESULT.md) so the material the folding conditions read — the source it grew, the scenario
    its delta turned green — is in the record. The worker records no loop: the check that judges
    it is the architect's scenario, run red→green by the gate over this fence."""
    body = f"# worker result\n\n## report\n{report}\n\n## delta\n{refined}\n"
    tree.atomic_write(os.path.join(fence, "RESULT.md"), body)
    commit_tree(fence, "worker: result")


@tree.serialized
def _git(cwd: str, *args: str) -> None:
    """Every git invocation the worker makes — cutting and tearing down a fence, committing inside
    it — under the one record lock (`tree.serialized`), so concurrent workers never collide on the
    shared `.git`. The slow build between these calls (the model transport) runs unlocked, so the
    fences are cut and committed serially but the work in them proceeds in parallel."""
    subprocess.run(["git", *args], cwd=cwd, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


@tree.serialized
def _git_quiet(cwd: str, *args: str) -> None:
    """A best-effort git invocation under the one record lock — like `_git` but tolerant of failure,
    for teardown, where the fence to remove may already be gone (C2 `finally`). The act it would undo
    has already left the fence, so a no-op removal loses nothing; never raising lets `run`'s `finally`
    tear down on every path without an absent fence masking the real outcome."""
    subprocess.run(["git", *args], cwd=cwd, check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
