---
name: reference-calendar-rsvp-is-not-a-reply-owed
description: "A calendar RSVP to his invite (Accepted:/Accepté :/Accettato:, 'has accepted this invitation') never raises reply_owed in the CRM; the reader releases any reply owed it judged not owed (Ramana Sastry, 4 Oct 2026)"
metadata:
  type: reference
---

`~/.medtech-crm/crm-app/monitor.js` `isRsvp(ev)` / `MAIL_RSVP` (same test as gmail.py `_cal_type` 'reply', plus it/fr/de):
an RSVP still counts as their answer (facts.replied, stage) but `stepEffect` never sets `reply_owed` for it and writes
`reply_seen` at its day, unless a real reply is still owed. `crm-app/reader.js`: when the reader's step is not
"answer X" and the reply_owed in its prompt is still the same, the flag is released (before: only when who_owes = them).

**Why:** 4 Oct 2026 crm-review, Ramana Sastry: "You should have noticed that I did send this email in the end. It's a skip
because it was already sent." He answered and sent the invite on 1 Oct; Ramana's 2 Oct RSVP "with a note" set reply_owed,
the reader wrote "no reply is owed" but kept the step his (the demo call), so the flag stayed and Today asked "answer Ramana".
Vincent Carte-Jacquesson had the same flag from "Accepté : ... Intro Call".

**How to apply:** a new inbound source that can carry calendar responses sets `ev.rsvp = true` or goes through isRsvp.
Repair recipe: `tools/clear-rsvp-reply-owed-20261004.js [--pid x] [--apply]` (reads events-ledger.jsonl). Test:
`node --test tests/rsvp-no-reply.test.js`. :4124 server.js runs the monitor and loads the code on its next restart.

Related: [[reference-reply-check-before-draft]], [[reference-call-steps-get-no-draft]], [[project-crm-review-loop-vision]].
