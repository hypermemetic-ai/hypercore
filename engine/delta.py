"""The delta and the fold — how behavior change reaches the living spec.

A behavior-changing tree carries a delta (ADDED / MODIFIED / REMOVED / RENAMED
requirements); a trivial tree carries one with no ops and so says so. Folding a
tree applies its delta to `spec/` and commits, in one act: the spec never merges
unless the tree folds, and the tree never folds unless the delta merges. The
folding condition lives here — a missing delta or one that does not apply cleanly
to the current spec cannot fold — so drift is structurally impossible, not a thing
discipline must prevent.

On disk a delta is `delta.md` in a tree's folder:

    # delta — <subject>

    ## ADDED — <capability>
    ### Requirement: <name>
    <prose>
    #### Scenario: ...

    ## MODIFIED — <capability>
    ### Requirement: <name>
    ...

    ## REMOVED — <capability>
    ### Requirement: <name>

    ## RENAMED — <capability>
    ### Requirement: <old name>
    → <new name>

A delta with no `## VERB — capability` sections is trivial and applies nothing. An
ADDED requirement in a capability that does not yet exist *creates* that capability —
how the self-model grows a new top-level unit as the work reveals one (the spec's
own forecast; the worker capability is the first). MODIFIED, REMOVED, or RENAMED in
an absent capability is still a mismatch and cannot fold.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from . import channels, tree, spec

VERBS = ("ADDED", "MODIFIED", "REMOVED", "RENAMED")


class CannotFold(Exception):
    """The folding condition refused the fold; the spec is left untouched."""


@dataclass
class Op:
    verb: str
    capability: str
    requirement: spec.Requirement
    target: str = ""                 # RENAMED target title; empty for the other verbs


@dataclass
class Delta:
    subject: str = ""
    ops: list[Op] = field(default_factory=list)

    @property
    def trivial(self) -> bool:
        return not self.ops


# ── reading ──────────────────────────────────────────────────────────────────

def parse(text: str) -> Delta:
    subject, verb, cap, block = "", None, None, []
    ops: list[Op] = []

    def flush() -> None:
        if verb and cap and block:
            target = _rename_target(block) if verb == "RENAMED" else ""
            ops.append(Op(verb, cap, spec._req(block), target))
    for line in text.splitlines():
        if line.startswith("# delta"):
            subject = line[len("# delta"):].lstrip(" —-").strip()
        elif line.startswith("## "):
            flush()
            block = []
            head = line[3:]
            v, _, c = head.partition("—") if "—" in head else head.partition(" ")
            verb = v.strip().upper() if v.strip().upper() in VERBS else None
            cap = c.strip() or None
        elif line.startswith(spec.REQ):
            flush()
            block = [line]
        elif block:
            block.append(line)
    flush()
    return Delta(subject, ops)


# ── the folding condition ─────────────────────────────────────────────────────

def check(delta: Delta | None, sp: spec.Spec) -> str | None:
    """Why this delta cannot fold, or None when it folds clean.

    Renames are resolved before the other verbs within one delta, so a MODIFIED keyed on a
    post-rename title sees the retitled requirement. A re-applied RENAMED is clean when its old title
    is gone and its new title is already present; that is the idempotent retry after a crash, not a
    collision."""
    if delta is None:
        return "missing delta: a tree must carry a delta to fold"
    for cap_name in sorted({op.capability for op in delta.ops}):
        cap = sp.capability(cap_name)
        cap_ops = [op for op in _renames_first(delta.ops) if op.capability == cap_name]
        if cap is None:
            bad = next((op for op in cap_ops if op.verb != "ADDED"), None)
            if bad:
                return f"{bad.verb} in an absent capability: {cap_name!r}"
            continue
        blocks = {r.name: r.block for r in cap.requirements}
        for op in cap_ops:
            if op.verb not in VERBS:
                return f"unknown verb {op.verb!r}"
            n = op.requirement.name
            if op.verb == "RENAMED":
                if not op.target:
                    return f"RENAMED requirement has no target: {n!r}"
                old_exists, new_exists = n in blocks, op.target in blocks
                if old_exists and new_exists:
                    return f"RENAMED target already exists: {op.target!r}"
                if not old_exists:
                    if new_exists:
                        continue
                    return f"RENAMED requirement is absent: {n!r}"
                blocks[op.target] = _retitle(blocks.pop(n), op.target)
                continue
            existing = blocks.get(n)
            if op.verb == "ADDED" and existing is not None and existing.strip() != op.requirement.block.strip():
                return f"ADDED requirement already exists: {n!r}"
            if op.verb in ("MODIFIED", "REMOVED") and existing is None:
                return f"{op.verb} requirement is absent: {n!r}"
            if op.verb == "MODIFIED":
                blocks[n] = op.requirement.block
            elif op.verb == "REMOVED":
                blocks.pop(n, None)
            elif op.verb == "ADDED":
                blocks.setdefault(n, op.requirement.block)
    return None


def _renames_first(ops: list[Op]) -> list[Op]:
    return [op for op in ops if op.verb == "RENAMED"] + [op for op in ops if op.verb != "RENAMED"]


def _rename_target(block: list[str]) -> str:
    return next((line.strip()[1:].strip() for line in block[1:] if line.strip().startswith("→")), "")


def _retitle(block: str, target: str) -> str:
    lines = block.splitlines()
    if not lines:
        return f"{spec.REQ} {target}\n"
    lines[0] = f"{spec.REQ} {target}"
    return "\n".join(lines).rstrip() + "\n"




# ── the fold (applies the delta; atomic with the commit, both directions) ─────

@tree.serialized
def fold(delta: Delta | None, root: str | None = None, node=None, code=None) -> None:
    """Apply the delta to the living spec, **land the verified build's code**, archive the node, and
    commit — **one act, atomic in every direction** (spec.self-model). Raises CannotFold if a folding
    condition is not met; on refusal nothing lands and the tree is left untouched.

    The spec change *and* the node's archive land in **one commit** under the one held line, so the
    record never shows the spec merged without the node archived (or the reverse) — the H1 wedge, where
    a crash between two separate acts left the delta in the spec but the node un-archived and the retry
    hit a permanent CannotFold, cannot occur. The whole act is **idempotently retryable**: a crash
    after the on-disk write but before the commit leaves an already-applied delta, which `check`
    now reads as already-present (not a conflict), so the retry re-renders identically, moves the node,
    and commits once. Serialized on the one record: concurrent folds land one at a time, never
    interleaving their writes, while their builds ran in parallel. A trivial delta with a node
    still archives it (the fold of a no-op-delta tree).

    A **code-bearing** fold (`code` carries the worker's verified engine bytes, a `{path: CodeFile}`
    artifact captured at the hand-off) lands that code on main in this same act, so a code-bearing ask
    completes through the crossing without leaving main red or the node falsely archived. Three guards
    join the one held line, none of them a new commit or lock: a **staleness pre-check** refuses, before
    any write, a build whose engine paths main has moved under since the fence was cut; the verified tip
    bytes are **content-replayed** onto main beside the spec; and the touched capabilities are
    **re-verified on the merged tree** before the commit — a build red once merged rolls every write back
    and refuses, so green-in-fence can never mean red-on-main. A spec-only fold carries no code and runs
    none of these — its path is exactly as before."""
    sp = spec.read_spec(root)
    reason = check(delta, sp)
    if reason:
        raise CannotFold(reason)
    assert delta is not None  # check would have refused None

    base_dir = root or tree._root()
    touched = sorted({op.capability for op in delta.ops})

    def land() -> list[str]:
        # A code-bearing fold checks staleness first, under the held line, before any write: a build
        # whose engine paths main has moved under refuses to a decision rather than clobbering.
        if code:
            _staleness(code, base_dir)
        prior: dict[str, str | None] = {}                 # the pre-write image of every path, for rollback
        def write(path: str, content: str | None) -> None:
            prior.setdefault(path, _read_or_none(path))
            _restore(path, content)
        # the spec change
        for name in touched:
            existing = open(path).read() if os.path.isfile(path := spec.cap_path(name, root)) else _seed(name)
            write(path, _apply(existing, [o for o in delta.ops if o.capability == name]))
        # the verified build's code — content-replay of the fence-tip bytes onto main
        code_paths: list[str] = []
        for rel, cf in (code or {}).items():
            write(p := os.path.join(base_dir, rel), cf.tip)
            code_paths.append(p)
        # the keystone: re-verify the touched capabilities on the MERGED tree before the commit. A build
        # red once merged rolls back every write and refuses — nothing lands, the node recovers to a decision.
        if code:
            from . import scenario                         # lazy: scenario reads delta, so bind it at call time
            red = scenario.reverify(touched, base_dir)
            if red:
                for path, was in prior.items():
                    _restore(path, was)
                raise CannotFold(red)
        # The render step: every fold re-derives the static channels (skills, the agents file) from
        # the spec, so a committed artifact cannot drift from its source. Idempotent: an
        # unchanged source re-renders identically and re-staging no-ops, so a retry is safe.
        rendered = channels.materialize(root)
        paths = [spec.cap_path(n, root) for n in touched] + code_paths + rendered
        if node is not None:
            paths += tree.archive_in_place(node)      # the node's DONE write + folder move, same act
        return paths

    label = ", ".join(touched) or "channels"
    subject = delta.subject or (tree._subject(node.text) if node is not None else "delta")
    # `land` returns the exact paths it wrote (spec files, the replayed code, rendered channels, the
    # node's move endpoints); `transact` stages precisely those in the one held commit — atomic, all directions.
    tree.transact(land, None, f"fold: {subject} → {label}")


def _staleness(code, base_dir: str) -> None:
    """Refuse a code-bearing fold whose verified base no longer matches main — a concurrent fold moved an
    engine path under this build since its fence was cut, so its verified bytes would clobber the
    newer main. A path already at the tip bytes is an already-applied retry, not a collision (idempotent,
    H1). Read under the held line before any write, so the verdict is race-free and a stale build lands
    nothing, surfacing as a decision (re-cut off current main) rather than a silent overwrite."""
    for rel, cf in code.items():
        cur = _read_or_none(os.path.join(base_dir, rel))
        if cur == cf.tip:
            continue                                      # already applied — the idempotent retry, not stale
        if cur != cf.base:
            raise CannotFold(f"the verified build is stale: {rel} on main has moved since the fence was "
                             "cut — re-cut the build off current main")


def _read_or_none(path: str) -> str | None:
    return open(path, encoding="utf-8").read() if os.path.isfile(path) else None


def _restore(path: str, content: str | None) -> None:
    """Make `path` hold exactly `content`, or be absent when `content` is None — the one primitive the
    fold writes and rolls back through, so a write and its undo are the same operation in reverse."""
    if content is None:
        if os.path.isfile(path):
            os.remove(path)
    else:
        tree.atomic_write(path, content)


def _seed(name: str) -> str:
    """The base for a capability the fold is creating: only its name. The machine does
    not invent the rich prose of a hand-authored capability — the header states what it
    is and the delta's requirements carry the rest; the architecture review fills it in."""
    return f"# {name}\n"


def _apply(text: str, ops: list[Op]) -> str:
    """Splice one capability file: preamble kept, requirement blocks edited by name."""
    lines = text.splitlines()
    first = next((i for i, ln in enumerate(lines) if ln.startswith(spec.REQ)), len(lines))
    preamble = "\n".join(lines[:first]).rstrip()
    reqs = spec._requirements(text)
    blocks = {r.name: r.block for r in reqs}
    order = [r.name for r in reqs]
    for op in _renames_first(ops):
        n = op.requirement.name
        if op.verb == "RENAMED":
            if n in blocks and op.target not in blocks:
                blocks[op.target] = _retitle(blocks.pop(n), op.target)
                order = [op.target if x == n else x for x in order]
            continue
        if op.verb == "REMOVED":
            blocks.pop(n, None)
            order = [x for x in order if x != n]
        else:  # ADDED or MODIFIED
            if n not in blocks:
                order.append(n)
            blocks[n] = op.requirement.block
    body = "\n".join(blocks[n].rstrip() + "\n" for n in order)
    return preamble + "\n\n" + body
