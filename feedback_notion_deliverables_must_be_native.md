---
name: feedback_notion_deliverables_must_be_native
description: "Anything built for Notion must be Notion-NATIVE (real pages/databases people can collaborate on), never a local mirror or an export he opens through Claude"
metadata:
  node_type: memory
  type: feedback
---

2026-09-07, verbatim: *"for notion, you should know in your memory/guidelines that the
objective is to create something notion-native so its collaborative (i will then use it
through claude, but it should be notion-native)."*

**The rule.** When the destination is Notion, the deliverable is a real Notion page or
database - properties, relations, views, comments - living in the workspace where other
people (Caleb, Tundra collaborators) can open and edit it. NOT a local HTML/markdown
mirror, NOT a file he has to import, NOT a Claude-only artifact that merely *describes*
what should be in Notion.

**Why:** Notion is the collaboration surface. He will drive it through Claude, but the
artifact has to stand on its own for a human who never opens Claude Code. A local mirror
is invisible to everyone else and instantly drifts. This is the opposite of the
task-land / coattio pattern, where local files ARE the source of truth and the plumbing
deliberately stays local ([[project_notion_signals]]).

**How to apply:** design the Notion structure FIRST (which database, which properties,
which views), then write into it via the Notion MCP - after verifying `fetch self` shows
the Tundra workspace ([[reference_notion_tundra_system]]) and getting his go, since
Notion writes need approval ([[feedback_notion_write_needs_approval]]). If the MCP
cannot express something, say so and propose the nearest Notion-native shape - do not
silently fall back to a local file. Excluded from the draft-review lane for now (he kept
Notion out of scope there on 2026-09-07 for exactly this reason: it needs a native
design, not a queue entry).

Related: [[reference_notion_mcp_access]], [[project_notion_signals]].
