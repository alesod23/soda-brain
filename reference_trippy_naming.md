---
name: reference_trippy_naming
description: /trippy is the CURRENT deep travel skill (was trippy-v2); /trippy-old is the superseded one-shot sweep (was trippy). Renamed 2026-08-03.
metadata: 
  node_type: memory
  type: reference
  originSessionId: bf0bebd2-3604-423b-9a28-9e820c600e70
  modified: 2026-08-03T18:55:30.206Z
---

Renamed 2026-08-03 at Alessandro's request, because "which one is v2 again?" kept costing time.

| Now | Was | What it is |
|---|---|---|
| **`/trippy`** | `trippy-v2` | **THE CURRENT ONE.** Deep search + persistent trip boards on the local webapp (`node app/server.js`, port 4126) + pairwise **context duels** → **big search** + the cross-trip preference wiki `travel-search/v2/preferences.json`. Code lives in `travel-search\v2\`. A new trip = a new DATA folder `app/trips/<slug>/`, never new UI. |
| **`/trippy-old`** | `trippy` | **SUPERSEDED.** One-shot sweep whose deliverable was a standalone HTML in OneDrive `cooked trips\`. No boards, no duels, no preference learning. Kept only because the shared helper (`travel-search\search.py`, the `sites/` adapters, the momondo/skiplagged anti-bot map) is still used and the old cooked-trips artifacts are still on disk. |

**How to apply:** route ALL new travel work to `/trippy`. Only touch `/trippy-old` if Alessandro
explicitly asks for the old one or wants a legacy `cooked trips\*.html` read back.

Naming debris that is NOT worth chasing and should not confuse you — these still say "v2" and
that is correct, they refer to the CURRENT skill:
- the code directory `travel-search\v2\` and everything under it
- the memory `project_trippy_v2.md` (its design log)
- `state/trippy-requests-watch.ps1` (a real filename on disk)
- older transcripts and the `.claude.json` history

The hard rule that survived the rename: **the persistent webapp is the ONLY deliverable.**
Never hand over a standalone `.html` as a trip board — a new trip is a data folder.

Related: [[project_trippy_v2]] · [[feedback_trippy_headless_parallel]] · [[feedback_trippy_durable_links]] · [[feedback_trippy_deep_dive]] · [[feedback_airline_direct_for_known_carrier]] · [[reference_travel_search]]
