# words

## from the queue . 2026-06-11

operator (2026-06-11): few things. work titles are cut all the way down to the first letter for some reason (a...). acceptance should be a -> y to confirm like other actions. acceptance should be differentiated visibly from decisions I think. in general, if we're thinking of there being different types of things the operator makes decisions about, these differences should be parseable at a glance from the main screen. also, I'm still not buying this "press m to summon" thing. I think it speaks to some architectural constraint, maybe stemming from a simplicity call? I understand and respect that but I think we can aim higher without making the app a complex mess. we just need to be clear about what we want. in my mental model, if what I'm saying belongs in an existing session, it should just go to that session. everything should feel instantateous. I don't want to think about context clearing, but that should also happen naturally. maybe a session clears and/or closes if unused for an amount of time (spawns back when related content sees new operator input?), or if a good opportunity presents itself mid-session (natural breakpoint, clear -> restart with context from file)? it is critical that you don't just take my words and run with them here. push back if you disagree or have alternative suggestions. we also need to start thinking about how this interface can support multiple work units, and intersecting work. right now we're only working on hypercore and still there's a lot to iron out. so the order is tall, we need to remain vigilant.

operator (2026-06-11): alright, here's another problem. I hit enter on a message and I see the machine is answering for 300+ seconds. I assume this means it's moved straight to building. this concerns me. I want to see decisions for me to approve/deny before the work begins and while the work is in progress. I want to direct the work and understand it while it happens. I think we had ratified this already but I'm not seeing the practical ramifications.

operator (2026-06-11): never mind? maybe it's just slow. looks good actually, I saw a couple cards come up already

machine (2026-06-11): all answered, in order. titles: fixed and accepted — the work view was subtracting a paragraph-long state field from the title's room. a then y: built, you accepted it; note this session is barred from editing SKILL.md (harness permission), so one line there still says "frictionless act" — CLAUDE.md carries your word. kinds at a glance: built, on its card — every queue entry leads with decide / accept / answered / sent and the header counts them apart. on "press m": pushback, as you asked. the disk is the session — every summon reads intent, queue, and words fresh, so a resumed conversation holds nothing a fresh one lacks except hidden state, which is exactly what this system forbids. speaking already summons instantly; m is only the recovery path (words landing mid-answer, a dead session's mess). so the aim-higher move is not routing to live sessions but making the recovery automatic: summon at launch when anything waits, re-summon when words land mid-answer, m only after a failure. that proposal sits in the work view — it spends machine runs without an act from you, so it waits on your go. if the real pain is the wait itself, that is model latency, not architecture; say so and we explore a warm standby. multiple work units: recorded as an open ask in the work view, undrafted.

machine (2026-06-11): the 300 seconds was building, and your concern bit: two of your four asks (kinds, m) had design latitude and should have surfaced as decisions before material — the titles fix and a-then-y were your explicit words executed. heard and applied mid-session: the latitude items now sit in the work view as proposals, nothing built until your word. the gap behind "not seeing the practical ramifications": the interface has no surface for in-flight decisions — speech is the only channel into running work. proposed (in the work view, unbuilt): the machine writes a decision entry before building, with options and entailments, and it surfaces on the queue marked apart; you approve, deny, or redirect there, mid-flight. your word sets its shape.

machine (2026-06-11): the cards you saw were the first two slices landing. the worry still stands answered above — the decision surface is proposed, not dropped.

operator (2026-06-11): so what state is the work in? I see entries under w but I don't know what that entails for me. does in-flight mean it's happening now? also it would be nice if the interface showed what model the machine is using. I'm assuming it's fable 5 right now. in flight -> in-flight. as a first step towards multi-project, maybe w should be organized by graph? so one entry, hypercore, with current entries a level below that? it's a cheap starting point before we start thinking about how the rest of the interface would have to change too.

operator (2026-06-11): I'll also ask - how do I start the interface if I close it? right now I log out and back in but some shortcut that launches it from desktop would be nice.

## from the acceptance card, on "the screen names the machine" . 2026-06-11

operator (2026-06-11): I think name should be on the very top row, somewhere tasteful. and yes, let's pin fable 5.

operator (2026-06-11): I like this but this should be the expanded view. default I think should be just hypercore, enter -> it expands like now.

operator (2026-06-11): odd that both were listed as from the acceptance card on the screen names the machine. the second clearly isn't from there but from the other open item.

operator (2026-06-11): just the model name is fine. not claude claude-fable-5.

