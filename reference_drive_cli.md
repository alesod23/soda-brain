---
name: reference_drive_cli
description: ~/triage/drive.py + drive.cmd - multi-account Google Drive CLI that reaches the CDTM shared drives the Drive MCP connector cannot see
metadata: 
  node_type: memory
  type: reference
  originSessionId: bcf4ed36-d8ed-4e48-817b-146c5998e5ca
  modified: 2026-08-11T21:58:03.417Z
---

`~/triage/drive.py` (+ `drive.cmd` shim), built 2026-08-11. Same shape as `gmail.py`: `--account <name>`, token per account at `~/triage/tokens/drive-<account>.json`, shared `credentials.json`.

**Why it exists:** the Drive MCP connector is bound to **tundrahealth only** and 404s on anything in CDTM (see [[reference_kb_systems]] / TUNDRA-STACK). The pre-existing `~/.claude/scripts/drive-upload-share.py` used scope `drive.file`, which can only ever see files that script itself created, so every existing shared-drive file was invisible to it too. `drive.py` uses the full `drive` scope and sets `supportsAllDrives` / `includeItemsFromAllDrives` / `corpora=allDrives` on every call.

**Live as of 2026-08-11:** `drive.cmd drives --account cdtm` returns `0AMi2sWohuCKfUk9PVA  _CDTM Munich`, and the Kickoff deck reads with `canEdit: true`.

Commands: `auth`, `reauth`, `whoami`, `drives`, `find` (`--name/--exact/--mime/--query`), `ls --parent <id>`, `meta --id`, `export --id --out [--mime]` (Google-native -> pptx/docx/xlsx, `--mime text/plain` is the fast way to read a deck's text), `download`, `upload`, `update --id --file --confirmed`.

- **`update` is a DRY RUN without `--confirmed`** and refuses outright if `capabilities.canEdit` is false. It replaces content in place, keeping the file id, link and sharing - this is the safe half of the pptx round-trip for editing a `.gslides` deck.
- **Auth carries the same hard guard as gmail.py** ([[feedback_never_trigger_bare_account_chooser]]): the browser flow only runs for `auth`/`reauth`, `--allow-auth`, or `GMAIL_ALLOW_INTERACTIVE_AUTH=1`. Always pass `--login-hint <exact@address>`.
- The full-scope reauth **backed up the old narrow token** to `tokens/drive-cdtm.json.bak-reauth`. `scripts/drive-upload-share.py` still works against the new token (its `drive.file` needs are a subset).

Related: [[reference_triage_gmail]], [[feedback_oauth_login_hint_and_verify]], [[project_cdtm_kickoff_tf]].
