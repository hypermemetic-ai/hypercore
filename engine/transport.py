"""The model transport — the one call to the model and the one read of its reply.

A small deep module the rest of the engine depends on **downward**: summon the model with a
prompt and get its text back (`call`), and read the first JSON object out of a reply (`parse`).
It carries the model identity too — the id the call runs against and the label the window shows.

It was named out of `conversation` (ADR 0021). The architect's voice and the worker's, the
grilling pass and the design contest all need the same `claude -p` call and the same lenient JSON
read, and they had been reaching into `conversation`'s privates for them
(`conversation._claude`, `conversation._parse`) — five modules past one module's interface (the
information-leakage red flag) and a `conversation ↔ grill` import cycle besides. The transport is
the shared knowledge; giving it its own module lets `conversation`, `grill`, `design`, and
`worker` each depend on it downward, so the cycle and the reaching-through-privates both dissolve.

The transport is **injectable** — the live `claude -p` here, a scripted fake in the acceptance
check — so the whole system drives deterministically under the harness without an LLM.
"""
from __future__ import annotations

import json
import subprocess

MODEL = "claude-opus-4-8"
MODEL_LABEL = "opus 4.8"


class MalformedReply(Exception):
    """The model returned no JSON object where a structured reply was required — a failure to surface,
    not a no-op to fold (H3). The lenient `parse` degrades such a reply to a spoken answer (right for
    the architect answering in prose); a caller that *needs* structure (`parse_object`, the worker)
    raises this so an empty/truncated/timed-out reply takes the failure path instead of folding as a
    silent success."""


def call(prompt: str) -> str:
    """Summon the model once with `prompt` and return its stdout — the live transport. The one place
    the `claude -p` invocation lives, so every role reaches the model the same way. A non-zero exit or
    empty stdout is a failed summon, not a silent empty reply: it raises `MalformedReply`, so a timeout
    or a crashed `claude` becomes a surfaced failure (the C2 recovery handles it) rather than a
    `{"done": True}` no-op fold (H3)."""
    r = subprocess.run(
        ["claude", "-p", prompt, "--model", MODEL],
        capture_output=True, text=True, timeout=120,
    )
    if r.returncode != 0 or not r.stdout.strip():
        raise MalformedReply(f"the model call failed (exit {r.returncode}, "
                             f"{len(r.stdout)} bytes out)")
    return r.stdout


def _object(raw: str) -> dict | None:
    """The first JSON object in a reply, or None when there is none — the one read of the model's
    structured form, shared by the lenient and the strict parse so they never diverge on what counts
    as an object."""
    start = raw.find("{")
    if start != -1:
        try:
            obj, _ = json.JSONDecoder().raw_decode(raw[start:])
            if isinstance(obj, dict):
                return obj
        except ValueError:
            pass
    return None


def parse(raw: str) -> dict:
    """Extract the first JSON object from a model reply; fall back to treating the whole text as
    'say'. The lenient read the prose-friendly roles share — a model that wraps its JSON in prose
    still parses, and a reply with no object at all degrades to a plain spoken answer rather than an
    error (the architect answering a question)."""
    obj = _object(raw)
    return obj if obj is not None else {"say": raw.strip(), "done": True}


def parse_object(raw: str) -> dict:
    """The strict read for a caller that *requires* a structured reply (the worker's hand-off): the
    first JSON object, or `MalformedReply` when there is none. This is the H3 fix — a worker whose
    model returns prose, a truncated object, or nothing must take the failure path, never fold the
    lenient `{"say": raw, "done": True}` fallback as a no-op success. Structure is the worker's
    contract; its absence is a failure to surface, not a clean fold."""
    obj = _object(raw)
    if obj is None:
        raise MalformedReply("the worker's model returned no JSON object — a malformed hand-off, "
                             "not a foldable result")
    return obj
