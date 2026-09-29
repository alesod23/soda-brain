---
name: feedback_after_a_call_prepare_the_followup
description: After a call the follow-up is PREPARED (draft in the lane + invite ready), not only proposed; a call with no notes still gets a card (2026-09-29, UPMC and San Raffaele)
metadata:
  type: feedback
---

His words (2026-09-29, 23:00): "You did not see that from my call with UPMC. It's clearly we have to send them some material. You are not proactive on that at all ... give me an approval card, which is like: Hey, I have a draft ready for you to tell them that you've just sent them an invite, and I have an invite ready for you to send."

**Why:** the meeting loop only proposed a step; the mail and the invite he owed after San Raffaele and UPMC were not prepared for hours, and the UPMC notes were empty so nothing happened at all.

**How to apply:** `meeting_loop.py` now drafts the follow-up through the lane (its own card) and keeps the invite as a dry run created on his yes to the meeting card; a calendar call with an outside attendee and no notes gets a card asking for one sentence, and his sentence becomes the draft. A session that sees a finished call does the same by hand: draft + invite + one card, within the hour. Kevin Marraccini at UPMC was findable in the invite thread, not in the notes: look in the mail threads too.
