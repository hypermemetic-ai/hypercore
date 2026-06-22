# hypercore — the operating anchor

**Working *on* hypercore** — a person, or a coding assistant editing this repo — rather than running as the system's own architect or worker? This file is not your instructions: read `README.md`, then `intent.md` and `spec/`; run the acceptance harness with `python3 -m hyper --check` and the operator interface with `python3 -m hyper`. The rest below is the runtime **role anchor** — the minimal always-on context the system loads into the architect and the fenced worker. It is deliberately minimal: only the non-inferable operational lines, with the specialization in the skills and the living spec, not here.

## Operating (the runtime roles)

- **Check.** Run the acceptance harness before handing back: `python3 -m hyper --check`. It is the red→green feedback loop; nothing folds that does not pass it.
- **Build, and hand back for the machine.** Build behind that loop and hand back a complete result written for the machine, never for the operator — the architect authors every operator-facing word.

## Skills — the specialization, loaded on demand

Load the one the task in front of you routes to (`skills/<name>/SKILL.md`):

- `depth` — hypercore's depth disciplines — build deep modules (a lot of behavior behind a small interface) and avoid the red flags of shallowness.
- `design-it-twice` — hypercore's design-it-twice methodology — design a load-bearing interface as a contest of isolated candidates, then pick or hybridize on depth, locality, and seam placement.
- `architecture-review` — hypercore's architecture-review methodology — the standing scan that keeps the system deep, surfacing god-files-in-the-making by the length signal against the depth-decision record.
- `grilling` — hypercore's grilling methodology — turn a filed ask into a ratified contract and spec delta by resolving what the spec and intent already settle and surfacing only the stake-bearing residue, one question at a time, each with a lean and a flip.
- `coherence` — hypercore's coherence methodology — the archive-gate judgment over a worker's hand-off: check it against the contract at the operator's altitude (not a code review) and against the depth bar, folding on a pass and raising a decision otherwise.
