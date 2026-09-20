---
name: feedback_state_check_sent_and_calendar
description: "Before saying a follow-up is pending, check the SENT folder and the calendar. An open hub card or an unanswered inbox thread is not proof that nothing was done."
metadata:
  type: feedback
---

His verdict on the first CRM catch-up board (2026-09-20, 01:28): *"hai fatto schifo. in molti non
ti sei accorto che c'e stato un progresso dopo."* Four items of twelve described a world that had
already moved:

- Nocco: I wrote "the email has not gone out". He had written twice, 15 and 18 September, and he
  sees Nocco in person at the AIIC Lombardia convegno on the 21st.
- Roussel: I wrote "the draft has been sitting for eleven days". He had replied on 18 September.
- Iadanza: I proposed resending on Monday. He had resent on the 18th.
- Ward: I proposed verifying the invite. It was already booked for Monday 16:30.

**Root cause, exactly:** I read inbox threads and approval-hub cards, and never read the SENT
folder or the calendar. A hub card is a *proposal frozen at the moment it was written*, so an open
card proves nothing about reality. An unanswered inbox thread proves nothing either: he may have
answered from another account, or handled it by phone, or already have the meeting on the calendar.

**Before any statement of the form "this is still pending":**
1. `gmail.py search --query "in:sent (<name or address>) newer_than:30d"` on EVERY account he uses
   for that person (tundra, cdtm, sodano23, lobbly), not just the one the thread lives in.
2. The calendar, both `alessandro.sodano@cdtm.com` and `alessandro@tundrahealth.ai`: a booked
   meeting is the strongest possible evidence that the thread moved.
3. The WhatsApp store when the person is reachable there.
4. Only then the hub cards, and treat them as proposals, never as state.

Every item on a review board must also declare what it was checked against and up to when, so he
can see the freshness rather than trust it.

**And his reframing, which is the real instruction:** *"when it comes to triage you might suck for
now... but its a good visibility tool -> to get reminded of where we stand on each. then we also
show a potential next step and make as frictionless as possible me telling you why it sucks."* So:
the board shows state and proposes; he decides; and every item carries a free-text comment box
whose content comes back in the commit line, because his reasons are the only training signal
there is. Related: [[feedback_diagnose_before_naming_root_cause]],
[[feedback_review_page_design_system]].
