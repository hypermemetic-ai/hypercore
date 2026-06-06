# hypercore

How operator and machine ship code together — a lot of it, kept coherent over time.

The methodology itself lives in [`hypercore.md`](hypercore.md). Read it first.

This repository is **hypercore applied to itself**. It has one reserved tree:

- `intent/` — the falsifiable statements about what hypercore must be, divided into segments (see [`intent/organizing-document.md`](intent/organizing-document.md)).

Everything else beside `intent/` is node-local material: the methodology prose (`hypercore.md`), `check.sh`, the adapter, active work nodes, durable child nodes such as `home/`, and mounted child nodes. `check.sh` re-runs the structural statements against the root and every current child node.

The intent is the abstract contract — what hypercore must *be*. The material is the concrete artifact you read and run. They are distinct, and the material is held true against the intent by checks.

**Work and mounted material nest as child nodes.** A child under hypercore is not a new kind of thing — it is a *node*, the same reserved `intent/` tree plus node-local material, living at `<name>/` or reached through a settled mount path. Parent intent statements define their own reach, and any parent segment that houses a child states the contract the child must satisfy. The sweep reads across the boundary. The recursion holds to any depth. `home` is a durable child node for linked mounted project nodes, not the universal container for root-directed work.

hypercore governs its own evolution. Work runs the loop — orient, frame, implement, check, archive. Active root-directed work lives directly under the root as `<NNN-slug>/`; legacy change records under `intent/changes/` and `intent/history/change-folders/` remain readable history of the retired change abstraction.

Run the structural checks:

```bash
./check.sh
```

**Lineage.** hypercore is the distilled successor to *portable-core* (the Contract Loop). It keeps the essence — intent as falsifiable statements, the loop, the sweep, ownership read off an endorsement, drift as a check that falls — and drops the accumulated mechanism.
