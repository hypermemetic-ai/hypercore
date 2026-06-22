"""The architect: the only voice between the operator and the system.

A thread is one throwaway conversational session — opened when the operator
types in, closed when they have what they came for. It holds no durable state;
durability lands on the graph. The architect reads the operator's words
and lands one concrete consequence: a filed intent (standing work), a card
returned to the queue, or an answer (with the thread closed when satisfied).

The architect no longer stubs the work: a ratified ask spawns standing
work, a worker builds it fenced (`worker`), and `integrate` is the archive stage —
it coherence-checks the result against the contract and authors every operator-facing
word from it, so a worker's raw output reaches the operator through no path at all.
The model transport is injectable — a live `claude -p` session in the window, a
scripted fake in the acceptance check.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import conditions, delta, graph, grill
from .transport import call, parse

SYSTEM = (
    "You are hypercore's architect — the single voice between the "
    "operator and the system. The operator just spoke. Decide what their words "
    "are and land one concrete consequence. Reply with ONLY a JSON object:\n"
    '{"say": <your words to the operator, short and plain>, '
    '"file": <a one-line ask to record as standing work, or null>, '
    '"card": <a crisp machine-owned statement or decision to put on the '
    'operator\'s queue, or null>, '
    '"done": <true if the operator now has what they came for>}\n'
    "File intent when they want something built or done. Raise a card when a "
    "real judgment is theirs to make. Answer (file and card null) when they "
    "asked a question. Keep 'say' to a sentence or two, plain, no jargon."
)


@dataclass
class Thread:
    turns: list[tuple[str, str]] = field(default_factory=list)
    open: bool = True

    def add(self, who: str, text: str) -> None:
        self.turns.append((who, text))


@dataclass
class Reply:
    say: str
    filed: graph.Node | None = None
    card: graph.Node | None = None
    done: bool = False
    grilling: graph.Node | None = None          # an ask held for a grilling pass
    questions: list[graph.Node] = field(default_factory=list)


def speak(thread: Thread, text: str, transport=None) -> Reply:
    """One turn: feed the operator's words to the architect and land
    whatever consequence it returns on the graph. A filed ask does not become
    work directly — it enters grilling, and only files straight through when
    it is below the floor."""
    transport = transport or call
    thread.add("operator", text)
    intent = parse(transport(_prompt(thread)))

    filed = grilling = None
    questions: list[graph.Node] = []
    if intent.get("file"):
        held, questions = grill.consider(intent["file"], transport)
        grilling, filed = (held, None) if questions else (None, held)
    card = graph.raise_card(intent["card"]) if intent.get("card") else None
    say = (intent.get("say") or "").strip()
    thread.add("machine", say)
    done = bool(intent.get("done"))
    if done:
        thread.open = False
    return Reply(say=say, filed=filed, card=card, done=done,
                 grilling=grilling, questions=questions)


COHERENCE = (
    "You are hypercore's architect, archiving a worker's hand-off. Judge "
    "coherence at the operator's altitude: does the result honor the contract? This is "
    "not a code review. The worker's report below is for you alone and MUST NOT reach "
    "the operator — author any operator-facing words yourself, short and plain. Reply "
    'with ONLY a JSON object:\n{"coherent": <true if the result honors the contract>, '
    '"say": <your plain note to the operator about what landed, or what is in doubt>, '
    '"card": <if not coherent, the decision to put on the queue — re-cut, abandon, or '
    'change the ask — else null>}'
)


def integrate(node: graph.Node, result, transport=None, root: str | None = None) -> Reply:
    """The archive stage, where the architect holds design judgment: take a worker's hand-off,
    hold it against the folding conditions and the contract, and on a pass fold its refined
    delta into the spec — the work integrates and leaves the threads view in the same act. The
    worker's raw report is *input* to the architect's judgment, never output: every
    operator-facing word here is authored fresh, so the report crosses to the operator through
    no path. A result that fails a non-negotiable condition (no recorded loop, a delta that will
    not apply), trips the **depth** condition (a module past the length signal with no
    depth-decision — re-cut / deepen / accept-with-reason), or that the architect judges
    incoherent raises a decision rather than folding. Depth surfaces to the operator as a
    decision, never a silent veto and never a silent pass (ADR 0006)."""
    transport = transport or call
    blocked = conditions.unmet(result, root)           # the folding conditions, before the merge
    if blocked:
        card = graph.raise_card(blocked, kind="decide", parent=node.id)
        return Reply(say="The result can't fold yet — a folding condition isn't met; "
                         "the reason is on your queue.", card=card)
    verdict = parse(transport(
        f"{COHERENCE}\n\nThe contract:\n{grill.contract_of(node)}\n\n"
        f"The worker's report (machine-facing — do not forward):\n{result.report}\n\n"
        "Reply with the JSON object now."))
    say = (verdict.get("say") or "").strip()
    if not verdict.get("coherent"):
        card = graph.raise_card(verdict.get("card") or say or
                                "the result did not honor the contract",
                                kind="decide", parent=node.id)
        return Reply(say=say, card=card)
    delta.fold(delta.parse(result.delta), root)        # archive ⟺ fold, one act
    graph.integrated(node)
    return Reply(say=say, done=True)


def explain(node: graph.Node, transport=None) -> str:
    """Tell the story toward a decision; the card stays on the queue."""
    transport = transport or call
    prompt = (
        "You are hypercore's architect. The operator pressed explain on "
        "this card and wants help toward the decision — tell the story plainly: "
        "what it changes, where you lean, and the one thing that would flip it. "
        "Reply with ONLY a JSON object {\"say\": <your explanation>}.\n\n"
        f"Card: {node.text}"
    )
    return parse(transport(prompt)).get("say", "").strip()


def _prompt(thread: Thread) -> str:
    convo = "\n".join(
        f"{'operator' if who == 'operator' else 'you'}: {text}"
        for who, text in thread.turns
    )
    return f"{SYSTEM}\n\n{convo}\n\nReply with the JSON object now."
