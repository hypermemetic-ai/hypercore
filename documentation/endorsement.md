# endorsement

ownership is read off an endorsement: an endorsed statement is the operator's, an unendorsed one is the machine's.
the machine never endorses, so everything unendorsed is the machine's and the machine is the floor.
endorsement does not cross a node boundary: the operator endorses the contract in the parent and the child's whole operator set in the child, as two separate acts, and the floor is per node.
endorsement is per segment: one operator stands behind the segment's whole operator set, not only the statements they last touched.
to change a segment is to take its whole operator set on, having read it and able to reason about it as a whole.
a segment's endorsement is a single line at the foot of its intent document.
there is no partial endorsement and no handover step: you own the operator set or you do not.
the relief for an over-large operator set is to split the segment or demote statements to `## machine`, not a finer endorsement.
a change carries one endorsement: the operator's vouch for every segment it touches.
on archive, a change's endorsement stamps the foot of each touched segment with this operator.
a segment whose change goes unendorsed falls to the machine.
ownership and truth are separate backings: the endorsement says who stands behind the set, a check says each statement holds.

## machine
a segment's foot endorsement is a `---` rule followed by a line reading `endorsed by <operator>`.
a change's endorsement is the file endorsement.md in the change folder.

---
endorsed by abacus-git
