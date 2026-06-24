---
name: writing-for-the-machine
description: hypercore's writing-for-the-machine methodology — the standard for the agent-facing channels (skills, anchor, prompts, hand-backs), written for the model that reads them in one pass. The machine-facing mirror of communication: one instruction per sentence, say what to do, density is signal. Load when authoring or evaluating a skill, the anchor, a prompt, or a worker hand-back.
---

# writing-for-the-machine

The agent-facing channels — the methodology skills, the shared anchor, the per-episode prompts, the
worker's hand-backs — are written for a reader that is not the operator: the model that loads them. This
capability is the discipline of writing them well for that reader. It is the machine-facing mirror of
`communication`: the same goal — spend the reader's attention on the decision, not on decoding — but the
opposite reader, so several rules invert. The model reads in one pass and has no back-channel, so an
ambiguity a human resolves by re-reading or asking, the model resolves by binding the most probable
antecedent and moving on. The evidence behind each discipline is provenance, cited not inlined
(`work/archive/agent-facing-hardening/research.md`, Part C and its sources). Structural conformance — the
frontmatter schema, the discovery location, the resolving pointers — is owned and gated by `channels`;
this skill is the prose discipline that gate cannot judge, and it renders into the loaded
`writing-for-the-machine` skill so either role carries it when it authors a channel.

## The disciplines — what good looks like

- **a channel is earned by a role-discipline, not minted for a mechanism** — A capability MUST become a skill only when a role — the architect or the worker — runs it as a discipline. An engine mechanism stays a mechanism and carries no skill. The test is who runs it, not what it touches: a discipline a role applies by judgment earns a channel, machinery the engine executes does not. This keeps the skill roster the set of things an agent is taught, never the set of things the engine does.
- **write each instruction to survive one pass** — The author MUST write for a reader that binds an antecedent once and cannot ask. Carry one instruction per sentence: a sentence packing several obligations drops the later ones, because attention favours the first. Say what to do, not only what not to do: negation is the most failure-prone construction, so a prohibition becomes the positive act wherever a positive form exists. Name every antecedent in its own sentence, and make the actor the subject, so the model never guesses who acts.
- **density is the signal; the excess is the cost** — The author MUST keep the dense house voice and cut only its excess. Compression where every clause is a reused, defined term is signal, not noise — the textual form of a deep module, much meaning behind a small surface — so it is preserved, exactly as `communication` preserves it for the operator. The cost is the excess on top of that density: the over-packed statement, the compound negation, the provenance reference wedged between a verb and its object. Provenance rides at the line-end as a trailing note, never mid-clause where it splits the binding. One term, one concept: a defined name is repeated verbatim, not varied for elegance.
- **the prose discipline is a signal, never a gate** — The discipline MUST stay watched, and its one mechanical aid MUST stay a signal. Three of its constructs are detectable: a sentence past sixty words, a compound negation, and a provenance reference off the line-end. The system raises these over the spec's own prose as a non-blocking signal — it flags candidates for judgment and never refuses a fold, the length tripwire's idiom pointed at writing. A readability score never gates, for the reason `communication` gives. The only true verdict is behavioural — a plain rewrite measured against the original on fixed tasks — so the author reads the signal as a prompt to look, never as the judgment itself. The documented validators are named where they help: a reference validator and a frontmatter-schema check for the metadata, a link checker for the pointers. The full vetted inventory is provenance (`research.md`, A.5).

## Going deeper

The full requirements and their scenarios are `spec/writing-for-the-machine.md`, this skill's single source.
