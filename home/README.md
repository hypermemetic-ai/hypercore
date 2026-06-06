# home - mount point

The home node is the mount surface for linked project nodes. Each mounted project is a
distinct git repository outside the hypercore root, exposed here by a symbolic link at:

    home/<name>

Create the first local shape and mount link with:

    bin/home greenfield <name> <target-path>

The target receives only its own `intent/organizing-document.md`. The root methodology,
root check script, adapter directory, bin directory, and root `AGENTS.md` are not copied.
Work through the mount path when the node needs to inherit the root methodology.

The home holds zero mounted projects until the operator mounts the first. A valid link whose
target carries `intent/` is a node the recursive `check.sh` reaches; broken links and
links to non-nodes are not materialized child nodes.
