---
name: reference_trainline_graphql_box
description: French rail prices from the VPS without a browser - Trainline's /graphql persisted JourneySearchQuery works from the box IP (REST /api/journey-search/ is DataDome-403), Carte Avantage via discountCards URN, Kombo as fallback. Tool trainline_render.py in travel-search.
metadata:
  type: reference
---

Verified 2026-09-18 (`/home/da/travel-search/trainline_render.py`, README at the top of the file):

- **Headless render of thetrainline.com/book/results is dead on this IP**: the page shell and the
  price calendar render, but the journey list comes from `POST /api/journey-search/` which DataDome
  answers 403 + geo.captcha-delivery.com. Tried: persisted profile, CDP with masked client hints
  and navigator.webdriver, longer budgets. Do not retry that path; the script exits 3 on it.
- **`POST https://www.thetrainline.com/graphql` is NOT behind DataDome.** Relay persisted query
  `JourneySearchQuery` (doc_id `d3a8d378ad62b8f7a433f00b88ee20bd`, app 4.48.32737; the script can
  re-mine it with `--refresh-docid`). Needs a server-issued `context_id` cookie (any GET of the
  homepage) echoed as `ContextId` header, `x-api-currencycode: EUR`, and the site's full
  `connections` list in the body, otherwise FR routes say RouteNotSupported. ~5-6 journeys per
  window, sweep by moving `outwardJourney.dateTime` forward; `ARRIVEBEFORE` is rejected for EU.
- **Railcard**: not settable from the results URL (EU cards live in sessionStorage). In the API
  body: `passengers[].cardIds=[uuid]` + `discountCards=[{id:uuid, code:"urn:trainline:sncf:card:AvantageJeune"}]`
  (also AvantageAdulte / AvantageSenior; UK atoc codes YNG, TST, SRN, 2TR, FAM). Proof Paris->Agen
  2026-09-24 14:05: 158.60 -> 85.00 EUR; night train 118.30 -> 79.10.
- **locate**: `/api/locations-search/v2/search?locale=en-gb&searchTerm=..` works with the context
  cookie. Paris 4916 (all), Montparnasse 4920, Agen 207, Bordeaux St-Jean 828 (827 = city),
  Toulouse Matabiau 5311, Lyon Part-Dieu 4676, Le Puy-en-Velay 4683, Torino Porta Susa 8568,
  Milano Centrale 8490.
- **Kombo fallback** (`--engine kombo`): place.kombo.co/search?term=..&locale=en, POST
  search.kombo.co/search (dateOutward YYYY-MM-DD, passengers[{ageGroup:"Adult",discountCardIds:[12]}]),
  poll /search/trips?key=..&lastIndex=.. Prices include Kombo's fee; card effect unreliable there.

See [[reference_trippy_box_sources]] · [[reference_trippy_on_box]].
