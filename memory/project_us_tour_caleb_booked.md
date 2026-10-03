---
name: project-us-tour-caleb-booked
description: "us-tour-2026-10: Caleb BOOKED his flights on 2026-09-28; the board now only plans Alessandro's flights and marks where he is on Caleb's day (yellow) or flight (green); Caleb's exact flights are still not recorded"
metadata:
  node_type: memory
  type: project
  originSessionId: 2b505a93-c80e-47bd-81f5-c7b174f73267
  modified: 2026-09-30T14:08:41.292Z
---

Caleb booked his US flights on 2026-09-28 (WhatsApp 18:53-18:56 UTC, "Ok booking now then" / "last check" image /
Alessandro "Yup. Good for me."); Alessandro confirmed "officially booked" on 2026-09-30. About EUR 800 total.
Orlando -> San Francisco: **Delta DL504+DL2267, Fri Oct 16, MCO 09:50 -> SFO 15:54, 1 stop, Main Basic** (his booking screenshot, sent 2026-10-01). Google's normal list omits that flight: `state/booked_flight_sweep.py` finds it with the airline filter (tfs leg field 6 = 'DL'), EUR 338 on Oct 1. His way into Florida (first proposal:
land Miami Oct 11 18:50) and his flight home from SF (around Oct 25-26, Frankfurt) changed several times and the
final version exists only in WhatsApp images, which no tool can read (the wa-daemon stores `[image]`, no media).

**Why:** from now on the trip board is only about Alessandro's own, longer trip; Caleb needs no more option cards.
**How to apply:** Caleb's flights live in `travel-search/v2/app/trips/us-tour-2026-10/caleb_booked.json` (null = not
known). `build_us_tour_board.py` reads it: every scenario uses Caleb's Orlando->SF day, rows get `comp`
(day = yellow, flight = green), cards get `compMatch`, `meta.booked` feeds the multi-select chips on the results
page (shared `app/server.js`, works for any trip with `meta.booked`). When Alessandro gives the booking photo or the
flight numbers: fill date / dep (24h) / carrier / from / to in that JSON, rebuild, run `state/qa_us_tour.py`.
Each whole trip has a 'Fly with Caleb from here' switch (build precomputes `compSwap`, page stores `swaps.json`); the picker writes `booked-pick.json` and re-runs the build. Never guess his flights from the chat: I once believed a photo showed them and it was board card #115.
**Alessandro BOUGHT the same Delta 09:50 MCO->SFO on 2026-10-03 for EUR 320**: recorded in `app/trips/us-tour-2026-10/my_booked.json`; the build makes a bought flight the only option for its leg in every whole trip, at the paid price, never re-checked (no `_v`, not a TICKET row). Add any future purchase there.
Related: [[feedback-trippy-companion-mirrors-until-split]].
