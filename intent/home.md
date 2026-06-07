# home

home is the named child node that mounts the operator's project nodes and governs them
within itself.
home is a durable child node of the root at `home/`, with its own `intent/`.
the root home contract binds only the named `home` child.
the root active-work contract governs root child work generally; home is not the universal
container for root-directed work.
root-directed active work lives directly under the root as a sibling to `home`.
home's mount surface is `home/`; each mounted project is reached at `home/<name>` through
a symbolic link to a distinct git repository outside the hypercore root.
when a mount link target has `intent/`, the mount is a child-node entry point the
recursive check reaches; broken links and links to non-nodes are dormant.
an unmounted project is absent; hypercore does not fabricate placeholder child-node
content.
home may stay active indefinitely.
`bin/home greenfield <name> <target-path>` creates a new external project repository with
its local node shape, root-managed direct-path entrypoint links, and a link under home; it
refuses path-like names, existing mount paths, non-empty targets, and targets inside the
hypercore root.

## machine
the home child node is at `home/`, carrying its own `intent/`; the recursive `check.sh`
reaches it as a node.
mounted projects live as symbolic links at `home/<name>` pointing to distinct git
repositories outside the hypercore root.
a linked mounted project is a child node when the link target has `intent/`; broken links
and links to non-nodes do not materialize child-node content.
`bin/home greenfield <name> <target-path>` creates the target's local node shape, writes
target-local `AGENTS.md` and `signoff` links to root-managed direct-path entrypoints, and
creates the mount link, with no copy of root `hypercore.md`, `check.sh`, `adapter/`,
`bin/`, or root `AGENTS.md` entry point.

---
endorsed by qqp-dev
