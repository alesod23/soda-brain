---
name: feedback_never_run_coattio_sync_by_hand
description: On the box never run coattio-sync.sh by hand to "pull now": racing the */2 cron run, its restart left :4124 and :4137 both DOWN (10 Oct 2026)
metadata:
  type: feedback
---

10 Oct 2026 15:29: SODA SYSTEM asked me to pull coattio on the box. I ran `bash coattio-sync.sh` by hand while the */2 cron run was doing the same pull; the two `start-box.sh --restart` raced ("already up" read on dying processes) and the CRM (:4124) and intake (:4137) stayed DOWN until I ran `start-box.sh` myself ~2 min later.

**Why:** the restart checks the port before the old process has released it (same family as the hub-review port race of 5 Oct).

**How to apply:** to get a coattio commit live on the box, wait for the cron (every 2 min) and verify with curl; if a pull is needed now, `git -C /home/da/coattio pull --ff-only` only (static files under crm-app/public are read from disk, no restart). A server change: `bash start-box.sh --restart` once, then check `ss -ltn` for :4124 and :4137.
