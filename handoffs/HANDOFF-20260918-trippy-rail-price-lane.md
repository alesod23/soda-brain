# Handoff draft (box -> laptop / DA SYSTEM): Trippy rail-price lane with his discount cards, and gflights guardrails

Status: SENT to the DA SYSTEM session 18 Sept 20:08 on his go ("setappa il processo allora da lato laptop").

## Why
From the VPS IP every French rail price source is 403 (sncf-connect + BFF, tgvinoui, maxjeune, Trainline API, Omio, Rail Europe); Italo has no API; DB's vendo API is 403. Only the laptop's logged-in Chrome profile can price these, and only there do his cards apply. Details: memory `reference_trippy_box_rail_price_limits`.

## Lane to build (laptop side)
1. Request file: box writes `travel-search/v2/state/requests/<trip-slug>-<ts>.json` in task-land (or the existing `trippy-requests-watch.ps1` inbox, whichever it already polls): `{trip, legs:[{from,to,date,earliest,latest}], cards:{sncf:"avantage_jeune", db:"bahncard25_2"}, operators:["sncf","ouigo","italo","db"], reply_to}`.
2. Laptop watcher (already exists: `state/trippy-requests-watch.ps1`) picks it up, runs the browser drivers (`paris_rail.py` for SNCF Connect with the profile logged into his account so the Carte Avantage Jeune price shows; `bahn_probe.py` for bahn.de with BahnCard 25 set in the search URL `r=` parameter or the profile; an Italo driver on italotreno.com), writes `<request>.result.json` with per-journey dep/arr/operator/changes/price_with_card/price_full/book_url.
3. Box board build reads the result and swaps "prezzo: in attesa del laptop" cards for priced ones; `status.json` shows what is pending.
4. Failure modes: laptop off -> request waits, board says so; captcha -> watcher notifies him (PushNotification) and pauses; never a bare account chooser; reap browsers per `reap.py`.

## gflights guardrails (box side, can be done here)
- Detect Google's "unusual traffic" / consent page in `fetch()`, return an error cell instead of empty; exponential backoff; cap ~4 req/s; resume-able sweeps (skip cells already in the output file).
- Multi-city: extend `build_tfs` with N legs and trip type 3.
- Self-connection composer: build multi-stop itineraries from one-way cells with a min-connection rule, so "heavy" searches are grids of one-ways, not one giant query.

## Acceptance
Turin→Agen board (`app/trips/turin-agen-2026-09`) shows SNCF Paris→Agen, Bordeaux→Agen, Toulouse→Agen and Lyon→Agen with Avantage Jeune prices, Italo n/a on this trip, and a DB test leg (Berlin→Munich, BahnCard 25) priced from the laptop.
