---
name: feedback_thesis_artifacts_to_vault
description: "Standing instruction — any future Claude Artifact relevant to the thesis must also be saved into 07-thesis-kb/Raw, not left as a chat-only link."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8e2e5475-b48d-4138-800d-77e685716da7
---

Whenever a Claude Artifact (or any polished research deliverable) relevant to Alessandro's thesis is created, save a copy of its underlying content into `C:\Users\Alessandro\07-thesis-kb\Raw\` and record the live Artifact URL in `Raw/2026-07-10 live artifact links.md` (append a new entry, don't overwrite).

**Why:** set 2026-07-10 when Alessandro asked for the source dossier artifact to be added to the newly created thesis vault — he doesn't want research outputs to exist only as ephemeral chat links; they need to land in the wiki's Raw folder so a later `/kb-ingest` pass can pull them in like any other source.

**How to apply:** applies to HTML reports, markdown dossiers, or any other artifact/deliverable produced during thesis-research work — not just the one this rule originated from. See [[project_thesis_system]] for the vault's full structure and the 2026-07-10 revival of a dedicated thesis vault (superseding the earlier "merge into vault_kb" decision, for thesis research specifically).
