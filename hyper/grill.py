"""Intent extraction by grilling — the floor, the one-at-a-time interview, the gate.

Before an ask that opens real choices becomes work, the conversationalist runs a
grilling pass. It resolves every decision it can from the living spec and intent,
and surfaces only the residue — the decisions the operator has a stake in — as
questions on the queue, **one at a time**, each carrying the machine's *lean* (its
recommended answer) and the one thing that would *flip* it. An ask whose every
decision is already determined by intent, the spec, or an ADR is **below the floor**
and files straight to work, ungrilled.

A finished pass yields the **operator-view entry** — the contract the result is
later checked against — and the **spec delta** the change will realize. Work MUST
NOT spawn until that entry is ratified; ratifying it is the operator's informed go.

The pass is durable on the graph, not in the throwaway thread: the held ask
(GRILLING), its question children surfaced one at a time (AWAITING / PENDING), and
the view-entry card. So a pass survives the operator leaving and coming back — the
next episode reads it off the graph.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import conversation, graph, spec

FLOOR = (
    "You are hypercore's conversationalist running a grilling pass on an ask before "
    "it becomes work. Resolve every decision you can from the living spec and intent; "
    "put to the operator ONLY the decisions they have a stake in — ones that change "
    "operator-visible behavior, are hard to reverse, or commit real cost. Err toward "
    "asking when unsure: a wrongly-asked question is cheap, a wrongly-skipped one bites "
    "later. Ask in dependency order. Each question carries your recommended answer "
    "(lean) and the one thing that would flip it (flip). If every decision the work "
    "needs is already determined, return no questions. Reply with ONLY a JSON object:\n"
    '{"questions": [{"q": <the question>, "lean": <your recommended answer>, '
    '"flip": <the one thing that would change it>}, ...]}'
)

PRODUCTS = (
    "You are hypercore's conversationalist. The grilling pass is resolved. Produce two "
    "things. (1) entry — the operator-view contract: one plain paragraph stating what "
    "this ask will become, the thing its result is later validated against. (2) delta — "
    "the spec delta the change realizes, markdown with `## ADDED|MODIFIED|REMOVED — "
    "<capability>` sections over `### Requirement: <name>` blocks (each with at least "
    "one `#### Scenario:` line), against the existing capabilities. Reply with ONLY a "
    'JSON object {"entry": <the contract>, "delta": <the spec-delta markdown>}.'
)


@dataclass
class Question:
    text: str
    lean: str
    flip: str


# ── the pass ─────────────────────────────────────────────────────────────────

def consider(ask: str, transport=None) -> tuple[graph.Node, list[graph.Node]]:
    """Run the floor on a filed ask. Below it: file standing work as before, no
    questions. Above it: hold the ask and surface its first question on the queue."""
    transport = transport or conversation._claude
    questions = floor(ask, transport)
    if not questions:
        return graph.file_intent(ask), []
    held = graph.hold(ask)
    nodes = [graph.question(held.id, _q_text(q), awaiting=(i == 0))
             for i, q in enumerate(questions)]
    return held, nodes


def floor(ask: str, transport=None) -> list[Question]:
    """The residual stake-bearing decisions — the questions the operator must answer
    once the machine has resolved all it can. Empty means the ask is below the floor."""
    transport = transport or conversation._claude
    raw = transport(f"{FLOOR}\n\nThe living spec:\n{_digest()}\n\nThe ask: {ask}\n\n"
                    "Reply with the JSON object now.")
    obj = conversation._parse(raw)
    return [Question(q.get("q", ""), q.get("lean", ""), q.get("flip", ""))
            for q in (obj.get("questions") or []) if q.get("q")]


def advance(question: graph.Node, answer: str, transport=None) -> graph.Node:
    """Resolve one question with the operator's answer and surface the next, or — when
    the last is answered — produce the contract + delta and raise the view-entry card."""
    transport = transport or conversation._claude
    graph.resolve(question, answer)
    pending = [n for n in graph.children(question.parent) if n.state == graph.PENDING]
    if pending:
        return graph.surface(min(pending, key=lambda n: n.created))
    ask = graph.find(question.parent)
    entry, delta_text = products(ask.text, _answers(ask.id), transport)
    body = entry + (f"\n\ndelta:\n{delta_text}" if delta_text else "")
    return graph.raise_card(body, kind="decide", parent=ask.id)


def ratify(entry: graph.Node) -> graph.Node:
    """The view entry approved: the contract is endorsed and the held ask spawns as
    standing work. The gate opens here and only here."""
    graph.approve(entry)
    return graph.spawn(graph.find(entry.parent))


def products(ask: str, qa: list[tuple[str, str]], transport=None) -> tuple[str, str]:
    """The two machine-authored products of a folded pass: the operator-facing contract
    and the machine-side spec delta the change will realize."""
    transport = transport or conversation._claude
    answers = "\n".join(f"- {q}: {a}" for q, a in qa) or "- (none)"
    raw = transport(f"{PRODUCTS}\n\nThe ask: {ask}\n\nResolved:\n{answers}\n\n"
                    "Reply with the JSON object now.")
    obj = conversation._parse(raw)
    return obj.get("entry", "").strip(), obj.get("delta", "").strip()


# ── reading a pass's nodes (the on-disk shape lives here) ────────────────────

def is_question(node: graph.Node) -> bool:
    return bool(node.parent) and node.kind == "ask"


def is_entry(node: graph.Node) -> bool:
    return bool(node.parent) and node.kind == "decide"


def lean_of(node: graph.Node) -> str:
    return _field(node.text, "lean")


def flip_of(node: graph.Node) -> str:
    return _field(node.text, "flip")


def question_of(node: graph.Node) -> str:
    return node.text.splitlines()[0] if node.text.strip() else ""


def contract(node: graph.Node) -> str:
    return node.text.split("\ndelta:\n", 1)[0].strip()


def delta_of(node: graph.Node) -> str:
    parts = node.text.split("\ndelta:\n", 1)
    return parts[1].strip() if len(parts) == 2 else ""


def entry_of(ask: graph.Node) -> graph.Node | None:
    """The view entry hung off a spawned ask — the propose-stage product a worker reads
    for its handed delta, and the conversationalist later checks the result against."""
    return next((c for c in graph.children(ask.id) if is_entry(c)), None)


def contract_of(ask: graph.Node) -> str:
    entry = entry_of(ask)
    return contract(entry) if entry else ""


# ── internals ────────────────────────────────────────────────────────────────

def _q_text(q: Question) -> str:
    return f"{q.text}\nlean: {q.lean}\nflip: {q.flip}"


def _answers(ask_id: str) -> list[tuple[str, str]]:
    out = []
    for n in sorted(graph.children(ask_id), key=lambda n: n.created):
        a = _field(n.text, "answered")
        if n.kind == "ask" and a:
            out.append((question_of(n), a))
    return out


def _field(text: str, name: str) -> str:
    for line in text.splitlines():
        if line.startswith(name + ":"):
            return line.split(":", 1)[1].strip()
    return ""


def _digest() -> str:
    return "\n".join(
        f"- {c.name}: {', '.join(r.name for r in c.requirements)}"
        for c in spec.read_spec().capabilities
    ) or "(empty)"
