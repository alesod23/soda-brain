---
name: feedback-trippy-companion-mirrors-until-split
description: "In trippy, a travel companion (Caleb, us-tour-2026-10) copies the user's WHOLE chain up to the point where their plans split; never model them as \"doing their own thing\" in between"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 2b505a93-c80e-47bd-81f5-c7b174f73267
  modified: 2026-09-27T19:24:19.873Z
---

When the user adds a companion to a trip ("Caleb follows me..."), the companion does EXACTLY what the user does
(same arrival or same day, same ground steps, same event, same hotel spend, same connecting flight) until the
point where their plans explicitly split (for us-tour-2026-10: after San Francisco, Caleb flies home). Only the
part after the split is the companion's own search. I first modelled Caleb as "Florida on his own, lodging not
included", which dropped the train, the venue transfer, the Orlando hotel and the shared Orlando->SF flight, so his
cards were far too cheap; the user caught it (2026-09-27): "caleb does the same thing as me... you're missing a lot of
trip details".

**Why:** a companion card that skips shared steps is not a price, and the user compares his and the companion's
totals side by side.
**How to apply:** build the companion's cards FROM the user's chosen option (its inbound, ground block, hotel,
shared legs), then search only the divergent tail. Label "same flight" relative to each user option. Every card,
user's or companion's, must pass a completeness check (all chain steps present) and total = lines = booking rows.
See [[feedback-trippy-event-anchor-and-explicit-ground]].
