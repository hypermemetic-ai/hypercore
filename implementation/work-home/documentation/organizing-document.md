# organizing document — work-home

work-home is a child node of the hypercore root, materializing the root's `work-home`
segment — its contract: the home mounts the operator's work folders and governs them within
itself. This node holds its own corpus, divided into one segment to start:

- **mounting** — how a work folder mounts (a distinct git repository, a submodule) and is
  governed (within itself), and how the recursive check reaches it.

Each segment has an intent document at `documentation/<segment>.md` and a machine-statements
file at `documentation/machine-statements/<segment>.md`. The `mounting` segment is
leaf-materialized by `implementation/` — the mount point each work folder mounts into, as a
child node of this home at `implementation/<name>/`. The home holds zero work folders yet.

One group, one segment: nothing is partitioned twice. A second segment is added the first
time a real concern of the home's — cross-project governance, say — forces it, not before.
