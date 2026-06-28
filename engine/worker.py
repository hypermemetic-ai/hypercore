"""The worker seam: assemble grounding, run the model at its fence, and return a machine-facing
hand-off. The spec supplies the role discipline; this module holds the prompt economy, fence, and
handoff mechanics."""
from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass, field

from . import communication, delta, tree, grill, spec
from .transport import Envelope, Tag, instruction, read, worker_transport

# The salutation — who the worker is, in one line; the disciplines that follow are single-sourced from
# spec/worker.md (the methodology seam), not restated here, so they cannot drift from the slice.
SALUTATION = (
    "You are a hypercore worker — the system-facing half of the split. Your audience is the architect "
    "and the spec, never the operator. Your task comes first; the disciplines that follow are how you "
    "are held."
)

# The genuinely non-inferable grounding the slice does not carry — two engine facts the worker must be
# told because it cannot read them off the spec. They land here with engine-hardening's engine fix.
GROUNDING = (
    "Two facts about the shared record you cannot infer from the spec, and must respect:\n"
    "- **The single-writer record.** The one git record is shared across concurrent fences. Stage the "
    "*exact* files your change touches — never `git add -A` over a shared parent, which can sweep a "
    "sibling worker's uncommitted material into your commit.\n"
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

# One schema renders the prompt instruction and parses the hand-off; markdown rides verbatim.
WORKER_SCHEMA = Envelope(
    Tag("report", "the technical result and all relevant facts, for the architect"),
    Tag("delta", "the refined spec delta — ADDED / MODIFIED / REMOVED / RENAMED markdown over the "
                 "capabilities the change touches, including any new or sharpened scenario (with its "
                 "check block) the behavior needs"),
)
ENVELOPE = instruction(WORKER_SCHEMA)


@dataclass
class WorkerContext:
    """The whole-spec grounding model. `prompt` decides what is foregrounded, indexed, or left read-away;
    operator view, code, and archive grounds stay out."""
    capabilities: list[tuple[str, str]] = field(default_factory=list)  # (name, spec text) — all
    glossary: str = ""
    delta: str = ""                                   # the handed delta, to verify + refine
    touched: set[str] = field(default_factory=set)    # the grounding: capabilities the delta names
    proposed: bool = False                            # a resolved architect propose product exists

    @property
    def names(self) -> list[str]:
        return [name for name, _text in self.capabilities]


@dataclass
class CodeFile:
    """One touched engine path as fork-base bytes and verified tip bytes, content-replayed at fold."""
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
    node_path: str = ""                               # the result's node folder, so an authored record on it (a design decision) is reachable to the provenance gate
    base: str = ""                                    # the fork base — the commit the fence was cut from, so the gate runs the base there (not the tip's parent) and the capture spans the whole fork-base→tip range


# ── the spec slice (assembled by construction; no worker runs without it) ─────

def context(node: tree.Node, root: str | None = None) -> WorkerContext:
    """Assemble the grounding for a node: the *whole* spec — every capability's text and the glossary —
    with the ones the handed delta names marked as `touched`. `context` holds every full body; the
    economy falls in `prompt` — touched capability bodies and touched glossary entries are inlined, the
    rest stay indexed and read just-in-time from the checkout. Past-decision grounds are left out
    (greped from `work/archive/`, step 5). Not slice-confined: the index spans the whole map, so the
    rescan verifies the handed delta against it, not its list."""
    sp = spec.read_spec(root)
    handed = _handed_delta(node)
    touched = _touched(handed, sp)
    caps = [(c.name, _cap_text(c.name, root)) for c in sp.capabilities]   # all — full scan, incl. depth
    return WorkerContext(caps, sp.glossary, handed, touched, _has_proposed_delta(node))


def prompt(node: tree.Node, ctx: WorkerContext, root: str | None = None) -> str:
    """Render one worker prompt: touched bodies in full, untouched bodies indexed, named glossary terms
    inlined, standing skill-load routes hedged in brief, and the reply envelope last."""
    def _caps(items):
        return "\n\n".join(f"### capability: {n}\n{t.strip()}" for n, t in items)
    grounding = _caps([(n, t) for n, t in ctx.capabilities if n in ctx.touched])
    index = _index([(n, t) for n, t in ctx.capabilities if n not in ctx.touched])
    ask = grill.contract_of(node) or node.text
    glossary = _glossary(ask, ctx, root)
    handed = (ctx.delta if ctx.delta.strip()
              else ("(empty architect-proposed delta — a valid trivial delta; do not author a "
                    "replacement)" if ctx.proposed
                    else "(missing architect-proposed delta — worker.run refuses this node before "
                         "dispatch; do not author one)"))
    grounding_note = ("(no capabilities named by the proposed delta; use the whole-spec index for the "
                      "rescan and pull any implicated body just-in-time)")
    return (
        f"{SALUTATION}\n\n"
        f"The ask:\n{ask}\n\n"
        f"The handed delta (verify and refine it against the WHOLE spec):\n"
        f"{handed}\n\n"
        f"How you are held:\n\n"
        f"Your standing disciplines — load the `worker` skill from your checkout "
        f"(`skills/worker/SKILL.md`) and the `writing-for-the-machine` skill "
        f"(`skills/writing-for-the-machine/SKILL.md`); in brief, your audience is the architect and "
        f"the spec, never the operator, and you refine the delta you were handed rather than author "
        f"one.\n\n"
        f"{GROUNDING}\n\n"
        f"The depth standards — load the `depth` skill (`skills/depth/SKILL.md`); in brief, build "
        f"deep up front: deep modules, much behavior behind a small interface, complexity pulled "
        f"downward, strategic over tactical, away from the red flags (a shallow module above all).\n\n"
        f"Your grounding — the capabilities the delta names, in full:\n"
        f"{grounding or grounding_note}\n\n"
        f"The rest of the spec, indexed for your rescan — every other capability by its vision and "
        f"requirement titles, so you see the whole map and can catch one the delta mis-named or "
        f"missed. When your rescan implicates a capability, read its full body just-in-time from "
        f"`spec/<name>.md` in your checkout:\n{index or '(none — this is the whole spec)'}\n\n"
        f"The glossary entries named by the foregrounded prose:\n{glossary}\n\n"
        f"The long history and grounds of past decisions are not inlined here — they carry no "
        f"whole-picture stake, so you pull them just-in-time from your own checkout: the archived "
        f"nodes are in `work/archive/` at your worktree root; grep them for a past decision's grounds "
        f"as the change needs.\n\n"
        f"{ENVELOPE}"
    )


def _glossary(ask: str, ctx: WorkerContext, root: str | None = None) -> str:
    """The prompt's glossary economy: inline exactly the entries whose terms are named by the
    foregrounded prose — the ask, handed delta, and touched capability bodies. The full vocabulary stays
    in root `glossary.md` for just-in-time reads, so the worker carries the terms it uses without paying
    for the whole ratified set."""
    source = "\n\n".join([ask, ctx.delta, *(_cap_text(n, root) for n in sorted(ctx.touched))])
    entries = [entry for term, entry in _glossary_entries(ctx.glossary) if _mentions(source, term)]
    return "\n\n".join(entries) or "(none named — read glossary.md just-in-time when the rescan implicates a term)"


def _glossary_entries(text: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, list[str]]] = []
    term = ""
    body: list[str] = []
    for line in text.splitlines():
        m = re.match(r"- \*\*(.+?)\*\* — ", line)
        if m:
            if term:
                rows.append((term, body))
            term, body = m.group(1), [line]
        elif term:
            body.append(line)
    if term:
        rows.append((term, body))
    return [(term, "\n".join(lines).rstrip()) for term, lines in rows]


def _mentions(text: str, term: str) -> bool:
    return re.search(rf"(?<![0-9A-Za-z]){re.escape(term)}(?![0-9A-Za-z])", text, re.IGNORECASE) is not None


def _index(items: list[tuple[str, str]]) -> str:
    """A high-signal index of the capabilities not foregrounded — each one's name, vision line, and
    requirement titles: the whole-spec **map** the rescan reads to decide which full body to pull
    just-in-time from `spec/<name>.md` (where it already lives). The index, not the inlined bodies, is
    what the anti-myopia defense needs — every capability in view at ~5–10% of the bodies' cost."""
    out = []
    for n, t in items:
        m = re.search(r"<!--\s*vision:\s*(.*?)\s*-->", t)
        head = f"### capability: {n}" + (f" — {m.group(1).strip()}" if m else "")
        titles = [ln.split(":", 1)[1].strip() for ln in t.splitlines() if ln.startswith(spec.REQ)]
        out.append(head + "".join(f"\n  - {x}" for x in titles))
    return "\n\n".join(out)


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
    base = _head(fence)                                # the fork base — the fence HEAD before the worker builds
    transport = transport or worker_transport(fence)   # the live worker runs at its fence (step 5)
    obj = read(transport(prompt(node, ctx, root)), WORKER_SCHEMA)  # strict: a tagless reply surfaces, not a no-op (H3)
    report = obj["report"]
    refined = obj["delta"] or ctx.delta
    _record(fence, report, refined)                    # the worker's own commit, fenced
    return WorkerResult(report, refined, fence, _capture_code(fence, base), base=base)  # verified code, captured before teardown


def run(node: tree.Node, transport=None, root: str | None = None):
    """The whole crossing for one node: take it (it goes live), build it fenced, hand to the architect
    to coherence-check and archive, then tear the fence down — on *every* exit, not only the
    integrating one. The worker speaks only to the architect; what reaches the operator is its reply.

    Refusal is the steady-state path, not an edge: a folding-condition block, failed coherence, or a
    malformed reply returns not-done, and an error mid-build raises. On any of these the fence must not
    leak and the node must not strand in flight with no live worker. So the fence is torn down in a
    `finally`, a non-integrating crossing recovers the node to standing, and the error path recovers it
    too, then re-raises so the scheduler raises its own decision card."""
    if not _has_proposed_delta(node):
        card = _raise_missing_delta(node)
        return communication.Reply(say="", card=card)
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


def _has_proposed_delta(node: tree.Node) -> bool:
    return grill.entry_of(node) is not None


def _raise_missing_delta(node: tree.Node) -> tree.Node:
    existing = [c for c in tree.cards()
                if c.parent == node.id and c.kind == "decide"
                and "architect-proposed delta" in c.text]
    if existing:
        return existing[0]
    return tree.raise_card(
        "missing architect-proposed delta: this node carries no resolved propose product; "
        "propose one, abandon it, or change the ask",
        kind="decide", parent=node.id)


def _touched(handed: str, sp: spec.Spec) -> set[str]:
    """The capabilities a delta touches. An empty delta names no capability: the worker boundary
    refuses a node with no resolved propose product before dispatch, and a proposed trivial delta still
    builds without reviving the author-from-scratch fallback."""
    if not handed.strip():
        return set()
    return {op.capability for op in delta.parse(handed).ops}


def _cap_text(name: str, root: str | None) -> str:
    path = spec.cap_path(name, root)
    return open(path).read() if os.path.isfile(path) else ""


def _tree_path(node: tree.Node, base: str, tag: str = "") -> str:
    name = node.id + (f"-{tag}" if tag else "")
    return os.path.join(base, "work", "worktrees", name)


def _branch(node: tree.Node, tag: str = "") -> str:
    return f"worker/{node.id}" + (f"-{tag}" if tag else "")


def _head(fence: str) -> str:
    """The fence's HEAD before the worker builds — the **fork base** the gate and `_capture_code` use,
    robust to a self-committing worker (`spec/self-model.md`). Empty when the fence is not yet cut."""
    if not os.path.isdir(fence):
        return ""
    r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=fence, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def _capture_code(fence: str, base: str = "") -> dict[str, CodeFile]:
    """The engine code the worker built — per `engine/*.py` path, `(base, tip)` byte-images over the
    whole **fork-base→tip** range (`base`, else `HEAD~1`), so a self-committing worker's earlier commits
    cross too. Replayed onto main at fold, the base read for staleness; only `engine/*.py` crosses as
    code, never spec/channels/RESULT. A read of the fence, run unlocked — the verified bytes, not it."""
    ref = base or "HEAD~1"
    names = subprocess.run(["git", "diff", "--name-only", ref, "HEAD"], cwd=fence,
                           capture_output=True, text=True).stdout.split()
    code: dict[str, CodeFile] = {}
    for rel in names:
        if not (rel.startswith("engine/") and rel.endswith(".py")):
            continue
        tip_path = os.path.join(fence, rel)
        tip = open(tip_path, encoding="utf-8").read() if os.path.isfile(tip_path) else None
        shown = subprocess.run(["git", "show", f"{ref}:{rel}"], cwd=fence,
                               capture_output=True, text=True)
        base_bytes = shown.stdout if shown.returncode == 0 else None
        code[rel] = CodeFile(base_bytes, tip)
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
