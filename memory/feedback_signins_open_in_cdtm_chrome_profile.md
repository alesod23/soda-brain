---
name: feedback_signins_open_in_cdtm_chrome_profile
description: Every Google sign-in opens in his CDTM Chrome profile (it holds all his accounts), pre-selected on the one account, and finishes itself through the box receiver; never a card, never a chooser, never a paste-back
metadata:
  type: feedback
---

4 Oct 2026: "I'm always using the CDTM Chrome profile, and I have all my accounts there." Opening sign-ins in other
Chrome profiles (Work, tundra, Default) confused him. Hub rules H58 (no card asking, open it in front of him) and H59
(land on the one account, no chooser) apply to every sign-in.

**Why:** the Google project triage-495517 was in Testing, so tokens died every 7 days and each re-auth meant a card, an
account chooser and pasting a localhost URL back. He published the app (In production, privacy page on
alesod23.github.io) on 4 Oct.

**How to apply:** `triage/phone_auth.py url --account X --kind gmail|calendar|contacts|drive --login-hint <email>`,
then a laptop session opens the URL in his CDTM profile with `&authuser=<email>`. Google redirects to localhost:8765, the
laptop's netsh portproxy forwards it to the box receiver (`triage/oauth_receiver.py`, 100.85.52.84:8765,
supervised by `~/.local/bin/oauth-receiver-supervise.sh`), which exchanges and writes the token. Watch
`~/.local/state/oauth-receiver.log` for "signed in:". Lobbly account retired the same day.
