---
name: reference_notion_tundra_system
description: Tundra Notion is on tundrahealth.ai (reconnected); NOTION_SYSTEM.md constitution bridged to the System Rules page; Contacts DB = the radar; coattio→Notion auto-sync built.
metadata: 
  node_type: memory
  type: reference
  originSessionId: b67c8e8e-5603-49b6-a86c-c615c62739d2
  modified: 2026-07-21T22:07:24.887Z
---

Tundra Health Notion — the shared company workspace.

- **Account/workspace**: Notion MCP now on **`alessandro@tundrahealth.ai`** → "Tundra Workspace" (id `0f7b30c6-d57e-818c-ad08-0003a268b635`; Alessandro user id `3a3d872b-594c-81da-9329-00020d70532d`). Reconnected via `/mcp` on 2026-07-21, RESOLVING the old "MCP stuck on cdtm account" warning. ⚠️ A future re-auth can silently fall back to the cdtm account — always `mcp__notion__notion-fetch self` first; if it says cdtm, re-run `/mcp` and pick the tundra workspace before any write.
- **Constitution**: `medtech-brain/_system/NOTION_SYSTEM.md` (READ-FIRST for any Tundra Notion work) is **bridged** to the Notion "System Rules ⚙️" page (id `4f3c322a-546a-4074-b090-2c243e146e87`) — a change on either side must be reflected on the other. The Notion page is the richer hand-maintained map; the local file is Claude's read-first mirror. Alessandro empowered Claude to make structural Notion changes (schemas, categories, layout) AND keep both docs in sync.
- **Every call → Meetings DB** (no standalone call pages). **Every person → Contacts DB** (Category = Outreach/Ecosystem; Outreach has Stage = Radar/Active/Advanced). Hard rule: never auto-write without a yes — EXCEPT the one pre-authorized coattio→Notion contact sync.
- **Contacts DB = the "radar"**: db `a6d0ad77-4248-4bc4-a174-d131633de728`, data source `a747cb32-a4bd-42bf-818e-df4c97390f4f`. Meetings DB data source `3a3b30c6-d57e-8093-9e35-000b79676b41`. Added 2026-07-21: Luxembourg country option + "Last touch" text property.
- See [[reference_coattio_notion_sync]] for the auto-sync. See [[TUNDRA-STACK]] and [[reference_tundra_crm_taxonomy]].
