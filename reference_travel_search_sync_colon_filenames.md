---
name: reference-travel-search-sync-colon-filenames
description: "travel-search sync was stuck 19 days on ':' filenames the box committed and Windows cannot check out; FIXED 2026-09-25, guard_winnames now prevents it in every synced repo"
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

## FIXED 2026-09-25 evening (box side)

The three files are renamed to `-05-00` / `-10-00` and pushed: `origin/master` is **af7867e**, and
`git ls-files | grep ':'` now returns nothing. The one hard-coded reader (`turin-agen-2026-09/build.py:208`,
plus the `sources=` label at 262) follows the new names.

**There was no writer to fix.** The whole tree only ever READS those files (turin-agen hard-codes one,
rome-milan globs); the three names were typed by hand during that trip's build. Do not go looking for
a LeFrecce raw dumper, it does not exist.

Recurrence guard instead: **`guard_winnames` in `task-land/_system/vps/sync-guards.sh`**, called from
`repo-sync.sh` right after `git add -A`, so it covers all four synced repos. It UNSTAGES any staged path
containing `: * ? " < > |`, logs it, alerts once, and lets the rest of the commit through. Non-blocking
on purpose: refusing the whole commit (what `guard_markers` does) is what would recreate this exact
19-day stall. The file stays on disk untouched.

The laptop still has to merge `origin/master` and push its own `3ed5482` (us-tour board, `gflights_mc.py`,
preferences rule); real conflicts expected in `app/server.js` and `preferences.json`, the laptop takes them.

Lesson that generalises: the box reported sync success the whole time. A sync that only checks its own
side is not a sync check — [[reference_task_land_sync_parked_conflict]].

**RESOLVED 2026-09-25 20:50.** The box renamed the three files (`-05-00` / `-10-00`, commit af7867e); the laptop merged
origin/master (conflicts in `app/server.js`, one hunk, both sides kept; `preferences.json` resolved as a UNION of rules by
id, box version 2 + laptop `multi-city-book-anchors-only`, 20 rules) and pushed: master = origin/master = 0de4f2e.
There was NO LeFrecce writer to fix: the ':' names were typed by hand in that trip's build. Recurrence guard on the box:
`guard_winnames` in `task-land/_system/vps/sync-guards.sh`, non-blocking (unstages Windows-illegal names, alerts once),
wired after `git add -A` in `repo-sync.sh` for all four synced repos. Merge lesson: `git show :2:/:3:/:1:` the JSON and
union by id in Python instead of hand-editing three interleaved hunks.
