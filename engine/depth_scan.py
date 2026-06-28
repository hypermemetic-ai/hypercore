"""The model-driven depth scan.

This is the single seam that computes the watched module-depth assessment. It is
handed the architecture review's already-computed `Review` and a target set; it
consults that map and its complexity debt, asks the injected model transport for
the judgment a deterministic scan cannot make, and returns structured findings.

Nothing here walks the source tree. Callers that need a tree scan use
`review.review` first and pass the result in, so the structural map has one
owner and the model verdict cannot drift into a second review implementation.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass

from . import transport as model_transport

ASSESSMENT_SCHEMA = model_transport.Envelope(
    model_transport.Records(
        "findings", "finding",
        model_transport.Tag("subject", "the target module, e.g. review.py"),
        model_transport.Tag("red_flag", "the depth smell: shallow module, information leakage, deletion test"),
        model_transport.Tag("evidence", "why the smell applies, grounded in the supplied map/debt"),
        model_transport.Tag("lean", "the recommendation"),
        model_transport.Tag("flip", "the one fact that would change the recommendation"),
    ),
    model_transport.Tag("lean", "the overall recommendation, or empty if the findings carry it"),
    model_transport.Tag("flip", "the overall flip condition, or empty if the findings carry it"),
)


@dataclass(frozen=True)
class Finding:
    subject: str
    red_flag: str
    evidence: str
    lean: str
    flip: str


@dataclass(frozen=True)
class Assessment:
    targets: tuple[str, ...]
    findings: tuple[Finding, ...]
    lean: str
    flip: str


def assess(targets: Iterable[str], review, transport: Callable[[str], str] | None = None) -> Assessment:
    """Return the watched depth assessment for `targets` in the handed review map.

    `review` is the architecture review's already-computed structural map. The
    target set is filtered to modules present on that map; model rows outside
    that scope are ignored, so the returned assessment cannot smuggle in a
    second tree read.
    """
    scoped = _scoped_targets(targets, review)
    caller = transport or model_transport.call
    verdict = model_transport.read(caller(_prompt(scoped, review)), ASSESSMENT_SCHEMA)
    findings = tuple(f for row in verdict.get("findings", []) if (f := _finding(row, scoped)))
    lean = _text(verdict.get("lean")) or (findings[0].lean if findings else "no depth red flag raised")
    flip = _text(verdict.get("flip")) or (findings[0].flip if findings else "evidence that one target fails the deletion test")
    return Assessment(scoped, findings, lean, flip)


def _scoped_targets(targets: Iterable[str], review) -> tuple[str, ...]:
    requested = tuple(_text(t) for t in targets)
    known = {m.rel for m in getattr(review, "modules", [])}
    if requested:
        return tuple(t for t in requested if t in known)
    return tuple(m.rel for m in getattr(review, "modules", []))


def _prompt(targets: tuple[str, ...], review) -> str:
    target_list = ", ".join(targets) or "(no targets on the handed map)"
    return (
        "Load the depth standards as judgment, not a metric. Assess only the target modules named "
        "below for the red flags a deterministic scan cannot certify: shallow module, information "
        "leakage beyond a mechanical cycle, and deletion-test failure. Use only the supplied "
        "architecture-review map and debt; do not infer from a fresh tree walk.\n\n"
        f"Targets: {target_list}\n\n"
        "Structural map already computed by architecture-review:\n"
        f"{_map(review, targets)}\n\n"
        "Existing complexity debt and mechanical red flags:\n"
        f"{_debt(review)}\n\n"
        f"{model_transport.instruction(ASSESSMENT_SCHEMA)}"
    )


def _map(review, targets: tuple[str, ...]) -> str:
    wanted = set(targets)
    rows = []
    for m in getattr(review, "modules", []):
        bar = f", accepted@{m.bar}" if getattr(m, "bar", None) is not None else ""
        mark = " target" if m.rel in wanted else ""
        rows.append(f"- {m.rel}: {m.lines} lines, {m.status}{bar}{mark}")
    return "\n".join(rows) or "- (no modules on the handed map)"


def _debt(review) -> str:
    rows = [
        f"- {f.subject}: {f.note} ({f.strength})"
        for f in getattr(review, "findings", [])
    ]
    rows += [
        f"- {flag.subject}: {flag.detail} (red flag: {flag.rule})"
        for flag in getattr(review, "flags", [])
    ]
    return "\n".join(rows) or "- no length or mechanical debt on the handed review"


def _finding(row: dict, targets: tuple[str, ...]) -> Finding | None:
    subject = _text(row.get("subject"))
    if not subject or subject not in set(targets):
        return None
    lean, flip = _text(row.get("lean")), _text(row.get("flip"))
    if not lean or not flip:
        return None
    return Finding(
        subject=subject,
        red_flag=_text(row.get("red_flag")) or "model-driven depth red flag",
        evidence=_text(row.get("evidence")) or "model judgment over the handed review map",
        lean=lean,
        flip=flip,
    )


def _text(value) -> str:
    return " ".join(str(value or "").split())
