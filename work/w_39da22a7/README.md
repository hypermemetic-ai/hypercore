# the command center: a queue of decisions with consequences

`w_39da22a7` · **open** · check: operator

on: `s_7c4763c0` — "The operator's interface is a queue of decisions. A decision arrives with the context to …"
fold when: the operator runs one real piece of work end to end from the queue — scopes it, decides with consequences in view, answers in place — without the terminal or the raw graph

## frame

- `wn_265cec2f` the workbench inverted: the queue stops being a panel on the graph and becomes the interface; graph, statements, and material become the context a decision card draws on  (execute: machine, propose: machine)

## gather

- `wn_55eb6516` operator scoped the work: thin slice first, on the machine's recommendation — consequence engine + decision cards over the ratification queue; triage later, machine-behind-the-interface last (their words: your call, approved)  (execute: machine, propose: operator)
- `wn_63d267ae` operator judged the card slice failed: the interface looks unchanged; the test's own wording (grounds they type) was machine-speak they could not parse; zoom-and-pan to a card is good but the relation between a question and its context is still not clear. Machine diagnosis: the ratify queue was empty when they looked — zero pending statements means zero decision cards existed to render — and the judgment was queued before anything visible could exercise it  (execute: machine, propose: machine)

## generate

- `wn_34a0217b` decision cards: every unfilled operator role slot — ratify, judge, settle, fold, scope — rendered as one card: the question, why now, a context brief, options with consequences, the machine's recommendation, a grounds field, a free-text override  (execute: machine, propose: machine)
  - depends-on -> `wn_265cec2f` "the workbench inverted: the queue stops being a panel on th…"
- `wn_7a96b083` triage: machine-proposed work enters as candidates awaiting a scope decision — now, decompose, defer, decline — sized against the error-compounding rule  (execute: machine, propose: machine)
  - depends-on -> `wn_265cec2f` "the workbench inverted: the queue stops being a panel on th…"
- `wn_89444a47` the decision record: endorse, amend, strike, verdict, and fold each carry grounds and a timestamp, so why-did-we-decide-this is answerable from the history — the sweep's strikes carried no grounds and had to be explained in chat  (execute: machine, propose: machine)
  - depends-on -> `wn_265cec2f` "the workbench inverted: the queue stops being a panel on th…"
- `wn_b288d1af` consequence engine: reverse references and downstream depends-on cones computed per option, shown on the card before deciding — strike's after-the-fact referencing_nodes report inverted in time and pointed at the operator  (execute: machine, propose: machine)
  - depends-on -> `wn_265cec2f` "the workbench inverted: the queue stops being a panel on th…"
- `wn_ed747d80` the machine behind the interface: free text on any card reaches the machine as a boundary crossing; replies and in-between moves return as the pulse, a digest rather than a raw feed  (execute: machine, propose: machine)
  - depends-on -> `wn_265cec2f` "the workbench inverted: the queue stops being a panel on th…"

## test

- `wn_96296798` the operator ratifies from cards: context and consequences are in view at the moment of deciding, and the grounds they type survive the statement they answer  (execute: machine, judge: operator, propose: machine)
  - verdict: **fail** — operator, via the viewer: "the grounds they type"? not sure what that means. also if the goal is for the realtion between the question and its context to be clear, it isn't. I see the zoom and panning to a card which is good, but that alone doesn't make the system much clearer to me.
  - tests -> `wn_34a0217b` "decision cards: every unfilled operator role slot — ratify,…"
- `wn_b6fccf65` cards render in the queue: a pending statement shows its provenance, what each answer entails (strike warning computed live), and grounds fields on strike and amend; the confirm never lands without the breakage in view  (execute: machine, judge: machine, propose: machine)
  - verdict: **pass** — CDP suite 7/7 against a /tmp copy on :8013 — card renders, why-line present, warn line names the anchored open work, strike opens form with grounds + consequences before the red button, decision recorded as operator-via-the-viewer
  - tests -> `wn_34a0217b` "decision cards: every unfilled operator role slot — ratify,…"
- `wn_c988f5b1` the blast radius is computed before any answer lands: strike/amend/endorse record grounds in a decisions table that survives the statement and the snapshot round-trip; strike reports open anchors, orphaned folded records, lost links  (execute: machine, judge: machine, propose: machine)
  - verdict: **pass** — CLI checked on a /tmp copy: strike s_7c4763c0 listed w_39da22a7 as an open anchor before deletion; endorse/amend/strike each wrote a decision row with grounds and actor; load --replace kept the record
  - tests -> `wn_b288d1af` "consequence engine: reverse references and downstream depen…"
