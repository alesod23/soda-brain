---
name: feedback_approval_ping_once
description: "Approval cards ping ONCE on Telegram — the 5-min re-notify repeat is DISABLED (user rule 2026-08-31, supersedes the 2026-08-10 'reoccurs' rule)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 234469a5-bddc-4996-8988-c8ca2acf6cd5
  modified: 2026-08-31T14:48:04.206Z
---

**One approval card = ONE Telegram ping, at creation. Never repeat-ping for the same card.**

**Why:** 2026-08-31 the hub's re-notify loop re-fired the 🟣❓ TG ping for card #1 at +5 min (14:37 and 14:42). Alessandro: "you've done something which I specifically asked you not to do, which is to constantly ping me asking for approval… I think we removed that. You're only going to ask me once." This SUPERSEDES the 2026-08-10 rule that asked for re-firing cards ("reoccurs in the future…"), which is why the loop existed.

**How to apply:**
- `approval-hub/server.js` now has `TG_RENOTIFY_ENABLED = false` gating the loop's `pushTelegram(it)`. The re-notify loop still ticks (it also serves the deactivated phone lane); only the TG repeat is off. Fixed + hub restarted 2026-08-31 (verified: new process serving 4180, queue intact).
- Do NOT re-enable repeats, in the hub or by manually re-sending a card from a session, unless he explicitly asks. An unanswered card just waits in the queue (`/unresolved-ids`, laptop popup, /next).
- Same spirit session-side: never re-ping "did you see the card?" — ask once, then wait.

Related: [[reference-approval-hub]], [[feedback_laptop_ping_card_deactivated]], [[feedback_message_send_protocol]].
