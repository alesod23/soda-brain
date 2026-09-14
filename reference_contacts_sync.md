---
name: reference_contacts_sync
description: Phone-saved Google contacts (Blinq card scans, manual adds) flow into the CRM via triage/contacts_sync.py on the box; needs a ONE-TIME consent on the laptop with login_hint, then cron
metadata:
  node_type: memory
  type: reference
---

Asked 2026-09-14 at MEDICON: *"I would like you to access them [contacts saved on my phone] and insert them in CRM/contacts (set up a workflow there if not existing)"*. Before this the box had NO live Google-contacts access: only a one-off People-API snapshot of 685 contacts from 2026-05-23 in `wa-daemon/contacts.json` (used by the WA sender), and the `alesoda2002` Gmail token has no contacts scope (and is revoked anyway).

**The workflow** (`/home/da/triage/contacts_sync.py`, same OAuth app as gmail.py, separate token
`tokens/contacts-<account>.json`, scope `contacts.readonly`):
- `sync --account alesoda2002` (cron every 30 min on the box, log `~/.local/state/contacts-sync.log`): incremental via People API `syncToken`, state in `triage/state/contacts-<account>.json`. New/changed people → **`task-land/_system/contacts-inbox.jsonl`** (one line each, `status: new`) and a best-effort POST to coattio intake `127.0.0.1:4137/intake`. Exits 2 quietly while the token is missing.
- **Filing into Notion Contacts is a SESSION step** (the savior or `/daily` reads the inbox jsonl and creates rows via the Notion MCP; a cron cannot reach the MCP). Mark lines `status: filed` after creating the row. Notion-native per [[feedback_notion_deliverables_must_be_native]].

**The one thing only he can do:** Google's consent runs `run_local_server`, i.e. needs a browser on the machine running it. On the LAPTOP (the script reaches it via the box→laptop mirror `task-land/_system/box-tools/triage/`):
`python contacts_sync.py auth --account alesoda2002 --login-hint alesoda2002@gmail.com` then
`scp tokens/contacts-alesoda2002.json da@box:/home/da/triage/tokens/`. Never a bare account chooser ([[feedback_never_trigger_bare_account_chooser]]).

Related: [[reference_triage_gmail]], [[reference_notion_tundra_system]], [[project_outreach_crm]].
