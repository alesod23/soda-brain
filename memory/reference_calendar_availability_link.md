---
name: reference-calendar-availability-link
description: "Source of truth for Alessandro's calendar availability. ALWAYS use this link, not raw Google Calendar MCP queries, when suggesting/checking slots."
metadata: 
  node_type: memory
  type: reference
  originSessionId: f40a4476-95b6-422a-8cd4-4bb5a02d00c0
---

For any "when am I free / propose slots / check availability" task, **DO NOT** rely on the Google Calendar MCP (`list_events` across cdtm / lobbly / phibi2303 etc.) — those calendars are incomplete and missed real conflicts (incident on 2026-05-13: proposed Tue 19 May 18:00 which was already booked elsewhere).

**Use this Google appointment scheduling link as the authoritative free/busy view (updated 2026-06-22, supersedes the old B9gWY5Mjt9t41UsJ9):**

https://calendar.app.google/CSydXCR7rq9CC47s6

It aggregates every calendar Alessandro actually keeps availability on. The MCP only sees a subset.

## How to apply
- This is MANDATORY for ANY booking/slot task — when finding a time to meet someone, when proposing slots, when booking via a counterpart's link (meetergo etc.). Check it EVERY time, across all sessions. Never propose a time from `suggest_time`/`list_events` alone — they disagree with this link and have given wrong slots.
- The page is **client-side rendered — WebFetch returns nothing**. Render it with `node ~/.claude/web-fetch-pw/avail.js "<link>"` (headless Chrome, clicks the target day and dumps free slots). Slots are GMT+02:00 Berlin (CET).
- The slots shown ARE the only times Alessandro is genuinely free — propose ONLY from that set. Slots are 30-min; a 1-hour meeting needs two consecutive open slots.
- For a meeting with others, intersect: Alessandro's link slots ∩ each other attendee's free/busy (Caleb = caleb.seeling@clickhouse.com, `list_events`) ∩ counterpart's booking page. Propose only what is free for ALL.
- Still good to cross-reference cdtm/lobbly calendars for context (e.g. "out of town until X"), but never use them as the sole free/busy source.

## Incident 2026-06-22 (why this got hardened)
Booking a Thursday slot with Max Knaus + Caleb: I used `suggest_time` (Alessandro's MCP calendars + Caleb) and it returned 13:45–15:00 as the only mutual free window. User pushed back — he was actually BUSY then. His availability link showed he was only free Thursday mornings (busy all afternoon); Caleb was busy all morning. → NO mutual slot existed. Root cause: skipped the availability link. Rule: always render and obey the link first.

## Combined Ale+Caleb overlay link (created 2026-07-14)
Live multi-src Google embed overlaying Ale's busy-carrying calendars + Caleb's free/busy (caleb.seeling@clickhouse.com, already subscribed in Ale's calendar list). Gaps with no blocks from either = mutually free. Only renders when signed into Ale's Google account (Caleb's cal is "Anyone can see nothing"); shows nothing to third parties. Live on every page load; the 3 @import ICS feeds lag up to ~12-24h (Google's refresh cadence).

https://calendar.google.com/calendar/embed?mode=WEEK&wkst=2&ctz=Europe%2FRome&src=phibi2303%40gmail.com&src=alessandrosodano23%40gmail.com&src=alesoda2002%40gmail.com&src=alessandro.sodano%40cdtm.com&src=l0ebr59bkad6u2n8c1hgq9ji60b88bvq%40import.calendar.google.com&src=lhjehnlm1l6o8lvib142lhqj1qcv5mod%40import.calendar.google.com&src=tk1f825nufvf83i60r6vvdcad3k95ssh%40import.calendar.google.com&src=c_d0779b5d99348c470155ae9bcf2899109656b56015a9a21a3fe8c3ee452c1c7d%40group.calendar.google.com&src=c_d24b4bf4b6e7bd4992724a6d2e5e3d1be003e8511a1f74218ad99ff2359a672c%40group.calendar.google.com&src=c_d6bbe28f7cf7a96ccbc484cd7ed43ac647e3dcdb0d8b37515ffb1b350ffa5b15%40group.calendar.google.com&src=c_47f92b3145fdf813be94567bbe65e1e2a40f547ca5b87f609f8188c6a7fee906%40group.calendar.google.com&src=c_0643b3bcd2f9439bf66a9812542eac2268df37a4122452ae1f1b3dd2bca419ac%40group.calendar.google.com&src=caleb.seeling%40clickhouse.com&color=%23D50000

Caveat: the appointment-schedule link above stays the AUTHORITATIVE source for Ale's side (it may include calendars the MCP/embed can't see). For actually proposing slots: render the scheduling link, then confirm the slot is also gap-free on this overlay (Caleb's side).

## Why
The MCP-visible calendars don't capture personal commitments, lectures, social plans, etc. The scheduling link is the single source of truth the user maintains for "is Ale free then?".
