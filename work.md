# work

## the trak client

- ask: the trak-backend graph's client step, executed on your decision (option 2 — hand-write, skip codegen). trak.py is a thin, stdlib-only client living in hyper's repo: it speaks Plexus's streaming JSON-RPC over a hand-written WebSocket to trak on :44107, and maps trak's ~13-method facet surface (create/get/update/delete/move_to/list/tree/link/unlink/links/blocked/search/grep) plus login to plain Python methods. No codegen, no third-party dependency — so hyper stays one file, stdlib only when this becomes its document backend.
- try: with trak running on :44107, run `python3 trak.py` from the repo. It logs in, then create → get → update → list → delete against the live trak, printing each step and a final ROUND-TRIP line — it printed PASS this session. No interface change, so nothing to relaunch; this is backend machinery the next slice (document→facet mapping) will wire hyper onto.
- state: awaiting acceptance
- blocks: the trak-backend graph's forward path — the document→facet mapping, then retiring the filesystem backend — builds on this client; until you accept, it stays machine-owned material and reverts in one git command (rm trak.py). Nothing else in hypercore depends on it.

