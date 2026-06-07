# frame - 006-collaboration-deliberation

## work

Addressed node: root

Node-local work name: 006-collaboration-deliberation

Target segments: collaboration, loop, adapter

Work in flight: none before this work was scaffolded. `find . -maxdepth 4 -type d
-path '*/intent/frame' -print` returned no active frame directories before start, and
`git status --short` was clean.

## problem

The current collaboration contract lets the machine move too quickly from an operator's
broad intent to a proposed route. The frame may be complete as a mechanical artifact while
the operator still has not exerted enough judgement over the problem domain to know
whether the work is likely to help.

The operator named the failure mode directly after a premature frame for autonomy and git
strategy: the machine did not ask clarifying questions, did not give the operator enough
evidence and reasoning to review, and treated a broad collaboration problem as an
implementation route before the operator had shaped the problem space.

This is not a one-off chat failure. The adopted history already contains collaboration
hardening work, including `005-harden-loop-collaboration`, yet the workflow still allowed
a frame that was technically complete and strategically wrong. The collaboration segment
needs a stronger pre-sign-off contract: governed work must help the operator form a
reasonable expectation of value before phase two is sealed.

## constraints

- The new rule applies to all governed work, not only broad or high-risk work.
- The rule must not put a vague burden on the operator. If the operator is expected to
  judge, the machine must provide enough information, alternatives, evidence, uncertainty,
  and reasoning for the operator to reach a conclusion without discomfort.
- Evidence standards are problem-relative. Some problems benefit from quality research;
  some do not; some domains lack reliable research; and superficial literature use can be
  worse than careful reasoning from local facts and constraints.
- Preserve hypercore's fast property. The deliberation requirement must scale with the
  problem rather than impose a fixed research ceremony on every governed change.
- Preserve the sign-off boundary. Sign-off remains the operator's act, but sign-off should
  mean informed expectation, not just permission to proceed.
- Preserve phase two. Once sign-off closes a sufficiently deliberated frame, phase two
  still re-derives from the written frame and executes without reopening design unless the
  frame is incomplete or proof fails.

## decision surface or open direction

Four materialization routes were considered:

Route A: prompt-only guidance.
The adapter could tell the machine to ask better questions and provide more context. This
is light, but it repeats the current failure: a machine can satisfy a vague prompt while
still moving too fast.

Route B: required operator-deliberation contract in every governed frame.
Every governed frame must recover enough pre-sign-off deliberation for the operator to
form an expectation of value: problem/domain map, decision surface, evidence basis,
uncertainty, options and tradeoffs, operator expectation, and rejection conditions. The
depth of evidence is justified by the problem, not fixed in advance.

Route C: fixed research rubric for every governed frame.
Every frame would require outside literature or expert evidence. This is sound-looking but
too blunt: it would be wasteful for local mechanical work and harmful in domains where the
available literature is weak or superficial.

Route D: leave deliberation outside the loop.
The operator can always ask for more discussion before sign-off, but the system would not
make that need visible or recoverable. This keeps the current gap.

The selected route is Route B. It follows the operator's decisions and keeps the burden on
the collaboration system: the machine prepares the problem space, and the operator judges
from a recoverable record.

## route

Implement Route B.

1. Amend `intent/collaboration.md` and `hypercore.md` so collaboration explicitly requires
   pre-sign-off operator deliberation for governed work. The statement should say that the
   operator must be able to exercise judgement over enough of the problem domain to form a
   reasonable expectation of whether the work will help.
2. Amend collaboration intent so the machine's burden is explicit: provide the problem
   map, domain context, local evidence, relevant external evidence when it is useful and
   trustworthy, logical and practical reasoning, alternatives, tradeoffs, uncertainty, and
   failure modes.
3. Amend collaboration intent so evidence depth is problem-relative. The machine should
   justify the evidence standard it chose and avoid superficial research when good
   literature is unavailable or irrelevant.
4. Amend `intent/loop.md` and `intent/machine-statements/loop.md` so a new governed frame
   must carry recoverable operator-deliberation fields before sign-off. Suggested fields:
   problem/domain map, evidence standard, evidence basis, options and tradeoffs, operator
   expectation, rejection conditions, and unresolved discomfort or open judgement.
5. Amend `intent/adapter.md`, `intent/machine-statements/adapter.md`, `adapter/codex.md`,
   and `adapter/gates/frame.md` so the Codex harness and frame gate ask for this
   deliberation record before settling a route.
6. Amend `adapter/loop.sh` start scaffolding and frame completeness validation so new work
   frames include and require the deliberation fields. Keep the check semantic by field
   labels rather than by one rigid filename.
7. Amend `check.sh` to prove the intent, gate prompt, scaffold, and frame validation carry
   the new deliberation contract.
8. Run `./check.sh`; then phase two runs the sweep and adopts or shelves according to this
   frame.

## methodology adherence

Work classification: governed work. It changes the root methodology's collaboration
contract and the loop/adapter material that enforces frame completeness.

Loop waiver: none. The work exists because a convenient but insufficient frame passed the
old collaboration surface; convenience cannot waive the loop.

## common ground

### operator decisions

- The deliberation standard applies to all governed work.
- If the operator carries the judgement burden at sign-off, the machine must provide all
  information needed for the operator to reach a conclusion without discomfort.
- Evidence depth depends on the problem. Some work benefits from quality research, some
  does not, some domains lack quality research, and superficial literature use can be
  worse than sound local reasoning.
- The point of collaboration is for the operator to exert their faculties over the problem
  domain and express intent across enough of the problem space to judge expected value.

### authority

This work may amend root methodology intent and material for the `collaboration`, `loop`,
and `adapter` segments. It may update `hypercore.md`, `adapter/codex.md`,
`adapter/gates/frame.md`, `adapter/loop.sh`, and `check.sh` only to materialize the
selected collaboration contract.

It may not reintroduce the deleted autonomy/git strategy frame, settle a git strategy, or
broaden phase-two permissions. Those topics may become later governed work after this
collaboration contract is in place.

### machine assumptions

- `SOA` in the operator's earlier request meant state of the art.
- The problem is not that the machine omitted a single clarifying question; the problem is
  that the system did not require enough pre-sign-off deliberation for the operator to
  judge the route.
- "Without discomfort" does not mean certainty or exhaustive proof. It means the operator
  has enough context, options, evidence, and uncertainty on the table to make an informed
  judgement and to name remaining discomfort if it exists.
- The most useful enforcement point is frame completeness, because sign-off already seals
  phase one and phase two re-derives from the frame.
- The deliberation record should scale: a tiny local change may need a short local
  evidence basis; a methodology change may need outside literature, comparison across
  domains, and explicit reasoning.

### evidence

Local evidence:

- `intent/collaboration.md` currently requires common ground and reliance calibration, but
  not an operator expectation statement or a problem-relative evidence standard before
  sign-off.
- `intent/loop.md` says orient and frame are the design phase and that open direction must
  surface before route, but it does not require operator deliberation over options,
  evidence, or rejection conditions for all governed work.
- `adapter/gates/frame.md` requires common frame fields, but those fields can be satisfied
  without proving the operator had enough context to judge expected value.
- The deleted `006-autonomy-and-git-strategy` frame demonstrated the gap: it was able to
  pass the frame gate even though the operator judged the collaboration inadequate.
- Adopted history already includes `005-harden-loop-collaboration`, so this work should be
  framed as a refinement to an already-active concern, not a brand-new discovery.

External evidence gathered during phase-one research:

- Human-AI teaming research reports that human-plus-AI systems do not automatically beat
  the better solo performer; coordination, communication, task design, and evaluation
  matter. Source: "When combinations of humans and AI are useful: A systematic review and
  meta-analysis", Nature Human Behaviour, 2024,
  https://www.nature.com/articles/s41562-024-02024-1
- Joint-activity/common-ground literature treats collaboration as active maintenance of
  shared goals, roles, state, capabilities, and breakdown repair, not a static handoff.
  Source: Klein, Feltovich, Bradshaw, and Woods, "Common Ground and Coordination in Joint
  Activity", https://www.jeffreymbradshaw.net/publications/Common_Ground_Single.pdf
- Human-AI interaction guidelines emphasize making capabilities and limits clear, showing
  why the system acts, enabling correction, and supporting granular feedback. Source:
  Amershi et al., "Guidelines for Human-AI Interaction", CHI 2019,
  https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/Guidelines-for-Human-AI-Interaction-camera-ready.pdf
- Mixed-initiative interaction literature warns that systems fail when they infer user
  goals or timing poorly and do not provide the user with good opportunities to guide or
  refine automation. Source: Horvitz, "Principles of Mixed-Initiative User Interfaces",
  CHI 1999, https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/chi99horvitz.pdf
- Automation and situation-awareness literature warns that automation can push humans out
  of the loop, degrading monitoring and recovery. Source: Endsley and Kiris, "The
  Out-of-the-Loop Performance Problem", Human Factors, 1995,
  https://journals.sagepub.com/doi/10.1518/001872095779064555
- Shared decision-making in medicine separates choice talk, option talk, and decision
  talk; the relevant pattern is that a person can only express informed preference after
  options and tradeoffs are made explicit. Source: Elwyn et al., "Shared Decision Making:
  A Model for Clinical Practice", 2012, https://pubmed.ncbi.nlm.nih.gov/22618581/
- Participatory design and requirements elicitation literature supports iterative
  stakeholder involvement and acknowledges that values, tacit knowledge, ambiguity, and
  context are part of the work. Sources:
  https://arxiv.org/abs/2409.17952 and
  https://www.sciencedirect.com/science/article/pii/S0950584903000326

Reasoning from this evidence:

- The operator should not be reduced to a checkpoint after the machine has already chosen
  the solution shape.
- A fixed research requirement would confuse evidence with literature citation. The
  collaboration rule should require justified evidence sufficiency, not universal
  literature search.
- The frame should expose enough of the problem space that operator correction becomes
  specific and durable.

### uncertainty

- The exact labels for the new required frame fields should be chosen during
  implementation to fit the existing frame completeness scanner and keep prose readable.
- Some existing history frames will not contain the new fields. The implementation should
  require the new fields for new active work, not rewrite adopted history.
- Mechanical checks can prove the presence of labels and prompts, but cannot prove the
  operator's internal comfort. The durable proxy is a written operator expectation and any
  named unresolved discomfort or open judgement.
- If `SOA` meant something other than state of the art, the evidence record should be
  corrected before adoption.

### open blockers

None before sign-off. The main implementation risk is overfitting the frame scanner into a
rigid paperwork checklist instead of preserving problem-relative depth.

### feedback capture

The operator correction that deleted the prior scaffold is direct feedback: a frame that
does not ask enough questions or provide enough decision support is collaboration drift,
even when the mechanical frame gate passes. This feedback must become current
collaboration/loop/adapter intent or an explicit debt.

### handoff state

Phase two should re-derive the work from this frame alone. It should implement the
operator-deliberation contract, prove it mechanically, run the sweep, and adopt if the
post-archive corpus says all governed work must support informed operator expectation
before sign-off.

## proof state

Required proof:

- `./check.sh` is green after implementation and after archive fold.
- The sweep reports coherent.
- `check.sh` proves current intent and material mention operator deliberation or equivalent
  language in collaboration, loop, adapter, gate prompts, loop scaffold, and frame
  completeness validation.
- Starting a new work node scaffolds fields sufficient for problem/domain map, evidence
  standard, evidence basis, options/tradeoffs, operator expectation, rejection conditions,
  and unresolved discomfort or open judgement.
- The frame/signoff validation blocks a new governed work frame missing the new
  deliberation record.

## sweep

Initial sweep:

- Collaboration already owns role partition, common ground, reliance calibration, control,
  feedback, handoff, and graceful failure. Operator deliberation belongs there.
- Loop owns the frame/sign-off boundary and required recoverable fields. Requiring the
  deliberation record before sign-off belongs there as enforcement.
- Adapter owns Codex gate prompts and rigid workflow materialization. Updating the frame
  gate prompt and scaffold belongs there as harness enforcement.
- This work should not alter ownership, endorsement, git strategy, or phase-two execution
  permissions.
- No concurrent active work nodes are known, so no work-in-flight collision is present.

## adoption claim

Adopt this work after sign-off, implementation, green checks, coherent sweep, and archive
fold if the root methodology now requires every governed work frame to support informed
operator deliberation before sign-off, with evidence depth scaled to the problem and
superficial literature use explicitly avoided.

## shelving claim

Shelve this work if implementation cannot make operator deliberation recoverable without
turning all governed work into fixed ceremony, weakening sign-off, or pretending mechanical
field checks can prove the operator's internal judgement.
