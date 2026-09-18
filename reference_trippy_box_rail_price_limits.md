---
name: reference_trippy_box_rail_price_limits
description: "Trippy on the box, audited 2026-09-18: French rail prices ARE reachable via Trainline GraphQL with his Avantage Jeune (see reference_trainline_graphql_box); everything else on the French side is blocked from the VPS IP (sncf-connect, tgvinoui, maxjeune, Trainline API, Omio, Rail Europe all 403; Navitia = timetables only), Italo has no API, DB vendo API 403 (bahn.de HTML 200). Timetables via Trainline SEO pages work. gflights: 30 cells in 3.2 s with 8 workers, no throttling code yet. His discount cards (SNCF Avantage Jeune, BahnCard 25) only apply through the laptop browser profile."
metadata:
  type: reference
---

**Measured 2026-09-18 (Turin→Agen search):**
- Reachable from the box: Google Flights (gflights.py), FlixBus (ground2.py), Trenitalia LeFrecce BFF incl. international routings (Torino→Lyon/Paris via Switzerland while the Fréjus line is closed; Paris prices not exposed), Trainline SEO pages `thetrainline.com/en/train-times/<a>-to-<b>` (first/last train, frequency, changes, fastest; NO prices), bahn.de homepage.
- Blocked (403) from the box IP: sncf-connect.com and its BFF, tgvinoui.sncf, maxjeune-tgvinoui.sncf, sncf-voyageurs.com, thetrainline.com API, omio.com, raileurope.com, bahn.de vendo API (`/web/api/reiseloesung/...`). api.sncf.com (Navitia) = 401 without a key and timetables only. Ouigo has no API. Italo: no headless price path (unchanged).
- gflights throughput: 30 (from,to,date) cells, max_stops 1, 8 workers = 3.2 s, 0 errors. No "unusual traffic" detection or backoff in the code yet; add before big grids. Multi-city (3+ legs on one ticket) not implemented (protobuf allows repeated legs, trip type 3).
- Empty cells are usually real (no route with <=1 stop), e.g. BGY→ORY, TRN→MRS.

**His requirement (2026-09-18):** prices with his cards: SNCF Carte Avantage Jeune, DB BahnCard 25; Italo; heavy multi-stop Google Flights grids that may run for hours. Plan agreed in principle: box does flights/bus/Trenitalia and the board; a box→laptop request lane (laptop watcher `state/trippy-requests-watch.ps1` already exists, SNCF driver `paris_rail.py`, DB `bahn_probe.py` with Playwright) fills SNCF/Italo/DB prices from the logged-in Chrome profile where the cards apply. See `task-land/_system/HANDOFF-20260918-trippy-rail-price-lane.md`.

Related: [[reference_trippy_box_sources]], [[reference_gflights_engine]], [[reference_trippy_on_box]], [[reference_travel_search]].

**UPDATE same day (20:40):** Trainline's `/graphql` gateway (Relay persisted JourneySearchQuery) is NOT behind DataDome and prices with `discountCards=[{code:"urn:trainline:sncf:card:AvantageJeune"}]`: Paris→Agen 24/9 14:05 = 158.60 full / 85.00 with card, confirmed by `appliedDiscountCards`. Tool: `~/travel-search/trainline_render.py` (`locate`, `search --railcard`, Kombo fallback, block detection exit 3). Rendered results pages stay 403 (journey-search API behind DataDome). Details: [[reference_trainline_graphql_box]]. The laptop lane is still needed for Italo and for DB with BahnCard 25 until a BahnCard URN is found.
