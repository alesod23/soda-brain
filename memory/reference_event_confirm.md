---
name: reference-event-confirm
description: "Event mode - the Confirmed button under every conversation note of an event companion page works the next steps (CRM, Gmail draft through the lane, plan back on the page)"
metadata:
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-28T12:40:46.731Z
---

His words, 2026-09-28, from the Snitem DM connecte day: "you are to understand when i am going to an event ... i'll
always have in these events two places in which you can find important data: a series of messages on tg about it, a
webapp to add notes/events. even if i dont push them, those are to be monitored for next steps. have for each
conversation a button that says confirmed -> it starts to proactively work the next steps, based on all the text
from the meeting."

**Built the same hour (box, `~/research-page/`, not a synced repo; sources kept in `~/hubrev-work/event/`):**
- `event_confirm.js`: generic, adds "Confirmed" under every `<textarea data-k="note:<key>">` with text. Served at
  `/confirm.js`; the server appends the script tag when it serves the page, so a rebuild keeps it.
- `snitem_server.py`: `POST /api/confirm {k}` sets `confirmed:<key>` and starts the worker detached
  (TELEGRAM_STATE_DIR = telegram-null, so the savior's poller is never touched).
- `event_next_steps.py`: reads the note, the person's card on the page, the other notes naming the person, an
  address left in an empty Gmail draft; Opus (no tools, his drafting skill in the prompt) returns who, what was
  said, promises, dated next steps, the message. Then: CRM `POST :4137/intake` (event + comment = next step), the
  email as a REAL Gmail draft through the lane (his empty draft filled in place with `update-draft`, sidecar,
  `register.py` = hub card), the plan written back under the note, "FOR YOU" = what only he can answer. Never sends.
  Dry run on Alexandre Benoist: 48 s. Log `data/event-next-steps.jsonl`.

**Not built yet:** detecting by itself that he is at an event (calendar + Telegram), reading the Telegram messages
about the event into the worker, watching notes he never confirms, checking proposed slots against his calendar.
A new event page gets the button by serving `event_confirm.js` and adding the `/api/confirm` route.

Related: [[feedback-event-companion-pages]], [[project-event-contact-workflow]], [[reference-system-agent]].
