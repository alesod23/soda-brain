---
name: feedback_trippy_durable_links
description: "cooked-trip HTML booking links must be durable (airline-direct or Google Flights route+date), never momondo/skiplagged session tokens"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4b116091-5aff-47a4-b90c-e7133706c72b
---

Trippy cooked-trip HTML links "never work afterwards" because they stored momondo per-result redirect URLs (`/book/flight?code=…&cookieOverrides=…&viewId=…`) — these embed a live-search `viewId`/`code` session token that expires in minutes-to-hours, so every link is dead on the next open.

**Why:** the HTML is reopened days later with zero session state; a link is only useful if it resolves cold. The "airline link inside the momondo result" is ALSO a momondo redirect token, so scraping it does NOT make it durable.

**How to apply:** store links carrying the flight's own identity (route + date), which regenerate a live search every open:
1. Airline-direct search deep-link for single-carrier flights. Verified durable for United: `united.com/en/us/fsr/choose-flights?f=<O>&t=<D>&d=<YYYY-MM-DD>&tt=1&sc=7&px=1&taxng=1&newHP=True&clm=7&st=bestmatches&tqp=R` (cold-tested in a fresh no-cookie profile → landed on the right results).
2. Google Flights route+date for multi-stop/multi-carrier connections: `google.com/travel/flights?q=Flights%20one%20way%20from%20<O>%20to%20<D>%20on%20<YYYY-MM-DD>&curr=EUR&hl=en`.

Always cold-test a new link template once before trusting it. Repair tool: `~/.claude/travel-search/fix_html_links.py` (momondo `/book` → Google Flights, keeps airline-direct, writes `.bak`). Rule baked into trippy SKILL.md cooked-trips section 2026-06-09. Also relevant: United transatlantic Basic Economy includes a full carry-on trolley (unlike US-domestic Basic). See [[reference_travel_search]].
