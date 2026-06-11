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
  only. Home is the queue of decisions; cards carry context and what each
  pick entails; approve / cut / explain land on disk and commit in the
  operator's name before the screen redraws; s speaks from anywhere and
  the place travels with the words; w shows work in flight.
- **queue.md / words.md / work.md** — the ledgers behind the views:
  decision cards, open exchanges, work in flight. Machine-maintained;
  the operator only reads and decides.
- **hyper.desktop / hyper.ghostty** — the launcher: ghostty opens hyper
  fullscreen at login, high contrast, IBM Plex Mono, one color (red)
  reserved for "the record is behind".

The conversation with the machine is disposable; the repo is the state.
