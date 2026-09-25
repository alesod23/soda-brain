---
name: feedback-trippy-event-anchor-and-explicit-ground
description: "In trippy, when a trip is anchored on an event, read the event's own schedule first; and every paid ground step must be its own visible dated line in the totals"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 2b505a93-c80e-47bd-81f5-c7b174f73267
  modified: 2026-09-25T13:51:37.477Z
---

When a trip has a fixed event (us-tour-2026-10: MD Expo Orlando), look up the event's official schedule
and venue BEFORE planning: it decides the arrival deadline, the nights, which train to take, and when the
next leg may leave. He had said "Oct 13 morning"; the real schedule (registration 13:00, finale Oct 15 18:00)
moved the train from 05:45 to 07:42, opened a cheaper direct-to-MCO Oct 13 arrival, and made a 3rd night
(finale) cost about nothing.

Every paid ground step (Miami->Orlando train, bus alternative, last mile to the venue, hotel) must appear as its
own dated line with its price in the whole-trip card. The Brightline fare WAS in the totals but folded into a
"incl. feeder + to Orlando" line, and he read it as missing (2026-09-25).

**Why:** he checks the chain line by line; a cost he cannot see does not exist for him.
**How to apply:** event -> fetch its schedule page; model arrive-by / leave-after from it; render each ground
step separately with a train-vs-bus comparison (he values working on a train). See [[project-trippy-v2]].
