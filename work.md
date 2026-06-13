# work

## push hypercore to remote — now or wait

- ask: you asked to push, then reconsidered — should you wait until the trak work is finished? You're still entirely on files: hyper reads and writes intent.md / work.md / queue.md / words.md and the graphs on disk and does not reference trak; trak.py landed and is dormant. So the current version is fully portable (Python 3 + git, no trak required), trak.py just rides along inert, and we're at a clean checkpoint — nothing half-wired ships. No correctness or portability reason to wait; the trak owner only integrates their install once the backend switch actually lands (the document→facet mapping, then retiring the file backend, both future). So it's a publishing-timing call — and since a push leaves the project folder, it's yours.
- options: push now — publish the file-based, portable hypercore to origin/main, trak.py dormant alongside it; `git push -u origin main` (local main has no upstream and is ~188 commits ahead of the last-known origin/main) . wait until the trak switch lands — hold the push until hyper actually reads and writes trak, so the first published version is the trak-backed one
- state: awaiting your decision
- since: 2026-06-13
- blocks: nothing in the work depends on it — the only cost of waiting is origin staying behind the local epoch-2 history, and anyone with the repo not seeing the current state.
