---
name: feedback_resolve_account_before_linking
description: "Never hand Alessandro a Gmail authuser link from an assumption, and never let an OAuth flow show him a bare account chooser — resolve the mailbox first, state it, and always re-auth via setup_all_accounts.py."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1984c76b-671e-4733-b9d6-3b2db89db8bd
  modified: 2026-08-05T22:24:48.585Z
---

Two linked failures on 2026-08-05, both his correction: *"why didnt you directly send me to the account you wanted to me to access triage with? i just had to guess it was alessandro.sodano@cdtm.com..."*

**1. Resolve the mailbox before printing a link.** I printed
`...#drafts?compose=X&authuser=alessandro@tundrahealth.ai` from an assumption. Run
`gmail.py whoami --account <acct>` first, **state the address in the message**, then build the link
from what came back. `gmail.py`'s own `Open:` line is not authoritative — it prints an authuser hint
that can disagree with the mailbox the draft actually landed in.

**2. `gmail.py` re-auth drops him into a BLIND chooser — never use it.**
`gmail.py:76` is `flow.run_local_server(port=0)`: no `login_hint`, so Google defaults to whatever
account the browser last used. When `tokens/<acct>.json` is missing or unrefreshable, ANY gmail.py
command silently triggers that flow mid-task.

**Always re-auth with `python setup_all_accounts.py gmail:<acct>`** (or `cal:<acct>`). It passes
`login_hint` + `prompt=consent`, and it VERIFIES the identity before writing, retrying up to 3x on
the wrong account. Its map is the source of truth:
`cdtm → alessandro.sodano@cdtm.com` · `tundra → alessandro@tundrahealth.ai` ·
`sodano23 → alessandrosodano23@gmail.com` · `alesoda2002 → alesoda2002@gmail.com`.

**What it cost:** `tokens/tundra.json` got rebound to `alessandro.sodano@cdtm.com`. The Jakob
draft was created in the CDTM mailbox with `from: alessandro.sodano@cdtm.com` and would have
reached a prospect from the wrong address; the correct earlier draft was orphaned in the other
mailbox and a `delete-draft` against it 404'd, which is the tell that the binding moved.

**Tell for this bug:** `tokens/<acct>.json` mtime changes during an ordinary command, or
`delete-draft` 404s on an id that worked minutes ago. Re-run `whoami` immediately.

`gmail.py:76` still lacks `login_hint` — patching it to reuse the `setup_all_accounts.py` ACCOUNTS
map was offered and is not yet done.

Related: [[feedback_oauth_login_hint_and_verify]], [[reference_triage_gmail]],
[[feedback_clickable_file_paths]], [[feedback_email_draft_must_be_real_not_clipboard]].
