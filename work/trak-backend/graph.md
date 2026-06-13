# graph: trak-backend

## switch hypercore's document backend to trak

- ask: from the operator's words (2026-06-13): switch hypercore's document backend from filesystem I/O to trak (hypermemetic's plexus-trak, a Plexus RPC facet store), through a direct and fast JSON-RPC client rather than the synapse CLI; it works today against a locally hosted trak and later a network-hosted one. trak is not the project — the switch is, and it is non-trivial.
- check: hypercore's documents — intent, the work graphs, the queue, the exchanges — live in trak as facets and are read and written through the direct client; the interface and a summoned session operate against a local trak with the operator seeing no loss, and the same client reaches a network server by configuration alone; the filesystem backend is retired only once trak carries the full state with no lingering doubt.
- state: open
- since: 2026-06-13
- of: hypercore

## survey trak's model, surface, and the standing-up cost

- op: check
- ask: pull hypermemetic's trak and read enough to ground the switch — its data model, its RPC surface, its transport and auth, and what a local server costs
- check: the facet model and the facet-activation methods are written down, the wire and auth are named, and the local-standup footprint is known well enough to put the first decision to the operator
- result: pulled to ~/projects/plexus-trak this session, unregistered — trak is a dependency, not a linked project. trak's primitive is the facet (id, parent_id, title, body, free-text status, owner, meta{priority,tags,extra}, timestamps) joined by four typed edges (depends_on, blocks, relates_to, duplicates); containment is parent_id, not an edge. This is hypercore's own model — nodes, relations, material on nodes — almost one-to-one. Facet methods: create/get/update/delete/move_to/list/tree/link/unlink/links/blocked/search/grep, plus checkout/diff/flush (a markdown round-trip to disk) and import_plans; a discuss activation gives threaded markdown comments on a facet. Wire: Plexus streaming JSON-RPC 2.0 over WebSocket on :44107, responses newline-delimited event envelopes ({type:data}…{type:done}); state in SQLite at ~/.config/trak/trak.db. Auth: OIDC/RS256 — short-lived tokens from plexus-idp (:4460/:4461), no shared secret. Standing-up cost is real: nothing listens locally, no synapse, no creds, and plexus-trak builds only against the whole plexus workspace (path deps on plexus-core/-macros/-transport/-auth-core) plus plexus-idp to issue tokens.
- state: done
- since: 2026-06-13
- of: switch hypercore's document backend to trak

## the foothold is the operator's: where today's local trak comes from

- op: decide
- ask: nothing serves trak locally and the build pulls in the whole plexus workspace plus plexus-idp; whether to stand that full stack up here or target a trak the operator already runs is a resource call only they can settle. the card stands in work.md.
- check: the card settles; with a reachable trak the next seams open — the client's shape, then the document→facet mapping — each surfaced as its own decision before its material exists
- state: awaiting your decision
- since: 2026-06-13
- of: switch hypercore's document backend to trak

## the client is generated, not hand-written: synapse-cc

- op: decide
- ask: the operator steered the client's shape (2026-06-13, words.md): use synapse-cc for client generation. synapse-cc (in hypermemetic-ai/synapse, pulled to ~/projects/synapse) is Plexus's build-time client compiler — live schema → IR → hub-codegen renders a typed client written into hyper; at runtime that client talks JSON-RPC straight to :44107 with no synapse process in the loop (the "direct and fast" path already asked for), the backend url lives in config with per-target override (the root's "network by configuration alone"), and integration mode writes only the generated files and leaves build to the host. The fork: hyper is Python and synapse-cc's proven, exercised target is TypeScript. Its config lists language = typescript | python | rust and the docs sketch a Python client (asyncio + websockets, dataclasses/Pydantic), but that sits under "Future Extensions," the renderer hub-codegen is a separate repo not pulled, and every concrete example is TS — Python is declared, not confirmed built. So: (a) if hub-codegen emits a usable Python client, generate and import it — cleanest; (b) if not, add a Python target to hub-codegen, or hand-write a thin client over trak's ~15-method facet surface (cheap; codegen may be more than hyper needs).
- check: with a reachable trak, hub-codegen is confirmed to emit (or not) a usable Python client; the path is chosen and a generated-or-handwritten client connects to :44107 and round-trips a facet
- state: blocked
- blocked-by: the foothold — no live schema to introspect and nothing to test against until a trak listens on :44107; this decision returns through the queue once that card settles
- since: 2026-06-13
- of: switch hypercore's document backend to trak
