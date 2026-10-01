---
name: reference_permission_allowlist_gaps
description: Global settings.json allowlists Bash/Read/Write/Edit/Glob/Grep/* but NOT PowerShell or any MCP tool — so MCP- or PowerShell-using skills prompt y/n every run unless added to settings.local.json.
metadata: 
  node_type: memory
  type: reference
  originSessionId: 275dd959-6416-4d79-9d30-55c651bd453e
---

`C:\Users\Alessandro\.claude\settings.json` → `permissions.allow` covers `Bash(*) Read(*) Write(*) Edit(*) Glob(*) Grep(*) WebFetch(*) WebSearch(*)` — but **not** `PowerShell(*)` and **not** any `mcp__*` tool. So a skill that uses PowerShell (schtasks, Get-Date) or MCP (Google Calendar, etc.) triggers a permission prompt on every run even though Bash/file ops are silent.

Per-tool allowlist additions live in `C:\Users\Alessandro\.claude\settings.local.json`. On 2026-06-01, to make `/daily` smooth, added: the 5 Google Calendar MCP tools (`list_events`, `list_calendars`, `create_event`, `update_event`, `delete_event`) + scoped PowerShell rules (`schtasks /Query:*`, `schtasks /Create /TN Slot-Check-*:*`, `Get-Date:*`).

NOTE: editing `settings.local.json` to widen permission allow rules is gated by the auto-mode classifier as self-modification — it needs explicit user authorization in the turn, not just an inferred preference. Related: [[reference_daily_briefing]].
