"""The codex worker harness — codex's CLI shape, behind the engine's `transport`.

The worker runs a *different* model from the architect by ratified design (the operator's settled
spend decision), summoned through the **codex** coding agent (`codex exec`). codex's CLI differs from
the prior harness in two facts the rest of the engine must not learn: it returns the model's reply
through an **`-o <file>`** (stdout is a human transcript, not the answer), and it **blocks on an open
stdin** (a piped-empty `< /dev/null` is required, or it hangs). This module holds both, plus the
fenced-home seed codex needs to start under a read-only host, and the experiment env profile — so
`transport` depends on it **downward** and learns none of codex's shape. It imports nothing from the
engine (acyclic by construction; the review's import-cycle scan reads no edge back).

**The fence-home seed.** Under the worker's OS jail the host home is read-only, but codex writes its
session store under `~/.codex` and dies at startup otherwise. `fence_home` seeds a *fresh writable*
`~/.codex` carrying only the four small auth/config files — never a copytree, because the real
`~/.codex` holds a mult-hundred-MB rollout sqlite the worker neither needs nor should see. Each worker
gets its own private copy, so nothing it writes touches the operator's home or a sibling's.

**The experiment profile.** `experiment_provider` reads one env switch (`HYPERCORE_SYNTH=1`) and, when
set, returns the model slug and the `-c` provider flags that point codex at the synthetic spine through
the codex-shim bridge — the weak-model loop's override. Unset (production), it returns `(None, [])` and
nothing changes: the worker runs the production model on codex's own auth. The override is an env
profile, not a default flip, so production never depends on it.

This module spawns nothing under the acceptance harness — the scripted fakes inject a `(prompt) -> str`
transport above it — so its seams stay pure and testable: `argv` builds an argument vector, `run`
spawns one process and reads one file, `fence_home` copies a few files. Whether a *live* codex build
runs to completion inside the jail is **watched** evidence (a real model run), like the fence's
anchor/skill load — the gate proves the fence holds, not that the worker thrives in it.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile

# codex's identity — its binary name, the one source the role seam (`transport.WORKER_CMD`) binds to,
# so the worker's harness name is stated once and `argv[0]` and the named flip point cannot disagree.
BINARY = "codex"

# The four small files codex reads to authenticate and configure itself — the only home state the
# fence seeds. NOT the rollout sqlite (history/sessions, hundreds of MB): the worker starts fresh.
_HOME_SEED = ("auth.json", "config.toml", "version.json", "installation_id")


def experiment_provider() -> tuple[str | None, list[str]]:
    """The weak-model experiment's env profile, or production's no-op. Reads `HYPERCORE_SYNTH`: unset
    (production) returns `(None, [])` and nothing routes through it — the worker runs its production
    model on codex's own auth. Set to `1` returns `(model_slug, provider_flags)` pointing codex at the
    synthetic spine through the codex-shim loopback bridge (`HYPERCORE_SYNTH_MODEL` overrides the slug).
    The override is an env profile a run opts into, never a changed default, so production is untouched."""
    if os.environ.get("HYPERCORE_SYNTH") != "1":
        return None, []
    model = os.environ.get("HYPERCORE_SYNTH_MODEL", "glm-5-2")
    flags = [
        "-c", "model_providers.codex_shim.name=codex_shim",
        "-c", "model_providers.codex_shim.base_url=http://127.0.0.1:8765/v1",
        "-c", "model_providers.codex_shim.wire_api=responses",
        "-c", "model_providers.codex_shim.env_key=SYNTHETIC_API_KEY",
        "-c", "model_provider=codex_shim",
        "-c", "model_reasoning_effort=low",
    ]
    return model, flags


def argv(prompt: str, model: str, sandbox: str, reply_file: str,
         provider: list[str] | tuple = ()) -> list[str]:
    """Build the `codex exec` argument vector — the one place codex's flags are named. `sandbox` is
    `"bypass"` for the fenced worker (`--dangerously-bypass-approvals-and-sandbox`: codex runs no
    sandbox of its own because the OS jail already is one) or `"read-only"` for the architect's
    read path (it reads the tree and emits text, never edits). The reply lands in `reply_file` via
    `-o`, hooks are off, and the git-repo check is skipped so codex runs in a worktree whose `.git`
    is a file. `provider` carries the experiment's `-c` flags, empty in production."""
    sandbox_flags = (["--dangerously-bypass-approvals-and-sandbox"] if sandbox == "bypass"
                     else ["--sandbox", "read-only"])
    return [BINARY, "exec", "--disable", "hooks", "--skip-git-repo-check",
            *provider, "-m", model, "-o", reply_file, *sandbox_flags, prompt]


def run(argv: list[str], reply_file: str, timeout: int, cwd: str | None = None) -> tuple[str, int]:
    """Spawn one codex invocation and return `(reply, returncode)`. stdin is closed (`DEVNULL`) because
    codex blocks on an open one; the reply is read from `reply_file` (codex's `-o`), not stdout, which
    carries only the human transcript. A missing or unreadable reply file degrades to the empty string,
    so the caller's empty-reply check catches a crashed or timed-out run as a failure, never a no-op.
    It raises nothing of its own — the wire-level `MalformedReply` verdict stays the caller's, in
    `transport`, so codex's process shape and the engine's error contract do not bleed together."""
    r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout,
                       cwd=cwd, stdin=subprocess.DEVNULL)
    try:
        with open(reply_file, encoding="utf-8") as fh:
            reply = fh.read()
    except OSError:
        reply = ""
    return reply, r.returncode


def read_only(prompt: str, model: str, provider: list[str] | tuple, timeout: int) -> tuple[str, int]:
    """Run codex **read-only** — the architect's experiment path: it reads the tree and emits the
    envelope text, never edits, exactly as the production architect (a completion) cannot. Owns the
    private reply-dir lifecycle (a temp dir outside any worktree, cleaned after) and returns
    `(reply, returncode)`; the empty/non-zero verdict stays the caller's, in `transport`. The worker's
    reply dir is *not* managed here — it must be bound into the OS jail, so it lives at the fence."""
    reply_dir = tempfile.mkdtemp(prefix="codex-architect-")
    try:
        reply_file = os.path.join(reply_dir, "reply.txt")
        return run(argv(prompt, model, "read-only", reply_file, provider), reply_file, timeout)
    finally:
        shutil.rmtree(reply_dir, ignore_errors=True)


def fence_home() -> tuple[str, list, list]:
    """Seed the per-worker, writable, ephemeral `~/.codex` the jail's read-only home would otherwise
    deny — without it codex dies at startup writing its session store under `--ro-bind / /`. Returns
    `(seed_dir, rw, tmpfs)`: a fresh dir holding a copy of only the small auth/config files
    (`_HOME_SEED`), bound writable over the real `~/.codex` path so the worker authenticates and writes
    its sessions in isolation. It is **not** a copytree — the real `~/.codex` carries a large rollout
    sqlite the worker neither needs nor should read. The caller cleans up `seed_dir`. (`tmpfs` is empty
    here — codex needs no separate scratch path beyond its seeded home — but the triple matches the
    fence's `(seed, rw, tmpfs)` shape so `transport` binds every harness the same way.)"""
    home = os.path.expanduser("~")
    src = os.path.join(home, ".codex")
    seed = tempfile.mkdtemp(prefix="fence-codex-")
    rw: list = []
    if os.path.isdir(src):
        dest = os.path.join(seed, ".codex")
        os.makedirs(dest, exist_ok=True)
        for name in _HOME_SEED:
            p = os.path.join(src, name)
            if os.path.isfile(p):
                shutil.copy(p, os.path.join(dest, name))
        rw.append((dest, src))
    return seed, rw, []
