---
name: project_gmail_snippets_extension
description: "Gmail Snippets — local-only Chrome extension for saving named email excerpts/whole emails from Gmail, browsable in a side panel. Architecture, phase status, and where it's headed."
metadata: 
  node_type: memory
  type: project
  originSessionId: 46a48b57-9810-4f97-b46c-01d6bfbe6f9b
---

**What it is:** a personal Chrome extension, requested 2026-07-14, that saves selected
text or whole emails from Gmail into a named local library — no cloud, no sender/
recipient metadata captured. Long-term goal (his words): "understand how I write emails,"
tied to the existing outreach CRM template system ([[feedback_outreach_template_mining]],
[[project_outreach_crm]]) so Claude can eventually reference saved snippets when drafting
emails in any Claude Code session.

**Location:** `C:\Users\Alessandro\gmail-snippets\` — workplan at
`WORKPLAN-20260714-gmail-snippets.md` in that folder (read it first for full phase
breakdown before touching this project again).

**Architecture (mirrors the existing `medtech-capture-extension` pattern):**
- MV3 content script on `mail.google.com`, plain fixed-position DOM injection (no Shadow
  DOM), same style as `coattio-badge.js`.
- `chrome.sidePanel` for the workspace (persists next to Gmail/compose across
  navigation — deliberately NOT a popup or in-page panel).
- Local Node server on **port 4160**, flat JSON file (`data/snippets.json`), no DB,
  no deps — same "flat JSON, no server framework" pattern as `~/.medtech-crm/crm.json`.
- Deep-link back to source = `location.href` at save time; side panel's "open source"
  updates the **current tab** via `chrome.tabs.update` (never opens a new tab, per
  explicit requirement).

**Phase 1 (done 2026-07-14):** save whole email / save selected excerpt, name (required)
+ comment (optional) at save time, flat list side panel, no Claude/API calls anywhere.

**Deferred, in priority order he set:**
- Phase 2: expand/search toggle in the side panel (stays a flat list by default —
  "don't want it cluttered" was explicit) + local full-text search via **MiniSearch**
  (picked over FlexSearch/Lunr — right fit at this dataset scale).
- Phase 3: **optional** Claude-assisted auto-naming, explicitly modeled on
  `.medtech-crm/comment-agent.js`'s headless pattern (background tick, per-item
  watermark, hidden `claude.exe -p --output-format json` calls, capped per run, silent
  unless actionable) — NOT the Anthropic API, and never blocking manual naming.
- Phase 4: grouping/labels (outreach templates, blurbs, introductions) + the CRM
  template-system tie-in itself.

See [[feedback_local_server_start_pattern]] for the gotcha hit while building this (the
local server got silently killed twice via `run_in_background` before switching to a
detached `Start-Process`).
