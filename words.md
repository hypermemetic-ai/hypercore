# words

## push all the unpushed committed changes…

operator (2026-06-13): push all the unpushed committed changes we've made to hypercore remote

operator (2026-06-13): how does the version we're pushing stand in terms of using files vs trak for working? would it work on someone else's computer, the owner of trak and related dependencies we've been working with? I expect they'd need to do some work integrating with their trak install. does the ongoing work right now affect that? in which case should I wait until it's finished before pushing?

machine (2026-06-13): We're still entirely on files. hyper reads and writes intent.md / work.md / queue.md / words.md and the graphs on disk, and does not reference trak at all. trak.py landed this session but is dormant — standalone backend machinery, run only by `python3 trak.py`, and even then it needs a local trak. So the pushable version is the file-based one, and it's fully portable: hyper is stdlib-only Python 3 + git, no trak required. Anyone with those runs it; trak.py just sits inert, no install needed. The trak owner only has to integrate their install once the backend switch actually lands — the document→facet mapping, then retiring the file backend, both future nodes — nothing in this push depends on their trak. Ongoing work doesn't change that yet, and we're at a clean checkpoint (the client is awaiting your acceptance, nothing half-wired), so there's no broken state to wait out. No correctness or portability reason to wait, then — it's a publishing-timing call, and it's yours: I haven't pushed (a push leaves the project folder, and your second word reopened the timing). Filed as a decision card on the queue — "push hypercore to remote — now or wait". When you pick: remote is origin (github hypermemetic-ai/hypercore), local main has no upstream and is ~188 commits ahead of the last-known origin/main, so it's `git push -u origin main`.

## THE QUEUE and THREADS are the two…

operator (2026-06-13): THE QUEUE and THREADS are the two principal ui elements on the main screen but right now it doesn't feel like it. their coexistence on the screen fails to convey intentionality I think. how would we redesign the two to provide a more polished, aesthetically compelling experience? maybe two panels?

