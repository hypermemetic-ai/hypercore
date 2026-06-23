"""The model transport — the one call to the model and the one read of its reply.

A small deep module the rest of the engine depends on **downward**: summon the model with a
prompt and get its text back (`call` for the architect, `worker_transport` for the fenced worker),
and read the first JSON object out of a reply (`parse`). It carries the two role identities too —
the model each role runs against and the label the window shows.

It was named out of `communication`. The architect's voice and the worker's, the
grilling pass and the design contest all need the same model invocation and the same lenient JSON
read, and they had been reaching into `communication`'s privates for them
(`communication._claude`, `communication._parse`) — five modules past one module's interface (the
information-leakage red flag) and a `communication ↔ grill` import cycle besides. The transport is
the shared knowledge; giving it its own module lets `communication`, `grill`, `design`, and
`worker` each depend on it downward, so the cycle and the reaching-through-privates both dissolve.

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

import json
import subprocess

MODEL = "claude-opus-4-8"
MODEL_LABEL = "opus 4.8"

# The worker's model identity — its own line, the role-assembly step-6 flip point. The worker runs a
# *different* model from the architect (Opus) by ratified design: GPT via the `omp`
# multi-model harness, which auto-loads the fence's anchor and discovers its skills at the worktree.
# The flip to a new vendor was the operator's spend decision (2026-06-22); nothing else names them.
WORKER_CMD = "omp"
WORKER_MODEL = "gpt-5.5"


class MalformedReply(Exception):
    """The model returned no JSON object where a structured reply was required — a failure to surface,
    not a no-op to fold (H3). The lenient `parse` degrades such a reply to a spoken answer (right for
    the architect answering in prose); a caller that *needs* structure (`parse_object`, the worker)
    raises this so an empty/truncated/timed-out reply takes the failure path instead of folding as a
    silent success."""


def _summon(argv: list[str], cwd: str | None = None) -> str:
    """Run one model invocation and return its stdout — the shared body of every live transport
    (the architect at the repo root, the worker at its fence). A non-zero exit or empty stdout is a
    failed summon, not a silent empty reply: it raises `MalformedReply`, so a timeout or a crashed
    harness becomes a surfaced failure (the C2 recovery handles it) rather than a `{"done": True}`
    no-op fold (H3)."""
    r = subprocess.run(argv, capture_output=True, text=True, timeout=120, cwd=cwd)
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
