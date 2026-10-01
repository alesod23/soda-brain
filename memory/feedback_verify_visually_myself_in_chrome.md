---
name: feedback-verify-visually-myself-in-chrome
description: "When a result needs a visual check (a Notion page, an embed, a rendered doc), open it myself with Claude in Chrome instead of asking him to look"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 6348fc75-8a1b-4478-85e9-3ebb6e4556d4
  modified: 2026-09-30T14:13:47.688Z
---

When I cannot confirm from an API read-back how something looks (a Notion page, an embed, a published page), I open it myself with Claude in Chrome and look, then report what I saw. I do not end with "open the page once to check it".

**Why:** 2026-09-30, after I put an HTML embed on a Notion meeting page and wrote "I haven't seen how the embed looks inside Notion, so open the page once to check it", he answered: "take me out of the loop, in these cases try yourself to open it with claude for chrome and see it".
**How to apply:** invoke the `claude-in-chrome` skill, load the tools in one ToolSearch call, open the page in a NEW tab (never reuse his tabs), screenshot, and state what is on screen. GTM boards are the exception: those open only via `open-board.ps1` ([[feedback_gtm_boards_open_via_script]]). Same turn, also: "put X in Notion" for a file means upload it to Drive (Research Docs, `drive.py upload --account tundra`) and LINK it, not embed it.
