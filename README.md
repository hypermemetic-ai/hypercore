# hypercore

How operator and machine ship code together — a lot of it, kept coherent over time.

The methodology itself lives in [`material/hypercore.md`](material/hypercore.md). Read it first.

This repository is **hypercore applied to itself**. It is two trees:

- `intent/` — the falsifiable statements about what hypercore must be, divided into segments (see [`intent/organizing-document.md`](intent/organizing-document.md)).
- `material/` — the code and child nodes that materialize the intent: the methodology prose (`hypercore.md`), `check.sh`, the adapter, active work nodes, and durable child nodes such as `material/work-home/`. `check.sh` re-runs the structural statements against the root and every child node.

The intent is the abstract contract — what hypercore must *be*. The material is the concrete artifact you read and run. They are distinct, and the second is held true against the first by checks.

**Work and mounted material nest as child nodes.** A child under hypercore is not a new kind of thing — it is a *node*, the same two trees governed by the same loop, living at `material/<name>/`. Parent intent statements define their own reach, and any parent segment that houses a child states the contract the child must satisfy. The sweep reads across the boundary. The recursion holds to any depth. `work-home` is a durable child node for mounted operator work, not the universal container for root-directed work.

hypercore governs its own evolution. Work runs the loop — orient, frame, implement, check, archive. Active root-directed work lives directly under `material/`; legacy change records under `intent/changes/` and `intent/history/change-folders/` remain readable history of the retired change abstraction.

Run the structural checks:

```bash
./material/check.sh
```

**Lineage.** hypercore is the distilled successor to *portable-core* (the Contract Loop). It keeps the essence — intent as falsifiable statements, the loop, the sweep, ownership read off an endorsement, drift as a check that falls — and drops the accumulated mechanism.
