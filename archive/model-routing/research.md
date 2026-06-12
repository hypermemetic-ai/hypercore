# model routing — is there a free lunch?

research for the operator's ask (2026-06-11): is there anything like a
free lunch in model routing, and can hypercore fold it in as a
structural element buying speed without accuracy loss?

## what the field has measured

The field's results cluster around one mechanism: most queries are easy,
frontier prices are paid for the hard ones, and a router that can tell
the two apart shifts the easy mass down-tier.

- **RouteLLM** (LMSYS, open framework): routing between a strong and a
  weak model reached **95% of GPT-4 performance using 26% of the GPT-4
  calls** (~48% cheaper); cost cuts of 85% on MT-Bench, 45% on MMLU,
  35% on GSM8K at the 95%-quality bar. Routers train on preference data;
  they transfer across model pairs.
- **FrugalGPT** (the earlier cascade): query the cheap model first, fall
  upward until an answer scores reliable. Cascades need a scorer you can
  trust; their cost saving is bounded by how often the cheap model is
  right *and provably so*.
- **Cascade routing** (ICLR 2025 line of work): combining routing and
  cascading beats either — ~4% absolute over routing alone across
  RouterBench settings. Quality-cost-uncertainty scoring reached **97%
  of GPT-4 accuracy at 24% of its cost**.
- **Difficulty-aware routers** (BEST-Route, GraphRouter, Universal
  Routing 2025): a small classifier (DeBERTa-scale) estimates query
  difficulty and picks model + sampling strategy; thresholds trade cost
  against accuracy continuously.
- **The survey's sober note** (Dynamic Model Routing and Cascading for
  Efficient LLM Inference, 2026): every gain rides on the router's own
  error rate. The "free" in free lunch is conditional — routing is free
  exactly where misroutes are cheap to catch or cheap to suffer.

## the actual free lunches

Ordered by how free they really are:

1. **Speculative decoding** — a draft model proposes tokens, the target
   model verifies them in one pass; output is *provably identical* to
   the target model's. This is the only unconditional free lunch, and it
   runs provider-side, inside Anthropic's serving stack. Nothing for
   hypercore to fold in; we already eat this lunch.
2. **Structural difficulty signals** — when the *task class*, not a
   learned classifier, tells you difficulty, the router has a 0% error
   rate and costs nothing. This is the lunch hypercore already took:
   the mini. A bare true-up (record behind, no words waiting) is
   mechanically identifiable, mechanically verifiable (git holds the
   diff; the bar is commit-only, never correct), and every miss
   escalates to the full machine by rule. That is textbook
   cascade-with-verifier, instantiated without a router model.
3. **Effort, not model** — on this API generation the same model runs
   at low/medium/high effort; low effort on the frontier model often
   exceeds the *maximum* effort of the previous tier. Routing effort
   within one model keeps one cache, one behavior envelope, one quality
   floor — a near-free speed lever for task classes that don't need
   depth.
4. **Learned routers (RouteLLM-style)** — real savings at scale, but
   the lunch is paid for by the 3–5% quality gap and the router's
   misroutes. Worth it when query volume is high and per-query stakes
   are low. Hypercore is the opposite shape: low volume, high stakes
   per exchange.

## what it means for hypercore

The economics here are not token economics. intent.md's own foundation:
the operator's attention is the scarcest resource in the system. A
misrouted answer to an operator's words costs an operator round-trip —
worth more than every token the route saved. So:

- **Words never route down.** Reading the operator's words is the
  machine's highest-stakes work; the full model holds it.
- **The mini is the free lunch, already eaten.** Its class (bare
  true-ups) is exactly the class with a mechanical verifier. The
  pattern generalizes only when a new class gains one — the question to
  ask is never "is this task easy" but "is a miss caught by machinery."
- **Caching cuts against cross-model routing.** Prompt caches are
  per-model; a conversation that switches models pays cold-cache prices
  at the switch. Routing belongs at session boundaries (which is where
  hypercore's summons already sit), never mid-conversation.
- **Current price ladder** (per MTok in/out): fable 5 $10/$50 ·
  opus 4.8 $5/$25 · sonnet 4.6 $3/$15 · haiku 4.5 $1/$5. The mini's
  fable→sonnet drop is ~70%; speed follows the same ladder.

## sources

- RouteLLM — framework and results: https://github.com/lm-sys/routellm
  and https://www.lmsys.org/blog/2024-07-01-routellm/
- Dynamic Model Routing and Cascading for Efficient LLM Inference: A
  Survey (2026): https://arxiv.org/html/2603.04445v2
- Cascade routing at ICLR 2025:
  https://proceedings.iclr.cc/paper_files/paper/2025/file/5503a7c69d48a2f86fc00b3dc09de686-Paper-Conference.pdf
- Universal Model Routing for Efficient LLM Inference:
  https://arxiv.org/pdf/2502.08773
- Routing, Cascades, and User Choice for LLMs:
  https://arxiv.org/pdf/2602.09902
- Anyscale router tutorial:
  https://www.anyscale.com/blog/building-an-llm-router-for-high-quality-and-cost-effective-responses
- Production routing field notes:
  https://tianpan.co/blog/2025-10-19-llm-routing-production
- Anthropic model/pricing/caching facts: platform.claude.com docs
  (models overview, pricing, prompt caching — caches are per-model).
