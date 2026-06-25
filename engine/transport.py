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

The architect and the worker differ only where they must: the **architect** runs at the repo root, the
**worker** runs **jailed at its worktree** (`worker_transport` spawns it inside a real OS fence —
`jail` — rooted there, the host read-only and the worktree and shared store writable) so the harness
auto-loads the fence's anchor and discovers its skills and the worker greps `work/archive/` for past
grounds in its own checkout (role-assembly step 5), and yet can write no path outside that checkout.
The worker runs a *different* model from the architect by ratified design — the production model through
the **codex** coding agent — named in one place (`WORKER_CMD`/`WORKER_MODEL`, role-assembly step 6), the
operator's settled spend decision. codex's CLI shape (the reply read from an `-o` file, the closed
stdin, the seeded home) lives one module down in `codex`, so the engine learns none of it. The OS fence
is built from one named mechanism (`FENCE_CMD`, bubblewrap) behind the pure `jail` seam, so a design
re-contest swaps it there and nowhere else.

The transport is **injectable** — the live invocation here, a scripted fake in the acceptance
check — so the whole system drives deterministically under the harness without an LLM.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass

from . import codex

MODEL = "claude-opus-4-8"
MODEL_LABEL = "opus 4.8"

# The worker's harness and model identity — the role-assembly step-6 flip point, named here and nowhere
# else. The worker runs a *different* model from the architect (Opus) by ratified design: the production
# model summoned through the `codex` coding agent on its own auth, which auto-loads the fence's anchor
# and discovers its skills at the worktree. `WORKER_CMD` binds codex's own binary identity (one source,
# `codex.BINARY`) into the seam; `WORKER_MODEL` is the operator's spend-decision model, passed to codex.
# The omp→codex flip was the operator's settled call; nothing else names them.
WORKER_CMD = codex.BINARY
WORKER_MODEL = "gpt-5.5"

# The OS sandbox the worker fence is built from — the ONE place the enforcement mechanism is named, so
# the design-it-twice re-contest (Landlock, a container) repoints it here and `jail` and nothing else.
# bubblewrap (`bwrap`): unprivileged, no root, no daemon, no image — it fences an ordinary process to
# its worktree on the real machine. (design-decision on `the-worker-fence-must-isolate` → the hybrid:
# bubblewrap's pure-transform spine, a reason-returning probe, no no-op jail.)
FENCE_CMD = "bwrap"

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
    """The reply instruction a role's prompt carries, and the prompt's closing line — the envelope's
    tags shown in order with each field's guidance as its placeholder, then the one imperative to
    reply. It is meant to come **last** in every prompt: the role's task and material lead, this reply
    shape closes, so the exact format the model must emit is the freshest thing in view as it answers,
    and the single "Reply now" line lives here, not hand-appended at each call site (where one copy
    once drifted to the retired JSON). One source for the instruction, the closing line, and the
    parse: a sharpened field description reaches the model with no second copy to drift. (Named
    `instruction`, not `render`, so it does not collide with the `render` module — a collision the
    review's import-cycle scan would read as a false dependency edge.)"""
    head = [
        "Reply with ONLY these tags, in this order. Put each field's content verbatim between its",
        "tags — nothing escaped; markdown, code fences, and newlines all pass through as-is:",
        "",
    ]
    return "\n".join(head + _render_fields(schema.fields, 0) + ["", "Reply now."])


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
    """Run the architect's production model invocation and return its stdout — `claude` answers over
    stdout. A non-zero exit or empty stdout is a failed summon, not a silent empty reply: it raises
    `MalformedReply`, so a timeout or a crashed harness becomes a surfaced failure (the C2 recovery
    handles it) rather than a no-op fold (H3). stdin is closed so a model that probes for it cannot
    block the line. (codex answers through an `-o` file, not stdout — it summons via `codex.run`.)"""
    r = subprocess.run(argv, capture_output=True, text=True, timeout=SUMMON_TIMEOUT, cwd=cwd,
                       stdin=subprocess.DEVNULL)
    if r.returncode != 0 or not r.stdout.strip():
        raise MalformedReply(f"the model call failed (exit {r.returncode}, "
                             f"{len(r.stdout)} bytes out)")
    return r.stdout


def call(prompt: str) -> str:
    """Summon the model once with `prompt` and return its reply — the architect's live transport, run
    at the repo root. The one place the architect's invocation lives, so its voice, the grilling pass,
    and the design contest all reach the model the same way. In production it speaks to `claude` over
    stdout; under the weak-model experiment profile (`codex.experiment_provider`) it reads the tree
    through `codex` **read-only** — it edits nothing, exactly as the production architect, a completion,
    cannot — and takes the reply from codex's `-o` file."""
    model, provider = codex.experiment_provider()
    if model is None:
        return _summon(["claude", "-p", prompt, "--model", MODEL])
    out, code = codex.read_only(prompt, model, provider, SUMMON_TIMEOUT)
    if code != 0 or not out.strip():
        raise MalformedReply(f"the codex architect call failed (exit {code}, {len(out)} bytes out)")
    return out


def worker_argv(prompt: str, reply_file: str | None = None) -> list[str]:
    """The argv the worker's live transport runs — the one place the worker's harness binary and model
    are named, so the role-assembly omp→codex flip (step 6) repoints them here and nowhere else. The
    worker runs codex **bypass** (the OS jail is already its sandbox) and its reply lands in `reply_file`
    via codex's `-o`; the experiment profile, when set, repoints the model and adds its provider flags.
    Pure (it spawns nothing), so the scaffold check can assert the worker targets its own binary and
    model without a live call (the honest harness limit)."""
    model, provider = codex.experiment_provider()
    return codex.argv(prompt, model or WORKER_MODEL, "bypass", reply_file or "", provider)


# ── the OS fence: spawn the worker jailed, not merely at a cwd ─────────────────

def _store(worktree: str) -> str:
    """The shared git object store the worker's commits must reach, absolute. A worktree's `.git` is a
    *file* pointing into `<repo>/.git/worktrees/<name>`; the objects and the shared refs live in
    `<repo>/.git`. `git --git-common-dir` resolves it — the difference between *commits land on the one
    record* and *commits die in the jail*. It is the second writable region the fence must open, and the
    reason the fence is **working-trees only**: the store stays reachable so the record is reachable."""
    r = subprocess.run(["git", "-C", worktree, "rev-parse", "--git-common-dir"],
                       capture_output=True, text=True)
    common = (r.stdout.strip() if r.returncode == 0 else "") or os.path.join(worktree, ".git")
    return os.path.abspath(common if os.path.isabs(common) else os.path.join(worktree, common))


def jail(argv: list[str], worktree: str, store: str,
         tmpfs: tuple = (), rw: tuple = ()) -> list[str]:
    """Wrap `argv` in an OS jail rooted at `worktree` — the worker-fence seam. **Pure**: it builds the
    sandbox argv and spawns nothing, so the live fence and the gate's escape-probe run the *identical*
    code path (the only structural reason the gate validates what production actually runs — the
    2026-06-24 escape was a fence that was *named* but was not the thing under test). The ONE place the
    mechanism (`FENCE_CMD`) is named.

    The guarantee, expressed as binds applied in order — a later bind on a sub-path overrides the
    read-only host, which is how the writable holes punch through:

      `--ro-bind / /`     the whole host, read-only: the main tree and every sibling worktree are
                          visible but un-writable, so a worker can reach no path outside its own tree.
      `--dev`/`--proc`    a live runtime without exposing the host's.
      `--tmpfs /tmp` + each `tmpfs` path   fresh, private, ephemeral filesystems, so a coding-agent
                          harness inits its scratch without EROFS while exposing nothing of the real
                          home, and nothing it writes there outlives the fence or reaches a sibling.
      each `rw` (src,dest)   a seeded per-worker state bound writable (the harness's private home).
      `--bind worktree`   the worker's own tree, re-opened writable.
      `--bind store`      the shared object store, writable so the worker's commits reach the record.

    The net is left **open** (§74 — no `--unshare-net`): the fence guards parallel work, not the net;
    spend/publish/pull is the decisions floor's, not walled here. All binds are **absolute** — a
    relative dest mkdir's under the read-only `/` and the jail dies before it runs. The `tmpfs`/`rw`
    holes come **before** the worktree bind so none can shadow it (the home-under-repo footgun)."""
    worktree, store = os.path.abspath(worktree), os.path.abspath(store)
    out = [FENCE_CMD, "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp"]
    for d in tmpfs:
        out += ["--tmpfs", os.path.abspath(d)]
    for src, dest in rw:
        out += ["--bind", os.path.abspath(src), os.path.abspath(dest)]
    out += ["--bind", worktree, worktree]
    if store != worktree:                                   # the store is the worktree's own .git only for a non-worktree checkout
        out += ["--bind", store, store]
    out += ["--die-with-parent", "--chdir", worktree, "--", *argv]
    return out


def jail_available() -> str | None:
    """Whether this host can enforce the fence — `None` when it can, else a one-line reason naming what
    is missing. There is **no no-op jail**: absence is a reason the gate surfaces, never a silent pass —
    the negative-space invariant, the structural bar against the failure that let the escape land. It
    does not trust `which`: it runs a throwaway **real** jail around a trivial command and reports
    whether it held, collapsing *binary missing*, *kernel user-namespaces disabled*, and
    *seccomp/sysctl blocks it* into one truthful bit by exercising the actual mechanism."""
    probe = tempfile.mkdtemp(prefix="jail-probe-")
    try:
        r = subprocess.run(jail(["true"], probe, probe), capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            return (f"the OS fence ({FENCE_CMD}) could not run: "
                    f"{(r.stderr or r.stdout or '').strip()[:200] or 'non-zero exit'}")
        return None
    except FileNotFoundError:
        return f"the OS fence binary ({FENCE_CMD}) is not installed"
    except (OSError, subprocess.SubprocessError) as e:
        return f"the OS fence ({FENCE_CMD}) could not run: {type(e).__name__}: {e}"
    finally:
        shutil.rmtree(probe, ignore_errors=True)


def worker_transport(cwd: str):
    """Bind the worker's live transport to its fence (role-assembly step 5): every worker call is
    **spawned inside a real OS jail rooted at its worktree** — not merely with its working directory
    set there, because a starting directory is not a jail (the 2026-06-24 escape: a cwd-only worker
    edited the main tree). Under the jail the host is read-only, the worktree and the shared store
    writable, the net open, and codex gets its seeded ephemeral private home (`codex.fence_home`); so
    the checkout is still the working directory — the harness auto-loads the fence's anchor and skills
    and the worker greps `work/archive/` in its checkout — but every path outside the worktree refuses
    writes at the OS level. codex's reply lands in an `-o` file inside a host temp dir bound writable
    **outside** the worktree, so it never pollutes the delta the worker commits. An empty reply or a
    non-zero exit raises `MalformedReply` (the wire-level verdict, kept here, not in `codex`), so a
    timed-out or crashed build surfaces (C2) rather than folding a no-op (H3). The injection boundary
    stays `(prompt) -> str` and `.cwd` is preserved, so the scripted fakes and the scaffold check are
    untouched."""
    def at_fence(prompt: str) -> str:
        seed, rw, tmpfs = codex.fence_home()
        reply_dir = tempfile.mkdtemp(prefix="fence-codex-reply-")
        try:
            reply_file = os.path.join(reply_dir, "reply.txt")
            jailed = jail(worker_argv(prompt, reply_file), cwd, _store(cwd),
                          tmpfs=tuple(tmpfs), rw=(*rw, (reply_dir, reply_dir)))
            out, code = codex.run(jailed, reply_file, SUMMON_TIMEOUT)
            if code != 0 or not out.strip():
                raise MalformedReply(f"the worker's codex build failed (exit {code}, {len(out)} bytes out)")
            return out
        finally:
            shutil.rmtree(seed, ignore_errors=True)
            shutil.rmtree(reply_dir, ignore_errors=True)
    at_fence.cwd = cwd
    return at_fence
