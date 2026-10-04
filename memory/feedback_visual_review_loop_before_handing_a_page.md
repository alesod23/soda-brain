---
name: feedback_visual_review_loop_before_handing_a_page
description: "Any page, chart or deliverable he will look at gets a screenshot review loop BEFORE he sees it: render, screenshot every region, fix every crossing line / overlapping label / off-centre text, repeat until clean. One glance is not a review (the SODA System Map, 4 Oct 2026)."
metadata:
  type: feedback
since: 2026-10-04
---

**His words (4 Oct 2026 04:30, the first SODA System Map):** "you didn't even bother to put a review mechanism that
actually meant you sure you outputted something that is readable. This is disgusting. You need to do better in this.
Recreate it with such a review. Continue until loop until you have all those minor details fixed. The lines are all
messy like that. The text that is not centered inside is surrounding figures and shapes, it's weird."

**What happened:** the lane chart drew ~60 bezier wires across a six-column grid, so wires crossed nodes and edge
labels sat on top of boxes; the gate hexagons had left-aligned text; the legend samples were inline spans with broken
borders. I took one screenshot, saw "it renders", and handed it over.

**Why:** a chart is a deliverable like a report: the design skill's "look once" is the minimum, not the review. The
review is a loop with a checklist, region by region, until the checklist is empty.

**How to apply:** before any visual deliverable reaches him: (1) serve it and screenshot every chart or region at
readable zoom; (2) check: no line through a node, no label on a shape, every label centred in its shape, nothing
clipped, consistent spacing, both themes; (3) fix and repeat; (4) only then open it for him. Prefer drawing methods
that cannot produce the mess (orthogonal routing in gutters, adjacent-lane wires, chips for the rest, hover
highlight) over patching a bad method. See [[feedback_event_companion_pages]], [[feedback_design_on_merit_not_his_offhand_numbers]].
