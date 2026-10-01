---
name: reference_google_doc_edit_path_from_box
description: "How to create and EDIT a Google Doc for the tundra account from the box (2026-09-18): Drive MCP creates (owner alessandro@tundrahealth.ai) but cannot edit text; drive-tundra and cal-tundra tokens are dead (invalid_grant); working path = share the doc with alessandro.sodano@cdtm.com as writer via the Drive MCP, then Docs API batchUpdate with triage/tokens/drive-cdtm.json (drive scope is accepted by the Docs API). Calendar writes on the tundra calendar work through the Calendar MCP (cdtm login, writer) and through cal-cdtm.json."
metadata:
  type: reference
---

**Facts (verified 2026-09-18 while building the "Retro (weekly)" event + notes doc):**
- `mcp__claude_ai_Google_Drive__create_file` with `contentMimeType: text/plain` creates a Google Doc owned by **alessandro@tundrahealth.ai** (the Drive MCP is the tundra login). `update_file` changes only title/parent. No text edit, no append.
- `~/triage/tokens/drive-tundra.json` and `cal-tundra.json` are **dead** ("token present but unusable" / `invalid_grant`). Re-auth needs him (`drive.py auth --account tundra --login-hint alessandro@tundrahealth.ai`), never a bare chooser.
- Working edit path: `share_file(fileId, alessandro.sodano@cdtm.com, writer)` via the MCP, then Docs API `documents().batchUpdate` with `Credentials.from_authorized_user_file('tokens/drive-cdtm.json')` (scope `auth/drive` is enough for Docs). Insert at `endIndex-1` of the last paragraph (the doc's final newline cannot be written past). This keeps his bullets/bold; replacing the whole file with `drive.py update` would flatten them.
- Calendar on the tundra calendar: `mcp__claude_ai_Google_Calendar__create_event/update_event` with `calendarId: alessandro@tundrahealth.ai` (cdtm has writer access; organizer shows tundra). Attachments via `addedAttachments[{fileUrl}]`. For timed/cron writes use `cal-cdtm.json` (calendar scope) with `events().patch(..., sendUpdates='all')`.
- Deferred invites ("invite X in 20 minutes"): one-shot self-removing cron + `.done` state file + Bot API line; he moves the time freely ("10 more"), so keep the script's time string in one sed-able place.

Related: [[reference_drive_cli]], [[reference_calendar_availability_link]], [[feedback_never_trigger_bare_account_chooser]].
