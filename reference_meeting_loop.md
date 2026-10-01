---
name: reference_meeting_loop
description: Meeting loop (task DA-MeetingLoop, every 5 min): a finished call in Notion meeting notes becomes a CRM event and ONE hub card proposing the next step, within 15 min (CRM H41, 2026-09-29)
metadata:
  type: reference
---

`~/gtm-eng/agent/meeting_loop.py run|status|redo <url>`, task DA-MeetingLoop every 5 minutes through `meeting-loop-hidden.vbs`, watched by the system agent. State `meeting-loop-state.json`, trace `meeting-loop.jsonl` (every `carded` line carries `minutes_after_the_call`: that is the number to judge it by; his limit is 15).

How it sees a call: his Notion AI meeting notes, read by a headless claude carrying only the Notion server (no Notion token exists). Listing = sonnet, every 10 min; a note known to be recording is read directly by opus at every pass. Internal meetings (Caleb, weekly) and empty notes get no card. The other side's address comes from the calendar event at that time (tundra and cdtm).

Output (his ruling 2026-09-29, CRM H41): the call is written on the person's row at once (activity `meeting`, `last_meeting` with what each side owes, facts), and ONE hub card proposes the next step: yes = step on the row, a sentence = his sentence is the step, no = no step. Before this the calendar scan (cdtm only) wrote a silent `meeting` on the row and the Notion scan of `crm-app/sources.js` timed out every time; the notes themselves were never read.

**Why:** "dovresti essere tu proattivo e farmi una richiesta, di un evento, di un automatico next step, su cui posso darti un feedback in maniera semplice".
**Known limits:** each model start takes minutes when the laptop is short of memory; laptop off = nothing runs (the box would be the place). After a yes the step is set, the follow-up mail or invite is not drafted by the loop yet.

**Booked calls (2026-10-01):** `calendar_booked()` / `booked_verdicts()` in the same loop, see [[reference_booked_call_loop]].

Related: [[reference_system_agent]], [[reference_event_confirm]], [[reference_approval_hub]].
