---
name: feedback_trippy_metro_airport_normalization
description: "Trippy aggregation must normalize metro vs specific airport codes to a city bucket and trust the searched destination, not parsed tokens — else one engine's cheap nonstops vanish"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7d32292e-8942-4e7f-9ad7-ae4d372f0de1
---

Trippy multi-engine flight aggregation has TWO failure modes that silently drop the cheapest fares. Both caught 2026-06-05 when the user found a EUR 204 Norse JFK->FCO nonstop that my report missed (I'd reported EUR 343 as cheapest to Rome — a EUR 139 error).

**Bug 1 — metro vs specific-airport mismatch.** momondo searches by METRO code (NYC->ROM, ->MIL) and labels results `ROM`/`MIL`; skiplagged searches SPECIFIC airports (JFK->FCO) and labels `FCO`/`MXP`. My aggregator's Italy filter only accepted specific codes `{MXP,FCO,...}`, so EVERY momondo metro result (`ROM`/`MIL`) was excluded — the entire momondo contribution, including the EUR 204 Norse, was dropped, leaving only skiplagged feeding the rankings. **Fix:** normalize all destination codes to a CITY bucket (ROM/FCO/CIA->Rome; MIL/MXP/LIN/BGY->Milan; TRN->Turin) and group/rank by city, so both engines' nonstops merge.

**Bug 2 — momondo destination parser guessed wrong.** momondo `_parse` extracted the arrival IATA by regex over the whole card text and picked the LAST/second 3-letter token. Card text is full of connection-airport codes (STN/LTN/ATH on 1-stop itineraries) and airline codes (ITA/KLM), so it scattered real Rome flights under bogus destinations (89 Norse fares mislabeled). **Fix:** destination = the QUERIED `to` code; never guess it from card tokens. Every result of a from->to search lands at `to`.

**Bug 3 — momondo returns nothing for small US origins.** momondo's deep-link `flight-search/MKE-...` (Milwaukee) and `MSN-...` (Madison) returns its "non abbiamo trovato voli / seleziona le date" empty-state for BOTH metro AND specific-airport destinations (verified 0 every time 2026-06-05), while Chicago (CHI) returned 467. skiplagged handles the SAME small origins fine (MKE->MXP 21 flights, MSN->MXP 22). **Rule: for small/regional US origins (MKE, MSN, MDW, and likely other non-hub airports) use skiplagged, not momondo.** Don't report "no flights" from a momondo-only result for a small origin — cross-check skiplagged first.

**Standing rule:** when aggregating across engines with different code granularity, normalize to the city/searched-destination and trust the QUERY, not parsed text. The cross-engine "cheapest" must actually include BOTH engines — if one engine contributes ~0 rows to a destination it serves heavily, suspect a code-mismatch filter bug, not a real absence. Retro-fix without re-scraping: TripResult.destination stores `"PARSED (SEARCHED_LABEL)"`; trust the parenthetical SEARCHED_LABEL. See [[feedback_trippy_headless_parallel]].
