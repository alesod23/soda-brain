---
name: feedback_verify_state_not_queue
description: "\"It's not in the queue\" is never an answer to \"is it done?\" — when he names a task, go check the real system state (calendar, inbox, file) and do it if it isn't done."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 76b27505-2fd7-4161-a548-77a992a2ef56
  modified: 2026-08-03T21:54:04.070Z
---

When Alessandro says **"do card #N"** or **"N needs to be done"**, the only acceptable move is to
**check the underlying system** — the actual calendar event, the actual sent mail, the actual file —
and then do it if it is not already done. Queue state is not evidence.

**Why:** an approval card leaving the pending queue means *something resolved it*, not that the work
happened. The hub prunes resolved items and keeps no verdict, so "gone from the queue" is
indistinguishable between approved-and-executed, rejected, and expired. Cards with `action: null`
(most CDTM ones) execute NOTHING on approval by design — they are signals for whichever session
created them, so a card can be approved and still leave the work undone forever.

**Burned 2026-08-03:** he said "do #7". I answered that #7 had already left the queue so there was
nothing to do. He pushed back: *"If I tell you that number seven needs to be done you go and look.
Was it done? Was it not done?"* I looked: the Pre-Kick off tour event did NOT have Sharayoo or Jonas
on it. #7 had never been done. Same for #11, whose event did not exist. Both then took two minutes.

**How to apply:** name the observable that would prove it done, go read that observable, act on the
gap. For calendar work the CDTM route is `~/triage/gcal.py --account cdtm` (`list`, `invite`); it has
no update verb, so adding guests to an EXISTING event needs a direct `events().patch` with the full
attendee list preserved (see [[reference_approval_hub]] for why the card alone proves nothing).
Note `gcal.py invite` needs full RFC3339 seconds — `2026-08-18T17:30:00`, not `...T17:30`, which
400s.
