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

import json
import os
from collections import namedtuple
from dataclasses import dataclass, field

from . import conditions, delta, depth_scan, provenance, review, tree, grill
from .transport import Envelope, Flag, MalformedReply, Tag, call, instruction, read

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
    Tag("caveat", "the load-bearing qualifier the operator-facing words must carry, or leave empty"),
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

COHERENCE_ATTEMPTS = 3


ENTAILMENT_SCHEMA = Envelope(
    Flag("survives", "true if the operator-facing words entail the load-bearing caveat"),
)

ENTAILMENT = (
    "Load the `communication` skill before you answer. Judge only whether the "
    "operator-facing words entail the load-bearing caveat. The verdict is watched "
    "model judgment; return only the survival flag."
)

REDRAFT_SCHEMA = Envelope(Tag("say", "your operator-facing words, redrafted to carry the caveat"),
                          lenient=True, fallback="say")

REDRAFT = (
    "Load the `communication` skill before you answer. Your operator-facing words below dropped the "
    "load-bearing caveat. Redraft the words to carry it in its own stress position — as concrete and as "
    "hard as the claim. Edit expression only; do not change what the words decide. Return the redrafted words."
)

CAVEAT_ATTEMPTS = 3


def carry_caveat(say: str, caveat: str, transport=None) -> tuple[str, bool]:
    """The archive render's caveat-survival self-repair seam — the architect editing its own expression.

    An empty caveat is the no-caveat path and makes no model call. A non-empty caveat is checked for
    survival in the operator-facing words; a dropped one is the architect's to repair, not the operator's
    to settle — the words are redrafted to carry the caveat (edits expression only), the watched verdict
    re-run over each revision, up to `CAVEAT_ATTEMPTS` times. Returns the words to cross — the redraft once
    it carries the caveat — and whether the caveat is carried. A caveat still dropped after the bound is the
    rare contract-level miss the wording cannot cure, surfaced (not silently crossed) by the False flag."""
    caveat = (caveat or "").strip()
    if not caveat:
        return say, True
    transport = transport or call
    if _survives(say, caveat, transport):
        return say, True
    for _ in range(CAVEAT_ATTEMPTS):
        say = _redraft(say, caveat, transport)
        if _survives(say, caveat, transport):
            return say, True
    return say, False


def _survives(say: str, caveat: str, transport) -> bool:
    """The watched entailment verdict — does the draft carry the caveat — over a scriptable oracle."""
    verdict = read(transport(
        f"{ENTAILMENT}\n\n"
        f"Operator-facing words:\n{(say or '').strip()}\n\n"
        f"Load-bearing caveat:\n{caveat}\n\n"
        f"{instruction(ENTAILMENT_SCHEMA)}"), ENTAILMENT_SCHEMA)
    return bool(verdict.get("survives"))


def _redraft(say: str, caveat: str, transport) -> str:
    """Ask the architect to rewrite its own words to carry the dropped caveat; the decision is untouched."""
    redrafted = read(transport(
        f"{REDRAFT}\n\n"
        f"Your operator-facing words:\n{(say or '').strip()}\n\n"
        f"The load-bearing caveat they dropped:\n{caveat}\n\n"
        f"{instruction(REDRAFT_SCHEMA)}"), REDRAFT_SCHEMA).get("say", "").strip()
    return redrafted or say


# ── the held build: preserve-and-decide (spec.coherence) ─────────────────────
# A watched integrate verdict — an incoherence judgment, or a caveat the architect's redrafts cannot carry —
# over a build whose deterministic gate is green raises a decision but MUST NOT discard the verified build.
# The build (its refined delta and the captured engine bytes) is held as durable material on the node, surviving the
# fence's teardown because it lands in the node's folder, not the fence. Settling by override re-folds
# the *same* artifact through the unchanged `delta.fold` — no rebuild. The deterministic gate stays
# authoritative for soundness; only a genuine re-verify failure on merged main still discards.
HELD_BUILD = "held-build.json"

_HeldCode = namedtuple("_HeldCode", "base tip")   # the .base/.tip pair `delta.fold` content-replays


@dataclass
class _Held:
    delta: str
    base: str
    code: dict                                    # {engine path: _HeldCode}
    report: str


def hold_build(node: tree.Node, result, root: str | None = None) -> None:
    """Preserve a verified WorkerResult as durable material on the node — the *preserve* half. Duck-types
    the result (delta / base / code), so it crosses no boundary into the worker; the bytes outlive the
    fence's teardown because they land in the node's committed folder."""
    code = {rel: {"base": cf.base, "tip": cf.tip}
            for rel, cf in (getattr(result, "code", None) or {}).items()}
    payload = {"delta": result.delta, "base": getattr(result, "base", ""),
               "code": code, "report": getattr(result, "report", "")}
    path = os.path.join(node.path, HELD_BUILD)
    tree.transact(lambda: tree.atomic_write(path, json.dumps(payload, indent=2)),
                  [path], f"hold build: {tree._subject(node.text)}")


def has_held_build(node: tree.Node) -> bool:
    return bool(node.path) and os.path.isfile(os.path.join(node.path, HELD_BUILD))


def held_build(node: tree.Node) -> _Held | None:
    path = os.path.join(node.path, HELD_BUILD) if node.path else ""
    if not path or not os.path.isfile(path):
        return None
    d = json.loads(open(path).read())
    code = {rel: _HeldCode(c["base"], c["tip"]) for rel, c in d.get("code", {}).items()}
    return _Held(d.get("delta", ""), d.get("base", ""), code, d.get("report", ""))


def settle_held(node: tree.Node, root: str | None = None) -> Reply:
    """The *decide* half: the operator overrode the watched flake, so re-fold the held gate-proven build
    with no rebuild. The same artifact folds through the unchanged `delta.fold` — its staleness pre-check
    and whole-system re-verify run over the held build, since main may have moved under it. A genuine
    deterministic failure (stale, or red once merged) still surfaces a decision rather than landing an
    unsound build; it never silently discards the held work."""
    held = held_build(node)
    if held is None:
        return Reply(say="", done=False)
    try:
        delta.fold(delta.parse(held.delta), root, node=node, code=held.code or None)
    except delta.ResourceLimitReached as refusal:
        card = tree.raise_card(str(refusal), kind="decide", parent=node.id)
        return Reply(say="The held build's re-verify hit a resource limit — the retryable decision is on "
                         "your queue.", card=card)
    except delta.CannotFold as refusal:
        card = tree.raise_card(str(refusal), kind="decide", parent=node.id)
        return Reply(say="The held build no longer holds on current main — the reason is on your queue.",
                     card=card)
    provenance.commit_verdict(node, provenance.FENCED_RUN, _fenced_run_verdict(node), root)
    return Reply(say="The held build folded with no rebuild.", done=True)


def integrate(node: tree.Node, result, transport=None, root: str | None = None) -> Reply:
    """The archive stage, where the architect holds design judgment: take a worker's hand-off,
    hold it against the folding conditions and the contract, and on a pass fold its refined
    delta into the spec — the work integrates and leaves the threads view in the same act. The
    worker's raw report is *input* to the architect's judgment, never output: every
    operator-facing word here is authored fresh, so the report crosses to the operator through
    no path. A typed flat refusal is raised verbatim. A typed depth guard raises a neighborhood-aware
    assessment over the standing review map. A coherent result folds; an incoherent one raises a
    decision rather than folding."""
    transport = transport or call
    blocked = conditions.verdict(result, root, node)   # the folding conditions (incl. provenance), before the merge
    if blocked:
        text = (_depth_assessment(blocked, root, transport)
                if blocked.guard == conditions.DEPTH else blocked.reason)
        card = tree.raise_card(text, kind="decide", parent=node.id)
        return Reply(say="The result can't fold yet — a folding condition isn't met; "
                         "the reason is on your queue.", card=card)
    verdict = _coherence_verdict(node, result, transport)
    if verdict is None:
        card = tree.raise_card(_unreadable_coherence(COHERENCE_ATTEMPTS),
                               kind="decide", parent=node.id)
        return Reply(say="The coherence reply was unreadable; the retryable decision is on your queue.",
                     card=card)
    say = (verdict.get("say") or "").strip()
    if not verdict.get("coherent"):
        hold_build(node, result, root)                 # preserve-and-decide: never discard a gate-proven build
        card = tree.raise_card(verdict.get("card") or say or
                                "the result did not honor the contract",
                                kind="decide", parent=node.id)
        return Reply(say=say, card=card)
    say, carried = carry_caveat(say, verdict.get("caveat") or "", transport)   # a dropped caveat is redrafted, not raised
    if not carried:
        hold_build(node, result, root)                 # the rare caveat the wording cannot carry: held, never discarded
        card = tree.raise_card(_caveat_uncarriable(CAVEAT_ATTEMPTS), kind="decide", parent=node.id)
        return Reply(say="The result can't fold yet — the load-bearing caveat could not be carried in the "
                         "words even after redrafting; the decision is on your queue.", card=card)
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


def _coherence_verdict(node: tree.Node, result, transport) -> dict | None:
    """Ask the watched coherence judgment until it returns a usable verdict or exhausts the bound."""
    for attempt in range(COHERENCE_ATTEMPTS):
        try:
            raw = transport(_coherence_prompt(node, result, retry=attempt > 0))
        except MalformedReply:
            continue
        verdict = read(raw, COHERENCE_SCHEMA)
        if verdict.get("coherent") is None:
            continue
        return verdict
    return None


def _coherence_prompt(node: tree.Node, result, retry: bool = False) -> str:
    retry_note = ("\n\nThe previous coherence reply carried no usable "
                  "<coherent>true</coherent> or <coherent>false</coherent> verdict. "
                  "Re-answer the same judgment with the full envelope."
                  if retry else "")
    return (
        f"{COHERENCE}\n\nThe contract:\n{grill.contract_of(node)}\n\n"
        f"The worker's report (machine-facing — do not forward):\n{result.report}"
        f"{retry_note}\n\n"
        f"{instruction(COHERENCE_SCHEMA)}"
    )


def _unreadable_coherence(attempts: int) -> str:
    return (
        f"decision — coherence reply unreadable after {attempts} attempts. Retry the coherence "
        "judgment, re-cut the ask, or change the ask; the verified build is held live behind this "
        "decision."
    )


def _caveat_uncarriable(attempts: int) -> str:
    return (
        f"decision — the load-bearing caveat could not be carried in the operator-facing words after "
        f"{attempts} redrafts; the words cannot honor it, which points past the wording to the build or "
        "the ask. Re-cut, change the ask, or abandon — the verified build is held live behind this decision."
    )


def _fenced_run_verdict(node: tree.Node) -> str:
    """The live-run trace's payload: evidence that this node reached the archive stage through a
    fenced worker crossing. It deliberately carries no worker report, so the machine-facing hand-off
    still has no path to the operator-facing tree."""
    return f"fenced worker crossing folded\n\nnode: {node.id}\nsubject: {tree._subject(node.text)}"


def _depth_assessment(blocked: conditions.Verdict, root: str | None, transport) -> str:
    """Render the advisory depth assessment raised in place of the bare length template."""
    rv = review.review(root)
    assessment = depth_scan.assess(blocked.subjects, rv, transport)
    flagged = ", ".join(blocked.subjects) or "the flagged file"
    findings = "\n".join(
        f"- {f.subject}: {f.red_flag}; {f.evidence}"
        for f in assessment.findings
    ) or "- no model red flag was raised from the handed architecture-review map"
    return (
        f"decision — depth assessment for {flagged}\n\n"
        f"{findings}\n\n"
        f"Lean: {assessment.lean}\n\n"
        f"Flip: {assessment.flip}\n\n"
        "The depth guard already holds the fold; this assessment informs the settlement."
    )


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
