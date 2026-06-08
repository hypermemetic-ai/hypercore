# options - 013-two-step-build

Direction options are drafted by the machine for operator selection. The operator
selects one route, rejects all options, or aborts without writing direction.

Both options do the same two-step thing: a short signed frame, then for each unit the strong
model writes a plan, then the cheap fast model builds from that plan. The cheap model only
does mechanical tasks; anything that cannot be broken down goes to the strong model; a check
confirms each plan matches what you signed; and the default builder flips to the cheap model.
The only difference between the options is whether you can read the plan.

## option 1

id: plan-stays-hidden
kind: selected-route
summary: Keep the plan under the hood. The strong model writes a plan for each unit and the
  cheap model builds from it, but the plan is never shown to you — you sign the short frame
  and judge the result. The plan-matches-frame check reuses the existing review approach.
  Smallest amount of new machinery.
reversibility: one-way
tradeoff: Least to build, least for you to read. You are trusting the strong model and the
  match check; you never see the plan yourself.

## option 2

id: plan-you-can-read
kind: selected-route
summary: Same two-step, but each plan is saved where you can read it if you want (you do not
  have to). "Cannot be broken down" becomes an explicit signal a check confirms, and the
  plan-matches-frame check is its own dedicated check. More transparency, stronger match check.
reversibility: one-way
tradeoff: More to build and prove, and having the plan readable risks pulling you back into
  reading the detail the short frame was meant to spare you.

## rejection choices

none: The operator may reject all options and send the work back to frame.
abort: The operator may abort without writing direction.
