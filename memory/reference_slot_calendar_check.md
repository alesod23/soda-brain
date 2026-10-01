---
name: reference_slot_calendar_check
description: "calendar_source: every meeting slot offered to him or by him is checked against his calendar with its duration (~/triage/slots.py), wired into inbound_asks, register.py and the CRM reader"
metadata:
  node_type: memory
  type: reference
  originSessionId: 1bce0277-2f03-4f61-b9ab-209001651170
  modified: 2026-10-01T01:07:05.356Z
---

**Built 2026-10-01 from his sim-learner sentence (sim 2026-10-08, E0039/E0040).** Before it, no writer read the calendar:
Francesca's step offered Tue 13 09:30 (45 min) or Thu 15 10:00 and picked neither, though Tue 13 runs into the 10:00 Vantro
call; the savior's rewrite (card #7) offered Felix Tue 13 10:00, the Vantro slot itself. (The CRM's own `sources.js`
calendar scan reads only the cdtm calendar; Tundra bookings land on the tundra one.)

`~/triage/slots.py` (laptop AND box `~/triage/`, not in a synced repo, scp it by hand after a change; a copy also in
`~/sim/harness/fakes/triage/` so the sandbox reads the fake calendar):
- `busy()` both calendars (tundra + cdtm), declined/transparent/cancelled skipped; an unreadable calendar is an error, never "free".
- `check(slots, cal)` overlap WITH duration (end == start is not a clash); `block()` the prompt block; `guard(body, ctx)` =
  regex prefilter for a clock time -> model extracts proposed/accepted slots -> check -> one rewrite to a free slot -> re-check.
- CLI: `python slots.py block|busy|check <start> <min>|guard --body-file F`.

Wired in: `gtm-eng/agent/inbound_asks.py` judge() (calendar block in the prompt, `slots` in the JSON, a clashing chosen slot
is asked again once, else a question on the card; card + sidecar carry a "calendar:" line); `task-land/_system/drafts/register.py`
calendar_guard() on EVERY email draft, with or without the critic (the savior registers with --no-critic): a clash is
rewritten as a new draft (pre-loop body kept, like a critic rewrite) and the sidecar gets `calendar:`, which send_card.py
appends to the card text; `.medtech-crm/crm-app/reader.js` refreshCalendar() before each read puts the block in the prompt
(the live CRM server picks it up on its next restart).

Proof: `python ~/sim/harness/tests/replay_slots_e0039.py --model` (ALL PASS 2026-10-01: Thu 15 10:00 chosen, Tue 13 clash
named, card #7 moved to a free slot). Backups `*.bak-20261001-slots-feedback` / `~/.claude/backups/*-20261001-feedback`.
Related: [[reference_simulation_harness]], [[reference_draft_review_lane]], [[reference_meeting_loop]].
