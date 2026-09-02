---
name: feedback_pending_send_check_before_nudge
description: "When a draft awaits the user's go-ahead and they don't address it for 2 messages, VERIFY myself whether they already sent it (list-drafts / read thread) instead of nudging again"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2b7bffd4-b341-4563-bac6-c61cb5a5f2ed
---

Standing rule from Alessandro (2026-07-15, Telegram): "if for 2 messages I don't tell you anything, do a check if I did it myself (for emails at least), so you don't bother me any longer."

**What happened:** I created a Gmail draft to Sebastian and waited for "send". The user sent it themselves from Gmail. Two messages later I was still nudging "the draft is waiting on your go" — annoying, and wrong about the state.

**Why:** A pending-confirmation draft is shared state the user can resolve out-of-band (they have the same Gmail). My in-conversation flag ("awaiting go") goes stale silently.

**How to apply:** Whenever a send is pending my confirmation gate ([[feedback_message_send_protocol]]) and the user sends 2 messages without addressing it, check the real state BEFORE mentioning it again:
- Email: `gmail.py list-drafts` (draft gone = sent) or read the thread for a new outbound message.
- Other channels where feasible (WA/Slack): read the chat for a recent outbound message matching the draft.
If they did it themselves, drop the pending item silently (at most a one-line "saw you sent it yourself"). Never re-nudge without checking first.
