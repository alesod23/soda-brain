---
name: feedback_thread_reply_leaks_internal_comms
description: "Threading a reply onto a MIXED thread quoted internal Alessandro-Raunaq chatter under a mail to Prof. Diepold. gmail.py now picks the quote target by recipient, not by last-inbound-message"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bcf4ed36-d8ed-4e48-817b-146c5998e5ca
  modified: 2026-08-11T22:47:50.151Z
---

2026-08-12: *"you made a big oopsie btw (i fixed): you had answered an email convo with internal comms btwn me and raunaq vs. just last sent email by me to prof. diepold"*. He caught it in Gmail and repaired it before sending.

**What happened.** The Diepold speaker thread (`19ee68ae7f33b9ed`) is **mixed**: mails to the professor interleaved with side chatter between Alessandro and Raunaq *about* him ("Should I send him a different type of slot since he's online?", the "Good news!" forward). I passed `--thread-id` and let `gmail.py` auto-quote. Its rule was *"walk backwards to the first message that is not SENT and not DRAFT"* - which landed on **Raunaq's internal reply**. The draft addressed to `kldi@tum.de` therefore quoted internal comms and set `In-Reply-To` to them.

**Fixed in `~/triage/gmail.py`** (2026-08-12), new `_pick_quote_target(msgs, to, cc)` used by BOTH `cmd_draft` and `cmd_send`:
1. prefer the most recent message **From** one of the `--to`/`--cc` addresses, so the quote reads "On <date>, <them> wrote";
2. else the most recent message they were merely **on** (From/To/Cc);
3. else quote nothing and print `WARNING: no message in this thread involves the recipient(s)`.
It prints `NOTE: skipped N later message(s)...` whenever it steps over side chatter, so the skip is visible in the output.
Verified on the real thread: `In-Reply-To` went from Raunaq's `@mail.gmail.com` id to Diepold's `<...@tum.de>`, and the quoted block is Diepold's own 27 Jul mail.

**How to apply, beyond the code:** the tool fix removes the sharpest edge, it does not remove the duty. **Before threading any reply, look at who is actually in the thread.** CDTM speaker threads, investor intros and anything Raunaq is Cc'd on routinely carry internal discussion in the same thread. If a thread is mixed, either reply to the specific message or start a clean one. Read what will be quoted before creating the draft, not after.

Related: [[reference_triage_gmail]], [[feedback_read_source_thread_before_acting]], [[project_cdtm_kickoff_tf]].
