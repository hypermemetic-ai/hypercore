# hypercore

hypercore is a small system for a human and an agent to think with together.

## Epoch 2 — reset 2026-06-10

The operator burned the first epoch: the engine (~2,600 lines), the viewer,
the database, the snapshots, all work graphs — deleted in one commit,
recoverable forever in git history. What survived is intent.

- **intent.md** — the system. One document (foundations, structure,
  statements, endorsement, work), edited directly, every change committed
  with plain-words grounds. A statement ending ` [machine]` carries no
  operator endorsement yet; only the operator's word drops the marker.
- **hyper** — the operator's interface. One python file, stdlib, keyboard
  only. Home is the queue: decisions and slices awaiting acceptance, each
  a card. Decision cards carry context and what each pick entails;
  approve / cut / explain land on disk and commit in the operator's name
  before the screen redraws. Acceptance cards show what a slice does and
  how to try it; a accepts in one act, and speech is for reservations.
  s speaks from anywhere, the place travels with the words, and speaking
  summons the machine — the answer lands while the operator watches.
  m summons for stragglers and whenever the record is behind. w shows
  open work; j/k move across cards, j previous and k next.
- **queue.md / words.md / work.md** — the ledgers behind the views:
  decision cards, open exchanges, open work. Machine-maintained;
  the operator only reads and decides.
- **machine** — the one visible setting: the command a summon runs,
  {prompt} standing for the instruction. claude today; codex or any
  harness that takes a prompt slots in by editing one line. brief.md is
  written fresh at every summon for any harness to read.
- **hyper.desktop / hyper.ghostty** — the launcher: ghostty opens hyper
  fullscreen at login, high contrast, IBM Plex Mono, one color (red)
  reserved for "the record is behind" — and the red line ends with its
  own way out. Every flash also lands in .hyper.log, so an error
  outlives the screen; the fullscreen request retries until the window
  manager confirms it took.

The conversation with the machine is disposable; the repo is the state.
