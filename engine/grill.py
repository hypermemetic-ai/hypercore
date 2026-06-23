"""Intent extraction by grilling — the floor, the one-at-a-time interview, the gate.

Before an ask that opens real choices becomes work, the architect runs a grilling pass. It
resolves every decision it can from the living spec and intent, and surfaces only the residue —
the decisions the operator has a stake in — as questions on the queue, **one at a time**, each
carrying the machine's *lean* and the one thing that would *flip* it. An ask whose every decision
is already determined files straight to work, ungrilled.

A finished pass yields the **view entry** — the contract the result is later checked against — and
the **spec delta** the change will realize. Work does not spawn until the entry is ratified.

Design B (ADR 0011): the pass is durable **within its tree's folder**, in `grilling.md`, not as a
scatter of question/entry node files. The held tree itself sits on the queue (state AWAITING) and
*is* the card; these predicates read its `grilling.md` to tell what the card currently shows — a
surfaced question, or the resolved contract awaiting ratification. So the queue stays a computed
view (L110) and the tree stays the on-disk unit (L112), while a half-finished pass survives a
session boundary — the next episode reads it off the folder.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from . import tree, spec
from .transport import call, parse

FLOOR = (
    "You are hypercore's architect running a grilling pass on an ask before "
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
    "You are hypercore's architect. The grilling pass is resolved. Produce two "
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


@dataclass
class _Pass:
    """The grilling pass, the durable content of a held tree's grilling.md."""
    surfaced: int                 # index of the question currently on the queue
    questions: list[dict]         # each {q, lean, flip, answer}; answer "" until resolved
    contract: str                 # the view-entry, produced once every question is answered
    delta: str                    # the spec delta the change will realize


# ── the pass ─────────────────────────────────────────────────────────────────

def consider(ask: str, transport=None) -> tuple[tree.Node, list[Question]]:
    """Run the floor on a filed ask. Below it: file standing work, no questions. Above it: hold the
    ask as its own tree and surface its first question on the queue (the held tree goes AWAITING)."""
    transport = transport or call
    questions = floor(ask, transport)
    if not questions:
        return tree.file_intent(ask), []
    held = tree.hold(ask)
    _save(held, _Pass(0, [{"q": q.text, "lean": q.lean, "flip": q.flip, "answer": ""}
                          for q in questions], "", ""))
    return tree.find(held.id) or held, questions


def advance(held: tree.Node, answer: str, transport=None) -> tree.Node:
    """Record the operator's answer to the surfaced question and surface the next, or — when the
    last is answered — produce the contract + delta on the tree. Returns the held tree, re-read:
    still on the queue (AWAITING), now showing the next question or the entry to ratify."""
    transport = transport or call
    p = _load(held)
    if p is None:
        return held
    if 0 <= p.surfaced < len(p.questions):
        p.questions[p.surfaced]["answer"] = " ".join(answer.split())
    if p.surfaced + 1 < len(p.questions):
        p.surfaced += 1
        _save(held, p)
        return tree.find(held.id) or held
    entry, delta_text = products(held.text, [(q["q"], q["answer"]) for q in p.questions], transport)
    p.contract, p.delta = entry, delta_text
    _save(held, p)
    return tree.find(held.id) or held


def ratify(held: tree.Node) -> tree.Node:
    """The view entry approved: the held ask spawns as standing work. The gate opens here and only
    here; the contract and delta stay in the tree's grilling.md as the worker's handed input."""
    return tree.spawn(tree.find(held.id) or held)


def floor(ask: str, transport=None) -> list[Question]:
    """The residual stake-bearing decisions — empty means the ask is below the floor."""
    transport = transport or call
    raw = transport(f"{FLOOR}\n\nThe living spec:\n{_digest()}\n\nThe ask: {ask}\n\n"
                    "Reply with the JSON object now.")
    obj = parse(raw)
    return [Question(q.get("q", ""), q.get("lean", ""), q.get("flip", ""))
            for q in (obj.get("questions") or []) if q.get("q")]


def products(ask: str, qa: list[tuple[str, str]], transport=None) -> tuple[str, str]:
    """The two machine-authored products of a folded pass: the operator-facing contract and the
    machine-side spec delta the change will realize."""
    transport = transport or call
    answers = "\n".join(f"- {q}: {a}" for q, a in qa) or "- (none)"
    raw = transport(f"{PRODUCTS}\n\nThe ask: {ask}\n\nResolved:\n{answers}\n\n"
                    "Reply with the JSON object now.")
    obj = parse(raw)
    return obj.get("entry", "").strip(), obj.get("delta", "").strip()


# ── reading a card's pass: what the held tree currently shows on the queue ──

def is_question(node: tree.Node) -> bool:
    """A held tree whose pass is still running — the card shows a surfaced question."""
    p = _load(node)
    return p is not None and not p.contract


def is_entry(node: tree.Node) -> bool:
    """A held tree whose pass is resolved — the card shows the contract awaiting ratification."""
    p = _load(node)
    return p is not None and bool(p.contract)


def lean_of(node: tree.Node) -> str:
    q = _surfaced(node)
    return q["lean"] if q else ""


def flip_of(node: tree.Node) -> str:
    q = _surfaced(node)
    return q["flip"] if q else ""


def question_of(node: tree.Node) -> str:
    q = _surfaced(node)
    return q["q"] if q else ""


def contract(node: tree.Node) -> str:
    p = _load(node)
    return p.contract if p else ""


def delta_of(node: tree.Node) -> str:
    p = _load(node)
    return p.delta if p else ""


def entry_of(node: tree.Node) -> tree.Node | None:
    """The tree itself once its pass is resolved — the propose-stage product a worker reads for
    its handed delta, and the architect later checks the result against."""
    p = _load(node)
    return node if (p and p.contract) else None


def contract_of(node: tree.Node) -> str:
    return contract(node)


# ── internals: the grilling.md pass-state, durable in the tree's folder ─────

def _pass_path(node: tree.Node) -> str:
    return os.path.join(node.path, "grilling.md")


def _load(node: tree.Node) -> _Pass | None:
    path = _pass_path(node)
    if not node.path or not os.path.isfile(path):
        return None
    return _parse(open(path).read())


def _save(held: tree.Node, p: _Pass) -> None:
    tree.atomic_write(_pass_path(held), _render(p))
    held.state = tree.AWAITING                       # the held tree sits on the queue
    tree._persist(held, f"grill: {tree._subject(held.text)}")   # commits the folder (intent + pass)


def _surfaced(node: tree.Node) -> dict | None:
    p = _load(node)
    if p and p.questions and 0 <= p.surfaced < len(p.questions):
        return p.questions[p.surfaced]
    return None


def _render(p: _Pass) -> str:
    out = [f"surfaced: {p.surfaced}", ""]
    for q in p.questions:
        out += [f"[Q] {q['q']}", f"lean: {q['lean']}", f"flip: {q['flip']}",
                f"answer: {q['answer']}", ""]
    if p.contract:
        out += ["[CONTRACT]", p.contract, ""]
    if p.delta:
        out += ["[DELTA]", p.delta]
    return "\n".join(out).rstrip() + "\n"


def _parse(text: str) -> _Pass:
    surfaced, questions = 0, []
    contract_lines, delta_lines, section, cur = [], [], "q", None
    for line in text.splitlines():
        if section == "q" and line.startswith("surfaced:"):
            surfaced = int(line.split(":", 1)[1].strip() or 0)
        elif line == "[CONTRACT]":
            section = "contract"
        elif line == "[DELTA]":
            section = "delta"
        elif section == "contract":
            contract_lines.append(line)
        elif section == "delta":
            delta_lines.append(line)
        elif line.startswith("[Q] "):
            cur = {"q": line[4:].strip(), "lean": "", "flip": "", "answer": ""}
            questions.append(cur)
        elif cur is not None:
            for k in ("lean", "flip", "answer"):
                if line.startswith(k + ":"):
                    cur[k] = line.split(":", 1)[1].strip()
    return _Pass(surfaced, questions, "\n".join(contract_lines).strip(),
                 "\n".join(delta_lines).strip())


def _digest() -> str:
    return "\n".join(
        f"- {c.name}: {', '.join(r.name for r in c.requirements)}"
        for c in spec.read_spec().capabilities
    ) or "(empty)"
