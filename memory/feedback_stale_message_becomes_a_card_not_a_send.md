---
name: feedback-stale-message-becomes-a-card-not-a-send
description: "Check the clock right before any send; a message whose time premise has gone stale becomes a hub card, never an automatic send, even on dsend."
metadata:
  node_type: memory
  type: feedback
  originSessionId: cf5ae3fd-6dd7-4c67-a2b6-86648910b2b3
  modified: 2026-10-05T19:19:38.555Z
---

Before any send, including a "dsend", check the clock and re-read the text. If time has passed since it was written and its premise has gone stale (a future appointment now in the past, "now", "today", "this afternoon", an urgency that has expired), it does NOT go out automatically. It becomes a hub card showing the text and naming what went stale, and he decides whether it still goes.

**Why:** 5 Oct 2026, he asked at ~15:40 for Caleb to get Isabella Heckel's details, "dsend on wa". The wa-daemon was down; I restarted it and sent at 21:15 without re-checking the clock. The message said "I'm with Isabella at 16:00 and I leave Germany this week" — five hours after that appointment. His words: "You should have checked the time before sending it, because you ended up sending it hours after you were supposed to. It was quite clear that was no longer a priority by that point. You should have maybe just turned it into a card, just to make sure. In general, it shouldn't have sent it automatically."

A dsend authorises the send at the moment he gives it, not hours later. A blocked send (daemon down, auth expired, a retry loop) is exactly the case where the delay is invisible to me and obvious to him.

**How to apply:** `Get-Date` or `date` immediately before the send call, not at the start of the task. Compare it against every time reference in the body. Stale → post the card instead and say so. Related: [[feedback_check_clock_before_timestamps]], [[feedback_every_email_draft_goes_through_the_lane]], [[feedback_message_send_protocol]]. Ledger: EMAIL-REVIEW-CONTRACT H107.
