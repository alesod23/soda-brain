---
name: reference_tundra_granola_folder
description: "The 'tundra health' Granola folder where Alessandro works on Tundra calls, how to read it, and /granola routing rules for it (medtech-brain not vault_kb; Tundra's own Notion Validation Reachout page, not Lobbly's)."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2128ab65-69ab-46de-9e4c-680c11ed4fc3
---

**The folder:** Alessandro's Granola folder **"tundra health"** — he works on Tundra calls here.
Folder link (confirmed working 2026-07-13): `https://notes.granola.ai/t/07374bce-2aee-4910-9394-68ed8fb3af3c`

**How to read it:** same gotcha as [[reference_mpd_granola_folder]] — the folder link's plain-text
render (via `node ~/.claude/web-fetch-pw/fetch.js`) lists notes (title/author/time) but strips
per-note hrefs. To get an individual note's real URL, either ask Alessandro to paste it, or drive
a quick Playwright script to click the note's row and read `page.url()` afterward (returns a
`/d/<uuid>?list_id=...` link) — that's the fetchable URL.

**Tundra-specific `/granola` routing:**
- Drop-to-Raw goes into **`medtech-brain/Raw/`** (`MM-DD <Title>.md`), NOT `vault_kb` — this is
  company content, not personal.
- **Customer / hospital-discovery calls** → a **Meetings** row (Type=Client Call) in the NEW
  tundra Notion workspace (`alessandro@tundrahealth.ai`), Meetings DB
  `3a3b30c6-d57e-8037-afdc-c49c85ddbe11`, with the external person linked in **Contacts**. This
  SUPERSEDES the old "Validation Reachout" page routing (that page lived in the retired cdtm
  workspace). Full routing spec + the ask-before-write rules in `TUNDRA-STACK.md` (Notion OS).
  **⚠️ 2026-07-21 the Notion MCP is still on the OLD cdtm workspace — writes 404 until Alessandro
  reconnects it to the tundra account; until then, route to Raw only and flag the pending Notion write.**
- **Advisor / peer-founder calls** (fundraising chats, other-founder strategy calls — not a
  hospital/customer call) → skip Notion, just drop to Raw. Worked example 2026-07-13: calls with
  Julian (medtech-strategy) and Sebastian (fundraising) — both advisor calls, correctly no
  Notion page created.
- Facts that belong on an *existing* Notion reference page (e.g. a competitor → "Competition", an
  event → "Events") are a **separate** action from the call-log routing above, and need
  standalone approval per [[feedback_notion_write_needs_approval]] — don't fold that decision
  into the call classification.

See `medtech-brain/_system/TUNDRA-STACK.md` for the full Tundra stack (this is one entry in it).
