"""Design-it-twice — the judgment use of the worktree concurrency (ADR 0007).

The worktree fence is hypercore's concurrency model. Slice 4 used it for *throughput*: one
worker per node, fenced from its siblings. This is the second use the model already affords —
**design quality**. For an interface decision the architect judges load-bearing, the first
shape committed is rarely the deepest; so the decision is **designed twice** — several
candidates, each in its own fence, each briefed to design the *same* interface radically
differently — and the architect picks or hybridizes on **depth, locality, and seam placement**.
This is hypercore's existing isolation applied to the one place first-draft commitment hurts
most: the shape of a deep module.

Four things define it, and each is structural:

- **The candidates are genuinely different, and isolated.** One per brief (minimize the
  interface / maximize flexibility / optimize the common caller / ports-and-adapters), each in
  its own fence (`worker.worktree`, tagged per candidate). They never see each other; several
  shapes advance one decision at once, exactly as several workers advance the graph at once.

- **The candidates *design*, they do not implement.** Each produces an interface, what it
  hides, where the seam falls, and the deletion-test argument for its depth — the properties
  the comparison turns on. Building each one out would throw most of the work away; depth,
  locality, and seam are judgable from the design itself. The winner carries forward as the
  contract for one ordinary `apply`.

- **The selection is machine-side — the architect's design judgment (operator-ratified, ADR
  0007).** The architect compares on depth/locality/seam, picks or hybridizes, and records the
  pick as a structured **design-decision** ADR — a load-bearing interface choice is hard to
  reverse, so it is ADR-worthy. The operator's trust anchor is the contract, not the
  machine-side design (ADR 0007), so the pick does not spend the operator's go.

- **A stake-bearing difference still reaches the operator.** When the comparison reveals a
  difference the operator has a stake in — operator-visible behavior, hard to reverse, real
  cost — it re-enters grilling as a card (the standing-guard floor). Only that
  architect-authored stake crosses; the candidate designs and the reasoning stay machine-side.

The contest is driven by the same transport as the rest of the system — `claude -p` live, a
scripted fake in the acceptance check — so it runs deterministically under the harness. The
parallelism is the orchestration; the fences are what make it safe, and they already exist.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from . import graph, grill, spec, worker
from .transport import call, parse

# The four briefs (ADR 0007): each pushes a candidate toward a radically different
# shape, so the contest spans real alternatives rather than minor variations of one instinct.
BRIEFS = [
    ("minimal", "Minimize the interface — the smallest surface the callers can live with; "
                "pull every bit of complexity down inside the module."),
    ("flexible", "Maximize flexibility — make the likely future variations cheap to reach, "
                 "even at some cost to the interface."),
    ("caller", "Optimize the common caller — shape the interface around the one call site that "
               "dominates and make its path trivial."),
    ("ports", "Ports-and-adapters — isolate the cross-seam dependency behind an adapter so the "
              "core never names it."),
]

CANDIDATE = (
    "You are a hypercore worker designing ONE interface for a load-bearing decision — not "
    "implementing it. Commit radically to the brief below. Produce the interface (the small "
    "surface its callers see), what it hides behind that surface, where the seam falls and "
    "what varies across it, and the deletion-test argument for its depth. Write for the "
    "machine. Reply with ONLY a JSON object:\n"
    '{"interface": <the proposed interface — signatures, one line each>, '
    '"hides": <the complexity it pulls down out of sight>, '
    '"seam": <where the seam falls and what varies across it>, '
    '"depth": <the deletion-test / depth argument for this shape>}'
)

SELECT = (
    "You are hypercore's architect, holding design judgment over a design-it-twice contest. "
    "The candidate interfaces below each realize the same load-bearing decision under a "
    "different brief. Compare them on DEPTH (the most behavior behind the smallest interface), "
    "LOCALITY (the change stays where it belongs), and SEAM PLACEMENT (the seam falls where "
    "something real varies). Pick one or hybridize, with a strong recommendation and your "
    "reasoning. This is machine-side design judgment, recorded as an ADR — it reaches the "
    "operator ONLY if the comparison reveals a difference the operator has a stake in "
    "(operator-visible behavior, hard to reverse, or real cost). Reply with ONLY a JSON "
    "object:\n"
    '{"chosen": <the brief you pick, or "hybrid">, '
    '"hybrid": <true if you synthesized across candidates>, '
    '"reasoning": <why this interface is deepest — the comparison on depth/locality/seam>, '
    '"comparison": {<brief>: <its note on depth/locality/seam>, ...}, '
    '"stake": <the stake-bearing difference to take to the operator, authored for them, '
    'or null>}'
)


@dataclass
class Candidate:
    """One shape in the contest: the brief it was built to, the fence it designed in, and its
    machine-facing design. Nothing of this is operator-facing — it lives in the fence and the
    ADR, never on a card."""
    brief: str
    worktree: str
    design: dict                                   # {interface, hides, seam, depth}


@dataclass
class Selection:
    """The architect's machine-side pick. `reasoning` and `comparison` are the ADR's body;
    `stake`, when set, is the one architect-authored line that crosses to the operator, and
    `card` is the decision it raised (the standing-guard floor)."""
    chosen: str                                    # the winning brief, or "hybrid"
    hybrid: bool = False
    reasoning: str = ""
    comparison: dict = field(default_factory=dict)
    stake: str | None = None
    candidates: list[Candidate] = field(default_factory=list)
    card: graph.Node | None = None


# ── the contest: several candidates, each fenced, each designing the one decision ──

def contest(node: graph.Node, briefs=None, transport=None,
            root: str | None = None) -> list[Candidate]:
    """Design the decision several ways at once, each in its own fence: one candidate per
    brief, each producing a design (not an implementation) for the same interface, isolated
    from the others exactly as concurrent workers are isolated."""
    transport = transport or call
    out: list[Candidate] = []
    for name, instruction in (briefs or BRIEFS):
        tree = worker.worktree(node, root, tag=name)
        design = parse(transport(_candidate_prompt(node, instruction)))
        _record_design(tree, name, instruction, design)
        out.append(Candidate(name, tree, design))
    return out


def select(node: graph.Node, candidates: list[Candidate], transport=None) -> Selection:
    """The architect compares the candidates on depth/locality/seam and picks or hybridizes —
    machine-side design judgment. The pick, the reasoning, and any stake-bearing difference
    come back; the architect authors the stake for the operator, never the raw designs."""
    transport = transport or call
    v = parse(transport(_select_prompt(node, candidates)))
    chosen = (v.get("chosen") or "").strip() or (candidates[0].brief if candidates else "")
    return Selection(
        chosen=chosen,
        hybrid=bool(v.get("hybrid")),
        reasoning=(v.get("reasoning") or "").strip(),
        comparison=v.get("comparison") if isinstance(v.get("comparison"), dict) else {},
        stake=(str(v["stake"]).strip() if v.get("stake") else None),
        candidates=candidates,
    )


def record(node: graph.Node, selection: Selection, root: str | None = None) -> str:
    """Record the pick as a structured design-decision ADR — the machine-side home of a
    load-bearing interface choice (hard to reverse → ADR-worthy). The parseable line

        design-decision: <subject> → <chosen> — <reason>

    names the decision the same way the depth-decision names a file, so a future scan can read
    the pick rather than re-derive it. Returns the ADR's path."""
    d = os.path.join(spec.spec_dir(root), "decisions")
    os.makedirs(d, exist_ok=True)
    num = _next_adr(d)
    subject = graph._subject(node.text)
    path = os.path.join(d, f"{num:04d}-design-{_slug(subject)}.md")
    briefs = ", ".join(c.brief for c in selection.candidates)
    grounds = "\n".join(f"- **{b}**: {note}" for b, note in selection.comparison.items())
    graph.atomic_write(path,
        f"# ADR {num:04d} — design-it-twice: {subject}\n\n"
        "Status: machine-owned, awaiting ratification. [machine]\n\n"
        "## Context\n\n"
        f"A load-bearing interface for {subject!r} was designed twice — candidates "
        f"{briefs}, each fenced, each built to a different brief — and compared on depth, "
        "locality, and seam placement (ADR 0007).\n\n"
        "## Decision\n\n"
        f"design-decision: {subject} → {selection.chosen} — {selection.reasoning}\n\n"
        "## Grounds\n\n"
        f"{grounds or '- (the comparison is recorded above)'}\n")
    graph.commit([path], f"design-it-twice: {subject} → {selection.chosen}")
    return path


def escalate(node: graph.Node, selection: Selection) -> graph.Node:
    """A stake-bearing difference re-enters grilling: a decision card on the operator's queue,
    parented to the decision node (the standing-guard floor). Only the architect-authored
    stake crosses — the candidate designs and the reasoning stay machine-side, in the ADR."""
    return graph.raise_card(selection.stake, kind="decide", parent=node.id)


def design_twice(node: graph.Node, briefs=None, transport=None,
                 root: str | None = None) -> Selection:
    """The whole contest behind one call: design the interface several ways in isolation, let
    the architect pick or hybridize on depth/locality/seam, record the pick as an ADR, and —
    only on a stake-bearing difference — raise it to the operator. The candidate fences are
    scratch, torn down once the design is recorded; the winning design carries forward as the
    contract for one ordinary `apply`."""
    candidates = contest(node, briefs, transport, root)
    selection = select(node, candidates, transport)
    record(node, selection, root)
    if selection.stake:
        selection.card = escalate(node, selection)
    for c in candidates:
        worker.teardown(node, root, tag=c.brief)
    return selection


# ── internals ────────────────────────────────────────────────────────────────

def _candidate_prompt(node: graph.Node, instruction: str) -> str:
    return (f"{CANDIDATE}\n\nThe interface decision:\n{grill.contract_of(node) or node.text}\n\n"
            f"Your brief — design radically to it:\n{instruction}\n\n"
            "Reply with the JSON object now.")


def _select_prompt(node: graph.Node, candidates: list[Candidate]) -> str:
    shown = "\n\n".join(
        f"### candidate: {c.brief}\n"
        f"- interface: {c.design.get('interface', '')}\n"
        f"- hides: {c.design.get('hides', '')}\n"
        f"- seam: {c.design.get('seam', '')}\n"
        f"- depth: {c.design.get('depth', '')}"
        for c in candidates)
    return (f"{SELECT}\n\nThe interface decision:\n{grill.contract_of(node) or node.text}\n\n"
            f"The candidate designs:\n{shown}\n\nReply with the JSON object now.")


def _record_design(tree: str, name: str, instruction: str, design: dict) -> None:
    """The candidate commits its design inside its own fence — proof each candidate runs in
    isolation, its material reaching the record on its own branch, fenced from its siblings."""
    graph.atomic_write(os.path.join(tree, "DESIGN.md"),
        f"# candidate design — {name}\n\n## brief\n{instruction}\n\n"
        f"## interface\n{design.get('interface', '')}\n\n## hides\n{design.get('hides', '')}\n\n"
        f"## seam\n{design.get('seam', '')}\n\n## depth\n{design.get('depth', '')}\n")
    worker.commit_tree(tree, f"candidate: {name} design")


def _next_adr(d: str) -> int:
    nums = [int(n[:4]) for n in os.listdir(d) if n[:4].isdigit() and n.endswith(".md")]
    return (max(nums) + 1) if nums else 1


def _slug(text: str) -> str:
    return "-".join("".join(c if c.isalnum() else " " for c in text.lower()).split())[:40]
