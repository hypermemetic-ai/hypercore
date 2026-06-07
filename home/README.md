# home - mount point

The home node is the mount surface for linked project nodes. Each mounted project is a
distinct git repository outside the hypercore root, exposed here by a symbolic link at:

    home/<name>

Create the first local shape and mount link with:

    bin/home greenfield <name> <target-path>

The target receives its own `intent/organizing-document.md` and root-managed direct-path
entrypoint symlinks: `AGENTS.md` points to the mounted-node Codex entrypoint, and
`signoff` points to the home signoff helper. The root methodology prose, root check
script, adapter directory, bin directory, and root `AGENTS.md` are not copied. Direct-path
work resolves the target's mount path through `bin/home resolve`, then routes back to the
governing root adapter and loop; local target checks are proof only when they exist.

The home currently mounts `codex-cockpit`. A valid link whose target carries `intent/` is
a node the recursive `check.sh` reaches; broken links and links to non-nodes are not
materialized child nodes.
