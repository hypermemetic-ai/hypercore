"""The folding conditions — the engineering standards made structural.

The standards that keep the model from drifting into a god-file of tangled code
bite only because each is a *folding condition* in hypercore's
existing sense: the thing that lets a tree fold. Advice can be ignored; a folding
condition cannot. This module is the gate, run at the archive stage before the merge.

Two conditions are **non-negotiable facts** — they refuse the fold automatically, because
there is nothing to judge:

- **the spec delta applies** — the delta the tree carries lands cleanly on the
  current spec. (Owned by the self-model; re-checked here so the gate gives one verdict.)
- **the scenario gate** — a behavior change folds only when the **architect-authored scenarios**
  of the capabilities it touches go red→green: failing at the fork base (the behavior was not yet
  built), passing at the tip. The oracle is the self-model's own account of the behavior, run by the
  side that does not build it — not a loop the worker records about its own work. The mechanism lives
  in `scenario`; this module asks it for a verdict. A correct narrative with no executed scenario is
  the failure this kills.

The third condition is a **judgment**, and so it is shaped differently (re-grounded in
Ousterhout — `spec/depth.md`):

- **depth** — the criterion is a *deep module*: a lot of behavior behind a small interface.
  Length is not the criterion; it is one **signal** of it, kept for a reason Ousterhout
  doesn't address and that survives his objection — every line is context an agent must
  load, so length is a fair proxy for a module's **context cost**. A source file the tree
  created or grew past the length signal does **not** auto-refuse (length is a signal, not a
  verdict). It **raises a decision** — re-cut / deepen / accept-with-reason — which
  `communication.integrate` puts on the operator's queue. The fold is held until that decision
  is settled; it is never silently refused and never silently passed.

**There is no second, higher length ceiling that auto-refuses.** A ceiling at
any number would be the very thing this re-grounding removes — a number standing in for the
judgment of depth — and would force back the escape hatch it deletes. Length raises a
decision across its whole range; judgment and the operator carry it. The anti-dilution
guarantee still holds: over-signal material is *un-foldable* until the operator settles the
decision — stronger than the old coincidental-acceptance escape, not weaker.

The model-driven red-flag **module depth judgment** (is it actually shallow?) is the
architecture review's standing job to grow and is not yet built; this slice ships
the mechanical scaffold — length raises the decision, the operator judges depth — honestly.
"""
from __future__ import annotations

import os
import re
import subprocess

from . import delta, spec
from .record import atomic_write, transact

# The length signal. Past this many lines a touched source file raises a
# decision — not a refusal. A starting value to tune, not a law: the prior epoch's
# 6,348-line god-file (the `window.py` torn down 2026-06-20, not this repo's small one) was
# ~16× this — the kind of file it exists to catch early. Keyed to length because length is what a
# file costs the worker's window, whatever each line means — its context cost, not its depth.
SIGNAL = 400

# The materiality margin on an accepted length. Accepting a length signal is bounded
# to the length it was accepted at — not granted forever — and the signal re-fires only when the
# file grows *materially* past that bar, so a one-line edit past it does not re-open a settled
# decision. SLACK is that margin, proportional to the accepted length: renewed growth past
# `bar + bar·SLACK` re-opens the decision; a stable or shrinking file stays cleared. A
# starting value to tune, like the signal itself.
SLACK = 0.1


def unmet(result, root: str | None = None, node=None) -> str | None:
    """The first folding condition this tree's material fails to meet, or None when all are
    met. `result` is the worker's hand-off (its delta, its worktree); `node` is its tree (so an
    authored record's reachability — a design decision on the node — can be read). The delta applies, the
    depth signal, and the **authored** provenance trails are the **material** conditions, judged
    in-process; the **derived** provenance trail is the behavioral proof — the architect-authored
    scenarios of the touched capabilities re-derived red→green in the fence (`provenance.derived` over
    the scenario gate). The depth condition returns a *decision* (re-cut / deepen / accept), which the
    architect raises on the operator's queue; the others refuse with a flat reason."""
    from . import provenance                            # lazy: provenance reads conditions, so bind it at call time
    return material_unmet(result, root, node) or provenance.derived(result, root)


def material_unmet(result, root: str | None = None, node=None) -> str | None:
    """The **material** folding conditions — the delta applies, the depth signal is met, and the
    **authored** records' provenance trail is reachable — judged in-process over a result's own delta,
    worktree, and node, without the base/tip re-derivation. This is the seam the scenario binding asserts
    against: a capability's `gate`/`spec` scenario reads the gate's verdict on planted material here, so a
    scenario can never recurse into the scenario gate that runs scenarios. `unmet` is this plus the
    derived (re-derivation) trail."""
    from . import provenance
    d = delta.parse(result.delta)
    sp = spec.read_spec(root)
    return _delta(d, sp) or _depth(result, root) or provenance.reachability(result, root, node)


def _delta(d: delta.Delta, sp: spec.Spec) -> str | None:
    reason = delta.check(d, sp)
    return f"the spec delta does not apply: {reason}" if reason else None


def _depth(result, root: str | None) -> str | None:
    """Depth is the criterion; length is its signal. A source file this tree created or
    grew past the length signal, with no accepted-length record clearing it *at a length it is still
    within*, raises a decision — re-cut / deepen / accept-with-reason — never a silent
    refusal and never a silent pass. Scoped to what this tree touched — the .py files in its own
    commit — so a tree is judged on the depth of what *it* built, not a sibling's. Length never
    auto-refuses (F2): a long file is either judged deep (fine — length was only context-cost
    signal) or raises this decision for the operator to settle. Acceptance is bounded:
    a file that has grown materially past the length an accepted-length record accepted it at re-opens
    the decision, so an old acceptance cannot silence unbounded later growth."""
    tree = result.worktree
    for rel in _touched_py(tree):
        path = os.path.join(tree, rel)
        if not os.path.isfile(path):
            continue                        # removed by the tree — frees context, never spends it
        n = sum(1 for _ in open(path, encoding="utf-8", errors="ignore"))
        if n > SIGNAL and not accepted(rel, n, root):
            return _depth_decision(rel, n, root)
    return None


def _depth_decision(rel: str, n: int, root: str | None) -> str:
    """The decision the gate raises on `rel` at `n` lines — phrased for the two cases the
    operator must tell apart: a file never accepted past the signal, and a file whose earlier
    acceptance the new length has *outgrown* (the ratchet). Both name re-cut / deepen /
    accept and the exact accepted-length record to write, so the architect can settle it in one step."""
    bar = accepted_at(rel, root)
    if bar is not None:
        return (f"decision — {rel} is {n} lines, materially past the {bar}-line bar an "
                f"accepted-length record accepted it at — the acceptance is stale (it ratchets, it does "
                f"not silence later growth). Re-cut it, deepen it, "
                f"or renew the acceptance at the new length: `accepted: {rel} @{n} "
                f"— <reason>`. Length is a context-cost signal, not a verdict on depth; the depth "
                f"judgment is the operator's.")
    return (f"decision — {rel} is {n} lines, past the {SIGNAL}-line length signal — re-cut "
            f"it, deepen it, or record an accepted-length record at this length: "
            f"`accepted: {rel} @{n} — <reason>`. Length is a "
            f"context-cost signal, not a verdict on depth; the depth judgment is the operator's.")


def _touched_py(tree: str) -> list[str]:
    """The .py files this tree's commit added or grew — its own material, not the whole tree.
    The worker hands back one commit (`worker._record`); its diff against the fork is exactly
    what the tree built."""
    out = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], cwd=tree,
                         capture_output=True, text=True).stdout
    return [ln for ln in out.split() if ln.endswith(".py")]


def accepted(rel: str, lines: int, root: str | None) -> bool:
    """True when an **accepted-length record** accepts this exact file at a length it is still
    within. Acceptance is **bounded, not permanent**: an
    accepted-length record records the file accepted *at a stated length* and clears the gate only while
    the file stays within that bar plus the materiality margin (`SLACK`). Renewed growth
    materially past the accepted length re-opens the decision; a stable or shrinking file
    stays cleared — the bar lives in the record, so a shrink never lowers it and a regrow back to
    the old size never re-nags. `lines` is the file's current length. Public because the
    architecture review (`review`) consults the same record — one criterion, the per-tree gate
    and the standing scan. `rel` is the file's path relative to the repo root (e.g.
    `engine/foo.py`)."""
    bar = accepted_at(rel, root)
    return bar is not None and lines <= bar + round(bar * SLACK)


def accepted_at(rel: str, root: str | None) -> int | None:
    """The length an accepted-length record records this file accepted at — the **ratchet
    bar** — or None when none accepts it. The record is a line in the durable store (`_ledger`):

        accepted: <repo-relative path> @<N> — <reason>

    `<N>` is the line count the operator accepted; the acceptance is bounded to it (`accepted`).
    The gate matches the *path*, not a basename appearing anywhere in prose, so a coincidental
    mention grants no exception (the slice-7 closure) — and a record with no `@<N>`
    is an *incomplete* acceptance that names no bound, so it does not clear the gate:
    the exception is the decision *at a stated size*, not the spelling. When several records name
    the same file — each re-acceptance as the file grows writes a new one — the **highest** bar
    governs: the ratchet only rises, so the most permissive recorded acceptance is the live one."""
    f = _ledger(root)
    if not os.path.isfile(f):
        return None
    want = rel.replace(os.sep, "/")
    bars = [rec[1] for line in open(f, encoding="utf-8", errors="ignore")
            if (rec := _depth_record(line)) and rec[0] == want]
    return max(bars) if bars else None


def accept(rel: str, n: int, reason: str, root: str | None = None) -> bool:
    """Record `rel` accepted at `n` lines — the settle side of the length decision the gate raises,
    and the **one writer** of the accepted-length record. Ratcheting and idempotent: a no-op when the
    file is already accepted at `n` or higher (the bar only rises, so re-accepting at the same or a
    lower length writes nothing), else it appends one parseable `accepted: <rel> @<n> — <reason>` line
    to the durable store under the single-writer line and commits it. Returns whether a record was
    written. The store's location lives behind this seam and `accepted_at`, so a caller — the architect
    settling the decision today, the operator's acceptance card (`card-kind`) tomorrow — names only the
    file, the length, and the reason, never where the record sleeps."""
    rel = rel.replace(os.sep, "/")
    bar = accepted_at(rel, root)
    if bar is not None and bar >= n:
        return False
    f = _ledger(root)
    line = f"accepted: {rel} @{n} — {reason.strip()}\n"
    def write() -> list[str]:
        prior = open(f, encoding="utf-8").read() if os.path.isfile(f) else ""
        atomic_write(f, prior + line)
        return [f]
    transact(write, [f], f"accept length: {rel} @{n}")
    return True


def length_decision(text: str) -> tuple[str, int] | None:
    """Read a length decision's `accepted: <rel> @<N>` template back to `(rel, length)`, or None when
    the card is not a length acceptance. The depth gate emits that exact template in the decision it
    raises (`_depth_decision`), so settling that decision with approve can write the record the
    template names — the queue's accept-the-length action over `accept`, the producer that gives the
    writer seam its caller."""
    m = re.search(r"accepted:\s*([^\s`]+)\s+@(\d+)", text)
    return (m.group(1).replace(os.sep, "/"), int(m.group(2))) if m else None


def accept_length(text: str, root: str | None = None) -> bool:
    """Settle a length decision by recording its accepted length — the queue's accept-the-length act.
    A no-op (returns False) on a card that is not a length acceptance, so the settle path can call it
    unconditionally before clearing any card. Returns whether a record was written (True only when the
    card named a length and the bar rose)."""
    rn = length_decision(text)
    return bool(rn) and accept(rn[0], rn[1], "accepted by the operator from the queue", root)


def _ledger(root: str | None) -> str:
    """The accepted-length record's durable home: `engine/accepted-lengths.md`, beside its only
    reader (this gate) and the standing review that shares it. It is the system's one piece of
    **authored, mutable** state — live gate-state that must outlive the work that grew a file past the
    length signal, so it cannot ride a node (a node archives with its work, intent §50/§116) and is not
    re-derived on fold like the channels. Reached only through `accepted_at` and `accept`, so the
    location is a hidden decision the rest of the system never names."""
    return os.path.join(os.path.dirname(spec.spec_dir(root)), "engine", "accepted-lengths.md")


def working_accepted(root: str | None) -> set[tuple[str, int]]:
    """Every `(path, @N)` accepted-length record in the **working-tree** ledger — what the depth gate
    reads. The provenance gate diffs this against the committed ledger to find a record hand-appended
    this fold (a working-tree line with no commit), the cooperating short-circuit it refuses."""
    f = _ledger(root)
    return _ledger_records(open(f, encoding="utf-8", errors="ignore").read()) if os.path.isfile(f) else set()


def committed_accepted(root: str | None) -> set[tuple[str, int]]:
    """Every `(path, @N)` accepted-length record **committed** to the ledger — the durable artifact the
    one accept seam leaves (it writes and commits in one held act). A record present here either went
    through the seam or was folded before the gate (grandfathered); a working-tree record absent here is
    the un-committed forge with no trail."""
    return _ledger_records(_committed_ledger(root))


def _ledger_records(text: str) -> set[tuple[str, int]]:
    return {rec for line in text.splitlines() if (rec := _depth_record(line))}


def _committed_ledger(root: str | None) -> str:
    """The committed ledger's text at HEAD, or empty when none is committed — read through git so the
    durable record is what the seam's commit left, never the working tree the forge edits."""
    base = os.path.dirname(spec.spec_dir(root))
    r = subprocess.run(["git", "show", "HEAD:engine/accepted-lengths.md"], cwd=base,
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def _depth_record(line: str) -> tuple[str, int] | None:
    """Parse one `accepted: <path> @<N> — …` line to `(path, accepted-length)`, or
    None. A line is an accepted-length record only with the exact `accepted:` prefix and an `@<N>`
    token naming an integer length; a record with no `@<N>`, or prose, is not a
    pass — the acceptance must name the length it is bounded to."""
    text = line.strip()
    if not text.lower().startswith("accepted:"):
        return None
    parts = text.split(":", 1)[1].split()
    if len(parts) < 2:
        return None
    path = parts[0].rstrip(",").replace(os.sep, "/")
    for tok in parts[1:]:
        if (n := _accepted_length(tok)) is not None:
            return (path, n)
    return None


def _accepted_length(token: str) -> int | None:
    """`@<N>` → N (the bounded length); a token with no `@<N>` or anything else → None.
    Tolerant of trailing punctuation (`@450,`) and case."""
    t = token.strip(",.—-").lower()
    digits = t[1:] if t.startswith("@") else ""
    return int(digits) if digits.isdigit() else None
