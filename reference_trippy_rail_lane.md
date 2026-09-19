---
name: reference_trippy_rail_lane
description: "Box-to-laptop rail-price lane (live 2026-09-19): the box drops a request JSON in Drive, the laptop prices DB (BahnCard 25 by URL token) and Italo, writes the result next to it; captcha = toast + card, plan B = Claude in Chrome after 3 passes."
metadata: 
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-19T09:26:33.395Z
---

**Rail-price lane, live since 2026-09-19 01:10.** Protocol file: `~/.claude/travel-search/v2/RAIL-LANE.md` (mirrored in the Drive folder). Folder: laptop `G:\My Drive\DA\trippy\{requests,results}` = box `/home/da/gdrive/DA/trippy/`. The box (savior, Trippy) writes `requests/<trip>-<ts>.json` with legs `{from,to,date,earliest,latest,operators:[db|italo]}` and `cards:{db:"bahncard25_2"}`; the laptop task `Trippy-RailLane` (every 2 min, `v2\state\rail-lane-watch.ps1` via .vbs) runs `v2\rail_lane.py`, which runs `db_price.py` / `italo_price.py` and writes `results/<same>.result.json` (same per-leg schema as the box's Trainline results; `price_card_eur` = card fare). SNCF is NOT in the lane (box prices it via Trainline GraphQL).

Facts learned building it:
- **DB card = URL token** `r=13:17:KLASSE_2:1` (1 adult, BahnCard 25, 2nd class; `13:16:KLASSENLOS` = no card), found through bahn.de's "Anfrage ändern" dialog. No login. Card fare = 0.75x, shown as a struck-through price.
- **Italo prices come from the booking XHR** (`api-biglietti.italotreno.com/api/v1/booking/status/<op>`) captured in a headed off-screen Chrome; the site is behind Akamai, so no cold calls. Station spelling comes from `/api/v1/stations?sn=` (Firenze S.M.Novella, Venezia S.Lucia). Italo has no deep-link search URL: `book_url` is session-bound.
- **Drivers own their profiles** (`profile-rail-lane`, `profile-rail-lane-italo`), reset the Chrome crash flag before launch (taskkill leaves the profile "Crashed" and the next launch dies with TargetClosedError), reap only their own profile.
- **Lane rules:** missing driver = the request waits (no pass counted); captcha = `status: captcha`, Windows toast + hub card, retried each pass, `plan_b: claude-in-chrome` after 3 passes, `final` error after 5; a pass takes 60-90 s for two legs.
- **Gotchas fixed:** a `2>>` redirect in the watcher held `lane.log` open and swallowed every log line (Python appends itself now); drivers must run with `PYTHONUTF8=1` or "München" arrives as "M\ufffdnchen"; never run a driver by hand while the watcher may be mid-pass (same profile, browser dies).

See [[reference_trippy_box_rail_price_limits]] (why the box cannot price these), [[reference_trippy_on_box]], [[reference_approval_hub]].
