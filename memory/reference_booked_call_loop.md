---
name: reference_booked_call_loop
description: A call somebody books on his calendar (website link / their invite) -> CRM row + step + stale slot cards closed + ONE keep/move/decline card (meeting_loop.calendar_booked); register.py refuses slot offers to a booked person (exit 7)
metadata:
  node_type: memory
  type: reference
  originSessionId: a0b93892-0bfc-4233-a9b1-90dc29d6e1b7
  modified: 2026-10-01T01:26:38.846Z
---

**Built 2026-10-01 from his sim-learner sentence (sim 2026-10-08, E0040, scenario S017):** Felix booked Tue 13 Oct
14:00 through the website link; the row kept "confirm a 20-minute intro call", and the savior's rewrite of the
'propose slots' draft (card #7) reached the hub 7 min later. "nobody asked me if i keep it or send the deck".

- `~/gtm-eng/agent/meeting_loop.py` `calendar_booked()` runs every pass (07-23, calendar read only, no model):
  future event on tundra or cdtm whose organizer is outside OR whose description says "Booked by" (Google appointment
  schedule puts HIM as organizer, e.g. "30 min with Alessandro (Anna Candiani)"), created since `booked_since`
  (state; first pass = now - 2 h, so old bookings are never carded), address = a CRM row -> `call_booked` + activity
  `meeting_booked` linked to their last inbound message, step "decide: keep, move or decline the call X booked for
  ...; still open from before: <old step>", open hub cards about them that offer a time before the call ends are
  closed (`/close`, `[observer]`, sidecar `withdrawn_booked`, Gmail draft kept), ONE card (meta.kind booking).
  `booked_verdicts()`: yes = "prepare the call (kept)", a sentence = the step, no = "decline the call (email)".
  Never accepts, declines or sends. Unknown booker -> `booking-no-row` in meeting-loop.jsonl, no card (not built).
- `~/task-land/_system/drafts/register.py` `booked_gate()`: addressee already in a future event and the body offers
  an alternative before that call ends -> not registered, exit 7, sidecar `withdrawn_booked`. A follow-up AFTER the call passes.
- `~/triage/slots.py`: events carry id/created/organizer/with/booked_via; `booked_with()`, `proposes_other()`,
  CLI `slots.py booked <addr>`; when gcal is not importable it reads through `~/triage/venv` (the box's register.py
  runs system python3 and could NOT read the calendar before, so the E0039 slot check was blind there too).
  Box copy scp'd by hand (not a synced repo).

Proof: `python ~/sim/harness/tests/replay_booking_e0040.py` (ALL PASS 2026-10-01). Backups `*.bak-20261001-booking-feedback`
(laptop, sim copies, box ~/triage/slots.py).
Related: [[reference_meeting_loop]], [[reference_slot_calendar_check]], [[reference_simulation_harness]], [[reference_draft_review_lane]].
