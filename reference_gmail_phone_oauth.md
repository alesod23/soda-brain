---
name: reference_gmail_phone_oauth
description: "Re-authorize a Gmail account on the box from the PHONE: triage/phone_auth.py, two steps, no browser on the box and no laptop."
metadata:
  type: reference
---

`gmail.py auth/reauth` uses `run_local_server()`, which needs a browser on the same machine, so
on the box it is unusable. `~/triage/phone_auth.py` (written 2026-09-19) splits the flow:

```
./venv/bin/python phone_auth.py url --account <name> --login-hint <exact address>   # print consent URL
# he opens it in Chrome/Safari (NOT Telegram's in-app browser: Google rejects it), approves,
# lands on "Unable to connect" at localhost:8765, and pastes that whole address back
./venv/bin/python phone_auth.py exchange --account <name> --response "<pasted url>"  # writes tokens/<name>.json
```

Nothing listens on 8765. The loopback redirect is only the carrier for `code=`; the "site can't
be reached" page IS the success state, and the code expires in minutes, so ask for the paste
immediately. The script sets `OAUTHLIB_INSECURE_TRANSPORT` (http loopback) and
`OAUTHLIB_RELAX_TOKEN_SCOPE` (Google returns the scopes in another order) itself, and it refuses
to build a URL without `--login-hint`, so the bare account chooser still cannot appear
([[feedback_never_trigger_bare_account_chooser]]).

**Personal mailbox:** the token named `sodano23` is **alessandrosodano23@gmail.com** (not
sodano23@gmail.com). It holds the ICLN / YCGL lane, university-era mail, and everything personal;
`cdtm`, `lobbly`, `tundra` are the work accounts. `alesoda2002` is still dead as of 2026-09-19.

Both personal tokens had been dead since 3 August 2026, which is why the box could not answer
"find that email I sent from my personal address" until this existed. Related:
[[reference_triage_gmail]], [[feedback_oauth_login_hint_and_verify]].
