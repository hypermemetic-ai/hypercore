# options - 009-operator-acts

Direction options are drafted by the machine for operator selection. The operator's
recorded direction selects one route; this file is frame material, not current intent.

## option 1

id: tty-options
kind: selected-route
summary: Add one shared `/dev/tty` operator gate and make direction a neutral numbered
choice from `options.md`; make sign-off render a short frame-derived brief and require the
work number as the confirming token.
reversibility: one-way
tradeoff: strongest non-cryptographic assurance and clearest operator agency, with more
loop and helper changes than the minimal route.

## option 2

id: tty-hmac-ready
kind: selected-route
summary: Build the Route A terminal gate and also add a passphrase-keyed marker so
operator artifacts resist same-user file forgery.
reversibility: one-way
tradeoff: closes more of the bypass gap, but asks the operator to manage a secret and adds
cryptographic behavior outside the current scope.

## option 3

id: tty-free-text
kind: selected-route
summary: Keep today's free-text direction shape, but require the direction and sign-off
helpers to read confirmation from `/dev/tty` and stamp `operator-gate: tty`.
reversibility: one-way
tradeoff: smallest implementation change, but weaker as a real multiple-choice direction
act because the route text can still be drafted as a single machine-preferred path.

## rejection choices

none: The operator may reject all options and send the work back to frame.
abort: The operator may abort without writing direction.
