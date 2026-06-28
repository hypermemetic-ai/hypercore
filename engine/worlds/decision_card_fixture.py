"""Shared decision-card fixture for queue and interface scenarios."""
from __future__ import annotations

from ..card_anatomy import DecisionAnatomy, DecisionOption, DelayCost

SUBJECT = "choose how the decision card carries its anatomy"
SYNTHESIS = "Record the anatomy on the node before rendering the card"
DETAIL_TOKEN = "round-trip proof lives in the node front matter"


def anatomy() -> DecisionAnatomy:
    return DecisionAnatomy(
        synthesis=SYNTHESIS,
        synthesis_detail=DETAIL_TOKEN,
        options=(
            DecisionOption(
                "Store anatomy with the card kind",
                "one node authority for queue and interface",
                "old bare decision callers until they pass anatomy",
                "no side queue or render-only inference",
                "a metadata migration, not a screen parser",
                "the kind and anatomy are read from the same intent record",
            ),
            DecisionOption(
                "Parse the decision body at render time",
                "a quick-looking first paint",
                "the recorded kind stops being the only authority",
                "shape guesses whenever prose changes",
                "rewriting historic prose once the parser drifts",
                "this rejected option is here to prove alternatives carry consequences",
            ),
        ),
        delay=DelayCost(
            "operator judgment on real forks",
            "bare cards keep accumulating unbacked context",
            "queue order already claims attention cost, so delay cost belongs on the card",
        ),
        lean="store anatomy on the node and render it through the card seam",
        flip="the node format cannot carry structured front matter safely",
        lean_detail="the flip is about the storage authority, not visual taste",
    )


def laid_out(rows) -> tuple[bool, str]:
    text = _text(rows)
    for cue in (SYNTHESIS, "Store anatomy with the card kind", "Parse the decision body at render time",
                "unblocks", "breaks", "running unbacked", "reversal costs", "Waiting blocks",
                "Machine leans", "flips if"):
        if cue not in text:
            return False, f"the opened decision face is missing {cue!r}"
    return True, ""


def synthesis(rows) -> tuple[bool, str]:
    forbidden = {"synthesis", "options", "cost of delay", "machine lean", "flip"}
    for row in rows or []:
        text = _row_text(row).strip().lower().rstrip(":")
        if text in forbidden:
            return False, f"the opened decision card exposes a bare label: {text!r}"
    return True, ""


def face(rows) -> tuple[bool, str]:
    text = _text(rows)
    needed = (SYNTHESIS, "Store anatomy with the card kind", "Waiting blocks",
              "Machine leans", "[enter] confirm detail")
    if not all(cue in text for cue in needed):
        return False, "the decision face does not carry the decision material and its affordance"
    return ((True, "") if DETAIL_TOKEN not in text
            else (False, "confirming detail leaked onto the face before it was summoned"))


def confirm_below(rows) -> tuple[bool, str]:
    text = _text(rows)
    if DETAIL_TOKEN not in text:
        return False, "the confirming detail did not surface when summoned"
    face_at, detail_at = _row_index(rows, SYNTHESIS), _row_index(rows, DETAIL_TOKEN)
    if face_at is None or detail_at != face_at + 1:
        return False, "the confirming detail is not one row below its face finding"
    return ((True, "") if "[enter] hide confirming detail" in text
            else (False, "the unfolded detail does not advertise the same one-key fold"))


def _text(rows) -> str:
    return "\n".join(_row_text(row) for row in (rows or []))


def _row_text(row) -> str:
    return "".join(text for text, _style in row)


def _row_index(rows, needle: str) -> int | None:
    return next((i for i, row in enumerate(rows) if needle in _row_text(row)), None)
