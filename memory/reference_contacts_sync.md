---
name: reference_contacts_sync
description: "Phone-saved Google contacts flow into the CRM via triage/contacts_sync.py on the box, but ONLY after he picks them on a hub card (never auto-file every contact); one-time consent done on the laptop 2026-09-14"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 9273b0c0-e971-446b-be10-19e5d8d2401d
  modified: 2026-09-14T11:14:06.651Z
---

Asked 2026-09-14 at MEDICON: *"I would like you to access them [contacts saved on my phone] and insert them in CRM/contacts (set up a workflow there if not existing)"*. Same day, the gate: *"i dont want this to be automatically done for EVERY contact, sometimes i just saved a new contact that has nothing to do with work"*. Before this the box had NO live Google-contacts access: only a one-off People-API snapshot of 685 contacts from 2026-05-23 in `wa-daemon/contacts.json` (used by the WA sender).

**The workflow** (`/home/da/triage/contacts_sync.py`, mirror `task-land/_system/box-tools/triage/`, laptop copy `~/triage/`; same OAuth app as gmail.py, separate token `tokens/contacts-alesoda2002.json`, scope `contacts.readonly`):
- cron on the box every 30 min: `sync --account alesoda2002` (log `~/.local/state/contacts-sync.log`). Incremental via People API `syncToken`, state `triage/state/contacts-alesoda2002.json`.
- **First run = BASELINE**: all existing contacts recorded as seen, nothing queued. Only adds/changes after that flow. (`--full-import` overrides.)
- New/changed people → `task-land/_system/contacts-inbox.jsonl` (`status: new`) → **ONE approval-hub card per batch** (POST `127.0.0.1:4180/pending` on the box, numbered list in `context`, max 40 per card). Card reply semantics: **yes = all · no + "1 3" = only those · no + "none" / bare no = skip all · no + other text = left `new` with the feedback stored for a session.**
- Next cron runs poll `/item/<card>` and apply the verdict: `approved` rows are POSTed to coattio intake `127.0.0.1:4137/intake` (retried while the port is down), `skipped` rows stay in the file for the record.
- **Notion Contacts row is a SESSION step** (cron cannot reach the Notion MCP): `contacts_sync.py review` (default status `new`; `--status approved` for filing) → create the row via Notion MCP → `mark-filed --resource people/cXXX --notion-id ID`. `decide --card ID --keep "1 3"|all|none` is the manual override when a card came back unparsable. Notion-native per [[feedback_notion_deliverables_must_be_native]].

**NEVER file every contact automatically.** Personal contacts land in the same Google account; the card is the filter and he is the one who picks. Do not "simplify" by skipping the card.

**Auth (done on the laptop 2026-09-14):** `auth` never opens a browser itself (`open_browser=False`); it prints the consent URL with `login_hint` forced in, and the session opens THAT (account preselected, never a bare chooser, [[feedback_never_trigger_bare_account_chooser]]). Run with `python -u` or the URL sits in the stdout buffer. Then `scp tokens/contacts-alesoda2002.json box:/home/da/triage/tokens/`.

Related: [[reference_triage_gmail]], [[reference_approval_hub]], [[reference_notion_tundra_system]], [[project_outreach_crm]].
