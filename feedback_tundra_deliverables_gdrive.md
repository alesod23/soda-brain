---
name: feedback_tundra_deliverables_gdrive
description: "Tundra-related list/outreach/event deliverables go to the Tundra Health gdrive as a Google Sheet, not a local CSV"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 040b02ee-cbd5-4294-b80e-6e8423801f02
---

STANDING RULE (any CC session): when Alessandro asks for a document that is a **list of companies / events / contacts / outreach or anything clearly Tundra-Health-related**, do NOT hand back a `.csv` (or file) in the local file directory. Instead put it in the most relevant place inside the **Tundra Shared Drive** and give him a **Google Sheet link**.

**Why:** Tundra is a real company effort; its artifacts belong in the company Shared Drive, not scattered as local files he then has to move.

**How to apply (NEW canonical location 2026-07-21):**
- Location = **`H:\Shared drives\Tundra Shared Drive`** (the company Shared Drive), usually the `Outreach/` subfolder. This REPLACED the old personal `G:\My Drive\Tundra Health` (cdtm account, old folder id `1efXmHj0wVoUXaOfGnJrCYcRM6NtgSiAA`).
- **⚠️ Drive MCP is NOT currently on an account that can see these files (all searches return `{}`).** Until it's reconnected to the account that owns the Shared Drive, you cannot `create_file` into it via MCP. FALLBACK: write the sheet locally, then drop the file into `H:\Shared drives\Tundra Shared Drive\Outreach\` via the sync path (note: dropping a `.csv` there keeps it a CSV — for a real Sheet the user converts it, or it's created via MCP once reconnected).
- Once the Drive MCP is on the right account: `create_file` with `contentMimeType: 'text/csv'` (auto-converts to a Sheet), `parentId` = the Shared Drive subfolder id, return the `docs.google.com/spreadsheets/...` link.

Related: [[reference_overnight_harness]] (produces these lists), [[reference_gdrive_public_share]], and the Tundra stack doc `medtech-brain/_system/TUNDRA-STACK.md`.
