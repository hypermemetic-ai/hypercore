"""The model transport — the one call to the model and the one read of its reply.

A small deep module the rest of the engine depends on **downward**: summon the model with a
prompt and get its text back (`call` for the architect, `worker_transport` for the fenced worker),
and read a reply in the one wire format the whole system shares (`read`, against a per-channel
`Envelope` schema). It carries the two role identities too — the model each role runs against and
the label the window shows.

**The format is tag-delimited, not JSON** (the ratified `handoff-format` design-decision). Every
channel declares a tiny `Envelope` of fields; `instruction` turns that schema into the reply
instruction the role's prompt carries, and `read` parses the reply back. A field's content lives **verbatim**
between its tags (`<delta>…</delta>`) — no escaping, so a worker's markdown delta, with its `##`
headers and ` ```check ` fences, round-trips losslessly and a field can never arrive as a typed
object to crash on. Record-shaped channels nest (`<questions><question>…</question>…</questions>`),
so one format serves both the authored-content and the multi-entity channels. The delimiter is
collision-safe because markdown essentially never emits a closing `</delta>`. This retired JSON —
`json.dumps`/`parse`/`parse_object` — from every model reply: the *"Let Me Speak Freely?"* reasoning
tax of constrained decoding, and the report-as-object crash class, both gone by construction.

It was named out of `communication`. The architect's voice and the worker's, the grilling pass and
the design contest all need the same model invocation and the same reply read, and they had been
reaching into `communication`'s privates for them — five modules past one module's interface (the
information-leakage red flag) and a `communication ↔ grill` import cycle besides. The transport is
the shared knowledge; giving it its own module lets `communication`, `grill`, `design`, and `worker`
each depend on it downward, so the cycle and the reaching-through-privates both dissolve.

The two live transports share one summon (`_summon`) and differ only where they must: the
**architect** runs at the repo root, the **worker** runs at its fence (`worker_transport`, cwd =
its worktree) so the harness auto-loads the fence's anchor and discovers its skills and the worker
greps `work/archive/` for past grounds in its own checkout (role-assembly step 5). The worker runs a
*different* model from the architect by ratified design — GPT via `omp` — named in one place
(`WORKER_CMD`/`WORKER_MODEL`, role-assembly step 6), the operator's settled spend decision.

The transport is **injectable** — the live invocation here, a scripted fake in the acceptance
check — so the whole system drives deterministically under the harness without an LLM.
"""
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass

MODEL = "claude-opus-4-8"
MODEL_LABEL = "opus 4.8"

# The worker's model identity — its own line, the role-assembly step-6 flip point. The worker runs a
# *different* model from the architect (Opus) by ratified design: GPT via the `omp`
# multi-model harness, which auto-loads the fence's anchor and discovers its skills at the worktree.
# The flip to a new vendor was the operator's spend decision (2026-06-22); nothing else names them.
WORKER_CMD = "omp"
WORKER_MODEL = "gpt-5.5"

# The summon timeout — one bound, both roles. It is not a tuned per-role budget but an **extreme-runaway
# backstop**: a model call (the architect's quick turn or the worker's whole fenced build) that runs past
# an hour is hung or looping, not working, so the summon kills it and the failure surfaces (C2 recovery)
# rather than wedging the line forever. Generous on purpose — it bounds the pathological case, nothing else.
SUMMON_TIMEOUT = 3600       # seconds (1h)


class MalformedReply(Exception):
    """The model returned a reply carrying none of the envelope's tags where a structured reply was
    required — a failure to surface, not a no-op to fold (H3). A `lenient` envelope degrades such a
    reply (the architect answering in prose becomes the `say` field; a grilling floor with no tags is
    "no questions"); a strict envelope (`read` of the worker's hand-off) raises this, so an
    empty/truncated/timed-out reply takes the failure path instead of folding as a silent success."""


# ── the wire format: a per-channel Envelope of tag-delimited fields ───────────

@dataclass(frozen=True)
class _Field:
    """One field in an envelope: a `<name>…</name>` tag whose inner text is taken verbatim. `kind`
    is `text` (the stripped inner string), `flag` (a true/false inner read to a bool), or `records`
    (the inner holds repeated `<item>` blocks, each parsed by `fields` into a sub-record). `desc` is
    the per-field guidance `render` shows the model as the tag's placeholder."""
    name: str
    desc: str = ""
    kind: str = "text"             # "text" | "flag" | "records"
    item: str = ""                 # records: the per-item tag
    fields: tuple = ()             # records: the sub-fields (a tuple of _Field)


@dataclass(frozen=True)
class Schema:
    """A channel's reply shape: its ordered fields, reason-first (content/reasoning fields before
    answer/flag fields, the *Let Me Speak Freely?* mitigation made structural). `lenient` lets a
    tagless reply degrade to defaults instead of raising; `fallback` names the field a tagless
    reply's whole text degrades into (the architect's prose answer), lenient only."""
    fields: tuple
    lenient: bool = False
    fallback: str = ""


def Tag(name: str, desc: str = "") -> _Field:
    """A verbatim text field — `<name>…</name>`, inner taken exactly (outer whitespace stripped)."""
    return _Field(name, desc, "text")


def Flag(name: str, desc: str = "") -> _Field:
    """A boolean field — `<name>true</name>` / `<name>false</name>`, read to a Python bool."""
    return _Field(name, desc, "flag")


def Records(name: str, item: str, *fields: _Field, desc: str = "") -> _Field:
    """A repeated-record field — `<name>` wrapping zero or more `<item>` blocks, each a sub-record of
    `fields`. The one place a keyed format earns its keep: unambiguous attribution of many entities
    (the grilling questions, the design comparison), carried by nesting in the same one format."""
    return _Field(name, desc, "records", item, tuple(fields))


def Envelope(*fields: _Field, lenient: bool = False, fallback: str = "") -> Schema:
    """Declare a channel's reply shape. List fields reason-first; pass `lenient=True` (with an
    optional `fallback` field) for a channel whose tagless reply is meaningful rather than malformed."""
    return Schema(tuple(fields), lenient, fallback)


def instruction(schema: Schema) -> str:
    """The reply instruction a role's prompt carries — the envelope's tags shown in order with each
    field's guidance as its placeholder, so the model emits exactly what `read` parses. One source
    for the instruction and the parse: a sharpened field description reaches the model with no second
    copy to drift. (Named `instruction`, not `render`, so it does not collide with the `render`
    module — a collision the review's import-cycle scan would read as a false dependency edge.)"""
    head = [
        "Reply with ONLY these tags, in this order. Put each field's content verbatim between its",
        "tags — nothing escaped; markdown, code fences, and newlines all pass through as-is:",
        "",
    ]
    return "\n".join(head + _render_fields(schema.fields, 0))


def _render_fields(fields: tuple, depth: int) -> list[str]:
    pad = "  " * depth
    out: list[str] = []
    for f in fields:
        if f.kind == "records":
            out.append(f"{pad}<{f.name}>")
            out.append(f"{pad}  <{f.item}>")
            out += _render_fields(f.fields, depth + 2)
            out.append(f"{pad}  </{f.item}>")
            out.append(f"{pad}  (one <{f.item}>…</{f.item}> per item; emit <{f.name}></{f.name}> "
                       f"empty if none)")
            out.append(f"{pad}</{f.name}>")
        elif f.kind == "flag":
            out.append(f"{pad}<{f.name}>true or false — {f.desc}</{f.name}>")
        else:
            out.append(f"{pad}<{f.name}>")
            if f.desc:
                out.append(f"{pad}{f.desc}")
            out.append(f"{pad}</{f.name}>")
    return out


def read(raw: str, schema: Schema) -> dict:
    """Parse a model reply against its envelope — the one read the whole system shares. Each field's
    inner text is taken verbatim (text stripped of outer whitespace, a flag coerced to bool, records
    collected to a list of sub-records); every declared field is present in the result, at its
    default when absent. A reply carrying **none** of the envelope's tags is malformed: a strict
    envelope raises `MalformedReply` (the H3 fix — the worker's hand-off never folds a no-op), a
    lenient one degrades to defaults, routing its whole text into the `fallback` field when one is
    named (the architect's prose answer)."""
    if not any(_present(raw, f.name) for f in schema.fields):
        if not schema.lenient:
            raise MalformedReply("the reply carried none of the envelope's tags — a malformed "
                                 "hand-off, not a foldable result")
        out = _defaults(schema.fields)
        if schema.fallback:
            out[schema.fallback] = raw.strip()
        return out
    return _read_fields(raw, schema.fields)


def emit(schema: Schema, values: dict) -> str:
    """Render a reply in the wire format from a field→value mapping — the inverse of `read`, and the
    one place a reply is *written* in this codebase: the scenario fixtures script their model
    stand-ins with it, so a fixture's reply is guaranteed to round-trip through `read` (what the
    acceptance check pins). Production never emits — the model does."""
    return "\n".join(_emit_fields(schema.fields, values or {}))


def _present(text: str, name: str) -> bool:
    return re.search(rf"<{re.escape(name)}>", text) is not None


def _inner(text: str, name: str) -> str | None:
    """The verbatim inner of the first `<name>…</name>` — non-greedy to the first closer, which is
    collision-safe because authored markdown never emits a literal `</name>`."""
    m = re.search(rf"<{re.escape(name)}>(.*?)</{re.escape(name)}>", text, re.DOTALL)
    return m.group(1) if m else None


def _read_fields(text: str, fields: tuple) -> dict:
    out: dict = {}
    for f in fields:
        inner = _inner(text, f.name)
        if f.kind == "records":
            blocks = re.findall(rf"<{re.escape(f.item)}>(.*?)</{re.escape(f.item)}>",
                                inner or "", re.DOTALL)
            out[f.name] = [_read_fields(b, f.fields) for b in blocks]
        elif f.kind == "flag":
            out[f.name] = (inner or "").strip().lower() in ("true", "yes", "1")
        else:
            out[f.name] = (inner or "").strip()
    return out


def _defaults(fields: tuple) -> dict:
    return {f.name: ([] if f.kind == "records" else (False if f.kind == "flag" else ""))
            for f in fields}


def _emit_fields(fields: tuple, values: dict) -> list[str]:
    out: list[str] = []
    for f in fields:
        v = values.get(f.name)
        if f.kind == "records":
            out.append(f"<{f.name}>")
            for item in (v or []):
                out.append(f"<{f.item}>")
                out += _emit_fields(f.fields, item)
                out.append(f"</{f.item}>")
            out.append(f"</{f.name}>")
        elif f.kind == "flag":
            out.append(f"<{f.name}>{'true' if v else 'false'}</{f.name}>")
        else:
            out.append(f"<{f.name}>{'' if v is None else v}</{f.name}>")
    return out


# ── the live transports: one summon, two role bindings ────────────────────────

def _summon(argv: list[str], cwd: str | None = None) -> str:
    """Run one model invocation and return its stdout — the shared body of every live transport
    (the architect at the repo root, the worker at its fence). A non-zero exit or empty stdout is a
    failed summon, not a silent empty reply: it raises `MalformedReply`, so a timeout or a crashed
    harness becomes a surfaced failure (the C2 recovery handles it) rather than a no-op fold (H3)."""
    r = subprocess.run(argv, capture_output=True, text=True, timeout=SUMMON_TIMEOUT, cwd=cwd)
    if r.returncode != 0 or not r.stdout.strip():
        raise MalformedReply(f"the model call failed (exit {r.returncode}, "
                             f"{len(r.stdout)} bytes out)")
    return r.stdout


def call(prompt: str) -> str:
    """Summon the model once with `prompt` and return its stdout — the architect's live transport,
    run at the repo root. The one place the architect's invocation lives, so its voice, the grilling
    pass, and the design contest all reach the model the same way."""
    return _summon(["claude", "-p", prompt, "--model", MODEL])


def worker_argv(prompt: str) -> list[str]:
    """The argv the worker's live transport runs — the one place the worker's harness binary and
    model are named, so the role-assembly OMP/GPT flip (step 6) repoints them here and nowhere else.
    Pure (it spawns nothing), so the scaffold check can assert the worker targets its own model
    without a live call (the honest harness limit)."""
    return [WORKER_CMD, "-p", prompt, "--model", WORKER_MODEL]


def worker_transport(cwd: str):
    """Bind the worker's live transport to its fence (role-assembly step 5): every worker call runs
    with its working directory set to `cwd` = its worktree, so the harness auto-loads the fence's
    anchor and discovers its skills and the worker greps `work/archive/` for past grounds in its checkout.
    The injection boundary stays `(prompt) -> str` — the fence is closed over, not threaded through it,
    so the scripted fakes are untouched — and the binding carries `.cwd` so the scaffold check can
    assert the worker runs at its fence without a live model."""
    def at_fence(prompt: str) -> str:
        return _summon(worker_argv(prompt), cwd=cwd)
    at_fence.cwd = cwd
    return at_fence
