"""Intent extraction by grilling — the floor, the one-at-a-time interview, the gate.

Before an ask that opens real choices becomes work, the architect runs a grilling pass. It
resolves every decision it can from the living spec and intent, and surfaces only the residue —
the decisions the operator has a stake in — as questions on the queue, **one at a time**, each
carrying the machine's *lean* and the one thing that would *flip* it. An ask whose every decision
is already determined files straight to work without surfacing an operator interview, but it still
carries the architect's propose-stage product.

A finished pass yields the **view entry** — the contract the result is later checked against — and
the **spec delta** the change will realize. Above the floor, work does not spawn until the entry is
ratified; below it, the same product is attached to the standing work directly.

Design B: the pass is durable **within its tree's folder**, in `grilling.md`, not as a
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
from .transport import Envelope, Records, Tag, call, instruction, read

FLOOR_SCHEMA = Envelope(
    Records("questions", "question",
            Tag("q", "the question"),
            Tag("lean", "your recommended answer"),
            Tag("flip", "the one thing that would change it")),
    lenient=True,                  # a tagless / empty reply is "no questions" (below the floor), not malformed
)

FLOOR = (
    "You are hypercore's architect running a grilling pass on an ask before "
    "it becomes work. Resolve every decision you can from the living spec and intent; "
    "put to the operator ONLY the decisions they have a stake in — ones that change "
    "operator-visible behavior, are hard to reverse, or commit real cost. Err toward "
    "asking when unsure: a wrongly-asked question is cheap, a wrongly-skipped one bites "
    "later. Ask in dependency order. Each question carries your recommended answer "
    "(lean) and the one thing that would flip it (flip). If every decision the work "
    "needs is already determined, return no questions (an empty <questions>)."
)

PRODUCTS_SCHEMA = Envelope(
    Tag("entry", "the operator-view contract: one plain paragraph stating what this ask will become"),
    Tag("delta", "the spec-delta markdown the change realizes"),
)

PRODUCTS = (
    "You are hypercore's architect. The grilling pass is resolved. Produce two "
    "things. (1) entry — the operator-view contract: one plain paragraph stating what "
    "this ask will become, the thing its result is later validated against. (2) delta — "
    "the spec delta the change realizes, markdown with `## ADDED|MODIFIED|REMOVED|RENAMED — "
    "<capability>` sections over `### Requirement: <name>` blocks; a RENAMED block carries "
    "`→ <new name>`, and non-rename requirement blocks carry at least one `#### Scenario:` line. "
    "Write against the existing capabilities."
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
    """Run the floor on a filed ask. Below it: file standing work with the resolved propose product,
    no surfaced questions. Above it: hold the ask as its own tree and surface its first question on the
    queue (the held tree goes AWAITING)."""
    transport = transport or call
    questions = floor(ask, transport)
    if not questions:
        entry, delta_text = products(ask, [], transport)
        return propose(tree.file_intent(ask), entry, delta_text), []
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


def propose(node: tree.Node, contract: str, delta_text: str) -> tree.Node:
    """Attach the architect's resolved propose product to an already-filed node without surfacing an
    operator interview. This is the below-floor path and the hand-authored-material path: callers do
    not learn the `grilling.md` format, only that a standing node now carries the contract and delta a
    worker is allowed to apply."""
    p = _Pass(0, [], contract.strip(), delta_text.strip())
    tree.atomic_write(_pass_path(node), _render(p))
    tree._persist(node, f"propose: {tree._subject(node.text)}")
    return tree.find(node.id) or node


def floor(ask: str, transport=None) -> list[Question]:
    """The residual stake-bearing decisions — empty means the ask is below the floor."""
    transport = transport or call
    raw = transport(f"{FLOOR}\n\nThe living spec:\n{_digest()}\n\nThe ask: {ask}\n\n"
                    f"{instruction(FLOOR_SCHEMA)}")
    obj = read(raw, FLOOR_SCHEMA)
    return [Question(q.get("q", ""), q.get("lean", ""), q.get("flip", ""))
            for q in (obj.get("questions") or []) if q.get("q")]


def products(ask: str, qa: list[tuple[str, str]], transport=None) -> tuple[str, str]:
    """The two machine-authored products of a folded pass: the operator-facing contract and the
    machine-side spec delta the change will realize."""
    transport = transport or call
    answers = "\n".join(f"- {q}: {a}" for q, a in qa) or "- (none)"
    raw = transport(f"{PRODUCTS}\n\nThe ask: {ask}\n\nResolved:\n{answers}\n\n"
                    f"{instruction(PRODUCTS_SCHEMA)}")
    obj = read(raw, PRODUCTS_SCHEMA)
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


# the recorded `kind` field carries a short code; the queue speaks the glossary's five card kinds.
_KIND = {"decide": "decision", "approval": "request for approval",
         "statement": "request for approval", "acceptance": "acceptance"}


def card_kind(node: tree.Node) -> str:
    """The card's **kind**, the one authority the render and the window read instead of inferring it
    (glossary `card`: the kind is recorded on the node, not guessed at render time). One of the five
    kinds along the work's life. The two pass-stage kinds are read off the held tree's pass — a
    grilling question while it is still surfacing, a ratification once it has resolved into a contract
    — because a card whose identity *is* the pass progress cannot be a static field without going
    stale; the other three are read from the recorded `kind`, normalized to the glossary word."""
    if is_question(node):
        return "grilling question"
    if is_entry(node):
        return "ratification"
    return _KIND.get(node.kind, node.kind)


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
