"""Decision-card anatomy: the durable payload a decision carries on its node.

The tree records card kind in a node's intent front matter; a decision's anatomy lives beside that
kind as a typed JSON value. The render reads this object back through the queue seam instead of
deriving meaning from the card's text or shape.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DecisionOption:
    name: str
    unblocks: str
    breaks: str
    unbacked: str
    reverse_cost: str
    detail: str = ""


@dataclass(frozen=True)
class DelayCost:
    blocks: str
    compounds: str
    detail: str = ""


@dataclass(frozen=True)
class DecisionAnatomy:
    synthesis: str
    options: tuple[DecisionOption, ...]
    delay: DelayCost
    lean: str
    flip: str
    synthesis_detail: str = ""
    lean_detail: str = ""


def coerce(value: "DecisionAnatomy | dict[str, Any] | None") -> DecisionAnatomy | None:
    """Accept the typed value callers should use, plus a dict for scripted fixtures."""
    if value is None or isinstance(value, DecisionAnatomy):
        return value
    if isinstance(value, dict):
        return from_dict(value)
    raise TypeError(f"decision anatomy must be DecisionAnatomy, dict, or None, not {type(value).__name__}")


def dumps(anatomy: DecisionAnatomy) -> str:
    return json.dumps(to_dict(anatomy), sort_keys=True, separators=(",", ":"))


def loads(raw: str) -> DecisionAnatomy | None:
    try:
        return from_dict(json.loads(raw))
    except (AttributeError, TypeError, ValueError, KeyError):
        return None


def to_dict(anatomy: DecisionAnatomy) -> dict[str, Any]:
    return {
        "synthesis": anatomy.synthesis,
        "synthesis_detail": anatomy.synthesis_detail,
        "options": [option.__dict__ for option in anatomy.options],
        "delay": anatomy.delay.__dict__,
        "lean": anatomy.lean,
        "lean_detail": anatomy.lean_detail,
        "flip": anatomy.flip,
    }


def from_dict(data: dict[str, Any]) -> DecisionAnatomy:
    if not isinstance(data, dict):
        raise TypeError("decision anatomy must decode to an object")
    return DecisionAnatomy(
        synthesis=_text(data, "synthesis"),
        synthesis_detail=_text(data, "synthesis_detail", "detail"),
        options=tuple(_option(o) for o in data.get("options", [])),
        delay=_delay(data.get("delay", {})),
        lean=_text(data, "lean"),
        lean_detail=_text(data, "lean_detail"),
        flip=_text(data, "flip"),
    )


def _option(data: dict[str, Any]) -> DecisionOption:
    return DecisionOption(
        name=_text(data, "name"),
        unblocks=_text(data, "unblocks"),
        breaks=_text(data, "breaks"),
        unbacked=_text(data, "unbacked", "keeps_running_unbacked"),
        reverse_cost=_text(data, "reverse_cost", "reverse"),
        detail=_text(data, "detail"),
    )


def _delay(data: dict[str, Any]) -> DelayCost:
    return DelayCost(
        blocks=_text(data, "blocks"),
        compounds=_text(data, "compounds"),
        detail=_text(data, "detail"),
    )


def _text(data: dict[str, Any], *keys: str) -> str:
    for key in keys:
        if key in data and data[key] is not None:
            return " ".join(str(data[key]).split())
    return ""
