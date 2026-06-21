"""The conversationalist: the only voice between the operator and the system.

A thread is one throwaway conversational session — opened when the operator
types in, closed when they have what they came for. It holds no durable state;
durability lands on the graph. The conversationalist reads the operator's words
and lands one concrete consequence: a filed intent (standing work), a card
returned to the queue, or an answer (with the thread closed when satisfied).

Slice 1 stubs "the work": filing intent records the node and nothing runs yet.
The model transport is injectable — a live `claude -p` session in the window, a
scripted fake in the acceptance check.
"""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field

from . import graph, grill

MODEL = "claude-opus-4-8"
MODEL_LABEL = "opus 4.8"

SYSTEM = (
    "You are hypercore's conversationalist — the single voice between the "
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
    """One turn: feed the operator's words to the conversationalist and land
    whatever consequence it returns on the graph. A filed ask does not become
    work directly — it enters grilling (§5), and only files straight through when
    it is below the floor."""
    transport = transport or _claude
    thread.add("operator", text)
    intent = _parse(transport(_prompt(thread)))

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


def explain(node: graph.Node, transport=None) -> str:
    """Tell the story toward a decision; the card stays on the queue."""
    transport = transport or _claude
    prompt = (
        "You are hypercore's conversationalist. The operator pressed explain on "
        "this card and wants help toward the decision — tell the story plainly: "
        "what it changes, where you lean, and the one thing that would flip it. "
        "Reply with ONLY a JSON object {\"say\": <your explanation>}.\n\n"
        f"Card: {node.text}"
    )
    return _parse(transport(prompt)).get("say", "").strip()


def _prompt(thread: Thread) -> str:
    convo = "\n".join(
        f"{'operator' if who == 'operator' else 'you'}: {text}"
        for who, text in thread.turns
    )
    return f"{SYSTEM}\n\n{convo}\n\nReply with the JSON object now."


def _parse(raw: str) -> dict:
    """Extract the first JSON object; fall back to treating the text as 'say'."""
    start = raw.find("{")
    if start != -1:
        try:
            obj, _ = json.JSONDecoder().raw_decode(raw[start:])
            if isinstance(obj, dict):
                return obj
        except ValueError:
            pass
    return {"say": raw.strip(), "done": True}


def _claude(prompt: str) -> str:
    r = subprocess.run(
        ["claude", "-p", prompt, "--model", MODEL],
        capture_output=True, text=True, timeout=120,
    )
    return r.stdout
