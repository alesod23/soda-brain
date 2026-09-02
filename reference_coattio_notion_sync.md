---
name: reference_coattio_notion_sync
description: coattio→Notion radar auto-sync — pushes live outreach contacts to the Tundra Contacts DB; the one pre-authorized Notion auto-write.
metadata: 
  node_type: memory
  type: reference
  originSessionId: b67c8e8e-5603-49b6-a86c-c615c62739d2
  modified: 2026-07-21T22:07:47.890Z
---

**coattio → Notion Contacts-DB "radar" sync** — `~/.medtech-crm/coattio-notion-sync.js`.

- **What**: when a coattio contact goes **live** (genuine 2-way: stage `repondu`/`call_booke`/`gagne`, or a real call — NOT a no-answer attempt or an un-actioned warm intro), it's pushed to the Tundra Notion **Contacts DB** as an **Outreach** row with Stage + a **Last touch** one-liner. Stage map: `repondu`/live call → Active; `call_booke`/`gagne` → Advanced. Ecosystem contacts are curated manually, not stage-managed.
- **How**: decides WHAT to sync deterministically in JS; executes the Notion write via the headless-claude bridge (`hidden-claude.js`) — **no Notion API token**. Idempotent (each coattio person stores `notion_contact_id`), additive-only (never deletes), never overwrites Category on an existing row. Change-detected → steady state is a no-op.
- **Trigger**: coattio server (`crm-app/server.js`) tick every 15 min, gated on `crm.json meta.notionSyncEnabled === true` (kill switch; currently ON).
- **This is the ONE pre-authorized exception** to NOTION_SYSTEM.md's "never auto-write" rule (Outreach Stage/Last-touch upserts only). Documented in both the constitution and the Notion System Rules page.
- First radar batch seeded 2026-07-21 (6): Ronan Dubois (ICO), Alexandre Massei, Renaud Scanu, Annabel Meunier, Martin Chanoine — Outreach·Active; Gilbert Farges — Ecosystem.
- Uses [[hidden-claude]]-style headless claude.exe (same as [[project_comment_agent]]-era comment-agent). See [[reference_notion_tundra_system]], [[reference_coattio_servers]].
