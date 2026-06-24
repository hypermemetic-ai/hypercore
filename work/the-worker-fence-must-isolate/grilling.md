surfaced: 2

[Q] How deep does the OS fence cut into the shared `.git`? Option A — **working-trees only**: the worker's worktree is writable, the main tree and every sibling worktree are read-only, and the shared `.git` stays writable so commits land — with corruption of the main ref or a sibling's branch held off where it already is (the single-writer record lock serializes every git op, and the fold is the only path to main). Option B — **also fence the store**: the OS jail itself must stop a worker from rewriting a sibling's branch or the main ref even by accident, not just stop stray file writes.
lean: Option A, working-trees only. §74 says in as many words "the shared git history writable so the worker's own commits reach the one record"; the record lock already makes every git operation serial, and the worker's branch never reaches main except through the fold — so ref/object corruption of the shared line is already structurally barred without duplicating it into the jail. The jail's job is the filesystem working trees: worktree writable, host read-only.
flip: If we model the worker (an autonomous GPT coding agent) as capable of issuing *arbitrary destructive git* against the shared store — not merely stray writes — then a shared writable `.git` is itself the hole, and the fence must give each worker its own object store with fetch-on-fold instead of a shared `.git`. That is a substantially deeper change than wrapping the transport, so it would re-scope the work.
answer: Working-trees only (Option A). The worker's own worktree is writable; the main tree and every sibling worktree are read-only at the OS level; the shared .git stays writable so the worker's own commits reach the one record (intent §74's "shared git history writable"). Accidental corruption of the main ref or a sibling's branch is already barred — the single-writer record lock serializes every git op and the fold is the only path to main — so the OS jail's job is the filesystem working trees, not the object store. A deliberately-destructive-git worker rewriting the shared store is left OUT of scope, the same scoping already ratified for the provenance gate (a-record-a-load-bearing): a role with write access to the shared store is unwinnable without per-worker object stores, a bigger change not taken here. Adopt this scope, but evaluate the mechanism fresh before committing — carry no debt from the prior (epoch-two) build.

[Q] May the fence take a new external dependency and/or elevated privilege to stand up the jail, or must it be built only from unprivileged primitives already present on a stock Linux host?
lean: No new privileged dependency: build from unprivileged Linux primitives (the user-namespace + read-only-bind-mount family, or Landlock path rules) that need no setuid binary and no root, accepting a minimum-kernel requirement as the cost. This keeps installing-a-sandbox and requiring-sudo — both decisions-floor acts — out of the picture. Which specific primitive wins is a design-it-twice contest the architect runs within this constraint; only the cost constraint is yours.
flip: If the hosts hypercore must run on can't be relied on to have unprivileged user namespaces or a recent-enough kernel enabled (several hardened distros disable userns by default), then a packaged sandbox (e.g. bubblewrap/firejail) is the only portable option, and adopting it as a ratified install prerequisite becomes the right call.
answer: Adopt bubblewrap (bwrap) as the strong, leading candidate — the epoch-two choice, proven there: a distro-maintained, UNPRIVILEGED (user-namespace-based) sandbox that needs no root, no sudo, no daemon, and no image; it fences an ordinary process to its worktree on the real machine. Neither raw hand-rolled primitives nor a heavyweight container — the lightest-correct shape, a packaged tool that wraps the unprivileged primitives. The cost accepted as a ratified prerequisite: bwrap (and unprivileged user namespaces) present on the host. CRUCIAL OPERATOR QUALIFIER: adopt but EVALUATE FRESH before committing — the OS-fence mechanism is a load-bearing interface decision, so it is run through a real design-it-twice contest (bubblewrap the leading candidate, weighed against alternatives such as Landlock and a container) rather than blindly ported, and it carries NO DEBT from the prior build: only the proven recipe and its hard-won lessons (absolute binds; private --tmpfs scratch holes for the harness's home-state and /tmp so it does not die at EROFS before running; omp's private writable seeded agent dir) are carried as evidence, re-derived clean.

[Q] Does the enforcement land as a **gated** red→green scenario — the harness actually spawns the jail, attempts a write outside the worktree, and asserts it fails at the OS level — accepting that `python3 -m engine --check` then requires the chosen sandbox primitive on whatever host runs it? Or does it stay **watched** evidence (a structural assertion that the transport wraps the jail, with live escape-prevention confirmed out-of-band), extending the README's honest-limit posture?
lean: Gate it. The honest-limit note is watched for a real reason — whether a live `omp` session loads the fence's anchor and skills genuinely needs a live model and can't be faked. An escape attempt is different: it can be exercised deterministically with no model in the loop (spawn the jail around a trivial out-of-worktree write, assert it fails; assert an in-worktree write and a commit still succeed). folding-conditions makes a mechanically-checkable property gated, not watched — and a structure-only assertion ("the argv contains the jail") is exactly the convention-level check the 2026-06-24 incident proved insufficient.
flip: If `--check` must stay runnable on hosts that lack the sandbox primitive (a stripped CI container, a minimal image), gating would break the harness there. In that case the escape test is watched/opt-in — run where the primitive exists — and a lighter structural assertion carries the fold, with the README note corrected to name escape-prevention as confirmed-where-supported rather than universally gated.
answer: Gate it. The enforcement lands as a gated red→green scenario: the harness spawns the real fence, attempts a write to a path OUTSIDE the worker's worktree (the main tree) and asserts it fails at the OS level, and asserts an in-worktree write plus a git commit still succeed and reach the record. Mechanically checkable with no model in the loop, so folding-conditions makes it GATED, not watched — a structure-only "the transport argv contains the jail" assertion is exactly the convention-level check the 2026-06-24 incident proved insufficient. Accepted cost: python3 -m engine --check then requires bwrap on whatever host runs it; where bwrap is absent the gate surfaces a clear skip/fail rather than passing silently. This corrects the README honest-limit note from "watched evidence the first autonomous run confirms" to a real gate.

[CONTRACT]
A live worker can no longer write any path outside its own git worktree. An attempt to modify the main tree, a sibling worker's worktree, or anywhere else on the host fails at the operating-system level — not by convention — while the worker's own worktree stays writable and the shared git object store stays reachable so its commits still land on the one record. The transport that spawns the worker (`transport.worker_transport`) no longer merely sets the subprocess's working directory to the worktree (a starting directory is not a jail); it spawns the worker inside a real OS jail rooted there, built from an unprivileged sandbox primitive that needs no root and no daemon — the mechanism settled by a fresh design-it-twice contest (bubblewrap the leading candidate, weighed against Landlock and a container, carrying no debt from the prior build beyond its hard-won recipe). The fence is working-trees only: it walls the filesystem, not the shared `.git` store — a worker deliberately rewriting a sibling's branch or the main ref is left out of scope, already barred where it stands by the single-writer record lock and the fold being the only path to main. §74's open net is untouched; only the filesystem and the shared `.git` are fenced. The guarantee is gated, not watched: the acceptance harness spawns the real fence, attempts a write to the main tree and asserts it is refused at the OS level, and asserts that an in-worktree write and a git commit both still succeed and reach the record — so `python3 -m engine --check` now requires the sandbox primitive on whatever host runs it, surfacing a clear skip or failure where it is absent rather than passing silently. The result is validated against this: the 2026-06-24 escape (a worker editing 11 tracked files on main) becomes impossible at the OS level, and the README's honest-limit note — which had recorded the fence as watched evidence the first autonomous run would confirm — is corrected by the gate that lands.

[DELTA]
## MODIFIED — worker

### Requirement: a worker runs fenced in its own git worktree
A worker MUST run in its own git worktree — a separate checkout on its own branch — and that worktree
MUST be the **only** filesystem location it can write. The main tree, every sibling worker's worktree,
and the rest of the host are **read-only at the operating-system level**, so a worker's attempt to modify
any path outside its own worktree fails as an OS refusal, not as a convention it could break by accident
(the 2026-06-24 escape — a live worker editing tracked files on main from a cwd-only fence — is barred by
construction). Its own worktree stays writable and the shared git object store stays **reachable and
writable**, so the worker's own commits reach the one record without touching another tree or the main
line until the result integrates. The enforcement wraps the **transport that spawns the worker's model**
(`transport.worker_transport`): that transport MUST spawn the worker inside a real OS jail rooted at the
worktree — not merely set the subprocess's working directory to it, since a starting directory is not a
jail — built from an **unprivileged** OS sandbox primitive present on the host, needing no root and no
daemon. Because the jail roots at the worktree, the checkout remains the worker's working directory: its
source, the archived grounds (`work/archive/`), and the derived channel files (the anchor and skills) are
read from the checkout, and the harness auto-loads the fence's anchor and discovers its skills. The fence
is **working-trees only**: it walls the filesystem, not the shared object store — a worker deliberately
rewriting a sibling's branch or the main ref in the shared `.git` is out of scope, already barred where it
stands by the single-writer record lock and the fold being the only path to main, and unwinnable without
per-worker object stores. §74's net stays open: only the filesystem and the shared `.git` are fenced.
Because the host must carry the sandbox primitive for the fence to stand, the acceptance harness's
enforcement check surfaces a clear **skip or failure** where the primitive is absent, never a silent pass.

#### Scenario: the fence holds
- WHEN a worker is dispatched a node
- THEN it gets a worktree distinct from the main tree, commits its result there on its own
  branch, and that commit is reachable in the record but absent from the main line

  ```check
  fence off-main
  ```

#### Scenario: the worker runs at its fence
- WHEN a worker's model is summoned to build
- THEN its transport runs with the worktree as its working directory, so it reads the archived
  grounds and its channel files from its own checkout rather than from an inlined prompt

  ```check
  fence binds-cwd
  ```

#### Scenario: a live worker cannot write outside its worktree
- WHEN a worker is spawned inside its real fence and attempts to modify a path outside its own worktree —
  the main tree, a sibling's worktree, or elsewhere on the host — and, separately, writes inside its own
  worktree and commits
- THEN the outside write fails at the OS level (the host is read-only to the worker), while the in-worktree
  write and the git commit both succeed and the commit reaches the shared record — and where the host lacks
  the sandbox primitive the check surfaces a clear skip or failure rather than a silent pass

  ```check
  fence host-read-only
  fence worktree-writable
  fence commit-lands
  ```
