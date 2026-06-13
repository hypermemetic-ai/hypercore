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
- state: decided (2026-06-13) — option 2 (operator, settled in hyper, commit 4254a3f): build trak on its single-user path, skip plexus-idp, defer real OIDC to the network phase, confirm writes work before relying on it. The decided card stands in work.md until the machine executes and clears it; execution is the standup node below.
- since: 2026-06-13
- of: switch hypercore's document backend to trak

## stand up a local trak on :44107, single-user, and confirm a write

- op: do
- ask: execute the foothold decision (option 2). Stand up a local trak the work can build against: build the plexus workspace trak needs (plexus-trak + path deps plexus-core/-macros/-transport/-auth-core), run trak on :44107 in its single-user / legacy-HS256 path — the default branch carries the legacy validator, so register a local user → HS256 token, no plexus-idp — and confirm a facet write round-trips. trak's auth branch does not touch the facet RPC surface (identical on both branches), so this standup serves the client and mapping work unchanged; real OIDC is deferred to the network phase per the decision.
- check (acceptance): a trak daemon listens on :44107; under single-user auth a facet create then get round-trips (the operator's own bar — "confirm writes work before relying on it"); the bring-up path is written down so any session can start trak again; then the foothold work.md card is cleared in the executing commit. How to try it: with trak running, a create+get against :44107 returns the same facet.
- progress (2026-06-13): the workspace is cloned and ready — plexus-trak (on its default branch feature/AUTHZ-TENANT-GATE-trak-facets, the legacy-HS256 single-user path) plus its four path deps plexus-core/-macros/-transport/-auth-core, all next to it in ~/projects. The toolchain wall is cleared: the operator decided option 1 (install rustup) and this session installed rustup current-stable into ~/.cargo + ~/.rustup — cargo/rustc 1.96.0 (stable) are usable. Toolchain card cleared from work.md in the same commit.
- progress (2026-06-13, build+run): a second wall in the staged workspace — plexus-trak and plexus-core both pin `plexus-auth-core = "0.1"` but the clone sat on main (0.2.0); checked auth-core out at its `plexus-auth-core-v0.1.0` tag (reversible, in the clone) and the workspace built. trak runs on :44107 (`./target/debug/plexus-trak --port 44107`; db ~/.config/trak/trak.db, HS256 jwt_secret auto-generated). Wire is jsonrpsee subscriptions: call `trak.call` with `{method:"facet.create",params:{…}}`; auth is a `Cookie: access_token=<JWT>` or `Authorization: Bearer <JWT>` on the WS upgrade. Over a throwaway Python client: register → login (HS256 JWT) → identity round-trips; auth propagates to the dispatcher correctly.
- progress (2026-06-13, write-path WALL): the acceptance bar — confirm a facet write round-trips — is NOT met by stock trak on this branch. facet.create returns "create requires an authenticated tenant". Traced to source: the tenant gate (src/tenant_gate.rs:138) rejects any caller that is not `is_authenticated()` (needs a non-empty session_id), but TrakAuth (src/auth.rs try_jwt/try_api_key) builds every wire AuthContext with an EMPTY session_id — so the auth module and the AUTHZ-TENANT-GATE feature on this branch are mutually inconsistent and ALL facet writes fail over the wire (reads of public facets + identity work). Verified the minimal fix (give try_jwt a non-empty session_id `jwt:<sub>`): facet create→get then round-trips, PASS (id/title/body match). Reverted it — trak left stock — because adopting a patched trak changes what the operator relies on. Surfaced as the decide node + work.md card below.
- state: blocked
- blocked-by: the write-path decide node below — stock trak on this branch can't accept facet writes; how to get a writable trak is the operator's call (their bar: "confirm writes work before relying on it"). build + run are done and reproducible from clean clones.
- since: 2026-06-13
- of: switch hypercore's document backend to trak

## stock trak can't write facets on this branch — the write path is the operator's

- op: decide
- ask: standing trak up (foothold option 2) reached a running daemon on :44107 with identity working, but facet writes fail — stock trak on feature/AUTHZ-TENANT-GATE-trak-facets is internally inconsistent: TrakAuth issues an empty session_id, the tenant gate requires a non-empty one for writes. The minimal one-line auth fix is demonstrated to make writes round-trip, but adopting it makes hyper rely on a patched trak, so the path is the operator's. Full card in work.md.
- check: a writable trak is reachable on :44107 under single-user auth — a facet create then get round-trips — by a path the operator has chosen (patch / different branch / pause); then the standup node clears and the client-shape (synapse-cc) node unblocks
- state: awaiting the operator (card filed in work.md, 2026-06-13)
- since: 2026-06-13
- of: switch hypercore's document backend to trak

## the client is generated, not hand-written: synapse-cc

- op: decide
- ask: the operator steered the client's shape (2026-06-13, words.md): use synapse-cc for client generation. synapse-cc (in hypermemetic-ai/synapse, pulled to ~/projects/synapse) is Plexus's build-time client compiler — live schema → IR → hub-codegen renders a typed client written into hyper; at runtime that client talks JSON-RPC straight to :44107 with no synapse process in the loop (the "direct and fast" path already asked for), the backend url lives in config with per-target override (the root's "network by configuration alone"), and integration mode writes only the generated files and leaves build to the host. The fork: hyper is Python and synapse-cc's proven, exercised target is TypeScript. Its config lists language = typescript | python | rust and the docs sketch a Python client (asyncio + websockets, dataclasses/Pydantic), but that sits under "Future Extensions," the renderer hub-codegen is a separate repo not pulled, and every concrete example is TS — Python is declared, not confirmed built. So: (a) if hub-codegen emits a usable Python client, generate and import it — cleanest; (b) if not, add a Python target to hub-codegen, or hand-write a thin client over trak's ~15-method facet surface (cheap; codegen may be more than hyper needs).
- check: with a reachable trak, hub-codegen is confirmed to emit (or not) a usable Python client; the path is chosen and a generated-or-handwritten client connects to :44107 and round-trips a facet
- state: blocked
- blocked-by: the standup — no live schema to introspect and nothing to test against until a trak listens on :44107; the foothold is decided (option 2, 2026-06-13) but a trak is not yet running, so this returns through the queue once the standup node lands a reachable trak
- since: 2026-06-13
- of: switch hypercore's document backend to trak
