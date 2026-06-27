"""The worker scenario world — the system-facing half of the split, over the real worker, integrate,
and `conditions` seams. The verbs name what the worker *is*, never the engine symbols: `spawn`/
`grounding` read the assembled grounding; `sharpen` proves the standards are single-sourced; `fence …`
proves the worktree isolation and at-fence transport; `build`/`integrates`/`leak none` run the whole
crossing; and `forge`/`fold` prove the provenance gate refuses a RESULT hand-authored with no fenced
build (no re-derivable trail). Each block runs against an isolated root seeded with the real spec.
"""
from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import tempfile
import re

from .. import communication, conditions, grill, render, spec, transport, tree, worker
from ..scenario import _GATE_GUARD, _git
from . import World as _Base, scripted

_REAL = tree._DEFAULT_ROOT
_DEMO = "demo-worker"                                       # a throwaway capability with no scenarios — the gate stays inert
_DEMO_REQ = "the worker's refined delta integrates"

# The framework tokens the depth grounding must foreground every episode, and the code tokens it must
# never carry — the worker holds the spec, not raw code (slice-4/7 properties, named as domain checks).
_DEPTH_FRAMEWORK = ("deep modules", "downward", "strategic", "red flags", "shallow module", "depth standards")
_CODE_TOKENS = ("import ", "curses")


def _glossary_entries(text: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, list[str]]] = []
    term = ""
    body: list[str] = []
    for line in text.splitlines():
        m = re.match(r"- \*\*(.+?)\*\* — ", line)
        if m:
            if term:
                rows.append((term, body))
            term, body = m.group(1), [line]
        elif term:
            body.append(line)
    if term:
        rows.append((term, body))
    return [(term, "\n".join(lines).rstrip()) for term, lines in rows]


def _mentions(text: str, term: str) -> bool:
    return re.search(rf"(?<![0-9A-Za-z]){re.escape(term)}(?![0-9A-Za-z])", text, re.IGNORECASE) is not None


class World(_Base):
    def __init__(self):
        self._prev_root = os.environ.get("ENGINE_ROOT")
        self.root = tempfile.mkdtemp(prefix="scenario-worker-")
        os.environ["ENGINE_ROOT"] = self.root
        for cmd in (("init", "-q"), ("config", "user.email", "scenario@hypercore"),
                    ("config", "user.name", "scenario")):
            _git(self.root, *cmd)
        shutil.copytree(os.path.join(_REAL, "spec"), os.path.join(self.root, "spec"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        g = os.path.join(_REAL, "glossary.md")
        if os.path.isfile(g):
            shutil.copy(g, os.path.join(self.root, "glossary.md"))
        _git(self.root, "add", "-A"); _git(self.root, "commit", "-qm", "base")
        self.node = self.ctx = self.prompt = self.reply = self.forged = None
        # Sentinels the worker's grounding is read against. They are world-owned and never authored into
        # a check block — the block's own text is part of the spec the worker's grounding carries, so a
        # sentinel named there would appear in the prompt via the spec and defeat the assertion.
        self.raw = "<<RAW-WORKER-PROSE-Rx4 — machine-facing, must reach no operator path>>"
        self.grounds = "<<JIT-ARCHIVE-GROUNDS-Zx9 — long past-decision history, greped JIT, never preloaded>>"
        self.nonce = "<<DEPTH-SOURCE-NONCE-Qz7 — proves the depth grounding is rendered from its slice>>"

    # ── fixture verbs ────────────────────────────────────────────────────────
    def _v_spawn(self, args: list[str]) -> tuple[bool, str]:
        """spawn <cap>… — file an ask whose handed delta names these capabilities, and assemble the
        worker's grounding (its context and prompt) over the whole seeded spec."""
        self.node = self._stage(self._handed(args))
        self._assemble()
        return True, ""

    def _v_sharpen(self, args: list[str]) -> tuple[bool, str]:
        """sharpen — rewrite the depth slice with a world-owned sentinel, so the grounding rendering it
        (`grounding renders`) proves the standards are read from `spec/depth.md`, not a frozen copy."""
        tree.atomic_write(spec.cap_path("depth", self.root),
            "# depth\n\n"
            "Build deep modules behind small interfaces; pull complexity downward; strategic over "
            f"tactical, with the red flags of a shallow module foregrounded — {self.nonce}.\n\n"
            "### Requirement: a sharpened depth discipline\n"
            "The worker MUST hold the sharpened discipline, building deep up front.\n"
            "#### Scenario: a module is built\n- WHEN a worker builds a module\n- THEN the discipline applies\n")
        if self.node is None:
            self.node = self._stage(self._handed(["worker"]))
        self._assemble()
        return True, ""

    def _v_plant_grounds(self, args: list[str]) -> tuple[bool, str]:
        """plant-grounds — write a past decision carrying the world-owned grounds sentinel into the
        checkout's `work/archive/`, the long history the worker greps just-in-time and must NOT inline."""
        tree.atomic_write(os.path.join(self.root, "work", "archive", "0099-past-decision", "intent.md"),
                          f"# a past decision — its long grounds\n\n{self.grounds}\n")
        return True, ""

    def _v_build(self, args: list[str]) -> tuple[bool, str]:
        """build — run the whole crossing: a worker hands back a raw report and a refined delta at its
        fence, and the architect coherence-checks and folds it."""
        self.node = self._stage(self._demo_delta())
        worker.worktree(self.node, self.root)
        tree.dispatch(self.node)
        result = worker.apply(self.node, scripted(transport.emit(worker.WORKER_SCHEMA,
            {"report": "built it. " + self.raw, "delta": self._demo_delta()})), self.root)
        self.reply = communication.integrate(self.node, result, scripted(transport.emit(
            communication.COHERENCE_SCHEMA, {"coherent": True, "say": "it landed.", "card": None})), self.root)
        return True, ""

    # ── assertion verbs ──────────────────────────────────────────────────────
    def _v_grounding(self, args: list[str]) -> tuple[bool, str]:
        """grounding <property> — read the worker's assembled grounding. Properties: `whole-spec` (the
        prompt maps every capability — touched in full, the rest indexed — so the worker sees the whole
        spec), `marks <cap>…`, `foregrounds <cap>` (the prompt inlines that capability's full body),
        `indexes <cap>` (the prompt carries it as an index — its requirement titles, body NOT inlined),
        `glossary-economical` (only foregrounded prose's glossary terms are inlined), `carries-depth`,
        `holds-no-code`, `omits-grounds`, `points-to-archive`, `renders` (the last two read the world's
        planted sentinels)."""
        if self.ctx is None:
            return False, "grounding read before spawn/sharpen"
        prop = args[0]
        if prop == "whole-spec":
            # The myopia-defense, read off the PROMPT (what the worker actually sees), not the context
            # object: every capability surfaces — touched in full, the rest as an index head — so the
            # rescan maps the whole spec even though the untouched bodies are a checkout read away.
            allcaps = {c.name for c in spec.read_spec(self.root).capabilities}
            missing = [c for c in allcaps if c != "depth" and f"### capability: {c}" not in self.prompt]
            return ((True, "") if allcaps and not missing
                    else (False, f"the prompt does not map the whole spec; missing {sorted(missing)}"))
        if prop == "marks":
            want = set(args[1:])
            return ((True, "") if self.ctx.touched == want
                    else (False, f"grounding marks {sorted(self.ctx.touched)}, expected {sorted(want)}"))
        if prop == "foregrounds":
            body = worker._cap_text(args[1], self.root).strip()
            return ((True, "") if body and body in self.prompt
                    else (False, f"{args[1]} is not foregrounded in full in the prompt"))
        if prop == "indexes":
            cap = args[1]
            body = worker._cap_text(cap, self.root).strip()
            c = spec.read_spec(self.root).capability(cap)
            titles = [r.name for r in c.requirements] if c else []
            titled = bool(titles) and all(t in self.prompt for t in titles)
            header = f"### capability: {cap}" in self.prompt
            return ((True, "") if header and titled and body not in self.prompt
                    else (False, f"{cap} is not carried as an index "
                                 f"(header={header}, titled={titled}, body-inlined={body in self.prompt})"))
        if prop == "glossary-economical":
            # Catches: a worker grounding regression that inlines the whole ratified glossary instead of
            # only the entries whose terms appear in the ask, handed delta, or touched capability bodies.
            return self._glossary_economical()
        if prop == "carries-depth":
            return self._needs(_DEPTH_FRAMEWORK)
        if prop == "holds-no-code":
            leaked = [t for t in _CODE_TOKENS if t in self.prompt]
            return (True, "") if not leaked else (False, f"the grounding carries code tokens {leaked}, not spec")
        if prop == "omits-grounds":
            return ((True, "") if self.grounds not in self.prompt
                    else (False, "the long past-decision grounds were inlined into the prompt"))
        if prop == "points-to-archive":
            p = self.prompt
            return ((True, "") if "work/archive/" in p and "just-in-time" in p and "spec/decisions/" not in p
                    else (False, "the prompt does not point the worker at work/archive/ for a just-in-time grep"))
        if prop == "renders":
            return ((True, "") if self.nonce in self.prompt
                    else (False, "the sharpened depth slice did not render into the grounding — a frozen copy?"))
        return False, f"unknown grounding property {prop!r}"

    def _v_envelope(self, args: list[str]) -> tuple[bool, str]:
        """envelope names-renamed — the worker-facing reply grammar names RENAMED beside the other
        delta verbs, so retitles have an operation the worker can write."""
        # Catches: a worker prompt regression that tells workers no RENAMED verb exists for retitles.
        if args != ["names-renamed"]:
            return False, f"unknown envelope assertion {' '.join(args)!r}"
        verbs = ("ADDED", "MODIFIED", "REMOVED", "RENAMED")
        missing = [v for v in verbs if v not in worker.ENVELOPE]
        return (True, "") if not missing else (False, f"the worker envelope omits {missing}")

    def _v_handoff(self, args: list[str]) -> tuple[bool, str]:
        """handoff <round-trips|surfaces-malformed> — the worker hand-off rides the tag envelope. A
        report and a markdown delta (with #### headers and a fenced ```check block) read back
        byte-for-byte with no escaping — the report-as-object crash is gone by construction; a reply
        carrying none of the envelope's tags surfaces as malformed rather than folding a no-op (H3)."""
        if args[0] == "round-trips":
            delta_md = ("## MODIFIED — demo-worker\n### Requirement: a retitle holds\n"
                        "It holds.\n#### Scenario: s\n- WHEN it runs\n- THEN it holds\n\n"
                        "```check\nbuild\nintegrates\n```")
            report = "built it; the delta below carries #### headers and a ```check fence, verbatim."
            reply = f"<report>\n{report}\n</report>\n<delta>\n{delta_md}\n</delta>\n"
            obj = transport.read(reply, worker.WORKER_SCHEMA)
            if obj["report"] != report:
                return False, "the report did not round-trip verbatim"
            if obj["delta"] != delta_md:
                return False, "the markdown delta did not round-trip verbatim (escaping or fence collision?)"
            return True, ""
        if args[0] == "surfaces-malformed":
            try:
                transport.read("prose carrying none of the envelope's tags", worker.WORKER_SCHEMA)
            except transport.MalformedReply:
                return True, ""
            return False, "a tagless hand-off did not surface as malformed"
        return False, f"unknown handoff assertion {args[0]!r}"

    def _v_fence(self, args: list[str]) -> tuple[bool, str]:
        """fence <off-main|binds-cwd|host-read-only|worktree-writable|commit-lands> — the worktree
        isolation and the at-fence cwd binding, plus the OS-level fence: a real `jail` is spawned and
        a write outside the worktree (the main tree) is refused at the OS level while an in-worktree
        write and a commit still land. The escape verbs run the SAME pure `transport.jail` production
        uses, so the gate exercises the real fence; on a host that cannot enforce it they fail loudly
        (the negative-space invariant), never a silent pass."""
        prop = args[0]
        if prop in ("host-read-only", "worktree-writable", "commit-lands"):
            return self._fence_os(prop)
        if prop == "off-main":
            node = self._stage(self._demo_delta())
            fence = worker.worktree(node, self.root)
            tree.dispatch(node)
            worker.apply(node, scripted(transport.emit(worker.WORKER_SCHEMA,
                         {"report": "built", "delta": self._demo_delta()})), self.root)
            on_branch = subprocess.run(["git", "log", "--oneline", f"worker/{node.id}"], cwd=self.root,
                                       capture_output=True, text=True).stdout
            off_main = subprocess.run(["git", "cat-file", "-e", "HEAD:RESULT.md"], cwd=self.root,
                                      capture_output=True, text=True).returncode
            distinct = os.path.isdir(fence) and fence != self.root and os.path.join("work", "worktrees") in fence
            if not distinct:
                return False, "the fence is not a distinct worktree under work/worktrees"
            if "worker: result" not in on_branch:
                return False, "the worker's commit is not on its own branch"
            return (True, "") if off_main != 0 else (False, "the worker's result leaked onto the main line")
        if prop == "binds-cwd":
            node = self._stage(self._demo_delta())
            fence = worker.worktree(node, self.root)
            if getattr(transport.worker_transport(fence), "cwd", None) != fence:
                return False, "the worker transport is not bound to the fence's working directory"
            seen: dict[str, str] = {}

            def spy(cwd: str):
                seen["cwd"] = cwd
                return scripted(transport.emit(worker.WORKER_SCHEMA,
                                               {"report": "built", "delta": self._demo_delta()}))

            saved, worker.worker_transport = worker.worker_transport, spy
            try:
                worker.apply(node, None, self.root)        # transport=None → the live fence-binding path
            finally:
                worker.worker_transport = saved
            return (True, "") if seen.get("cwd") == fence else (False, "apply did not run the worker at its fence cwd")
        return False, f"unknown fence property {prop!r}"

    def _fence_os(self, prop: str) -> tuple[bool, str]:
        """Exercise the real OS fence over a true worktree. `host-read-only`: a worker write to the
        main tree (outside its worktree) is refused at the OS level. `worktree-writable`: a write
        inside the worktree succeeds. `commit-lands`: an in-fence commit reaches the shared record.
        Each spawns `transport.jail` — the exact code path production runs — so the gate tests the
        live fence, not a stand-in. An unenforceable host is a loud failure, never a silent pass."""
        reason = transport.jail_available()
        if reason:
            return False, f"the OS fence is not enforceable on this host: {reason}"
        node = self._stage(self._demo_delta())
        fence = worker.worktree(node, self.root)
        store = transport._store(fence)
        if prop == "host-read-only":
            target = os.path.join(self.root, "FENCE_ESCAPE_PROBE")          # the main tree, outside the worktree
            subprocess.run(transport.jail(["sh", "-c", f"touch {shlex.quote(target)}"], fence, store),
                           capture_output=True, text=True)
            escaped = os.path.exists(target)
            if escaped:
                os.remove(target)
            return ((True, "") if not escaped
                    else (False, "a worker write to the main tree was NOT refused — the fence leaks"))
        if prop == "worktree-writable":
            r = subprocess.run(transport.jail(["sh", "-c", "touch in_fence && test -f in_fence"], fence, store),
                               capture_output=True, text=True)
            return ((True, "") if r.returncode == 0
                    else (False, f"a write inside the worktree was refused under the fence: "
                                 f"{(r.stderr or r.stdout).strip()[:160]}"))
        # commit-lands
        nonce = "fence-commit-" + os.urandom(4).hex()
        script = (f"echo {nonce} > fence_probe.txt && git add fence_probe.txt && "
                  f"git -c user.email=f@x -c user.name=f commit -qm {nonce}")
        r = subprocess.run(transport.jail(["sh", "-c", script], fence, store), capture_output=True, text=True)
        if r.returncode != 0:
            return False, f"an in-fence commit failed under the fence: {(r.stderr or r.stdout).strip()[:160]}"
        log = subprocess.run(["git", "-C", self.root, "log", "--all", "--oneline"],
                             capture_output=True, text=True).stdout
        return ((True, "") if nonce in log
                else (False, "the in-fence commit did not reach the shared record"))

    def _v_leak(self, args: list[str]) -> tuple[bool, str]:
        """leak none — the worker's raw report reaches no card, no render, and no node; the only words
        that cross to the operator are the ones the architect authored."""
        if args[0] != "none":
            return False, f"unknown leak assertion {args[0]!r}"
        nodes = tree.read_tree()
        frame = "".join(t for row in render.main_body(nodes, -1) for t, _s in row)
        files = ""
        for dp, dirs, fs in os.walk(os.path.join(self.root, "work")):
            if "worktrees" in dirs:
                dirs.remove("worktrees")                   # the scratch fence is not a node
            files += "".join(open(os.path.join(dp, fn), encoding="utf-8").read()
                             for fn in fs if fn in ("intent.md", "grilling.md"))
        cards = "".join(c.text for c in nodes)
        return ((False, "the raw worker report reached a card, a render, or a node")
                if self.raw in frame or self.raw in files or self.raw in cards else (True, ""))

    def _v_forge(self, args: list[str]) -> tuple[bool, str]:
        """forge result — a worker RESULT hand-authored with no fenced build: its derived red→green
        cannot re-derive, so the provenance gate must refuse it for no trail."""
        from .. import provenance                           # the brand-new seam — lazily, absent at the base
        self.forged = provenance.forged_result(self.root)
        return True, ""

    def _v_fold(self, args: list[str]) -> tuple[bool, str]:
        """fold held because provenance — the fold refuses the hand-authored RESULT (`no trail`); the
        gate guard is cleared so re-derivation runs (the forge is no fence, so it cannot recurse)."""
        guard = os.environ.pop(_GATE_GUARD, None)
        try:
            reason = conditions.unmet(self.forged, self.root)
        finally:
            if guard is not None:
                os.environ[_GATE_GUARD] = guard
        return ((True, "") if reason and "no trail" in reason.lower()
                else (False, f"expected a provenance refusal, got {reason!r}"))

    def _v_integrates(self, args: list[str]) -> tuple[bool, str]:
        """integrates — the architect folded the worker's refined delta, and the work left the work view."""
        if self.reply is None:
            return False, "integrates read before build"
        cap = spec.read_spec(self.root).capability(_DEMO)
        if not self.reply.done:
            return False, "the coherent result did not fold"
        if cap is None or cap.requirement(_DEMO_REQ) is None:
            return False, "the refined delta did not reach the spec"
        if self.node.id in [n.id for n in tree.work()]:
            return False, "the integrated work did not leave the work view"
        return True, ""

    # ── the proposer layer: a worker applies only an architect-proposed delta ──
    def _v_proposed(self, args: list[str]) -> tuple[bool, str]:
        """proposed <cap>… — file a node whose architect-proposed delta names these capabilities (its
        delta.md), then assemble its grounding; the handed delta IS the node's proposed delta."""
        self.node = self._stage(self._handed(args)); self._assemble()
        return True, ""

    def _v_built(self, args: list[str]) -> tuple[bool, str]:
        """built from-proposal — the worker's handed delta is exactly tree.proposed_delta(node), read
        from the folder, never reconstructed. Catches: a _handed_delta that scans/rebuilds the delta."""
        if args != ["from-proposal"]:
            return False, f"unknown built assertion {' '.join(args)!r}"
        proposed = tree.proposed_delta(self.node)
        if proposed is None:
            return False, "the node carries no proposed delta to build from"
        if worker._handed_delta(self.node) != proposed or self.ctx is None or self.ctx.delta != proposed:
            return False, "the handed delta is not the node's proposed delta — it was reconstructed"
        return True, ""

    def _v_unproposed(self, args: list[str]) -> tuple[bool, str]:
        """unproposed — a hand-authored standing node with NO delta.md (door 2, never-proposed): written
        by hand, not file_intent (which lands a proposal), to model an intent that never was proposed."""
        tree.atomic_write(os.path.join(self.root, "work", "hand-authored-standing-node", "intent.md"),
                          "---\nkind: ask\nstate: standing\nowner: operator\ncreated: 2026-06-27\n---\n"
                          "a hand-authored standing node that never went through a propose stage\n")
        self.node = tree.find("hand-authored-standing-node")
        return ((True, "") if self.node is not None and not self.node.has_delta
                else (False, "the unproposed node was not created deltaless"))

    def _v_held(self, args: list[str]) -> tuple[bool, str]:
        """held off-ready — the never-proposed node is held out of tree.ready, so it is never dispatched
        or assembled. Catches: a tree.ready that drops the has_delta conjunct."""
        if args != ["off-ready"] or self.node is None:
            return False, "held read before unproposed, or unknown assertion"
        return ((True, "") if self.node.id not in {n.id for n in tree.ready()}
                else (False, "a node with no proposed delta is in the ready work — it would be dispatched"))

    def _v_awaiting_delta(self, args: list[str]) -> tuple[bool, str]:
        """awaiting-delta surfaced — the standing render marks the never-proposed node awaiting a proposed
        delta (no card; the operator sees the gap). Catches: a render that shows it as ordinary work."""
        if args != ["surfaced"]:
            return False, f"unknown awaiting-delta assertion {' '.join(args)!r}"
        nodes = tree.read_tree()
        frame = "".join(t for row in render.main_body(nodes, -1) for t, _s in row)
        if "awaiting a proposed delta" not in frame:
            return False, "the render does not surface the deltaless node as awaiting a proposed delta"
        return ((True, "") if not any(c.id == self.node.id for c in tree.cards(nodes))
                else (False, "the deltaless node was raised as a card instead of standing work"))

    def _v_trivial_proposed(self, args: list[str]) -> tuple[bool, str]:
        """trivial-proposed ready — a node with an empty delta.md (a trivial proposal, distinct from
        never-proposed) IS build-ready. Catches: a readiness that treats trivial as never-proposed."""
        if args != ["ready"]:
            return False, f"unknown trivial-proposed assertion {' '.join(args)!r}"
        n = tree.file_intent("a node carrying a trivial architect proposal", delta="")
        if tree.proposed_delta(n) != "" or not n.has_delta:
            return False, "the trivial proposal did not land as an empty delta.md the node reads as carrying"
        return ((True, "") if n.id in {r.id for r in tree.ready()}
                else (False, "a trivially-proposed node is not build-ready — a trivial proposal is still a proposal"))

    def _v_no_author_from_scratch(self, args: list[str]) -> tuple[bool, str]:
        """no-author-from-scratch — no path foregrounds the whole spec for the worker to author its own
        delta: _touched("") names no capability (the all-caps branch deleted), and the deltaless node
        assembled foregrounds none with no 'full scan' instruction. Catches: the deleted fallbacks' return."""
        sp = spec.read_spec(self.root)
        if worker._touched("", sp) == {c.name for c in sp.capabilities}:
            return False, "an empty delta still foregrounds every capability — the author-from-scratch branch survives"
        if worker._touched("", sp):
            return False, "an empty delta names a capability — it should name none"
        ctx = worker.context(self.node, self.root)
        prompt = worker.prompt(self.node, ctx, self.root)
        if ctx.touched or "from the full scan" in prompt or "author it from" in prompt or "author the delta from" in prompt:
            return False, "a deltaless node still foregrounds the spec or instructs authoring from a full scan"
        return True, ""

    # ── internals ────────────────────────────────────────────────────────────
    def _assemble(self) -> None:
        self.ctx = worker.context(self.node, self.root)
        self.prompt = worker.prompt(self.node, self.ctx, self.root)

    def _needs(self, tokens) -> tuple[bool, str]:
        missing = [t for t in tokens if t not in self.prompt]
        return (True, "") if not missing else (False, f"the grounding is missing {missing}")

    def _glossary_economical(self) -> tuple[bool, str]:
        entries = _glossary_entries(open(os.path.join(self.root, "glossary.md"), encoding="utf-8").read())
        source = "\n\n".join([
            grill.contract_of(self.node) or self.node.text,
            self.ctx.delta,
            *(worker._cap_text(n, self.root) for n in sorted(self.ctx.touched)),
        ])
        inlined = [(term, entry) for term, entry in entries if entry in self.prompt]
        stray = [term for term, _entry in inlined if not _mentions(source, term)]
        if stray:
            return False, f"the prompt inlined glossary entries not named by the foregrounded prose: {stray}"
        named = [term for term in ("worker", "communication", "thread", "architect") if _mentions(source, term)]
        missing = [term for term, entry in entries if term in named and entry not in self.prompt]
        if missing:
            return False, f"the prompt omitted named glossary entries: {missing}"
        omitted = next((entry for term, entry in entries if term == "accepted length / the ratchet"), "")
        if not omitted:
            return False, "the fixture glossary does not define the omitted probe term"
        if omitted in self.prompt:
            return False, "an unnamed glossary entry was inlined instead of left for a just-in-time read"
        reachable = "accepted length / the ratchet" in open(os.path.join(self.root, "glossary.md"),
                                                           encoding="utf-8").read()
        return (True, "") if reachable else (False, "the omitted glossary entry is not reachable in glossary.md")

    def _stage(self, handed: str) -> tree.Node:
        # The handed delta lands as the node's architect-proposed delta (delta.md) in one filing act, so
        # _handed_delta reads it through tree.proposed_delta; grilling.md carries only the contract for
        # the ask path (the delta's home is delta.md now, not the pass).
        node = tree.file_intent("a worker builds a change", delta=handed)
        tree.atomic_write(os.path.join(node.path, "grilling.md"),
                          grill._render(grill._Pass(0, [], "contract.", "")))
        return node

    def _handed(self, caps: list[str]) -> str:
        return "".join(
            f"## ADDED — {c}\n### Requirement: a worker probe on {c}\n"
            f"The worker MUST hold {c}.\n#### Scenario: s\n- WHEN it runs\n- THEN {c} holds\n"
            for c in caps)

    def _demo_delta(self) -> str:
        return (f"## ADDED — {_DEMO}\n### Requirement: {_DEMO_REQ}\n"
                "The worker MUST hand back a refined delta that integrates.\n"
                "#### Scenario: s\n- WHEN it hands back\n- THEN it integrates\n")

    def teardown(self) -> None:
        if self._prev_root is None:
            os.environ.pop("ENGINE_ROOT", None)
        else:
            os.environ["ENGINE_ROOT"] = self._prev_root
        shutil.rmtree(self.root, ignore_errors=True)         # the fences live under the root — gone with it
