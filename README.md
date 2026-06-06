# hypercore

How operator and machine ship code together — a lot of it, kept coherent over time.

The methodology itself lives in [`implementation/hypercore.md`](implementation/hypercore.md). Read it first.

This repository is **hypercore applied to itself**. It is two trees:

- `documentation/` — the **intent**: falsifiable statements about what hypercore must be, divided into segments (see [`documentation/organizing-document.md`](documentation/organizing-document.md)).
- `implementation/` — the **code** that materializes the intent: the methodology prose (`hypercore.md`), `check.sh`, and the **governed projects** that mount here as child nodes (for now just `implementation/project-home/`, dormant). `check.sh` re-runs the structural statements against the root and every child node.

The intent is the abstract contract — what hypercore must *be*. The implementation is the concrete artifact you read and run. They are distinct, and the second is held true against the first by checks.

**Projects nest as child nodes.** A project under hypercore is not a new kind of thing — it is a *node*, the same two trees governed by the same loop, living at `implementation/<name>/`. The parent names it with a contract segment at `documentation/<name>.md`; the child's intent must satisfy that contract, and the sweep reads across the boundary. The recursion holds to any depth. hypercore ships with the mechanism in place and one dormant slot — `project-home`, the home your projects mount into. It holds nothing yet; it comes online the moment you open the first change against it.

hypercore governs its own evolution. Every change to it runs the loop — orient, frame, implement, check, archive. The founding change is [`documentation/changes/archive/001-bootstrap-hypercore/`](documentation/changes/archive/001-bootstrap-hypercore/).

Run the structural checks:

```bash
./implementation/check.sh
```

**Lineage.** hypercore is the distilled successor to *portable-core* (the Contract Loop). It keeps the essence — intent as falsifiable statements, the loop, the sweep, ownership read off an endorsement, drift as a check that falls — and drops the accumulated mechanism.
