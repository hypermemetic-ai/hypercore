# qq

My own agent core; bespoke because it only serves me. qq is the command center
I use to run agentic development: sharp skills, operating rules, code knowledge,
parallel sessions, a tuned terminal cockpit, and only the external tools that earn
their keep. **Capability I reach for — not process I maintain.**

Operating rules live in [`AGENTS.md`](./AGENTS.md) (loaded every session;
`CLAUDE.md` symlinks to it). The shared methodology is
[`qq-methodology.md`](./qq-methodology.md), linked live into other repos.

## The six layers
| layer | what | where |
|---|---|---|
| **Rules** | repo header + linked methodology | `AGENTS.md`, `qq-methodology.md` |
| **Actions** | curated, invocable skills linked live | `skills/` → `~/.claude/skills/` |
| **Knowledge** | auto-generated map of the code | `.understand-anything/knowledge-graph.json` |
| **Sessions** | many named parallel agents, each in its own worktree, state-aware | herdr (`herdr`) |
| **Cockpit** | human-driven terminal tools + tuned configs | `cockpit/` |
| **Externals** | live docs · GitHub · fast filesystem · gate | Context7 · `gh` · `fd`/`eza`/`rg` · `no-mistakes` |

## The loop
**Align → Plan → Build → Verify (autonomous) → Sign-off (human, gated) → Review →
Compound.** Trivial work takes the escape hatch — do it directly — but *never*
skips verification. Full detail in `AGENTS.md`. Invoke `orchestrate` to run the
whole loop end-to-end as one command — Claude conducts, Codex implements.

## Skills
16 skills, curated from four MIT collections (mattpocock, superpowers,
compound-engineering, gsd-core) plus authored pieces for qq. Link them live from
`skills/` into `~/.claude/skills/` with `bash bin/qq-link.sh skills`; invoke them
as `/grilling`, `/executing-plans`, and so on. The index is in `AGENTS.md`; full
provenance is in [`SKILLS-ATTRIBUTION.md`](./SKILLS-ATTRIBUTION.md).

## Setup
1. **Preflight** — `bash bin/install.sh` checks the external surface and cockpit
   tools, then prints exact install hints for anything missing.
2. **One-shot activation** — `bash bin/qq-activate.sh` installs the guardrail
   hook, wires the WIP savepoint, symlinks cockpit configs from this repo into
   `~/.config`, and links skills into `~/.claude/skills`.
3. **Skills** — link them live:
   ```
   bash bin/qq-link.sh skills
   ```
   Skills become `/grilling`, `/code-review`, etc.
4. **Linked repos** — wire a repo to the shared methodology:
   ```
   bash bin/qq-link.sh repo <path>
   ```
   This adds the live methodology symlink, ensures the repo imports it, merges
   Context7 into `.mcp.json`, and seeds `CONCEPTS.md` only when missing.
5. **Cockpit** — `cockpit/` is the source of truth for yazi, glow, herdr, and
   shell navigation. `herdr prefix+f` opens `qqy`; yazi starts at the repo root;
   pressing Enter on `.md` renders in-pane via mdcat or the tuned Glow theme.
6. **Context7** (live library docs) — `.mcp.json` is set; approve the `context7`
   server on next session start.
7. **Knowledge layer** — `/plugin marketplace add Egonex-AI/Understand-Anything`
   → `/plugin install understand-anything` → `/understand`.
8. **Sessions** — install herdr (`brew install herdr`), then
   `herdr integration install claude codex` so it tracks agent state. Fan out with
   `herdr worktree create --branch <name>` + `herdr agent start <name> --cwd <worktree> -- claude`.

## Provenance
Curated from MIT sources, kept only where they serve my workflow: superpowers
(obra), compound-engineering (EveryInc), gsd-core (open-gsd), agent skills
(mattpocock), context-engineering (muratcankoylan), and Karpathy's guidelines.
The authored pieces fill the gaps I actually use. All sources MIT.
