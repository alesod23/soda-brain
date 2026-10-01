---
name: Triage Gmail Helper Location
description: Local Python helper at ~/triage/gmail.py owns Gmail OAuth/read/label/send for cdtm + lobbly. Replaces claude.ai Gmail MCP for triage skill.
type: reference
originSessionId: 4ea78cff-05f2-45ae-964c-63e0bf48d72c
modified: 2026-08-04T07:17:00.180Z
---

> **2026-09-02: COMET ABANDONED — every "Comet" below now means CHROME (the default browser). See [[feedback-browser-chrome-default]].**
**Helper:** `C:\Users\Alessandro\triage\gmail.py`

**Why custom helper:** Anthropic's `claude.ai Gmail` MCP is read-only by design — no `send` tool exists at the protocol layer, and OAuth scope is read-only. To unlock send (and full label/draft) we built a custom Google Cloud OAuth app, mirroring how Perplexity does it. Same pattern as the `wa` skill, which uses a local Baileys script for sends since Anthropic doesn't ship a WhatsApp send MCP.

**Accounts (token files at `~/triage/tokens/<acct>.json`):**
- `cdtm` → `alessandro.sodano@cdtm.com` — token verified CORRECT 2026-08-04 (`whoami` returns alessandro.sodano@cdtm.com; the 2026-07-28 crossed-token state is resolved).
- `sodano23` → `alessandrosodano23@gmail.com` (added 2026-07-28)
- `alesoda2002` → `alesoda2002@gmail.com` (added 2026-07-28)
- `tundra` → `alessandro@tundrahealth.ai` (added 2026-08-02; the Tundra business mailbox — use for Tundra outbound drafts)
- `lobbly` → `alessandro@lobbly.tech` (DEAD account per [[reference_lby_dead]])

**Re-auth a single account (added `reauth` 2026-06-10):**
```
python C:\Users\Alessandro\triage\gmail.py reauth --account <acct>
```
`reauth` backs up the stale token to `<acct>.json.bak-reauth`, then forces a fresh OAuth flow that POPS the Google login in the default browser (Comet). **CLAUDE RUNS THIS FOR THE USER** — on any token failure (`RefreshError` in triage, a draft/send that 401s) OR when the user says "relogin <acct>". The user NEVER types a re-auth command; their only step is the click-through login in Comet. Run it `run_in_background: true` (the flow blocks until the browser redirect). Verify after with `whoami`. The user gets kicked out of lobbly often, so expect to run this for lobbly periodically. (Plain `auth` still exists but won't re-trigger a flow while a valid-but-wrong token sits in place — `reauth` is the one to use.)

**Draft auto-open (set 2026-06-10):** after creating an email draft, AUTO-OPEN it in Comet (the user's default browser, where Gmail lives) so they can review/edit/send. Use the `message_id` printed by `draft` and pin the sending account with `authuser`:
```
Start-Process "https://mail.google.com/mail/?authuser=<account-email>#drafts/<message_id>"
```
`Start-Process` (no explicit browser) → OS default handler = Comet. Verified 2026-06-10 for both cdtm and lobbly: the tab lands on the correct account and opens the draft. Do NOT launch `chrome.exe` for this — the user's Gmail is in Comet, not Chrome (corrected 2026-06-10). See [[feedback_message_send_protocol]] / [[feedback_output_delivery_rules]].

**Subcommands:** `auth`, `reauth`, `whoami`, `search`, `get`, `send`, `draft`, `send-draft`, `delete-draft` (added 2026-06-10, `--draft-id`), `list-drafts`, `contact-status`, `label`, `list-labels`, `create-label`. Run with `--help` on any for flags.

**Attachments (added 2026-06-10):** `draft` supports `--attach <path>` (repeatable, one per file) for PDFs/docs; it wraps the multipart/alternative body in a multipart/mixed when attachments are present, so attachment count is verified on the live draft. Use `--body-file` for multi-line bodies. Example: `python gmail.py draft --account cdtm --to x@y.com --subject "..." --body-file body.txt --attach "a.pdf" --attach "b.pdf"`. (`send` does NOT yet take `--attach`, only `draft`.) Paths with spaces work as separate quoted args.

**Send safety:** dry-run by default. Always show dry-run, get explicit "go", THEN re-run with `--confirmed`.

**Triage labels (created in both accounts):**
- `triage/action` (Label_1) — needs attention
- `triage/todo` (Label_2) — deferred
- `triage/done` (Label_3) — handled
- IDs happen to match across accounts but always re-resolve at runtime via `list-labels` — not hardcoded.

**OAuth app credentials:** `C:\Users\Alessandro\triage\credentials.json` (gitignored). App is in Google Cloud Console "Testing" mode; only listed test users (cdtm + lobbly addresses) can authenticate. To add a third account later, add it as a test user in the OAuth consent screen settings.

**Required Python deps:** see `~/triage/requirements.txt`. Pinned: `google-auth==2.36.0`, `google-auth-oauthlib==1.2.1`, `google-api-python-client==2.149.0`.
