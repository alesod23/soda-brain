---
name: feedback_use_his_local_time_zone
description: "Every time I write for him goes in the time zone he is in NOW (US trip from Oct 2026: the laptop clock, EDT, later PT), never UTC or Rome by default"
metadata:
  type: feedback
since: 2026-10-10
---

**His words (10 Oct 2026):** "we're in the us now, diff times, please make sure to use the time im in" (after I gave a
budget timeline in UTC with "Rome is +2").

**Why:** he reads times against his own day; UTC or Rome times make him convert, and Rome is no longer his clock.

**How to apply:** run `date`/Get-Date on the laptop first (it follows him: EDT in Florida, then PT on the West Coast) and
write every time in that zone with its label (e.g. "22:54 EDT, Fri"). Logs in UTC or Rome: convert before writing. A time
for someone else (a call in Italy) gets their zone too, said explicitly. Related: [[feedback_check_clock_before_timestamps]].
