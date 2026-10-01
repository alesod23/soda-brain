---
name: feedback-browser-comet
description: "For trippy browser automation, ALWAYS attach to the running Comet via CDP — never spawn a fresh launch_persistent_context profile"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5bf3e4d7-faea-4ab8-a723-c9f3ef764fcf
---

For any trippy browser automation (flight check, deep dive, booking funnel), **attach to the user's running Comet via CDP on port 9222**. Do NOT spawn a fresh Comet instance with `launch_persistent_context` or your own `user-data-dir`.

**Why:** The shared `profile-comet/` user-data-dir holds the user's airline logins — Volotea (MegaVolotea member fare), easyJet, Ryanair myRyanair, ITA Volare, plus bahn.de, sncf-connect, italospa. A fresh profile throws all of that away → re-logins, captchas, aggregator-level pricing instead of member fares. The user said it bluntly (2026-05-17): "always not open a new Comet profile, but this one here you worked on. For every flight we check."

**How to apply:**
- Use the exact prologue from `trippy/SKILL.md` (the "Copy-paste snippet for sub-agents" block). Every sub-agent dispatched for a browser task MUST start with `attach_or_launch_comet(...)` and then `connect_over_cdp("http://127.0.0.1:9222")`.
- If Comet's already running at 9222 → just attach. If not → `subprocess.Popen(comet.exe --remote-debugging-port=9222 --user-data-dir=<profile-comet>)`, wait for the port, then attach.
- Reuse `browser.contexts[0]` (carries cookies) and `ctx.new_page()` (opens a new tab in the running window).
- Leave the Comet window open at script end so the next agent in the chain attaches to the same instance and the user can verify / pay.

**Don'ts:**
- ❌ `launch_persistent_context(user_data_dir="profile-something-new", ...)` — old pattern, deprecated.
- ❌ `launch(headless=True)` — no Comet, no profile.
- ❌ Each sub-agent picking its own port — splits cookie state.
- ❌ Running `comet.exe` without both `--remote-debugging-port=9222` AND `--user-data-dir=<profile-comet>`.

**Comet executable + profile:**
- `C:\Users\Alessandro\AppData\Local\Perplexity\Comet\Application\comet.exe`
- `C:\Users\Alessandro\.claude\travel-search\profile-comet\`

**First-time-only seed:** `python setup_comet.py` once to dismiss Comet's `chrome://perplexity-onboarding/` screen — otherwise the very first CDP attach fails with "Browser window not found".

Related: [[reference_travel_search]] for the broader trippy infrastructure, [[feedback_airline_direct_for_known_carrier.md]] for why logged-in airline-direct prices matter.
