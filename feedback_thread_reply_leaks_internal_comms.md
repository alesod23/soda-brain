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

**2026-09-07 - the guard was silently OFF for every "Last, First" contact, and quoting has a SECOND leak path.** Both found while replying to Laurie Westover (UPMC) and both fixed in `~/triage/gmail.py` (backup `gmail.py.bak-20260907-addrset`).

1. **`_addr_set()` split on "," by hand**, so a display name like `"Westover, Laurie A" <westoverla@upmc.edu>` parsed to `{'westover','laurie'}` and **dropped the real address**. `from_recipient()` therefore never matched Laurie, the picker fell through to `involves_recipient()`, and the reply threaded under a message from 5 days earlier (`NOTE: skipped 2 later message(s)` was the only clue). This broke the 2026-08-12 guard for **most hospital and enterprise counterparts** - Outlook shops write "Last, First" by default, which is exactly Tundra's whole target market. Now uses `getaddresses()` and keeps only chunks containing "@". Verified on all four header shapes.

2. **A quote leaks more than the message you quote.** Even with the right target, the quoted body carries whatever chain the sender had embedded in THEIR mail. Laurie's 31 Aug note (to Alessandro alone) embedded the thread back to 3 Aug, including John Klink's personal reference letter about Alessandro (Knights of Malta, Lourdes, Fatima) and his father Guido's introduction - in BOTH the text/plain and text/html parts. Scot and Pat had been on those originals, but **Caleb had not**: Cc'ing him would have handed the co-founder that personal history. New **`--no-quote`** flag on `gmail.py draft` keeps In-Reply-To/References (so it still threads) and pastes nothing.

**How to apply:** whenever you ADD people to the Cc of a threaded reply, assume the quote carries history they were never on. Grep the created draft's decoded parts for names that should not travel BEFORE handing it over, and prefer `--no-quote` + one line of context over an auto-quote. A quote is cosmetic; threading comes from the headers.

Related: [[reference_triage_gmail]], [[feedback_read_source_thread_before_acting]], [[project_cdtm_kickoff_tf]].
