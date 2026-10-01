---
name: feedback-airline-direct-for-known-carrier
description: "Trippy — once a specific airline+flight is identified, verify final price on the airline's own site, not the aggregator"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5bf3e4d7-faea-4ab8-a723-c9f3ef764fcf
---

When a trippy deep dive has converged on a *specific* airline flight (e.g. "Volotea OLB→TRN 18:30 on Aug 21"), do NOT trust the aggregator price (momondo, skiplagged, kayak). **Re-check the price directly on the airline's website.**

**Why:** Aggregators are good for *discovery* — they reliably surface which airlines fly a route and the broad price band. But the final price is almost always best on the airline's own site (no aggregator booking fees, loyalty discounts visible — MegaVolotea, Ryanair myRyanair, ITA Volare, Lufthansa Miles & More — and freshest fare data). The user even pointed out a case where momondo said €138 OLB→TRN but Volotea direct showed €117. Same flight, €21 difference.

**How to apply:**
- Pass-1 broad sweep: aggregator is fine, momondo and skiplagged stay as discovery tools.
- Pass-2 deep dive on a chosen flight: switch to airline-direct immediately. Drive Volotea / Ryanair / easyJet / ITA / Lufthansa search for the exact route+date, click the same flight, capture the real fare + the real cabin-bag adder.
- The airline-direct number is what goes into the cooked-trips HTML (final source of truth), not the aggregator number.
- Exception: if the airline site is broken / requires a login the user doesn't have / is anti-bot-locked, fall back to aggregator and explicitly flag "fare from momondo, airline-direct unverified".

Related: [[feedback_trippy_deep_dive]] (luggage drive-past-modal rule), [[reference_travel_search]] (adapter status — Volotea is currently a stub but should be elevated to a first-class airline-direct adapter), [[feedback_browser_comet]].
