---
name: reference_travel_discount_cards
description: "His travel cards, to apply in EVERY search without being asked: SNCF Carte Avantage Jeune, DB BahnCard 25, Volotea Megavolotea subscription."
metadata:
  type: reference
---

**Standing rule, his words 2026-09-20: "Make sure you always do from now on. I should never have
to specify it. It's part of what we have."** Every travel search prices these in by default, and
the board says so per leg:

| Card | Where it applies | How to price it |
|---|---|---|
| **SNCF Carte Avantage Jeune** | TGV INOUI, Intercités, OUIGO-adjacent SNCF fares. He calls it 25%; the card is officially **-30%** on TGV/Intercités and the observed fares match 30%. | From the box: `travel-search/trainline_render.py search <a> <b> <date> --railcard avantage-jeune` (Trainline GraphQL, works, not DataDome-blocked). `--compare` gives with/without. `discount_applied` in the JSON says whether it actually bit. |
| **DB BahnCard 25** | Every DB leg (ICE, IC, and the German half of Paris-Munich). | NOT priceable from the box. Box-to-laptop rail lane: request JSON in `~/gdrive/DA/trippy/requests/`, `cards:{db:"bahncard25_2"}` - see [[reference_trippy_rail_lane]]. Trainline shows those legs as "Super Sparpreis Young" with `discount_applied:false`, i.e. the BahnCard is NOT in that price. |
| **Megavolotea (annual subscription, paid)** | Volotea flights. | Check Volotea on every search and compare against the rest; if it is not an advantage, ignore it silently. Volotea is a secondary-city carrier, so on Paris routes it often has no service at all - say "no Volotea route" only after checking, never as an assumption. |

**Known engine gap (measured 2026-09-20):** `gflights.py` returns Google's "best" block only, and
on airport-to-airport pairs it returns **nothing at all** - `MXP->CDG` nonstop came back with zero
options, which is false. So easyJet, Ryanair, Wizz and Volotea are effectively invisible to the box
flight search, and any "cheapest flight" claim from it is only about ITA/AF/LH. Either fix the
airport-pair path or price low-cost on the laptop before telling him a flight is the cheapest.

Related: [[reference_trippy_box_rail_price_limits]], [[reference_trainline_graphql_box]],
[[reference_gflights_engine]], [[reference_trippy_on_box]].
