# work-home

work-home is the named child node that mounts the operator's work folders -- typically
projects -- and governs them within itself.
work-home is a durable child node of the root at `material/work-home/`, with its own
`intent/` and `material/`.
the root work-home contract binds only the named `work-home` child.
the root active-work contract governs root child work generally; work-home is not the
universal container for root-directed work.
root-directed active work lives directly under root `material/` as a sibling to
`work-home`.
the home mounts the operator's work folders and governs them within itself; it holds zero
until the operator mounts the first.
each mounted work folder is a child node of work-home and governs itself in its own corpus.
an unmounted work folder is absent; hypercore does not fabricate placeholder child-node
content.
work-home may stay active indefinitely.

## machine
the work-home child node is at `material/work-home/`, carrying its own `intent/` and
`material/` trees; the recursive `check.sh` reaches it as a node.
mounted work folders live under `material/work-home/material/<name>/` when checked out.

---
endorsed by qqp-dev
