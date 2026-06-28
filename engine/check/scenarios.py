"""Acceptance — the self-model is self-verifying: a capability's scenarios are its executable checks.

This is the acceptance path that replaces the dissolved by-slice harness for every migrated
capability. As each capability's checks home in its own spec (`spec/<capability>.md`), it runs here
with no edit: the green-and-derive loop iterates **every capability whose spec carries a check block**
— the set is read off the specs, never hand-listed — so a newly migrated capability appears the moment
its first block lands. It asserts three things:

1. **the scenarios are green** — every `#### Scenario:` check block in every migrated capability runs
   against the live engine and passes, so the system meets its own spec right now;
2. **the classification is derived, not hand-tended** — a requirement is gated exactly when one of its
   scenarios carries a check block and watched otherwise (`scenario.classification`), checked here to
   read off the blocks themselves, so the register cannot drift from what is gated;
3. **the scenario gate is a real red→green** — over a fence whose tip changes a folding-conditions
   behavior (the length signal) and whose base does not, the gate runs the capability's scenarios at
   the fork base (red) and the tip (green), trusting exit codes — and refuses a tip that is not green.
   This is the gate the worker's self-authored loop is replaced by; it cannot certify itself from
   inside a fold, so the harness exercises it here, from outside.

A migrated capability may also carry **watched** invariants the closed scenario vocabulary cannot
honestly express — a retired constant, a scaffold the live model would otherwise verify, a structural
fact. Those are exercised here from outside (never a faked in-spec block), grouped by capability: the
gate red→green above is folding-conditions'; the worker section below is the worker's.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import threading

from . import build_reaches_main
from .harness import ok
from .. import (anchor, audit, channels, communication, design, grill, machine_writing, methodology,
                review, scenario, schedule, spec, transport, tree, worker)

REAL = tree._DEFAULT_ROOT                                  # hypercore's own source tree — the spec under test

# A behavior change touching folding-conditions: the delta the synthetic hand-off carries, so the gate
# runs that capability's scenarios. The worktree is the demo fence (below).
_DELTA = ("# delta — signal change\n## MODIFIED — folding-conditions\n"
          "### Requirement: length past the signal raises a decision, never a silent refusal\nx\n")


def check(root: str) -> None:
    print("\nscenarios — acceptance check  (the self-model is self-verifying: capability scenarios)\n")

    # 1. every capability that carries check blocks is green, and its gated/watched classification is
    #    READ OFF the blocks — derived, never hand-tended. The set of migrated capabilities is the set
    #    whose spec carries a block, read live, so a newly migrated capability appears here with no edit.
    migrated = [c.name for c in spec.read_spec(REAL).capabilities if scenario.checks(c.name, REAL)]
    ok({"folding-conditions", "coherence", "worker", "architecture-review", "design-it-twice", "grilling", "schedule", "self-model", "communication", "queue", "interface", "channels"} <= set(migrated),
       f"the migrated capabilities carry their executable scenarios ({', '.join(migrated)})")
    for cap in migrated:
        for o in scenario.run(cap, REAL):
            ok(o.passed, f"{cap} — scenario green: {o.scenario}" + ("" if o.passed else f": {o.detail}"))
        blocked = {c.requirement for c in scenario.checks(cap, REAL)}
        cls = dict(scenario.classification(cap, REAL))
        ok(all((k == "gated") == (r in blocked) for r, k in cls.items()),
           f"{cap} — gated/watched is read off the check blocks "
           f"({sum(k == 'gated' for k in cls.values())} gated, {sum(k == 'watched' for k in cls.values())} watched)")

    # 2. the scenario gate is a REAL red→green — and refuses a tip that is not green ───────────────────
    # The fence's tip lowers the length signal 500→400 (a real folding-conditions behavior change); its
    # scenarios are calibrated to 400, so they FAIL at the base (signal 500) and PASS at the tip. The
    # gate runs them in the fence, trusting only the exit codes.
    transit = _demo_fence(base=500, tip=400)
    try:
        ok(scenario.gate(worker.WorkerResult("built it", _DELTA, transit), REAL) is None,
           "RED→GREEN: the capability's scenarios fail at the fork base and pass at the tip — the gate clears")
    finally:
        _drop(transit)

    held = _demo_fence(base=500, tip=500)                  # the tip never built the behavior — still red
    try:
        ok(scenario.gate(worker.WorkerResult("did not build it", _DELTA, held), REAL) is not None,
           "a tip whose scenarios are not green is refused — narration is never the gate, the exit code is")
    finally:
        _drop(held)

    # 2b. the verified fenced build reaches main — a code-bearing fold lands the build's ENGINE CODE on
    #     the merged tree (not only its spec), in one commit, re-verified before the commit; a build that
    #     would leave merged main red is refused and nothing lands. Like the gate red→green above, this
    #     behavior cannot certify itself from inside the fold it tests, so it is exercised from outside,
    #     over a real merged tree. Held in its own module (build_reaches_main) — the fixture is heavyweight
    #     and the harness stays under the length signal it enforces.
    build_reaches_main.check()

    # 3. worker — structural/scaffold invariants the closed scenario vocabulary cannot honestly express
    #    (a retired constant, the model the worker targets, the scheduler's injection point): watched,
    #    exercised here from outside, never faked. The worker's behavior is gated in spec/worker.md.
    ok(not hasattr(worker, "DEPTH"),
       "worker — the frozen DEPTH constant is retired; the depth standards are single-sourced from spec/depth.md")
    argv = transport.worker_argv("PROMPT")
    ok(transport.WORKER_CMD in argv and transport.WORKER_MODEL in argv,
       "worker — the harness binary and model are named in one place, bound at the fence (the omp→codex flip point)")
    ok(schedule.Scheduler().transport is None,
       "worker — the scheduler forwards the live worker injection point untouched, so the worker binds its own fence")

    # 4. architecture-review — facts about hypercore's OWN source the standing scan reads, exercised
    #    from outside. The review's *behavior* (flag a god-file, tell a stale acceptance from an over
    #    file, read the mechanical red flags, render the derived operator view) is gated in
    #    spec/architecture-review.md; what no fixture can assert is the artifact itself — that the live
    #    engine tree is honestly clean, so a regression that grows a god-file or a cycle goes red here.
    rv = review.review(REAL)
    ok(not rv.findings or not any(f.strength == "strong" for f in rv.findings),
       "architecture-review — the real engine tree carries no strong complexity debt: every module is "
       "within the length signal or carries an accepted-length record (a settled decision, read from the "
       "one debt definition — `review.findings` — never a re-listed status set that can drift from it)")
    flags = review.red_flags(REAL)
    ok(not flags, "architecture-review — the real engine tree carries no mechanical red flags"
       + (f" (found: {[f.subject for f in flags]})" if flags else " (dead symbols, circular imports)"))

    # 5. design-it-twice — the architect's selection prompt routes to its skill, while the three
    #    comparison axes live in that rendered skill (a prompt-construction fact no domain verb can
    #    honestly express without naming the prompt; cf. the worker prompt invariants). The contest
    #    behavior is gated in spec/design-it-twice.md.
    dit_skill = methodology.skill("design-it-twice", REAL).lower()
    ok(_loads_skill(design.SELECT, "design-it-twice")
       and all(ax in dit_skill for ax in ("depth", "locality", "seam placement")),
       "design-it-twice — the selection prompt loads the skill, and the skill single-sources the "
       "depth, locality, and seam-placement axes")

    # 6. schedule — the single-writer line the concurrency scenario rests on, proven at the
    #    record-mechanism level: facts the closed scenario vocabulary cannot honestly express — an
    #    exact pathspec, a cross-process flock, slug atomicity, a strict hand-off parse, a crash-
    #    stranded node. The *behavior* (two workers advance, each folds its own delta) is gated in
    #    spec/schedule.md; what no in-process fixture proves is that the line is load-bearing by
    #    construction — remove it, widen the pathspec, or loosen the parse and these go red on the
    #    record itself. (Homing the single-writer-line proof here was the recorded concurrency-home
    #    decision; it dissolved the by-slice residue that carried it.)
    _schedule_invariants()

    # 7. communication — the glossary's shared vocabulary: a self-model content fact no scenario verb
    #    can express. The operator-facing channel's central noun (`thread`) is defined as the throwaway
    #    conversation, and the open `operator view` naming question is flagged honestly rather than
    #    silently settled. communication's *behavior* — the thread, the single voice, the no-raw-leak
    #    archive — is gated in spec/communication.md; the glossary's *content* is watched here. (Homing
    #    it dissolved the slice-2 residue that carried it.)
    glossary = spec.read_spec(REAL).glossary
    ok("throwaway conversation" in glossary,
       "communication — the glossary defines thread as the operator's throwaway conversation")
    ok("Open question: the name" in glossary,
       "communication — the glossary flags the open 'operator view' naming question, not silently settled")

    # 7b. the clarity standard — communication's *clear* quality: a WATCHED standard carried in the
    #     architect's loaded skill, never a gated readability metric (the folding condition the
    #     communication-clarity ask owes). The standard's prose is watched in spec/communication.md (the
    #     compression-to-a-shared-decoder spine, the working-memory load test); that it reaches the
    #     architect's skill and stays
    #     watched-not-gated is the structural fact the closed scenario vocabulary cannot say — asserted
    #     here, from outside, never faked as an in-spec block.
    comm_skill = methodology.skill("communication", REAL)
    ok("communication" in methodology.METHODOLOGIES,
       "communication — the clarity standard is registered as the architect's loaded skill")
    ok("compression" in comm_skill and "working memory" in comm_skill
       and "readability metric" in comm_skill,
       "communication — the skill carries the clarity discipline: compression to a decoder the one reader "
       "already runs, the working-memory load test, and no gated readability metric")
    comm_cls = dict(scenario.classification("communication", REAL))
    clear = [r for r in comm_cls if "clear" in r.lower()]
    ok(bool(clear) and all(comm_cls[r] == "watched" for r in clear),
       "communication — clarity is WATCHED, held by judgment, never a gated readability metric")

    # 7c. writing-for-the-machine — the machine-facing mirror of the clarity standard: a WATCHED
    #     discipline carried in the shared loaded skill, with one mechanical aid — a non-blocking signal
    #     over the spec's own prose (the length tripwire's idiom, pointed at writing). The discipline is
    #     watched in spec/writing-for-the-machine.md; that it registers, reaches the skill, stays watched,
    #     and that its signal fires on a planted construct yet never gates are the structural facts the
    #     closed scenario vocabulary cannot say — asserted here from outside, never a faked in-spec block.
    wm_skill = methodology.skill("writing-for-the-machine", REAL)
    ok("writing-for-the-machine" in methodology.METHODOLOGIES,
       "writing-for-the-machine — the machine-writing standard is registered as a shared loaded skill")
    ok("one instruction per sentence" in wm_skill and "say what to do" in wm_skill and "one pass" in wm_skill,
       "writing-for-the-machine — the skill carries the core discipline: write for the one-pass reader, "
       "one instruction per sentence, say what to do")
    wm_cls = dict(scenario.classification("writing-for-the-machine", REAL))
    ok(bool(wm_cls) and all(k == "watched" for k in wm_cls.values()),
       "writing-for-the-machine — the prose discipline is WATCHED throughout, never a gated readability "
       f"metric ({len(wm_cls)} requirements, all watched)")
    ok(bool(machine_writing.flags("This sentence has " + "padding word " * 60 + "in it.")),
       "writing-for-the-machine — the signal detects an over-long sentence (the instruction-density cliff)")
    ok(any(f.kind == "compound negation" for f in machine_writing.flags("It is never a veto and never a pass.")),
       "writing-for-the-machine — the signal detects a compound negation")
    ok(any(f.kind == "mid-clause reference" for f in machine_writing.flags("the scan (ADR 0020) reads the flags")),
       "writing-for-the-machine — the signal detects a provenance reference off the line-end")
    ok(not machine_writing.flags("The architect names the actor and states the act. The reference rides at the line-end. (ADR 0005)."),
       "writing-for-the-machine — clean prose raises no flag, so the signal is a prompt to look, never noise")
    prompts = (
        ("communication.SYSTEM", communication.SYSTEM, "communication"),
        ("communication.COHERENCE", communication.COHERENCE, "coherence"),
        ("communication.EXPLAIN", communication.EXPLAIN, "communication"),
        ("grill.FLOOR", grill.FLOOR, "grilling"),
        ("grill.PRODUCTS", grill.PRODUCTS, "grilling"),
        ("design.SELECT", design.SELECT, "design-it-twice"),
    )
    ok(all(_loads_skill(prompt, skill) for _, prompt, skill in prompts),
       "writing-for-the-machine — each per-episode architect prompt names and instructs loading its "
       "corresponding skill ("
       + ", ".join(f"{name}→{skill}" for name, _, skill in prompts) + ")")
    for line in machine_writing.advisory(REAL):                # the live, non-gating signal over the real spec
        print(line)

    # 8. channels — the derived-channel registry's exact composition: a structural fact the closed
    #    scenario vocabulary cannot honestly express (it names the engine's `CHANNELS` tuple, not a
    #    domain noun). channels' *behavior* — the fold re-renders every channel from its source, the
    #    skill is single-sourced, the anchor is minimal, the materialized channels conform and resolve —
    #    is gated in spec/channels.md; what no in-spec block can say is that the registry IS the one flat
    #    fold-driven set and that the anchor and its bridge are registered beside the skills, so a
    #    dropped or duplicated channel goes red here on the registry itself.
    ok(len(channels.CHANNELS) == len(methodology.METHODOLOGIES) * len(methodology.SKILL_DIRS) + 2,
       "channels — the registry is one flat fold-driven set: every capability skill per mirrored "
       "location, plus the anchor and its CLAUDE.md bridge")
    ok(anchor.materialize in channels.CHANNELS and anchor.bridge_materialize in channels.CHANNELS,
       "channels — the anchor and its bridge are registered in the channels registry beside the skills")

    # 9. audit — the standing drift sweep over hypercore's OWN committed tree (engine/audit.py): the
    #    coherence sibling of section 4's depth scan, proven from outside a fold like build_reaches_main.
    #    These are facts about the committed artifact, not a behavior over a fixture, so no in-spec block
    #    can say them: channels' gated scenarios prove the render *mechanism*, never that the *committed*
    #    SKILL.md was actually re-rendered after its source last moved — exactly the gap that let two
    #    skills go stale while the scenario gate stayed green. A hand-driven fold that skips the render or
    #    the archive move now goes red here, on the live tree itself.
    drift = audit.channel_drift(REAL)
    ok(not drift,
       "audit — every committed derived channel matches a fresh render from the live spec"
       + ("" if not drift else f": DRIFTED {', '.join(drift)} — run channels.materialize() to reconcile"))
    violations = audit.tree_hygiene(REAL)
    ok(not violations,
       "audit — every execution-tree folder carries its intent.md and no work/archive container is empty"
       + ("" if not violations else f": {'; '.join(violations)}"))


# ── the schedule single-writer-line and failure-recovery invariants, exercised from outside ──

def _inv_root() -> str:
    r = tempfile.mkdtemp(prefix="scenario-schedule-inv-")
    for c in (("init", "-q"), ("config", "user.email", "inv@hypercore"), ("config", "user.name", "inv")):
        subprocess.run(["git", *c], cwd=r, check=True, stdout=subprocess.DEVNULL)
    os.environ["ENGINE_ROOT"] = r
    return r


def _schedule_invariants() -> None:
    from .. import delta, record
    from ..transport import MalformedReply
    prev = os.environ.get("ENGINE_ROOT")
    try:
        # exact-path commits don't sweep a sibling's uncommitted work (the C1 lost-update sweep)
        root = _inv_root()
        a = tree.file_intent("worker A landing its own node")
        tree.atomic_write(os.path.join(root, "work", "sibling-in-flight.tmp"), "worker B's uncommitted change")
        tree.cut(a)                                            # A commits its own act over work/
        tracked = subprocess.run(["git", "ls-files", "work"], cwd=root, capture_output=True, text=True).stdout
        ok("sibling-in-flight.tmp" not in tracked,
           "schedule — a commit stages exactly its own act's files: a sibling's uncommitted file is not swept in (single-writer, C1)")

        # the line is a real cross-holder lock spanning the act, not a thread-only nicety
        entered, release, second_in = threading.Event(), threading.Event(), threading.Event()

        @record.serialized
        def hold_line():
            entered.set(); release.wait(timeout=5)

        @record.serialized
        def second():
            second_in.set()

        t1 = threading.Thread(target=hold_line, daemon=True); t1.start(); entered.wait(timeout=5)
        t2 = threading.Thread(target=second, daemon=True); t2.start()
        blocked_while_held = not second_in.wait(timeout=0.5)
        release.set(); entered_after = second_in.wait(timeout=5); t1.join(timeout=5); t2.join(timeout=5)
        ok(blocked_while_held and entered_after,
           "schedule — the line serializes a second holder: it cannot enter the record until the first releases (the flock is load-bearing)")

        # two workers fold the SAME spec file under overlap — both land, neither sweeps the other
        root = _inv_root()
        tree.atomic_write(os.path.join(root, "spec", "shared.md"), "# shared\n\nA capability two workers grow at once.\n")
        tree.commit([os.path.join(root, "spec", "shared.md")], "seed: the shared capability")
        gate = threading.Event()

        def fold_req(tag: str):
            gate.wait(timeout=5)
            delta.fold(delta.parse(
                f"# delta — grow shared with {tag}\n\n## ADDED — shared\n"
                f"### Requirement: the {tag} property holds\nThe {tag} property MUST hold.\n"
                f"#### Scenario: s\n- WHEN x\n- THEN y\n"))

        ths = [threading.Thread(target=fold_req, args=(t,), daemon=True) for t in ("first", "second")]
        for t in ths:
            t.start()
        gate.set()
        for t in ths:
            t.join(timeout=10)
        cap = spec.read_spec(root).capability("shared")
        names = {r.name for r in cap.requirements} if cap else set()
        ok({"the first property holds", "the second property holds"} <= names,
           "schedule — two workers folding the SAME spec file both land their requirement — neither fold overwrites the other")

        # slug reservation is atomic — N identical-text creations get N distinct folders (the C3 TOCTOU)
        root = _inv_root()
        N, start = 8, threading.Event()

        def create():
            start.wait(timeout=5); tree.raise_card("the worker could not complete the same ask", kind="decide")

        creators = [threading.Thread(target=create, daemon=True) for _ in range(N)]
        for t in creators:
            t.start()
        start.set()
        for t in creators:
            t.join(timeout=10)
        cards = tree.cards()
        ok(len(cards) == N and len({c.id for c in cards}) == N,
           f"schedule — {N} concurrent identical-text creations get {N} distinct folders — no slug collision lost a card (C3)")

        # a malformed model reply is a failure at apply, before coherence — not a silent no-op success (H3)
        root = _inv_root()
        g = tree.file_intent("a worker whose model returns garbage")
        raised = False
        try:
            worker.context(g, root)
            worker.apply(g, transport=lambda _p: "prose carrying none of the envelope's tags", root=root)
        except MalformedReply:
            raised = True
        ok(raised,
           "schedule — a reply with none of the envelope's tags raises at apply, before coherence — never a foldable no-op (H3)")

        # a crash-stranded IN_FLIGHT node with no live worker is recovered on the next step (C2)
        root = _inv_root()
        stranded = tree.file_intent("a node a crash left in flight")
        tree.dispatch(stranded)                               # IN_FLIGHT on disk, no live worker thread
        schedule.Scheduler(transport=lambda _p: "", root=root, limit=0).step()
        rs = tree.find(stranded.id)
        ok(rs is not None and rs.state != tree.IN_FLIGHT,
           "schedule — a crash-stranded in-flight node with no live worker is recovered on the next step (C2)")
    finally:
        if prev is None:
            os.environ.pop("ENGINE_ROOT", None)
        else:
            os.environ["ENGINE_ROOT"] = prev


def _loads_skill(prompt: str, skill: str) -> bool:
    """A prompt-construction watched fact: the prompt names a skill and tells the model to load it."""
    return bool(re.search(rf"\b[Ll]oad\b[^.]*`{re.escape(skill)}` skill", prompt))


# ── a fence with a real engine at two commits: the base and tip differ only in the length signal ──

def _demo_fence(base: int, tip: int) -> str:
    f = tempfile.mkdtemp(prefix="scenario-demo-")
    for c in (("init", "-q"), ("config", "user.email", "demo@hypercore"), ("config", "user.name", "demo")):
        subprocess.run(["git", *c], cwd=f, check=True, stdout=subprocess.DEVNULL)
    for d in ("engine", "spec"):                           # a real, runnable engine + the spec under test
        shutil.copytree(os.path.join(REAL, d), os.path.join(f, d),
                        ignore=shutil.ignore_patterns("__pycache__"))
    _set_signal(f, base); _commit(f, "base")               # HEAD~1 — the behavior not yet built
    _set_signal(f, tip); _commit(f, "tip")                 # HEAD — the tip the worker hands back
    return f


def _set_signal(fence: str, n: int) -> None:
    p = os.path.join(fence, "engine", "conditions.py")
    with open(p, encoding="utf-8") as fh:
        text = fh.read()
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(re.sub(r"^SIGNAL = \d+", f"SIGNAL = {n}", text, count=1, flags=re.MULTILINE))


def _commit(fence: str, msg: str) -> None:
    subprocess.run(["git", "add", "-A"], cwd=fence, check=True, stdout=subprocess.DEVNULL)
    # --allow-empty: the no-transition fence (base == tip) commits an identical tip — a legitimate fixture
    subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", msg], cwd=fence, check=True,
                   stdout=subprocess.DEVNULL)


def _drop(path: str) -> None:
    shutil.rmtree(path, ignore_errors=True)
