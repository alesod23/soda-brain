---
name: feedback_travel_comfort_door_time
description: "Score travel options by DOOR departure time, not flight time: before 07:30 from his Milan base is uncomfortable and worsens the earlier it gets. Always pair the cheapest option with a comfortable one and state the EUR delta."
metadata:
  type: feedback
---

His words, 2026-09-20: *"partire a quell'ora vuol dire non dormire... idealmente svegliarmi alle
7:00 e non dopo. La sveglia vuol dire uscire, vuol dire essere a Milano Centrale alle 7:30, quindi
devi fare un calcolo cosi'... sotto le 07:30 e' scomoda, pero' e' piu' un range, piu' la decadenza
di una curva."*

**The rule.** Every option is scored on the **door** departure time, computed backwards from the
flight: flight time minus airport transfer minus airport buffer. From his central-Milan base:
Malpensa 65 min, Linate 35 min, Bergamo Orio 70 min, plus 90 min at the airport with hand luggage.
Door after **08:00** = ideal · after **07:30** = comfortable · before **06:30** = the night is
destroyed. A decay curve, never a hard cutoff.

**And never show only the cheapest.** Every board pairs the cheapest option with a genuinely
comfortable one and states the EUR delta between them, because the delta is the question he is
actually answering. Worked example from this trip: MXP-CDG at EUR 51 with a 04:20 door against
EUR 82 with a 09:25 door = **EUR 31 for five hours of sleep**.

**Why it had never happened:** trippy's cross-trip model (`travel-search/preferences.json`) priced
DURATION (`GC = price_d2d + v*time_d2d`, v = 8 EUR/h) and had 15 rules about stops, layovers,
overnights and ground legs, but **no term at all for time of day**. So no context duel ever asked
him what an early start costs him, because the dimension did not exist. Fixed 2026-09-20: rules
`early-departure-discomfort` and `comfort-must-be-offered-next-to-cheapest`, plus a
`dep_door_penalty` term in the formula (backup `preferences.json.bak-20260920`). The rule carries a
`reconfirm` instruction: on EVERY trip with an early option, run one duel and record the euros he
accepted, which calibrates the price of his sleep.

**The general lesson he drew, worth applying beyond travel:** when he has to point out a dimension,
the gap is in the model, not in that one answer. Look for the missing dimension and write it into
the durable file, not into the reply. Related: [[reference_travel_discount_cards]],
[[project_trippy_v2]], [[feedback_trippy_deep_dive]].
