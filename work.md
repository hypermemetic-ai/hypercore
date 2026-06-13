# work

## stand up a local trak to build against — the first blocker

- ask: switching the backend needs a running trak to develop against, and there is none. Nothing listens on :44107, synapse and credentials are absent, and plexus-trak builds only against the full plexus workspace (path deps on plexus-core, plexus-macros, plexus-transport, plexus-auth-core) with plexus-idp issuing the OIDC tokens it now requires. Do I stand up that full local stack, or is there a trak you already run that I should target?
- options: stand up the full local plexus stack — clone and build plexus-core/-macros/-transport/-auth-core plus plexus-idp, run trak on :44107 with a local token; self-contained and offline, but a heavy Rust build and a second daemon (idp) to keep alive . build trak but run it in its simplest single-user auth mode — same workspace build, but skip plexus-idp and use trak's legacy/local auth for now, deferring real OIDC to the network phase; lightest standup that still runs here, and I confirm writes work on that path before relying on it . target a trak you already run — you give me the endpoint and how to authenticate; fastest start and closest to the eventual network mode, but "local today" becomes "your server today" and ties early work to that server staying up
- state: decided (2026-06-13) — option 2 — build trak but run it in its simplest single-user auth mode — same workspace build, but skip plexus-idp and use trak's legacy/local auth for now, deferring real OIDC to the network phase; lightest standup that still runs here, and I confirm writes work on that path before relying on it
- since: 2026-06-13
- blocks: the whole switch — no client, mapping, or cutover can be built or tested without a reachable trak. Nothing compounds while it waits: the filesystem backend keeps running untouched, so hypercore loses nothing by the delay.

