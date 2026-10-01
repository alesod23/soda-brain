---
name: reference_notion_mcp_access
description: Notion MCP (mcp.notion.com) only sees pages explicitly shared with the Claude connection; unshared pages 404 on fetch AND never appear in search
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6c80e9e6-7c02-4c69-b463-29472bfb6c5b
---

The Notion MCP server (`mcp.notion.com`, OAuth integration id `1f8d872b-594c-80a4-b2f4-00370af2b13f`) has **scoped access**: it can only read/write Notion pages that have been explicitly shared with the Claude connection.

**Symptom of an unshared page:**
- `notion-search` never returns it (it is not in the integration's index) — even exact-title or in-page-content queries come back empty or only surface the handful of already-shared pages.
- `notion-fetch` on its URL/ID returns `404 object_not_found` ("Could not find page with ID … Check that you have access").

This is NOT a search-indexing lag and NOT a Claude bug — it is Notion's per-connection access control.

**Fix (user must do it in Notion UI):** open the highest-level ancestor page that should be reachable → ••• (top-right) → Connections → Add connections → select **Claude** → confirm the "access to all child pages" warning. Sharing at a high ancestor cascades to all descendants and persists across all future sessions. Whole-workspace grant: Settings → Connections.

**Operational rule for me:** if `notion-search` returns empty/irrelevant for something the user insists exists, do NOT keep re-querying search with synonyms — it is almost certainly an access-scope problem. Ask the user to add the Claude connection to the relevant ancestor page (and paste the URL), rather than assuming the page doesn't exist or that search is merely lagging.
