---
name: feedback-event-companion-pages
description: "Event companion pages: tabbed sections like the AIIC one, LIGHT theme (not the AIIC dark), and every person card carries the questions to ask that person"
metadata:
  type: feedback
---

His feedback on the Snitem "2e journée du DM connecté" page, 2026-09-28 morning, an hour before
the doors opened.

**Three rules, all from his own words.**

1. **Tabbed sections, not one long scroll.** *"I told you to make it exactly like the other event
   that I went to, the AIIC, and it's just an HTML. I wanted one with the clickable sections... with
   a guide versus the people speaking versus the people I could meet."* The shape to copy is
   `research-page/event_server.py` (AIIC Lombardia): sticky header, `<nav>` of pill buttons with
   `data-s`, one `<section>` per tab, a two-line JS toggling `.on`. Minimum four tabs: the
   programme, who is on stage, who else could be in the room, the guide.

2. **LIGHT theme.** *"I also like the theme, meaning light theme, better than the dark theme we had
   used for the other event."* The AIIC companion is dark; every event page from here is light.
   Palette that he approved: `--bg:#faf9f7 --card:#fff --fg:#1a1a1a --line:#e7e4df --dim:#6b6b6b
   --acc:#1d4ed8`, with the ACTE/section dividers kept dark (#1e293b) for contrast. Same palette as
   the Paris hospitals guide, so the two pages look like one family.

3. **Every person card carries the questions to ask THAT person.** *"I did like the suggested
   questions for each of the people I should speak with in the card of the person."* Not a generic
   question list in a corner: three questions max, written for that person's actual job, inside
   their own card, next to their LinkedIn.

**Why:** he reads these standing up, in a corridor, between two sessions. A scroll makes him hunt;
tabs let him jump. And a question written for the person in front of him is usable as-is; a generic
one has to be adapted while someone is waiting for him to speak.

**How to apply:** start from `research-page/build_snitem_dm.py`, which is the approved shape (tabs +
light + per-person questions + "je lui ai parlé" checkboxes in localStorage that strike the name
through in the programme too). Keep separating what is PROGRAMME from what is DEDUCTION: the "who
could also be there" tab says in its own header that it is inference from the previous edition and
the venue's residents, never a list of registrants. See [[feedback_review_page_design_system]] and
[[project_event_contact_workflow]] for what happens to the contacts afterwards.
