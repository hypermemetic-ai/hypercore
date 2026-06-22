# Depth — hypercore's standing engineering disciplines

*The positive criterion the system is built to: deep modules — a lot of behavior behind a small
interface — built away from the red flags of shallowness. A faithful synthesis of John Ousterhout's
*A Philosophy of Software Design* (1st ed. 2018, 2nd ed. 2021, Stanford): the **single source**
`hyper/depth.py` renders into the worker's every-episode grounding and the `depth` skill, and the
criterion the architecture review scans for. These are **judgment, not a gate** (§4); the
re-grounding that adopted them — length demoted to a context-cost signal — is ADR 0006.*

**Provenance.** §5 (the *Clean Code* debate) is **primary** — Ousterhout's and Martin's own
words, from their 2024–25 written exchange at `github.com/johnousterhout/aposd-vs-clean-code`,
quoted below. §§1–4 (the book itself) are drawn through faithful secondary summaries cross-checked
against each other and against the debate, not the full primary text; three figures worth
confirming against the book before they bear weight are flagged inline as **[verify]**. The
operator wants facts checked against source, not agreement — where this synthesis is one remove
from the source, it says so.

---

## 1. The framework

**Complexity is the subject; everything else is a tactic against it.** Ousterhout defines
complexity operationally: *anything related to the structure of a software system that makes it
hard to understand and modify.* It is measured by its effect, not by intuition — the complexity
of a system is the complexity of the parts weighted by how much time developers actually spend in
each part (`C = Σ cₚ·tₚ`), so an ugly corner nobody touches barely counts and a busy one counts
double.

Complexity shows up as **three symptoms**:
- **Change amplification** — a simple change requires edits in many places.
- **Cognitive load** — how much a developer must hold in their head to get something done.
- **Unknown unknowns** — there is *something* you must change to do the task correctly, and no
  way to find out what. Ousterhout calls this the worst of the three: with the first two you at
  least know what you are up against.

It has **two root causes**:
- **Dependencies** — code that cannot be understood or changed in isolation, because it relates
  to other code that must be considered with it. Dependencies are not eliminable; the goal is
  *fewer*, and the ones that remain *simple and obvious*.
- **Obscurity** — important information that is not apparent. Obscurity is what breeds unknown
  unknowns. Its cure is design that makes the important things evident (often: good naming,
  consistency, and comments — §1's later tactics).

And it is **incremental**: complexity accrues a tolerable bit at a time — one dependency, one
shortcut, one shallow class — and no single increment looks like the problem, which is exactly
why it wins. *"Complexity is incremental; you have to sweat the small stuff."* This is the same
shape as hypercore's god-file diagnosis (the 6,348-line `window.py` as the sediment of many local
edits) — Ousterhout names the mechanism hypercore was built to resist.

### 1.1 Deep modules — the central technique

A **module** is any unit with an interface and an implementation (a class, a function, a
subsystem). It has two faces: the **interface** (what a caller must know to use it) and the
**implementation** (what it does inside). **Depth** is the ratio of the two — *how much
functionality is hidden behind how small an interface*.

- A **deep module** hides a lot behind a little: a powerful implementation under a simple
  interface. (Unix file I/O — `open/read/write/close/lseek`, five calls over an ocean of
  buffering, scheduling, permissions, device drivers — is his canonical example.)
- A **shallow module** is the opposite: an interface nearly as complicated as the
  implementation it fronts. It costs the reader almost as much as having no module at all,
  because the interface itself is the complexity. A method that does little but forward its
  arguments is the limiting case.

The load-bearing claim, and the one most at odds with conventional advice: **it is more important
for a module to have a simple interface than a simple implementation.** Complexity in an
implementation is paid once, by the author; complexity in an interface is paid by every caller,
forever. So the design move is to **pull complexity downward** — when something must be hard,
make it hard *inside* the module where the implementer absorbs it, not in the interface where
every user does.

Ousterhout names the opposite disease **classitis** — the belief, drawn to extremes, that classes
and methods should be as small as possible, which multiplies the *number* of shallow modules and
therefore the *number* of interfaces, raising total complexity while each piece looks tidy. This
is the precise hinge of the *Clean Code* disagreement (§5).

### 1.2 Information hiding and leakage

The mechanism that makes a module deep is **information hiding**: each module encapsulates a
design decision (a file format, a data structure, an algorithm) that nothing outside needs to
know. The antithesis is **information leakage** — the same knowledge embedded in two or more
places, so they must change together though nothing in the code ties them. Leakage is, for
Ousterhout, *"one of the most important red flags in software design."*

Its most common cause is **temporal decomposition** — structuring code around the *order
operations happen in* (read the file, then modify it, then write it) rather than around the
*knowledge each step needs*. Decompose by knowledge, not by time, or the same knowledge (the
file format) leaks across the read-stage and the write-stage. Related tactics: **general-purpose
modules are deeper** than special-purpose ones (designing the general case usually yields a
simpler interface *and* covers the specifics); **different layers should have different
abstractions** (adjacent layers that talk in the same terms are a sign a layer is doing nothing —
the pass-through smell).

### 1.3 Strategic vs. tactical programming

The mindset under all of it. **Tactical programming** optimizes for getting the next
feature/bug working; design is whatever falls out. Each tactical choice adds a little complexity
the author judged not worth fixing now — and §1's incremental accrual does the rest. Ousterhout's
**tactical tornado** is the prolific developer who ships fast and leaves a widening wake of
complexity for everyone else.

**Strategic programming** treats *working code as not enough* — the goal is a good *design* that
keeps the system cheap to change, and producing it is a continuous **investment**: small, regular
amounts of extra time spent getting the structure right and cleaning up degradations as you find
them. Ousterhout's suggested investment is on the order of **10–20% [verify]** of development
time — enough to compound, framed explicitly as paying down against future complexity, not
gold-plating. *"The increments of software development should be abstractions, not features"* — a
unit of progress is a clean abstraction added, not merely a feature made to work.

### 1.4 Define errors out of existence

The exception-handling chapter, and one of the book's sharpest moves. Exceptions and special
cases are a major, underrated source of complexity — each one is interface that every caller must
handle. The first instinct should not be to handle more exceptions but to **define them out of
existence**: redesign the interface so the exceptional case *isn't* exceptional. His example —
make `unset(var)` mean "ensure this variable does not exist" rather than "delete this variable,"
and the "variable doesn't exist" error vanishes because the normal case already covers it. Sibling
tactics: mask the exception low in the stack, or aggregate handling in one place. The point is
that the *number of places that must reason about the error* is a design variable, not a given.

### 1.5 Design it twice

*"Design it twice."* For any consequential design — an interface, a class, a module boundary —
the first idea is rarely the best, and the cost of considering a *genuinely different* second
(and third) approach before committing is trivial against the cost of living with a poor shape.
Even when the first design wins, comparing it to a real alternative sharpens it. (hypercore
operates this mechanically with parallel worktrees for load-bearing interfaces, as a *judgment*
discipline distinct from the throughput use of the same fence — ADR 0007.)

### 1.6 Comments as part of design

Ousterhout treats comments as **a first-class design activity, not a confession of failure** —
the single starkest contrast with *Clean Code* (§5). His claims:
- Comments capture information the author had but the **code cannot express** — the *why*, the
  rationale, the units, the invariants, the non-obvious. *"Comments should describe things that
  are not obvious from the code."* A comment that restates the code is the failure mode (a red
  flag); a comment that records what the code cannot is the point.
- **Interface comments are what enable abstraction.** A good interface comment lets a caller use
  a module without reading its implementation — it is the thing that makes the module deep from
  the outside. Without it the caller must read the code, and the abstraction is fictional.
- **Write comments first.** Used as a design tool, comments written before the code expose a
  clumsy interface early — if the method is hard to comment, it is hard to use.
- *Software is designed for ease of reading, not ease of writing* — the asymmetry that justifies
  the whole investment: code is read far more often than written.

---

## 2. The red flags

The book's signature contribution to everyday practice: named *symptoms* that a piece of code is
probably more complex than it needs to be, collected in a summary at the back. Faithful list:

1. **Shallow module** — the interface is complicated relative to the functionality it provides.
2. **Information leakage** — the same knowledge appears in multiple places.
3. **Temporal decomposition** — code structure mirrors the execution-time order, so knowledge gets
   split across the stages that happen to touch it.
4. **Overexposure** — using a common feature forces the caller to learn about rarely-used ones.
5. **Pass-through method** — a method that does nothing but forward its arguments to another with
   nearly the same signature.
6. **Repetition** — the same (or nearly the same) code appears over and over.
7. **Special-general mixture** — special-purpose code embedded in a general-purpose mechanism,
   coupling the two.
8. **Conjoined methods** — two methods so entwined you cannot understand one without reading the
   other. (The debate's PrimeGenerator turns on this — §5.)
9. **Comment repeats code** — the comment says what the adjacent code already plainly says.
10. **Implementation documentation contaminates interface** — interface docs forced to expose
    implementation details a user does not need.
11. **Vague name** — a name too broad to carry specific information.
12. **Hard to pick name** — difficulty naming a thing cleanly signals the thing itself is not
    cleanly defined.
13. **Hard to describe** — difficulty writing a short complete comment signals a design problem,
    not a writing one.
14. **Nonobvious code** — its behavior cannot be grasped in a quick read.

(Also recurring in the text though not always counted in the back-of-book list: **pass-through
variables** — a parameter threaded through a long call chain only to reach a distant user.)

Note the character of every one of these: they are **smells a reader judges**, not thresholds a
tool measures. None has a number. That property is why the gate keeps at most a length tripwire
while the red flags live in the standing architecture-review as judgment, not gate thresholds (ADR
0006).

---

## 3. The design principles

The book's other summary list — the positive form of the red flags. Faithful set (numbering is
indicative; wording cross-checked, not verbatim from the book — **[verify]** the exact phrasing
before quoting any as canonical):

1. Complexity is incremental — sweat the small stuff.
2. Working code is not enough — strategic beats tactical.
3. Make continual small investments to improve system design.
4. Modules should be deep.
5. Interfaces should make the common case simple.
6. It is more important for a module to have a simple interface than a simple implementation.
7. General-purpose modules are deeper.
8. Separate general-purpose and special-purpose code.
9. Different layers should have different abstractions.
10. Pull complexity downward.
11. Define errors (and special cases) out of existence.
12. Design it twice.
13. Comments should describe things that are not obvious from the code.
14. Software should be designed for ease of reading, not ease of writing.
15. The increments of software development should be abstractions, not features.

---

## 4. Epistemic status — *what these disciplines are, and are not*

Ousterhout is explicit, in the book's own framing, that this is **an opinion piece**: a set of
design principles distilled from one experienced practitioner's judgment, offered to be argued
with, not a proven method. The honest reading of its standing:

- **It is judgment, not a recipe.** Every technique above resolves to *"is this making the system
  easier to understand and change?"* — answerable only by a designer looking at a specific case.
  There is no procedure that applies "deep module" or "shallow" without a person weighing it. The
  red flags are heuristics for *where to look*, not verdicts.
- **It is not mechanical.** Nothing in the book is a threshold a CI gate could enforce. Ousterhout
  *resists* numbers on purpose — the book's central fight (§5) is against a *rule* ("functions
  should be 2–4 lines") precisely because the rule fires without judgment and produces shallow
  modules. A measure that can be gamed or that fires on the wrong cases is, by his lights, worse
  than the judgment it replaces.
- **It is not empirically proven.** It rests on argument, example, and the author's authority
  (a serious one — Tcl/Tk, the Raft consensus algorithm, RAMCloud, decades at Berkeley and
  Stanford), not on controlled studies. He invites skepticism and expects readers to disagree in
  places. *Software design is never finished;* the book offers awareness, not closure.
- **Its value is design awareness.** What it changes is what a designer *notices* — it trains the
  eye to see complexity accruing and gives shared names (deep, shallow, leakage, classitis) to
  argue about it. That is real and large; it is also, precisely, not a gate.

This is the seam the system is cut along. hypercore's folding conditions are **mechanical** — a
line-count number a graph either clears or doesn't. This framework is **judgment**. How a judgment
framework is honored by a system whose enforcement must be mechanical is resolved in ADR 0006: the
mechanical gate keeps a minimal length tripwire (length is what a module costs an agent's context
window — a real cost a number can track), and the red flags live as a standing, model-driven
**architecture-review** scan. Judgment kept judgment; the gate kept a backstop.

---

## 5. The contrast with *Clean Code* — the crux

The reason the operator named *"ESPECIALLY when compared to Clean Code."* In 2024–25 Ousterhout
and Robert C. "Uncle Bob" Martin (*Clean Code*, 2008) held a long written debate, published at
`github.com/johnousterhout/aposd-vs-clean-code` — a single README, primary text, both men's own
words. They picked the three places their philosophies actually collide.

### 5.1 Method length — *the central collision*

Martin (*Clean Code*): *"The first rule of functions is that they should be small. The second
rule is that they should be smaller than that."* Functions of two, three, four lines; extract
until you cannot extract further ("extract till you drop").

Ousterhout's objection is **depth**, not taste. Decompose past a point and two things go wrong:
- The functionality behind each interface shrinks while the **interfaces multiply and often grow
  more complex** — you have manufactured shallow modules, the #1 red flag.
- The fragments become **entangled**: *"two methods are entangled if, in order to understand how
  one works internally, you also need to read the code of the other."* Once entangled, *"there is
  no clever ordering of method definitions that will fix the problem"* — the reader ping-pongs
  between fragments and the side effects hide in the gaps.

The worked battleground is Martin's own **PrimeGenerator** (from *Clean Code*), split into eight
tiny methods. Ousterhout shows that understanding any one of them
(`isNotMultipleOfAnyPreviousPrimeFactor`, `smallestOddNthMultipleNotLessThanCandidate`, …)
requires reading the others — textbook entanglement — and rewrites it as essentially one cohesive
method carrying the algorithm, with heavy comments. **Martin's reply, partially conceding:** the
PrimeGenerator was a *pedagogical* illustration of decomposition, not a production design; but he
holds that *"small, well-named methods and the separation of concerns"* generally aid readability
by exposing intent. He also granted that *Clean Code* gave little guidance on recognizing **over-
decomposition** — the failure Ousterhout is naming.

### 5.2 Comments

The most temperamental split. Martin: *"Comments are always failures. We must have them because we
cannot always figure out how to express ourselves without them, but their use is not a cause for
celebration"* — prefer long descriptive names, trust code over comments (verify every comment
against the code), reserve comments for the unavoidable; within one team, well-named methods and
arguments suffice for internal interfaces.

Ousterhout: comments are **essential and irreplaceable** — they carry what code cannot (rationale,
the non-obvious insight) and they are *what makes abstraction real* (an interface comment lets you
use a module without reading it). He estimates he writes **5–10× more comments** than Martin and
holds that *"missing comments are a much greater cause of lost productivity than erroneous or
unhelpful comments."* The exchange dramatized it: Ousterhout's comment explaining *why* a prime's
first relevant multiple is its square confused Martin (who only got it after, by his account, bike
rides and staring at the ceiling); Ousterhout read Martin's reaction as a *"fundamental disbelief
in the value of comments,"* and said that in real life he would iterate with colleagues to improve
the comment rather than drop it.

### 5.3 Test-driven development

Ousterhout: *a huge fan of unit testing*, skeptical of **TDD's** demand to write tests first in
tiny red-green increments — that cadence, he argues, pins attention on making the next case pass
(tactical programming, §1.3) and never schedules the step back for design. He allows one clear
exception: **writing the failing test first when fixing a bug** is genuinely good. Martin defends
TDD by its three laws and the red-green-refactor cycle, holding that the *refactor* step *is* where
design happens, so TDD does not preclude design — it sequences it.

### 5.4 Where they agree

Not a standoff — they converged on a real floor: modular design reduces cognitive load;
**over-decomposition is a real failure** (Martin's concession); readability is the goal; **unit
testing is indispensable** (Ousterhout's agreement); and helping a future reader understand hard
code is a professional duty, however they weight comments-vs-naming to discharge it.

**The crux for hypercore:** the *Clean Code* rule Ousterhout fights ("functions should be
small — smaller than that") is *exactly* a mechanical line-count constraint of the kind hypercore
enforces at the fold. He does not reject smallness; he rejects **a number standing in for the
judgment of depth**, because the number fires without looking and manufactures shallow, entangled
modules — the very god-file-by-a-thousand-fragments that the opposite of a god-file can also be.
hypercore's 400-line *ceiling* is the mirror image of *Clean Code*'s small-function *floor*: both
are line-count rules; the question slice 7 must answer is whether hypercore's escapes Ousterhout's
objection (a ceiling punishes *un-deepened length*, a floor punishes *cohesive length*) or merely
inverts it.

---

## Sources

- **John Ousterhout & Robert C. Martin — *A Philosophy of Software Design* vs. *Clean Code*** (the
  debate; primary, quoted in §5): <https://github.com/johnousterhout/aposd-vs-clean-code>
- John Ousterhout, *A Philosophy of Software Design*, 2nd ed. (Yaknyam Press, 2021) — the book
  itself; §§1–4 are drawn through the summaries below, cross-checked, not the full primary text.
- Red-flags list cross-check: <https://notes.portebois.net/2021/03/04/13.html>
- Book summary cross-checks: <https://danlebrero.com/2021/02/24/philosophy-of-software-design-summary/>,
  <https://carstenbehrens.com/a-philosophy-of-software-design-summary/>
- The Pragmatic Engineer interview with Ousterhout (strategic/tactical, TDD):
  <https://newsletter.pragmaticengineer.com/p/the-philosophy-of-software-design>

*[verify] flags mark the three claims worth confirming against the book before they bear weight:
the 10–20% investment figure (§1.3), and the exact verbatim wording of the red-flags (§2) and
design-principles (§3) lists.*
