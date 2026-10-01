---
name: feedback_notion_update_content_fetch_first
description: Notion update_content anchors must match the page as Notion re-renders it (e.g. _(pending)_ becomes *(pending)*), and one bad anchor rejects the whole call - fetch the page, then update
metadata:
  node_type: memory
  type: feedback
---

2026-09-14: a 4-part `notion-update-page update_content` on the INBIT meeting page failed with
"No matches found for ## Full transcript\n\n_(pending)_" and NOTHING in the call was applied, even
though three of the four anchors were fine. Fetching the page showed Notion had rewritten my
markdown: `_(pending)_` → `*(pending)*`, and headings sit on the line right after the previous
paragraph (no blank line).

**Rule:** before `update_content` on any page I did not create in the same turn (or whose text I
wrote with markdown emphasis), `notion-fetch` it and copy the anchor verbatim from the fetched
`<content>`. Keep anchors short (a heading or a single unique line). Emphasis markers, blank
lines and "---" are not stable across the round trip.

Related: [[reference_notion_tundra_system]], [[feedback_notion_deliverables_must_be_native]].
