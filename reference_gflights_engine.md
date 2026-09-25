---
name: reference_gflights_engine
description: Browser-free flight-price engine for trippy on the VPS - Google Flights tfs protobuf over plain HTTP, no key, not IP-blocked.
metadata:
  type: reference
---

`/home/da/travel-search/gflights.py` (built 2026-09-04, VPS). Replaces momondo
for [[reference_trippy_naming]] / [[project_trippy_v2]] on the box.

Google Flights server-renders COMPLETE itineraries to a plain `curl` GET when
you pass a `tfs` param = base64url protobuf. No browser, no API key, no login,
and Google does NOT block this box's datacenter IP (momondo, Kayak, Skyscanner,
flightsfrom and lufthansa.com all 403 it - the IP is the blocker, not the
missing browser, so installing headless Chrome here would NOT have fixed it).

- tfs protobuf: `Info{ data=3 (repeated FlightData), passengers=8, seat=9,
  trip=19 }`, `FlightData{ date=2, max_stops=5, from=13, to=14 }` where the
  airport is `Airport{name=2}` nested. trip: 1=round, 2=one-way. Two FlightData
  entries = round trip. Hand-rolled varint encoder, zero deps.
- URL: `google.com/travel/flights?tfs=<b64>&hl=en&gl=us&curr=EUR` with a
  `CONSENT=YES+cb` cookie, else it 302s to consent.google.com.
- Parse the `aria-label`s: price, stops, carrier, local dep/arr times WITH
  dates, total duration, and each layover's airport + duration.
- **Round-trip labels read "From N euros round trip total." - the one-way ones
  read "From N euros."** The regex must make ` round trip total` optional or RT
  silently parses to 0 options.
- `--max-stops 0` works properly (unlike momondo's stops filter, which silently
  died on multi-airport queries) because every query is single-route.
- `sweep --spec <json> --workers 8`: **20 (from,to,date) cells = 187 options in
  3.3s**, no errors. That is the momondo strength (many searches at once)
  without the browser, the virtual-scroll top-50 cap, or the anti-bot fight.

Gotcha worth remembering for any trip: **a one-way transatlantic is a trap.**
MUC->SFO 2026-09-30 priced OW nonstop EUR 1613, but the SAME nonstop as a round
trip (back Oct 14) was EUR 653 total. Always price the RT before quoting a OW.

**Multi-city / open-jaw does NOT work from the box (2026-09-25).** A hand-built multi-leg `tfs`
(e.g. MUC->MCO 13 Oct + EWR->FRA 12 Nov) fetches fine but Google does NOT server-render the results:
the page comes back with 3 `aria-label`s and zero itineraries, so `parse()` returns []. One-ways and
round trips still render normally. Consequence: an open-jaw price can only come from the laptop.
Workaround that carries real information: price the two halves as separate one-ways and compare.
On the US tour that gave 820 + 352 = 1172 against an open jaw of 546, which is what made the decision.
The laptop has a `gflights_mc.py` in unpushed commit 3ed5482; once that lands here, re-test before
repeating the limitation above.
