# CATCH-UP surfaces messages he has already answered

His words, 2026-09-20 14:36, replying to a CATCH-UP card carrying "Anjella Klaiber 08:58 - Sure, I
will note this! Do you know if Caleb is planning to attend the event?":

> I've answered this. so clearly read it... this flags a limitation in the system. fix it so wont
> happen again

## Root cause, located

The rule he is invoking already exists **and is implemented on the box**. `sodanotif/pollers/slack_poll.py`
says so in its own header and enforces it in `incoming()`:

```python
# ... anything the user already answered (a message older than the user's own later
# message in the same conversation, user rule 2026-07-15)
keep = [m for m in keep if float(m["ts"]) > my_last]   # already answered by the user
```

So the per-message flagger cannot leak an answered message. The CATCH-UP card does not come from
there: it is `recap.ps1` on the LAPTOP (scheduled task `SODANOtif-Recap`, cadence gate in
`sodanotif/recap-last-push.txt`), which builds "everything currently unread" on its own and does
**not** apply the already-answered rule.

Note the file does not exist anywhere on the box, not even in `task-land/_system/box-tools/` or
`laptop-tools/`: it is unmirrored laptop code, which is why it keeps drifting from the box filters.

## This is the second leak of exactly this shape

`HANDOFF-20260918-recap-cdtm-groups.md` (2026-09-18) is the same story: a rule was implemented in
the box poller (CDTM community mail never surfaces) and `recap.ps1` still needs it. That one is
still open. Two independent rules, both enforced on the box, both missing from the recap.

**The pattern is the bug.** Any rule about what may reach him has to be enforced in one place, and
the recap is a second, unsynchronised place.

## The fix, in order of how durable it is

1. **Best: the recap stops computing its own unread list.** It consumes what the box already
   filtered (`sodanotif/notification-log.jsonl` + the poller store) instead of querying Slack and
   Gmail itself. Every current and future rule then applies to both surfaces for free, and the two
   open leaks close together.
2. **Or: move the recap to the box entirely.** Gmail and Slack polling already live there since
   2026-09-16; the recap is the only piece left on Windows, and PowerShell is not buying anything
   here. It would then reuse `incoming()` directly.
3. **Minimum patch, if the recap must stay as it is:** before rendering any Slack item, fetch
   `conversations.history` for that conversation and drop the item when a message from the user's
   own `user_id` has a later `ts`. Same for Gmail: drop a thread when the newest message in it is
   from him. That is the rule as the poller already implements it.

Whoever does 1 or 2: the answered-check must not be re-implemented, it must be imported from
`slack_poll.incoming()` so there is a single definition.

## Verification

Ask him for a conversation he has answered today, then run the recap on demand
(`recap.ps1 -OnDemand`) and confirm that conversation does not appear. Re-run after a fresh
incoming message in the same conversation and confirm it does appear again.
