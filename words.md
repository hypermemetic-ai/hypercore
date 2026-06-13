# words

## from the graph "trak-backend", on "the client is generated, not hand-written: synapse-cc" . 2026-06-13

operator (2026-06-13): when these entries open up, the view appears to snap to the bottom for long entries. I think it should snap to the top.

machine (2026-06-13): Fixed. On open, the work view scrolled the entry's *end* to the screen bottom, pushing its head off the top — that was the snap-to-bottom. Now an opened entry anchors to its top: never scroll past the entry's own start to chase its end, so its head shows and the tail runs below with "… N more below". Landed as a slice awaiting your acceptance — relaunch hyper and open a long trak-backend node to try it.

## I don't like "it asks" for decisions

operator (2026-06-13): I don't like "it asks" for decisions. we use ASK for work, is there a reason we're not consistent? does this apply anywhere else? look for incongruities of this kind and make them congruent. this leads to very real legibility wins.

## the utilization data can be shrunk…

operator (2026-06-13): the utilization data can be shrunk without utility loss. I think all we need is 5h percent as percent and time until reset, and same for 7d. with the space savings, let's think about what we can do about legibility without sacrificing taste.

