---
kind: ask
state: standing
owner: operator
created: 2026-06-24
---
# weak-model-loop-harness — run the full loop under a weaker model and capture per-run evidence for methodology refinement

The methodology has only ever driven its loop behind strong models (Opus architect, GPT-5.5 worker),
so we cannot yet tell which of its guarantees hold because the **method** is sound and which hold only
because the **model** was strong enough to paper over a thin seam. Spending the Synthetic credits, run
the full hypercore loop (grill -> design -> fenced build -> integrate -> fold) driven by a deliberately
weaker model — GLM-5.2 on synthetic.new — across a variety of asks, and capture a detailed report per
run, so the failures the weak model surfaces become the evidence that directs refinement of the method
itself.

## the model mapping
- **hypercore proper (production).** The worker harness changes `omp` -> **codex** (model unchanged:
  `gpt-5.5`, on codex's own ChatGPT auth); the architect is unchanged (`claude` / Opus 4.8). This is the
  shared prerequisite — codex-running-in-the-fence — that the experiment's worker also rides.
- **the experiment.** Both roles run through **codex on GLM-5.2 via synthetic** — codex exec pointed at
  the **codex-shim** bridge. The architect runs **read-only** (it reads the tree and emits the envelope
  text the engine applies; it never edits — production's architect is a completion that cannot either),
  the worker runs **jailed and writable** exactly as the production worker does. One weak model, one
  harness, behind both roles.

## the spine (validated 2026-06-24 — see setup-notes.md)
codex 0.142 speaks **only** the OpenAI Responses API; synthetic.new speaks **only** chat-completions
(`/responses` -> 404, `/chat/completions` -> 200). The bridge between them is **codex-shim**
(`github.com/sybil-solutions/codex-shim`, pipx), a loopback daemon on `127.0.0.1:8765` translating
Responses<->chat, with one `generic-chat-completion-api` route to `api.synthetic.new/openai/v1`. Both
the architect read-only path and the worker agentic tool-use path round-trip through it to glm-5.2
(including the Responses<->chat tool-call translation). The engine override rides an env profile in a
new `engine/codex.py` (extraction, not a transport ratchet) so production defaults never change.

## the runs
Each run operates on a **disposable clone** of the repo — the live tree is never touched by a weak
model — is fed one real ask, and drives the loop to a terminal (a fold or an escalation). A **per-run
report** is stored as material on this node: the ask, the model mapping, every architect/worker
prompt+reply, timings and Synthetic usage, the diff, the scenario verdicts, and where and why it failed
or folded — so the corpus can later be read together to direct refinement work on the methodology.

## folding condition
- the codex-in-fence worker change lands (as `engine/codex.py` + a slimmed `engine/transport.py`) and
  `python3 -m engine --check` is green;
- the harness brings up the synthetic spine and drives the full loop end-to-end under GLM-5.2, on a
  disposable clone, for a variety of asks;
- a detailed report per run is captured and stored as material on this node.

## teardown (temporary scaffolding to clear when the campaign folds)
- stop the codex-shim loopback daemon (`codex-shim stop`) — the experiment leaves no live service running;
- remove any temporary permission allow-rules added for the run (codex-shim / `codex exec`);
- the codex-shim install (pipx) and `~/.codex-shim/models.json` may stay or be removed at the operator's word.
