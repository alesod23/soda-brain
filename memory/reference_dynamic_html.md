---
name: reference_dynamic_html
description: "The dynamic-html system: server-backed HTML tools that autosave to disk, version, live-reload, and have per-answer + whole-form comment boxes that feed a CC inbox"
metadata: 
  node_type: memory
  type: reference
  originSessionId: eb084d3b-d52c-4019-a66b-a623cfb28a25
---

A reusable system so Claude-built HTML tools persist to real files (not browser localStorage) and can be iterated on through Claude. Lives in `OneDrive - HEC Paris\dynamic-html\` (zero-dep Node).

**Why it exists:** a double-clicked `file://` HTML can't write disk (browser sandbox); localStorage is per-origin and non-portable. A tiny local server outside the sandbox is the unlock.

**Pieces:**
- `server.js` — zero-dep http, binds `127.0.0.1:4140`. Routes: `GET /t/<tool>/` (serves `index.html`), `GET /t/<tool>/data` (data.json or `{}`), `POST /t/<tool>/save` (writes `data.json` pretty + throttled snapshot to `snapshots/`), `POST /t/<tool>/request` (appends `{at,field,question,text}` to `cc-inbox.jsonl`), `GET /t/<tool>/version` (index.html mtime, for live-reload).
- `_dynamic.js` — the ONE shared client. A tool becomes "dynamic" just by `<script src="/_dynamic.js"></script>`. By convention it gives: hydrate `[data-key]` fields from data.json, debounced autosave, word counters on `.q[data-limit]`, **per-answer** "✦ ask Claude" box on each `.field` (tags field+question), a floating **whole-form** "Note to Claude" box, and live-reload (page refreshes when Claude edits index.html).
- `tools/<tool>/` — one folder per tool: `index.html` (markup only), `data.json`, `snapshots/`, `cc-inbox.jsonl`.
- `start.cmd` — double-click launcher (starts server if down, opens index).

**Friendly URL:** hosts file maps `127.0.0.1 tools.local` (added elevated 2026-06-23), so tools open at `http://tools.local:4140/t/<tool>/` — readable in tabs/bookmarks even when the server is down (vs the bare IP). Server is host-agnostic (path-routed), so the alias just works. Each tool's `<head>` also sets a `<title>` + inline-SVG data-URI `favicon` so the browser tab shows the tool name + a distinct icon, not the IP.

**Editable rich content:** to make a static text block editable+persistent, convert it to `<textarea class="edit" data-key="...">` and seed the value in data.json — it then hydrates/autosaves like any field (bridge's video agenda + script done this way 2026-06-23).

**Read-only "Claude's draft" boxes:** `_dynamic.js` auto-injects a copy-to-clipboard + word-count box under any field whose key has a `draft_<key>` entry in data.json (Claude writes the draft, user copies it; respects the field's `data-limit`). Clipboard uses navigator.clipboard with an execCommand fallback (works on `tools.local` non-secure origin). Added 2026-06-24 for the EF/bridge answer drafts.

**CRITICAL save = MERGE, not overwrite:** `/save` merges the client's `[data-key]` payload into existing data.json (`Object.assign(existing, data)`), so keys the client doesn't own (`draft_*`, etc.) survive autosave. Before the 2026-06-24 fix it overwrote the whole file and silently wiped Claude-written `draft_*` keys on the first keystroke. Restart the node server (`server.js`, 127.0.0.1:4140) after editing it.

**Data ⟂ structure:** answers live in `data.json` keyed by `data-key`, NOT in the HTML. So Claude can restructure the form (add/reword/restyle questions) and answers survive — the ONLY rule is keep keys stable (migrate the value if renaming a key). Works for reports too (no `[data-key]` → autosave just unused; comment box + live-reload still work).

**The iteration loop:** user types in a per-answer/whole-form box → lands in `cc-inbox.jsonl` → user says **"apply the <tool> inbox"** → Claude reads it, edits HTML/`data.json`, page hot-reloads. (No watcher daemon — the inbox file is the lean channel.) First tool = `bridge` (the EF / Bridge Residency application, seeded 2026-06-23). Tested end-to-end with Playwright (hydrate/counter/autosave/comment/live-reload all pass). See [[feedback_dynamic_html_default]].

**Hub page (added 2026-07-10):** `tools/hub/index.html` — a manually-curated directory of ALL local webapps, not just dynamic-html ones: the dynamic-html tools (bridge, medtech-outreach, report-demo), the coattio/Lobbly CRM (`localhost:4124`), the curriculum tracker (`localhost:4117`, not always running — `~/.claude/curriculum-server/start.ps1`), and leftover static one-off HTML files. Client-side JS pings each URL and shows a live green/red status dot. **Bookmark this:** `http://tools.local:4140/t/hub/` — it's the single answer to "which localhost link was that". Keep this page updated by hand whenever a new webapp/server gets built.

**Gotcha — the server is NOT auto-persistent.** Unlike coattio (kept alive by a `Coattio-Watchdog` scheduled task), `server.js` on 4140 has no watchdog — it dies when the process that started it goes away (e.g. between Claude Code sessions) and every `tools.local`/`localhost:4140` link 404s until it's restarted. Fix: double-click `dynamic-html\start.cmd`, or `Start-Process -WindowStyle Hidden node "server.js" -WorkingDirectory "<dynamic-html dir>"`. Consider adding a real watchdog scheduled task (mirroring coattio's) if this keeps recurring.
