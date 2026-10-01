---
name: feedback_oauth_login_hint_and_verify
description: "Google OAuth flows must pre-select the account with login_hint and verify identity before saving the token, never show a bare account chooser"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8416f96f-965c-41e3-a618-179e3b6cd758
  modified: 2026-08-03T17:24:44.222Z
---

When triggering any Google OAuth consent flow, always (a) pass `login_hint=<the exact intended
email>` plus `prompt="consent"` so Google lands on the right account instead of showing a bare
chooser, and (b) call the API once with the fresh credentials to confirm *whose* account came
back, and refuse to write the token file if it does not match the expected address. Announce the
ordered list of accounts to pick before firing the flows.

**Why:** Alessandro has 4+ Google accounts. The generic chooser is ambiguous ("I don't know which
one to choose"), and the old `~/triage/gmail.py auth|reauth` saved whatever Google returned without
checking. That silently bound `tokens/cdtm.json` to his personal Gmail and later to Tundra, so
3 CDTM drafts were written into the wrong mailbox and would have sent from the wrong address.
He explicitly praised the guided version on 2026-08-03: "you directly threw me to the correct
accounts, keep it like this for future cases."

**How to apply:** reference implementation is `~/triage/setup_all_accounts.py` (verify-then-save,
retries up to 3x on a wrong pick, skips tokens that are already correct). Reuse that pattern for
any new Google credential, and prefer running it over the bare `auth`/`reauth` subcommands.
Related: [[reference_triage_gmail]], [[reference_google_accounts_tokens]], [[feedback_open_auth_directly]].
