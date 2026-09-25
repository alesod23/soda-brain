---
name: reference-travel-search-sync-colon-filenames
description: "travel-search laptop<->box git sync stuck since 2026-09-06 because the box commits filenames containing ':' that Windows cannot check out"
metadata:
  node_type: memory
  type: reference
  originSessionId: 2b505a93-c80e-47bd-81f5-c7b174f73267
  modified: 2026-09-25T12:05:14.559Z
---

Found 2026-09-25 (us-tour-2026-10 session): laptop `~/.claude/travel-search/v2` was `ahead 1, behind 26` on
`alesod23/travel-search` master. `git merge origin/master` fails with
`error: invalid path 'app/trips/turin-agen-2026-09/raw/lefrecce-torino-paris-05:00.json'` (':' is illegal on NTFS).
So every box commit since 2026-09-06 is unmergeable on the laptop, and laptop commits cannot be pushed.

Fix needs the box side: rename those raw files (no ':' in names, e.g. `05-00`) and fix whatever writes them
(the LeFrecce raw dump on the box), then merge on the laptop (merge, not rebase; see [[reference_task_land_sync_parked_conflict]]).
The remote also changed `app/server.js` (~248 lines) and `preferences.json` meanwhile, so expect real conflicts there.
Local commit 3ed5482 (us-tour board + gflights_mc.py + preferences rule) is waiting to be pushed.
