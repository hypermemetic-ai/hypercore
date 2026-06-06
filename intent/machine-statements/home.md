# home -- machine statements

the home child node is at `material/home/`, carrying its own `intent/` and `material/`
trees; the recursive `check.sh` reaches it as a node.
mounted projects live as symbolic links at `material/home/material/<name>` pointing to
distinct git repositories outside the hypercore root.
a linked mounted project is a child node when the link target has both `intent/` and
`material/`; broken links and links to non-nodes do not materialize child-node content.
`material/bin/home greenfield <name> <target-path>` creates the target's local node shape
and mount link, with no copy of root `material/hypercore.md`, `material/check.sh`,
`material/adapter/`, or `AGENTS.md`.
