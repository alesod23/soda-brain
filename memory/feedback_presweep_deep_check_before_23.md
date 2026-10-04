---
name: feedback_presweep_deep_check_before_23
description: "Standing rule 2026-09-19: every day BEFORE the 23:00 digest the savior does a thorough pass over every open hub card against what he has already said or done (Telegram history, Gmail Sent, WhatsApp store, coattio, tasks, board commits, brain notes) and closes with cited evidence everything already settled. Only real judgement calls survive. Final objective: he is not a bottleneck, no dumb reviews."
metadata:
  type: feedback
---

**His words (2026-09-19 01:14):** *"a lot of the ones i skipped could have figured out by taking a hard look at hte messages i sent (i had alreayd sent...) so everytime before 11pm from now on YOU WILL DO THAT THOROUGH CHECK. no need ot have stupid outstanding ones. final obj: to remove me as a bottleneck, no need for dumb reviews."*

**How it runs (since 4 Oct 2026, registry M5):** the pass is `task-land/_system/hub_outdated.py` (box cron every 10 min, durable); its first full pass from 22:12 local writes the stamp (`stamp_presweep`). The old savior session cron (CronCreate, 7-day expiry) never wrote a stamp from 19 Sep on and is retired: do not re-arm it. Durable backstop: `~/.local/bin/presweep-watchdog.sh` at 22:47 via crontab, which only tells him on Telegram when the check did not happen (stamp file `~/.local/state/presweep-<date>.done`, written by the savior at the end of the pass).

**The pass:** for every open card, hunt for an answer already given in his Telegram history (`resolve.py --last 400`), Gmail Sent on both accounts, `wa-daemon/message-store.jsonl`, coattio (`:4124/api/data`), `task-land/Tasks`, `gtm-eng/boards/*/commits`, medtech-brain. Close with `POST :4180/close {id, verdict, reason, notify:false}` and cite the evidence in the reason. Typical closables: a draft he sent himself from Gmail, a contact already in coattio, a notice he has acknowledged, a 48h task card whose task file exists, duplicates, cards whose date has passed. Fix what is fixable (create the task, write the CRM note, reconcile the sidecar) instead of leaving it. NEVER send anything outbound as part of the pass; a draft card closes only when the mail is already in Sent.

**Also ruled the same night:** the 23:00 digest is no longer a hub card (it was appearing inside the review page, self-referential); `triage/eod_sweep.py` sends it as a plain Telegram message with the review link and the key legend, and `hub-review` filters that type out for good.

Related: [[feedback_hub_digest_replaced_by_review_page]], [[reference_hub_review_ui]], [[feedback_commit_batch_is_the_yes]], [[reference_approval_hub]].
