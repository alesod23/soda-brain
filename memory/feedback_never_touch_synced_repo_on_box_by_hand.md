---
name: feedback-never-touch-synced-repo-on-box-by-hand
description: "Never scp, rm or edit a file inside a synced repo on the box by hand - the box sync commits it within minutes and it lands on both machines"
metadata:
  node_type: memory
  type: feedback
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-28T12:25:44.801Z
---

Never copy, delete or edit a file by hand inside `box:~/task-land` (or any repo the box syncs). Write it on the
laptop inside the repo and let the sync deliver it; for a first run on the box, copy it to `/tmp` and run it from
there.

**Why:** 2026-09-28. I scp'd `box_watch.py` into `box:~/task-land/_system/gtm-agent/`, then removed it to "let the
sync deliver it". The box's sync (every 5 minutes) committed the deletion and the file vanished on the laptop too.
Restored from git (`git show <commit>:<path>`), 75 minutes later.

**How to apply:** box code that lives in task-land is edited on the laptop only. If a file is missing after a sync,
`git log --diff-filter=D -- <path>` names the commit. See [[reference-task-land-sync-parked-conflict]].

**Exception agreed with the savior (2026-09-30, 01:00):** box-run code inside task-land (`_system/hub_outdated.py`, `_system/gtm-agent/box_*.py`, `_system/vps/*`) may be edited on the box when it cannot wait, provided the savior names the file and the commit in a message the same time, so the laptop merge is expected (merge, never rebase; keep both sides). Everything else in a synced repo is still changed on the laptop only. First case: `hub_outdated.py`, box commit 11671050a on top of laptop 782f89ae4; laptop H17 change in `main` section 1b/2, box change in `mail_events` + the moot branch of `main` section 2: both must survive the merge.
