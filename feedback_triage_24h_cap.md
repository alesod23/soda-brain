---
name: feedback-triage-24h-cap
description: /triage hard-caps the fetch window at 24h; anything older is out of scope even if last_check_at is older
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c19162ff-56f0-4383-9e07-0dfdff7a81b1
---

/triage must NEVER look at items older than 24h, regardless of how stale `last_check_at` is. Effective cutoff is `max(last_check_at, now - 24h)`. WA fetch hours capped at 24 (was 168). Sole exception: explicit carryover (Gmail `triage/todo`, WA `wa-state.json#todo`).

**Why:** Anything older than 24h has effectively been seen on the phone or is ambient noise; surfacing it pollutes the round and wastes compute. Pairs with [[reference_triage_operations]] auto-done semantic — items that didn't get acted on in the day they arrived are dropped.

**How to apply:** Set in /triage skill Hard Rule 7 + step 2 fetch logic. Within the 24h window, classify thoroughly (including pulling burst content for groups with `count > 1` via `show-thread.js`). High-volume known-noise chats (e.g., Newspapers, certain family groups) stay handled via `wa-groups-block.json` even inside the 24h window.
