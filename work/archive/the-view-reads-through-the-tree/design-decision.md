# design-it-twice (light): the view's path to the work tree [machine]

A load-bearing interface — how the operator view reaches the durable work tree — was designed twice,
candidates parameter-threaded and engine-context, each compared on depth, locality, and seam
placement. It is load-bearing because `read_tree` is the system's one reader of the work tree, and
every view-layer reader (the gap, the live status) rides whatever path it exposes. The bug being
fixed is precisely a second reader (`view._open_work`) that grew because the one reader took no root,
so the harness-rooted view had no path but to re-walk the disk itself.

design-decision: the view's path to the work tree → read_tree(root=None) (the parameter-threaded reader) — the one work-tree reader gains an optional `root` threaded through `_scan`, matching the root-threading idiom every view-layer reader already follows (`operator_view(root)`, `spec.read_spec(root)`, `review.review(root)`), so the view consumes `tree.read_tree(root)` and no second walker survives; backward-compatible — every existing caller keeps the default `_root()`.

## Grounds

- **parameter-threaded `read_tree(root=None)` (chosen)**: `read_tree` gains an optional `root`, threaded one level into `_scan`'s base path; the default resolves to `_root()` exactly as today. Deepest on locality — the change is confined to one signature and the view's consumption of it; no other caller moves. Seam placement is right: the root already crosses into the view layer as an explicit parameter (`operator_view(root)`, `spec.read_spec(root)`, `review.review(root)`, `scenario.classification(name, root)`), so this reader simply joins an idiom the view layer already speaks. Depth is preserved — the view hides "how the work tree is laid out and what counts as folded" behind one reader again, instead of leaking it into a second walker. The deletion test passes: `view._open_work` / `_done` / `_intent_subject` and the `os.walk` + git shell-out all delete with nothing left behind.
- **engine-wide context (rejected)**: thread the root through one context object every engine reader consults, set once by the caller. Rejected on locality and seam placement: it is a cross-module refactor (every reader retrofitted to read a context) to solve a problem one optional parameter solves, and it fights the established idiom — every view-layer reader already takes an explicit `root`, so a context would be a *second* way to say the same thing, the very duplication this item removes. Shallow for this decision: a large interface for a small need, no behavior the parameter cannot already express.
