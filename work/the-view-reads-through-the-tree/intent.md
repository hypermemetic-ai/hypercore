---
kind: ask
state: standing
owner: operator
created: 1782576911
---
The operator view reads through the tree API — root-parameterize the one tree reader and route the view through it, so "open work" and "folded" each have a single definition instead of two that disagree.

`view.py` never calls `tree.read_tree()`. It re-walks raw disk (`os.walk`, view.py:134), re-parses node frontmatter by hand (the `---`-fence parse at view.py:145, now living in two places against `spec.py:11`'s "the one place that knows the on-disk shape"), and shells out to git from inside the presentation layer (`subprocess.run(["git","ls-files","work"])`, view.py:22,111). The two readers already disagree: `tree.work()` is `state in (STANDING, IN_FLIGHT) and not folded` (tree.py:117), while `view._open_work` counts any non-archived node whose state is not `done` (view.py:129-151) — so a non-archived `grilling`/`awaiting` node is excluded by one and surfaced as gap by the other. The root cause is structural: `tree.read_tree()`/`work()`/`standing()` take no `root` (tree.py:72), hardwired to `_root()`, so the harness-rooted view had no path but to re-derive the tree itself.

A second defect rides the same seam: foldedness is encoded twice — the `state:` frontmatter field and the folder location. Location is authoritative (`Node.folded`, tree.py:31), the field advisory; confirmed stale across roughly half the archive (e.g. `work/archive/scenario-gate/intent.md` still says `state: standing`) because the standalone `_fold` relocates a node without touching its state (tree.py:308). The stale field is harmless only until a reader trusts it — and `view._done` does (view.py:150), which is exactly how the first defect bites.

Build it so the tree has one reader. Add `read_tree(root=None)` threading `root` through `_scan`, then delete `view._open_work`/`_done`/`_intent_subject`/`_has_watched_trace`'s hand-walk and have the view consume `Node` objects. That single change collapses the duplicate reader, removes both layering leaks (the git shell-out and the `os.walk`), eliminates the open-work divergence, and makes `Node.folded` the only arbiter of foldedness — neutralizing the stale `state:` field rather than trusting it.

To surface in grilling: whether the stale `state:` field is normalized at fold (`_fold` writes the folded state on relocate) or dropped from the schema entirely since location is already authoritative — lean **drop**, one less denormalized copy to drift, since `Node.folded` ignores it anyway; whether `read_tree(root=None)` is the right seam or `root` should thread through a context the whole engine shares; and that no second walker of the work tree survives the change — the audit's and review's `os.walk` are over different trees (`audit.py:91` over folders missing `intent.md`, `review.py:206` over the engine source) and correctly stay.
