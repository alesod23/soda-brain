---
name: feedback_never_trigger_bare_account_chooser
description: "HARD RULE - never run a command that can pop Google's \"Choose an account\" screen; only ever touch accounts that already have a token, and say which address before running"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bcf4ed36-d8ed-4e48-817b-146c5998e5ca
  modified: 2026-08-11T21:57:46.170Z
---

**Never leave Alessandro on Google's bare "Choose an account" page.** He said it plainly on 2026-08-10, second occurrence: *"you did it again: you opened without already directing me to the correct account. make it a rule that you never leave me here on this page."*

**What triggers it:** running `~/triage/gmail.py <cmd> --account <name>` for an account with **no token in `~/triage/tokens/`**. `gmail.py` silently falls into its OAuth flow, which opens a chooser with **no `login_hint`** — seven identical "Alessandro Sodano" rows plus two of Caleb's. Picking wrong binds the token to the wrong mailbox and nothing warns you. That is how `tundra` once got rebound to cdtm and three prospect drafts were misfiled. See [[feedback_resolve_account_before_linking]], [[feedback_oauth_login_hint_and_verify]].

**How I caused it (don't repeat):** a convenience loop `for acct in cdtm sodano23 alesoda2002` over `gmail.cmd search`, to check whether an email had been sent. `cdtm` had a token and answered; `sodano23` did not, so it launched a browser auth in his face mid-task.

**SECOND OCCURRENCE, 2026-08-11 — the rule as written above was NOT ENFORCEABLE.** *"WHY ARE YOU ASKING ME THIS AGAIN??? WE MADE A RULE YOU WOUDNTTT GO DIRECTLY IN THE ACCOUNT. DO IT AGAIN"*. I followed step 1 below: `sodano23.json` **existed**, so I ran `whoami --account sodano23`. The token was **dead** (revoked/scope-drifted), `gmail.py` fell through to `run_local_server()`, chooser again. **A token file existing is not proof it works.** Never treat "the file is there" as the safety check.

**THE STRUCTURAL FIX (2026-08-11) — this is now the real guarantee, not the checklist.**
Both `~/triage/gmail.py` and the new `~/triage/drive.py` gate the browser flow behind `INTERACTIVE_OK`:
- it runs ONLY for the `auth` / `reauth` subcommands, with `--allow-auth`, or with env `GMAIL_ALLOW_INTERACTIVE_AUTH=1`
- every other command raises `AUTH REQUIRED for account '<x>' (<why>)`, naming the token path and the exact reauth command, and **exits without opening anything**
- new `--login-hint` on every subcommand, passed into `run_local_server(login_hint=...)`, so even a deliberate reauth lands on the right account and the chooser never renders
Verified 2026-08-11: `whoami --account sodano23` prints AUTH REQUIRED and stops; `whoami --account cdtm` still returns the address. **If a future session sees that error, DO NOT add `--allow-auth` to make it go away** — that is the guard doing its job. Ask, or run `reauth` with an explicit `--login-hint`.

**How to apply:**
1. **`ls ~/triage/tokens/` FIRST.** Only accounts with a `<name>.json` are usable. Gmail today: `tundra`, `cdtm`, `lobbly`, `alesoda2002`(cal only), `sodano23`(**token present but DEAD** — do not use). Note `cal-*.json` is Calendar scope and does NOT make the Gmail account usable, and `drive-*.json` is Drive scope only.
2. **Never loop `--account` over names you have not verified.** One unverified name in a loop is enough.
3. If an account genuinely needs linking, **stop and ask**, then use `~/triage/setup_all_accounts.py gmail:<acct>` which passes `login_hint` and verifies the address before saving. Never let `gmail.py` self-auth.
4. Say the resolved address out loud before acting on any mailbox.

**Damage check after an accidental chooser:** `ls -lat ~/triage/tokens/` for anything newly written, confirm no live `gmail.py`/OAuth listener (`netstat` on 8080-8090), then `gmail.cmd whoami --account <each>` to prove nothing got rebound. On 2026-08-10 nothing was written and both `tundra` and `cdtm` still resolved correctly.
