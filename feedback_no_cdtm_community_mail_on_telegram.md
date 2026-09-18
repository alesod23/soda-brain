---
name: feedback_no_cdtm_community_mail_on_telegram
description: "Rule 2026-09-18: CDTM community / Google Group mail (jobs@, community@, all@ ... @cdtm.com) never surfaces on Telegram (cards or CATCH-UP recap) unless it is an event he could attend and was invited to. Box poller enforces it (CDTM_GROUP_RE / CDTM_EVENT_RE); laptop recap.ps1 still needs the same rule (handoff file)."
metadata:
  type: feedback
---

**His words (2026-09-18 13:35, replying to a CATCH-UP card carrying "[CDTM Jobs] Wanted | Chief of Staff ... Hypersonica"):** *"I don't want to see any of these CDTM community emails here on Telegram. It's not relevant for me. ... unless it's for an event that I could attend and we were invited to, I don't want to see it. Only the event ones are interesting to me."*

**Why:** CDTM Google Groups (jobs, community, alumni...) are high-volume and never actionable for him; the only thing he wants from them is an invitation he can accept.

**How to apply:**
1. Box live lane: `/home/da/sodanotif/pollers/gmail_poll.py` `classify_drop` returns `cdtm-group:not-an-event` for any mail whose To/Cc/List/Sender headers contain a cdtm.com group address, unless subject or snippet matches `CDTM_EVENT_RE`. A mail from a CDTM person sent directly to him is NOT a group mail and still passes.
2. Laptop recap (`recap.ps1`, the `🚨📬 CATCH-UP` cards): same rule to be added; see `task-land/_system/HANDOFF-20260918-recap-cdtm-groups.md`. Until then the leak can only come from there.
3. When in doubt about "event": invitation, workshop, talk, dinner, founders night, demo day, RSVP, save the date = keep; job posts, asks for help, surveys, announcements = drop.

Related: [[feedback_noreply_never_in_notifications]], [[feedback_sodanotif_never_surface_groups]], [[reference_sodanotif_live_gmail_slack]].
