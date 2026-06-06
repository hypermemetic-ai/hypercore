# home -- machine statements

the home child node is at `home/`, carrying its own `intent/`; the recursive `check.sh`
reaches it as a node.
mounted projects live as symbolic links at `home/<name>` pointing to distinct git
repositories outside the hypercore root.
a linked mounted project is a child node when the link target has `intent/`; broken links
and links to non-nodes do not materialize child-node content.
`bin/home greenfield <name> <target-path>` creates the target's local node shape and mount
link, with no copy of root `hypercore.md`, `check.sh`, `adapter/`, `bin/`, or `AGENTS.md`.
