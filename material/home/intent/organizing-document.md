# organizing document -- home

home is a child node of the hypercore root, materializing the root's `home` segment: the
home mounts the operator's project nodes and governs them within itself.
This node holds its own corpus, divided into one segment to start:

- **mounting** -- how an external project node mounts through a link as a distinct git
  repository and child node, and how the recursive check reaches it.

Each segment has an intent document at `intent/<segment>.md` and a machine-statements file
at `intent/machine-statements/<segment>.md`. The `mounting` segment is leaf-materialized by
`material/` -- the mount point each project link mounts into as a child node of this home
at `material/<name>/`. The home holds zero mounted projects yet.

One group, one segment: nothing is partitioned twice. A second segment is added the first
time a real concern of the home's -- cross-project governance, say -- forces it, not before.
