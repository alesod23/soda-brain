---
name: feedback_open_urls_with_correct_account
description: "Before opening any account-bound URL (Google console/docs/sheets etc.) in his browser, force the correct account - he is often logged into the wrong one."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 78631983-6577-43a6-a88b-ba9f4f055fae
  modified: 2026-08-24T15:49:16.295Z
---

When opening ANY account-bound URL in Alessandro's browser (Google Cloud console, Docs/Sheets/Drive links, admin panels), do NOT just `Start-Process <url>` - his browser is frequently on the wrong Google account (e.g. 2026-08-21: he was on alessandro@tundrahealth.ai while I opened the Sheets API console page for the cdtm/triage OAuth project, so he had to switch manually).

**Why:** wrong-account pages 403 or silently show the wrong project/file; he wastes a round trip figuring out it's an account problem.

**How to apply:** wrap the URL so Google lands on the right identity first:
`https://accounts.google.com/AccountChooser?Email=<exact@address>&continue=<url-encoded target>`
(or append `authuser=<exact@address>` for docs/console URLs). Pick the account from context: cdtm work -> alessandro.sodano@cdtm.com, Tundra -> alessandro@tundrahealth.ai, personal -> alessandrosodano23@gmail.com. This is a TARGETED chooser with Email pre-filled + continue URL, so it does not violate [[feedback_never_trigger_bare_account_chooser]] - the bare no-hint chooser stays forbidden. Same spirit as [[feedback_oauth_login_hint_and_verify]] and [[feedback_resolve_account_before_linking]], extended to every browser open, every CC session.

**Tool-managed OAuth flows (added 2026-08-24 after the rclone violation, his ALL-CAPS escalation):** when a CLI/library wants to open the browser itself (rclone authorize, gcloud, google-auth `run_local_server`), NEVER let it — its URL is always hint-less. Use the no-browser flag (`--auth-no-open-browser`, `--no-launch-browser`, `open_browser=False`), capture the URL it prints; if that URL is a `127.0.0.1:<port>` redirector, `curl -s -o /dev/null -w '%{redirect_url}'` it to get the real Google URL, append `&login_hint=<email>`, and Start-Process THAT. The localhost callback still receives the code, so the tool completes normally. The rule is now also escalated inline in global CLAUDE.md under the auth auto-open bullet — keep the two in sync.
