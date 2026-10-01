---
name: reference_event_loop_voice_feedback
description: Built 2026-09-27 evening. The CRM reads every event (mail feeder, WhatsApp by full name, events ledger + optional Events view), Ctrl+Alt+S feedback shortcut, voice review on the three review pages, phone/https links.
metadata:
  type: reference
---

**His rulings (2026-09-27):** every event is read, show more rather than less, he corrects with one sentence (CRM
H33); the loop must be judgeable and he needs a fast "you missed this" (H34). The Events view is "a link separate,
only done if I REALLY want to review, but ideally never".

**Event loop (laptop, `~/.medtech-crm/crm-app/monitor.js`):** `runMailOnce` every 10 min = `gmail.py recent` on cdtm +
tundra, one event per MESSAGE (real id, real time), matched by address then thread; WhatsApp direct messages whose
push name is a full name carried by exactly ONE person attach to that person and the number is kept in
`p.identifier_candidates` (a candidate matches, it is never shown as the phone: found details are proposed, the
savior brings them in the 23:00 sweep). Every event, matched or not, leaves a line in
`~/.medtech-crm/events-ledger.jsonl` (who, what, what the system did). Events view: `events-api.js` +
`events-page.html`, `http://127.0.0.1:4137/events`, a = right, s = wrong + sentence (filed with addrule --contract
crm), verdicts in `events-verdicts.jsonl` and decisions.jsonl surface `events`. First catch: Christopher Zubiate's
WhatsApp of 25 Sep (introduction of Jeff Donovan) was invisible because his row had no phone.

**Feedback shortcut:** Ctrl+Alt+S = `~/.claude/feedback-shortcut/feedback.ps1` (screenshot first, one comment line,
Enter sends): record in `task-land/_system/feedback-inbox/feedback-<id>.{png,json}`, sent AS HIM with the screenshot
to the savior by `box:/home/da/hub-review/send_feedback.py`; unreachable box = `queued`, flushed with the next one.

**Voice review (prototype):** `task-land/_system/voice/` = `voice-review.js` (page), `voice-server.js` (required by
hub-review on the box, the intake server, the GTM board server: routes `/voice-review.js`, `POST /api/voice`,
`GET /api/voice/<id>`), `voice_review.py` (faster-whisper small + Opus). The page marks focus and verdicts with
their time in the recording; speech is attached to the item on screen; he corrects the result in a sheet, then it
is put on the items; commit stays the yes. While recording, a verdict key sets the verdict at once. Sessions are
kept in `~/.voice-review/<id>/`.

**Phone:** the microphone needs https. Tailnet-only `tailscale serve` on the LAPTOP: root = CRM (`?review=1#today`
opens review mode; the page reaches the intake API on :8446 when on https), :8444 = hub review (through
`approval-hub/forward-hub-review.js`, because tailscaled cannot proxy to another tailnet address), :8445 = GTM
boards, :8446 = intake (Events). Never serve :4137 itself over https: tailscaled then takes the Tailscale address
of that port away from the intake server. The box cannot serve https until he runs
`sudo tailscale set --operator=da` there. The links were sent as one Telegram message for him to pin.

**Also that day:** two stale server copies from 21 Sep were running old code (a CRM server holding only the
Tailscale address, an intake server holding no port); `coattio-serve.ps1` now checks the loopback listener.
j = back / k = forward was wrong on the CRM review and the GTM boards: fixed.
Related: [[reference_todo_pipeline]], [[reference_hub_review_ui]], [[reference_pretooluse_hook_hang_npx]].
