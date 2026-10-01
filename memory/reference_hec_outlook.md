---
name: hec-outlook-cli
description: HEC mailbox + calendar CLI via Classic Outlook COM at C:\Users\Alessandro\hec-outlook\outlook.py
metadata: 
  node_type: memory
  type: reference
  originSessionId: 11fd5c49-9911-4b79-a7fd-814e46ef643c
---

CLI helper for HEC (alessandro.sodano@hec.edu) Microsoft 365 mailbox and calendar.

**Path:** `C:\Users\Alessandro\hec-outlook\outlook.py`

**Tech:** Python + `win32com.client` against **Classic Outlook** (`C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE`). NOT New Outlook (olk.exe from the Microsoft Store) — New Outlook has no COM/MAPI surface, COM dispatch will fail with "Operation aborted" if olk.exe is the running variant.

**Why this path:** HEC tenant is locked-down Azure AD (cannot register a tenant-wide app, cannot get admin consent). COM piggybacks on the user's already-authenticated Outlook client, sidestepping tenant policy entirely. See [[hec-outlook-setup]] for tenant info.

**How to apply:**
- Always call via the full Python path: `C:\Users\Alessandro\AppData\Local\Programs\Python\Python312\python.exe C:/Users/Alessandro/hec-outlook/outlook.py <cmd>` (use forward slashes when invoked from bash — backslashes get mangled). See [[feedback_python_full_path]].
- If COM dispatch errors with "Operation aborted": Classic Outlook isn't set up, or olk.exe is the running variant. Kill olk via `Get-Process olk* | Stop-Process` and launch the Office16 OUTLOOK.EXE binary explicitly.
- If first-run "Choose Profile" dialog blocks COM: open Classic Outlook once interactively, complete sign-in/MFA, wait for OST sync, then COM works silently going forward.

**Subcommands:**
- `whoami [--pretty]` — confirm account + folder counts
- `search [query] [--days N] [--sender X] [--unread] [--folder inbox|sent|drafts] [--limit N]`
- `read <entry_id> [--html] [--mark-read]`
- `draft --to --subject --body [--cc] [--bcc] [--body-file path] [--html] [--attach paths...]`
- `send-draft <entry_id> [--yes]` — dry-run preview unless `--yes`
- `cal-list [--days N] [--days-past N] [--limit N]`
- `cal-create --subject --start "YYYY-MM-DD HH:MM" --end ... [--location] [--body] [--attendees emails...] [--optional emails...] [--all-day] [--send --yes]`

All output is JSON. `--pretty` for indented. Drafts/invites require explicit `--yes` to actually send (CLAUDE.md "no destructive actions without confirmation").

**Not wired into /triage** by user request (2026-05-23). Standalone tool only. If wiring later: model after `~/triage/gmail.py` integration in `fetch-all.js`.

Related: [[hec-outlook-setup]] (OneAuth HRD blob, tenant ID), [[reference_triage_gmail]] (parallel pattern for Gmail), [[feedback_python_full_path]] (full python path).
