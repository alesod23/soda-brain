---
name: reference_granola_auto
description: "granola-auto — push-triggered pipeline turning new Tundra Granola notes into Notion Meetings rows + medtech-brain Raw docs; the MCP's workspace blind spot; the auto-write boundary."
metadata: 
  node_type: memory
  type: reference
  originSessionId: b3102940-5e76-40e1-8354-ffd1883e672a
  modified: 2026-07-31T04:52:15.365Z
---

# granola-auto (built 2026-07-30)

**Granola MCP is connected** (`https://mcp.granola.ai/mcp`, user scope, OAuth as
`alessandro@tundrahealth.ai`). Replaces pasted share links + `web-fetch-pw` for Tundra work.

**⚠️ THE BLIND SPOT:** the MCP sees ONLY the **Tundra Health** Granola workspace
(`b8c6f20f-1c22-49fb-8593-ab083e124687`). 2026-06-01→07-22 returns **0 notes** — the personal
workspace (old `tundra health` folder `07374bce…`, the MPD folder) is unreachable. So MPD can
never leak into Tundra Notion, AND a Tundra call captured on the personal account is invisible to
every automation. Always check which workspace a note lives in before assuming it's missing.

**The folder IS the Notion `Type`** (no content classification): Customer calls → `Client Call`,
Team meetings → `Internal`, Ecosystem/Other → `Ecosystem`.

**System:** `~/.claude/granola-auto/` — `watch.ps1` (FileSystemWatcher on
`%APPDATA%\Granola\cache-v6.json.enc`, the file Granola rewrites on every sync; `granola.db` only
stamps at app start — watching it is useless) → 90s quiet debounce → `run.js` → headless Claude via
`~/.medtech-crm/hidden-claude.js` with both MCPs. Watcher autostarts from the **Startup folder**
(`granola-auto-watch.vbs`) because `schtasks /SC ONLOGON` needs elevation. `Granola-Auto-Sweep`
schtask 08:15 daily is the safety net via `sweep.vbs` (one-shot; do NOT point it at
`start-watch.vbs` or it stacks a watcher every morning).

**Auto-write boundary — NOTION_SYSTEM.md Hard Rules exception #2:** Meetings rows only, plus
linking an ALREADY-EXISTING Contact. Never creates Contacts/Tasks/Competition/Events. Contact
search-miss → blank + logged to `state.json → pending_contacts`. No post-call scan (that's the
Notion AI agents' lane). Aborts without writing if `notion-fetch self` isn't Tundra Workspace or
Granola isn't the Tundra Health workspace.

**Readiness gate:** the MCP lists notes that have NO AI summary yet (unlike the REST API, which
filters them). A note without a summary is skipped and retried, never written half-formed.

**Known open:** `get_meetings` returns no share URL, so the body link is constructed as
`notes.granola.ai/d/<id>` — format UNCONFIRMED. Meetings DB has no date property (`Created on` is
row-creation time, so backfill misdates); adding one needs a yes + dual doc sync.

Related: [[reference_notion_tundra_system]], [[reference_mpd_granola_folder]],
[[feedback_notion_write_needs_approval]], [[feedback_schtasks_vbs_wrapper_no_console_flash]].
