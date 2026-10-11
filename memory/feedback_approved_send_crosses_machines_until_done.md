---
name: feedback_approved_send_crosses_machines_until_done
description: An approved send the current machine cannot do is handed to the other machine (laptop or box) and pursued like a /goal until sent; his approval is the send authorisation; laptop down = wait and be ready
metadata:
  type: feedback
---

10 Oct 2026, TG 21:22 Rome, after his edited Slack message to Lena Voß sat unsent on hub card #142 for a day (the hub has no Slack send action): "in the future, for ANY send that you cannot do on either laptop or box, find a way to communicate to the other that you want to do it. you have my confirmation to send in those cases, so its like a /goal function that you should not stop until completed. (if the laptop is down, the praxis is to wait until back up and be ready)". Filed in the hub ledger (addrule --contract hub).

**Why:** an approval that dies in a lane gap is worse than no approval: he believes it went out.

**How to apply:** when he has approved a message (yes on a card, "send", an edit he approved) and this machine cannot send it (no Slack/LinkedIn/WA/Gmail path here), send a cross-session message to the other machine's session (SODA SYSTEM on the laptop, the savior on the box) with the exact text, recipient, channel/thread and his approval quote; it sends without asking again. If the other machine is offline, the message queues; check on reconnect that it went out, and tell him it is pending, not done. The clock check still applies before the actual send ([[feedback_stale_message_becomes_a_card_not_a_send]]).

**11 Oct 2026, the miss:** his dsend on card #6 (Smoot + Stark LinkedIn DMs) went through hub-review's feedback worker into `jobs.py`/`job_runner.py`, which started it on the BOX (no LinkedIn) and told him "queued, waiting for the laptop". He: "why did you fail here?". The rule lived only in ledgers/memory, not in the job runner. Until the runner routes laptop-only jobs itself: when I see any approved send parked or "waiting", I hand it to SODA SYSTEM myself the same minute (exact text, recipient, thread, his quote) and stop any box copy so nothing double-sends.
