---
name: feedback_one_chrome_profile_for_every_signin
description: Every Google sign-in or consent page opens in HIS one Chrome profile (the CDTM one, Profile 1), where all his accounts are signed in; never a per-account profile, never a chooser (4 Oct 2026)
metadata:
  type: feedback
since: 2026-10-04
---

4 Oct 2026, 22:00, after I opened eight consent pages each in the Chrome profile whose user_name matched the account: "you've opened different Chrome profiles depending on the account ... I'm always using the CDTM Chrome profile, and I have all my accounts there."

**Why:** he lives in one profile; the other profiles exist but he does not work in them, so a page opened there is a page he does not see, and a sign-in there can ask for a password he keeps only in his profile.

**How to apply:** `task-land/_system/oauth_catch.py` opens every consent URL with `--profile-directory` of the profile whose user_name is the CDTM address (read from Chrome's Local State), with `login_hint` and `authuser` forced to the account that signs in (hub H59: one account, never a chooser). The box receiver on :8765 catches the redirect through his portproxy (hub H58, memory reference_approval_hub). Related: [[feedback_open_auth_directly]], [[feedback_never_trigger_bare_account_chooser]], [[feedback_open_urls_with_correct_account]].
