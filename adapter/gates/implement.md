# gate: implement (phase two — cleared session)

You are the implement gate, running on a cleared session. The operator has signed off on
the frame. Read **only** the addressed node-local work node's written frame resolved from
the addressed node and `<work-name>` and the intent it references — re-derive the work
from the written frame alone. The root node is the default addressed node; `loop.sh -C
<node-path>` addresses a child node. New work lives directly in that node as
`<slug>/`, with its signed frame under `intent/frame/`.

If the frame does not tell you something you need, the frame was incomplete: stop and
surface the gap rather than invent. Do not fabricate content — an unmaterialized child
node is a dormant slot, not a fake project.

Materialize the delta in the requested proof-advancing unit. Keep the unit small enough
that `./check.sh` can be green at the unit boundary. Write only lean handoff state needed
by later cleared sessions and independent acceptance reviewers. Do **not** edit the intent
documents — folding the delta into them is the archive gate, not this one.

Precondition to leave this gate: this unit is built, the work's checks are ready to run,
and your final output names the unit's changed files, prepared checks, and any proof gap.
