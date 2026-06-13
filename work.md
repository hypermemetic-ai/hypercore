# work

## trak OIDC path — which issuer, and the cost it actually carries

- ask: You decided to move to the OIDC branch (UT-wave3) and stand up an issuer — set. Executing it, two things surfaced that change the cost from how "move to a branch" sounded. (1) UT-wave3 doesn't drop into the current workspace: it pins plexus-core 0.6, plexus-transport 0.4, plexus-auth-core 0.2 (with the oidc-reqwest JWKS fetcher) — all higher than what's cloned now (0.5.3 / 0.3.0 / v0.1.0), so the WHOLE plexus workspace must move to the matching UT-1/UT-W3 version set before trak builds; that's a coordinated multi-repo checkout that may hit version-skew walls like the auth-core one did, plus a full rebuild. (2) trak then validates RS256 via OIDC discovery + JWKS against --oidc-issuer (default http://localhost:4461, audience "plexus:trak"); an issuer must serve /.well-known/openid-configuration + a JWKS and mint RS256 tokens with those claims. plexus-idp is the reference issuer but isn't cloned. The issuer is the resource fork, and it's yours:
- options: stand up a minimal local RS256/JWKS issuer — a small hand-written service (RS256 keypair, serve discovery + JWKS, mint a plexus:trak token); lightest, fully local, no second heavy build — but bespoke material your backend-auth leans on . clone and build plexus-idp — the real reference issuer at :4461, faithful to production and exactly what trak expects, but the full OIDC stack you deferred: clone + heavy Rust build + a second daemon to keep alive . fall back to the one-line patch on branch A — given the real OIDC cost above (workspace version bump + issuer standup), the session_id fix still gets writes TODAY with no issuer and no version bump, and you've seen it round-trip; I hold it as the honest fallback now that the OIDC price is visible
- state: decided (2026-06-13) — option 2 — clone and build plexus-idp — the real reference issuer at :4461, faithful to production and exactly what trak expects, but the full OIDC stack you deferred: clone + heavy Rust build + a second daemon to keep alive
- since: 2026-06-13
- blocks: the standup's write-confirmation and through it the whole switch — the client (synapse-cc) and the document→facet mapping can't be built or tested against a trak that won't accept writes. Nothing compounds: the filesystem backend keeps running untouched, so hypercore loses nothing while it waits.

## thread labels: short, clean phrases

- ask: from the operator's words (2026-06-13) — "I want better thread labels. short, clear." The old label took the first words and hard-cut at 48 chars on a word boundary, so a heading could trail off mid-sentence ("share your findings about the claude usage…"). thread_label() now keeps just the first sentence when that reads as a phrase, tightens to a 40-char cap cut on a clause-then-word boundary, and strips trailing punctuation — shorter, and cut where a phrase ends, not mid-thought. A pure heuristic shortens and cleans but cannot summarize: "share your findings about the claude usage endpoint…" becomes "share your findings about the claude…", not "Claude usage endpoint". A truly crisp topic label would need the machine to relabel a thread when it answers it (a thread can already be renamed by hand from its own view) — that is the operator's call, posed in the answer line; this slice is the heuristic alone.
- try: relaunch hyper (interface code loads only at launch). New main-screen speech opens a thread with a short, clean label; existing headings keep their old text until renamed. The labels in the queue show the tighter cut after relaunch.
- state: awaiting acceptance
- since: 2026-06-13
- blocks: nothing — labels are display only; the queue and threads work unchanged, this only changes how a new heading reads.

## louder attention cue

- ask: from the operator's words (2026-06-13) — "the notification sound isn't loud enough." play_cue() now passes paplay --volume=131072 (≈200% of the file's recorded level), so the actionable-card cue is louder. It amplifies only the cue's own playback stream — the system volume is untouched, so nothing else on the machine gets louder. The source .oga can't be re-mastered here (no ffmpeg/sox), and raising the system sink was off-limits (it touches what the operator owns), so stream-volume amplification is the lever; if it is still short, the value bumps.
- try: relaunch hyper (interface code loads only at launch). When the queue next turns actionable (a card or a fresh answer arrives), the cue sounds louder. On demand: `paplay --volume=131072 sounds/cue-attention.oga` plays it at the new level.
- state: awaiting acceptance
- since: 2026-06-13
- blocks: nothing — the cue is additive; the silent fallback (no paplay/sink) is unchanged, and the louder volume can't break the loop.

