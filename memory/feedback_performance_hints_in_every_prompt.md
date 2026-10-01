---
name: feedback_performance_hints_in_every_prompt
description: "His standing instruction (Aug 2026, repeated 1 Oct 2026): every model prompt of the system carries a summarized \"performance hints\" block, and those hints grow from the system's own misses"
metadata:
  node_type: memory
  type: feedback
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-30T23:49:38.396Z
---

He asked twice (2026-08-0x and 2026-10-01 01:50) to "memorize learnings from the 'Performance Hints' paper: give it to
a model summarized and it does better performance". No verified paper by that name is known to me; the principle is
applied as a practice: **every headless prompt of the system (CRM reader, inbound asks, meeting loop, due today,
critic, world/judge of the simulation) ends with a PERFORMANCE HINTS block**: what matters most for this task, the
pitfalls already seen, how a good answer looks, 5 to 12 lines, task-specific, not generic.

**Why:** the simulation of 30 Sep showed the same misses again and again (asks and deadlines lost, dates picked for
him, attachments claimed, "Lei" after a call, a booking not linked to the pending slot draft); each is one line of
hint that the model would have followed.

**How to apply:** the hints live in `task-land/_system/hints/<component>.md` (synced, one file per caller); the
callers append the file to their prompt; the simulation's learner (`~/sim/harness/learn.py`) adds a line with the
date and the evidence when a miss is a matter of attention rather than code, so the block self-grows every judged
day. Also for agent briefs I write: a "PERFORMANCE HINTS - how to do this task well" section (done since August).
See [[reference_simulation_harness]], [[feedback_design_on_merit_not_his_offhand_numbers]].
