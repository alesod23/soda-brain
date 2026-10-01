---
name: reference_web_fetch_pw
description: "Headless-Chrome renderer for public JS-heavy URLs that WebFetch can't get (403/bot-block) and that have no MCP. The INTERIM Granola reader until a Granola MCP exists."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2daa091e-0db7-4880-aba3-31d479e0bad9
---

# web-fetch-pw — render public JS pages WebFetch can't

`~/.claude/web-fetch-pw/fetch.js` (playwright-core + system Chrome, headless, UA-spoofed). Renders a public URL and dumps `main`/`body` innerText.

- **Usage:** `node ~/.claude/web-fetch-pw/fetch.js "<url>" [waitMs]` (default wait 4000; use 6000–7000 for slow apps).
- **When:** WebFetch returns 403/empty (bot-block) or the page is client-rendered, AND no MCP covers it. Public/share links only — no auth.
- **Granola share links** (`notes.granola.ai/d/...` AND `/t/...`): the page returns **HTTP 500 but renders the shared note client-side** — the text comes through anyway. This is the interim way to read a Granola note Alessandro pastes.
- **MCP-FIRST caveat:** this is a GAP fallback. The real fix for Granola is a Granola MCP (Phase 5 of [[project_thesis_system]]); building it would reach all notes without pasting links. Per [[feedback_mcp_over_pw]], pursue the MCP; use this only until it exists.
- Built 2026-06-02 while reading a thesis-supervisor Granola note.
