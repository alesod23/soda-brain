---
name: reference_gdrive_public_share
description: "How to upload a local file to Google Drive and produce a public 'anyone with link' URL (the Drive MCP can't set sharing)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: eb084d3b-d52c-4019-a66b-a623cfb28a25
---

To turn a local file into a **public Google Drive link** for Alessandro:

1. **Upload:** copy the file into `G:\My Drive\` (Drive Desktop, synced to the **cdtm** Google account) — it uploads in the background. (Or upload via the Drive API directly.)
2. **Make public + get link:** run a Python script using the triage OAuth client `C:\Users\Alessandro\triage\credentials.json` with **full `https://www.googleapis.com/auth/drive` scope** (needed because Drive-Desktop-created files aren't owned by the app, so `drive.file` can't touch them). `InstalledAppFlow.run_local_server(prompt="consent")` opens the browser; **pick the cdtm account**. Then `files().list(name=...)` → `permissions().create({type:anyone, role:reader})` → return `webViewLink`.

- **Token cached** at `C:\Users\Alessandro\triage\drive_token.json` (drive scope) — reuse it; no re-consent needed unless revoked.
- Google libs (`google_auth_oauthlib`, `googleapiclient`, `google.auth`) are installed under the Python312 interpreter.
- **The claude.ai Google Drive MCP can READ files but has NO tool to set sharing/permissions** — that's why this script route exists. See [[reference_onedrive_path]].
- Credential scanning is classifier-blocked; the user must authorize which creds to use (they OK'd the triage creds 2026-06-25). First use: shared the EF Bridge application video.
