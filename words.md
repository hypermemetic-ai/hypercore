# words

## words . 2026-06-13

operator (2026-06-13): pull hypermemetic's trak. we will make it our document backend. we could interface with it via synapse, but we would prefer something direct and fast. we do i/o against the file system currently, trak uses jsonRPsee. whatever we build will work today against a locally hosted server, in the future against a network hosted server. we don't treat trak as the project - we treat switching our backend to it as the project, and a non-trivial one.

machine (2026-06-13): Read as a new project — switching the document backend from the filesystem to trak — and opened as the execution graph work/trak-backend (of: hypercore). "hypermemetic's trak" is plexus-trak, a Plexus RPC facet store: facets (title/body/status/parent + typed edges depends_on/blocks/relates_to/duplicates) reachable over WebSocket JSON-RPC 2.0 on :44107, SQLite-backed. Its model is hypercore's own — nodes, relations, material on nodes — almost one-to-one, so the mapping is natural; "direct, not synapse" reads as our own JSON-RPC client straight to that socket. Pulled to ~/projects/plexus-trak, unregistered (trak is a dependency, not a linked project; if you meant trak-ui or another repo, one rm undoes it). The first blocker is yours and it's a card on the queue: there is no trak to build against — nothing on :44107, no creds, and trak builds only against the whole plexus workspace plus plexus-idp for its OIDC tokens. Stand up that full local stack, or target a trak you already run? Once a server is reachable, the client's shape (a Python client in hyper vs. a Rust/jsonrpsee client it drives) and the document→facet mapping come back as their own decisions before any of that material exists. The filesystem backend keeps running untouched meanwhile.

operator (2026-06-13): look at synapse-cc for client generation

