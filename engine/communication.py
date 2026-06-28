"""The architect: the only voice between the operator and the system.

A thread is one throwaway conversational session — opened when the operator
types in, closed when they have what they came for. It holds no durable state;
durability lands on the tree. The architect reads the operator's words
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

from . import conditions, delta, provenance, tree, grill
from .transport import Envelope, Flag, Tag, call, instruction, read

SYSTEM_SCHEMA = Envelope(
    Tag("say", "your words to the operator, short and plain"),
    Tag("file", "a one-line ask to record as standing work, or leave empty"),
    Tag("card", "a crisp machine-owned statement or decision to put on the operator's queue, "
                "or leave empty"),
    Flag("done", "true if the operator now has what they came for"),
    lenient=True, fallback="say",
)

SYSTEM = (
    "Load the `communication` skill before you answer. The operator just spoke. "
    "Decide what their words are and land one concrete consequence. File intent "
    "when they want something built or done. Raise a card when a real judgment is "
    "theirs to make. Answer with file and card empty when they asked a question."
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
    filed: tree.Node | None = None
    card: tree.Node | None = None
    done: bool = False
    grilling: tree.Node | None = None          # an ask held for a grilling pass
    questions: list[tree.Node] = field(default_factory=list)


def speak(thread: Thread, text: str, transport=None) -> Reply:
    """One turn: feed the operator's words to the architect and land
    whatever consequence it returns on the tree. A filed ask does not become
    work directly — it enters grilling, and only files straight through when
    it is below the floor."""
    transport = transport or call
    thread.add("operator", text)
    intent = read(transport(_prompt(thread)), SYSTEM_SCHEMA)

    filed = grilling = None
    questions: list[tree.Node] = []
    if intent.get("file"):
        held, questions = grill.consider(intent["file"], transport)
        grilling, filed = (held, None) if questions else (None, held)
    card = tree.raise_card(intent["card"]) if intent.get("card") else None
    say = (intent.get("say") or "").strip()
    thread.add("machine", say)
    done = bool(intent.get("done"))
    if done:
        thread.open = False
    return Reply(say=say, filed=filed, card=card, done=done,
                 grilling=grilling, questions=questions)


COHERENCE_SCHEMA = Envelope(
    Tag("say", "your plain note to the operator about what landed, or what is in doubt"),
    Flag("coherent", "true if the result honors the contract"),
    Tag("card", "if not coherent, the decision to put on the queue — re-cut, abandon, or change "
                "the ask — else leave empty"),
    lenient=True, fallback="say",
)

COHERENCE = (
    "Load the `coherence` skill before you answer. You are archiving a worker's "
    "hand-off. Judge this hand-off against the contract at the operator's altitude. "
    "This is not a code review. The worker's report below is machine-facing and "
    "MUST NOT reach the operator. Author every operator-facing word yourself."
)


def integrate(node: tree.Node, result, transport=None, root: str | None = None) -> Reply:
    """The archive stage, where the architect holds design judgment: take a worker's hand-off,
    hold it against the folding conditions and the contract, and on a pass fold its refined
    delta into the spec — the work integrates and leaves the threads view in the same act. The
    worker's raw report is *input* to the architect's judgment, never output: every
    operator-facing word here is authored fresh, so the report crosses to the operator through
    no path. A result that fails a non-negotiable condition (its capability's scenario did not go
    red→green, a delta that will not apply), trips the **depth** condition (a module past the length
    signal with no
    accepted-length record — re-cut / deepen / accept-with-reason), or that the architect judges
    incoherent raises a decision rather than folding. Depth surfaces to the operator as a
    decision, never a silent veto and never a silent pass."""
    transport = transport or call
    blocked = conditions.unmet(result, root, node)     # the folding conditions (incl. provenance), before the merge
    if blocked:
        card = tree.raise_card(blocked, kind="decide", parent=node.id)
        return Reply(say="The result can't fold yet — a folding condition isn't met; "
                         "the reason is on your queue.", card=card)
    verdict = read(transport(
        f"{COHERENCE}\n\nThe contract:\n{grill.contract_of(node)}\n\n"
        f"The worker's report (machine-facing — do not forward):\n{result.report}\n\n"
        f"{instruction(COHERENCE_SCHEMA)}"), COHERENCE_SCHEMA)
    say = (verdict.get("say") or "").strip()
    if not verdict.get("coherent"):
        card = tree.raise_card(verdict.get("card") or say or
                                "the result did not honor the contract",
                                kind="decide", parent=node.id)
        return Reply(say=say, card=card)
    try:
        delta.fold(delta.parse(result.delta), root, node=node,
                   code=getattr(result, "code", None))       # archive ⟺ fold ⟺ verified code, ONE atomic act (H1)
    except delta.ResourceLimitReached as refusal:
        card = tree.raise_card(str(refusal), kind="decide", parent=node.id)
        return Reply(say="The merged re-verify hit a resource limit — the retryable decision is on "
                         "your queue.", card=card)
    except delta.CannotFold as refusal:
        # A code-bearing build that does not hold once merged onto main (re-verify red), or whose paths
        # main has moved under (stale): nothing landed. Surface the reason as a decision; `run` recovers
        # the node to standing behind it, so the ask is re-cut off current main rather than half-folded.
        card = tree.raise_card(str(refusal), kind="decide", parent=node.id)
        return Reply(say="The verified build didn't hold once merged onto main — the reason is on your "
                         "queue as a decision.", card=card)
    provenance.commit_verdict(node, provenance.FENCED_RUN, _fenced_run_verdict(node), root)
    return Reply(say=say, done=True)


def _fenced_run_verdict(node: tree.Node) -> str:
    """The live-run trace's payload: evidence that this node reached the archive stage through a
    fenced worker crossing. It deliberately carries no worker report, so the machine-facing hand-off
    still has no path to the operator-facing tree."""
    return f"fenced worker crossing folded\n\nnode: {node.id}\nsubject: {tree._subject(node.text)}"


EXPLAIN_SCHEMA = Envelope(Tag("say", "your explanation toward the decision"),
                          lenient=True, fallback="say")

EXPLAIN = (
    "Load the `communication` skill before you answer. The operator pressed explain "
    "on this card. Tell the story toward this decision: what it changes, where you "
    "lean, and the one thing that would flip it."
)


def explain(node: tree.Node, transport=None) -> str:
    """Tell the story toward a decision; the card stays on the queue."""
    transport = transport or call
    prompt = f"{EXPLAIN}\n\nCard: {node.text}\n\n{instruction(EXPLAIN_SCHEMA)}"
    return read(transport(prompt), EXPLAIN_SCHEMA).get("say", "").strip()


def _prompt(thread: Thread) -> str:
    convo = "\n".join(
        f"{'operator' if who == 'operator' else 'you'}: {text}"
        for who, text in thread.turns
    )
    return f"{SYSTEM}\n\n{convo}\n\n{instruction(SYSTEM_SCHEMA)}"
