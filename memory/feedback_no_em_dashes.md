---
name: feedback-no-em-dashes
description: "Absolute ban on em dashes everywhere, including generated HTML/deliverables and titles."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8eabe48f-2156-48dd-b45d-d9c50450f3b1
---

NEVER use em dashes (—), ever. This includes prose, chat, AND generated artifacts (HTML pages, deck/doc titles, section headings, READMEs). The global CLAUDE.md rule already says this; it was violated in the MPD→BMW outline HTML (em dashes in section titles/subtitles), and the user re-emphasized "never use the em dashes ever."

**Why:** it's a hard style rule the user cares about strongly (reiterated across sessions).

**How to apply:** in titles/headings, replace a dash separator with **parentheses** `()` (e.g. "Technical side (formats & the data layer)" not "Technical side — formats…"). Elsewhere use commas, colons, or semicolons. Before shipping any deliverable, grep it for `—` and remove every one. En dashes in numeric ranges (10:30–11:30) are tolerated; em dashes are not. See [[feedback_clickable_file_paths]].
