"""Card rows for the resting face.

The frame renderer owns the screen; this leaf owns the opened-card anatomy so the queue's card
variants stay behind one small row-producing interface.
"""
from __future__ import annotations

import textwrap
from dataclasses import dataclass

from . import grill, tree
from .card_anatomy import DecisionAnatomy, DecisionOption

DIM, SAY, TAG, CARD = "dim", "say", "tag", "card"
Row = list


@dataclass(frozen=True)
class _FaceLine:
    finding: str
    detail: str = ""


def label(card: tree.Node) -> str:
    return grill.card_kind(card)


def detail(card: tree.Node, width: int, confirm: bool = False) -> list[Row]:
    kind = grill.card_kind(card)
    if kind == "decision" and (anatomy := grill.decision_anatomy(card)):
        return _decision_detail(anatomy, width, confirm)
    if kind == "grilling question":
        rows = [[("      lean  ", DIM), (grill.lean_of(card), SAY)]]
        if grill.flip_of(card):
            rows.append([("      flips ", DIM), (grill.flip_of(card), TAG)])
        rows.append([("      [a] accept the lean   ·   type to answer", DIM)])
        return rows
    if kind == "ratification":
        rows: list[Row] = []
        for w in _wrap(grill.contract(card), width - 8):
            rows.append([("      ", SAY), (w, SAY)])
        rows.append([("      [a] ratify — spawns the work   ·   [c] cut", DIM)])
        return rows
    return [[("      [a] approve   [c] cut   [e] explain", DIM)]]


def _decision_detail(anatomy: DecisionAnatomy, width: int, confirm: bool) -> list[Row]:
    rows: list[Row] = []
    for line in _face_lines(anatomy):
        _add(rows, "      ", line.finding, CARD, width)
        if confirm and line.detail:
            _add(rows, "        confirm: ", line.detail, DIM, width)
    if any(line.detail for line in _face_lines(anatomy)):
        hint = "[enter] hide confirming detail" if confirm else "[enter] confirm detail"
        rows.append([("      " + hint + "   ·   [a] approve   [c] cut   [e] explain", DIM)])
    else:
        rows.append([("      [a] approve   [c] cut   [e] explain", DIM)])
    return rows


def _face_lines(anatomy: DecisionAnatomy) -> tuple[_FaceLine, ...]:
    lines = [_FaceLine(anatomy.synthesis, anatomy.synthesis_detail)]
    lines.extend(_FaceLine(_option_finding(option), option.detail) for option in anatomy.options)
    lines.append(_FaceLine(
        f"Waiting blocks {anatomy.delay.blocks}; compounds {anatomy.delay.compounds}",
        anatomy.delay.detail,
    ))
    lines.append(_FaceLine(
        f"Machine leans {anatomy.lean}; flips if {anatomy.flip}",
        anatomy.lean_detail,
    ))
    return tuple(line for line in lines if line.finding.strip())


def _option_finding(option: DecisionOption) -> str:
    return (f"{option.name}: unblocks {option.unblocks}; breaks {option.breaks}; "
            f"keeps {option.unbacked} running unbacked; reversal costs {option.reverse_cost}")


def _add(rows: list[Row], prefix: str, text: str, style: str, width: int) -> None:
    for i, line in enumerate(_wrap(text, width - len(prefix))):
        rows.append([(prefix if i == 0 else " " * len(prefix), style), (line, style)])


def _wrap(text: str, width: int) -> list[str]:
    out: list[str] = []
    for para in text.splitlines() or [""]:
        out.extend(textwrap.wrap(para, max(8, width)) or [""])
    return out
