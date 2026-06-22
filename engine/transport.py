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


def call(prompt: str) -> str:
    """Summon the model once with `prompt` and return its stdout — the live transport. The one
    place the `claude -p` invocation lives, so every role reaches the model the same way."""
    r = subprocess.run(
        ["claude", "-p", prompt, "--model", MODEL],
        capture_output=True, text=True, timeout=120,
    )
    return r.stdout


def parse(raw: str) -> dict:
    """Extract the first JSON object from a model reply; fall back to treating the whole text as
    'say'. The lenient read every role shares — a model that wraps its JSON in prose still parses,
    and a reply with no object at all degrades to a plain spoken answer rather than an error."""
    start = raw.find("{")
    if start != -1:
        try:
            obj, _ = json.JSONDecoder().raw_decode(raw[start:])
            if isinstance(obj, dict):
                return obj
        except ValueError:
            pass
    return {"say": raw.strip(), "done": True}
