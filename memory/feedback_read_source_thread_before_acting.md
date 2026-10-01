---
name: feedback_read_source_thread_before_acting
description: "When a request references an external conversation (a message being replied to, a person's proposal), fetch and read that actual thread before acting — don't execute off the instruction's literal wording alone."
metadata:
  node_type: memory
  type: feedback
  originSessionId: b205178d-e8c7-4fb5-bb4a-2728bf7343bd
---

**Before executing an action tied to an external conversation, pull up the actual message thread/exchange being referenced and read it — don't just pattern-match the words in the user's instruction.**

**Why:** 2026-07-08 — user asked to send a reply to Sven ("...put it to 4pm (?). Caleb might be able to join online on friday, too.") and "move the meeting in which he's also invited from tonight to that time (4pm)". I moved the meeting to 4pm **today** instead of pulling up the actual WA exchange between the user and Sven first. That exchange (which I had access to via WA triage/search but didn't check) would have shown Sven's actual proposal was **Friday** 4pm — the "Caleb ... friday" clause in the very message I was sending was itself the tell, and I still missed it. The user corrected me and noted this is a general pattern: "you didn't really look at the full exchange of two messages we had... you seem pretty bad at considering the conversation block/cell in your reasoning."

**How to apply:** Whenever a task references "his message", "what we discussed", "the meeting he proposed", "her reply", etc. — even if not explicitly told to — fetch the actual source (WA thread via triage/search, email thread, Slack thread) and read both sides of the exchange BEFORE drafting a reply or taking a dependent action (rescheduling, confirming a decision, updating a record). Treat the literal instruction as a summary that may drop or garble a detail (like which day), not as the full ground truth. This matters especially because the user (his own words) doesn't ask often, so each ask deserves full-context care rather than fast literal execution. Cross-check any date/time reference in the instruction against the source thread's actual content before writing it to a calendar or sending it as confirmed.

See [[feedback_channel_sequential_handling]] (related: reconstructing channel context before acting) and [[reference_wa_sender]] (how to pull WA thread history).
