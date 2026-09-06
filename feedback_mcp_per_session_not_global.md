---
name: feedback_mcp_per_session_not_global
description: Rarely-used MCP servers are parked; switch them on for ONE session with cc-with, never globally.
metadata:
  type: feedback
---

Every stdio MCP server in `.claude.json` spawns a process in **every open Claude
Code session**. With 8 sessions open that was ~7.5 GB of commit for two servers
Alessandro almost never uses (zotero ~520 MB, langfuse ~430 MB each).

Parked 2026-09-06: **zotero** and **langfuse**, removed from `.claude.json`,
definitions (with their API keys) kept in `~/.claude/mcp-parked/parked.json` plus
one `<name>.mcp.json` per server.

**Why:** he wants them off by default. Critically, he does NOT want "turn it back
on" to mean "on for every new session from now on" - that just recreates the
problem and relies on him remembering to switch it off.

**How to apply:** to use a parked server, start ONE session with
`cc-with <name>` (PowerShell function, wraps `claude --mcp-config`; `-Only` adds
`--strict-mcp-config`). It writes nothing to the global config, so no other
session sees it and there is nothing to switch off afterwards. The global toggle
`~/.claude/mcp-parked/mcp-park.ps1 -Name <x> -On|-Off` exists only for making a
server permanent again - do not reach for it for one-off use.

MCP servers load only at session start, so a parked server can never be switched
on mid-session: the answer is always "relaunch with `cc-with`", never "hold on".

Langfuse is **not retroactive**: traces are emitted by the target script's own SDK
instrumentation, and the MCP is only a read client, so parking it loses no history.
`/langfuse-bananza` step 0 and `/scientific-drafting` both carry this now.
See [[reference_laptop_memory_pressure]].
