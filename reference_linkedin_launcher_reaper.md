---
name: reference-linkedin-launcher-reaper
description: "Why LinkedIn invites died with \"Connection closed\" and sessions showed linkedin-mcp disconnected - launcher.py killed every other launcher on start; fixed 2026-09-28"
metadata:
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-28T12:25:21.865Z
---

`~/.linkedin-mcp/launcher.py` used to kill EVERY other launcher on the live profile when one started ("newest
wins"). The campaign engine (`run-commit.py`), every Claude Code session and every headless `claude -p` without
`--strict-mcp-config` start that same launcher. So a Claude start during an invite killed the engine's server
("exception: Connection closed": privati-nord, 25 Sep 2026, a day with 139 headless runs), and every engine send
killed the LinkedIn server of every open session ("linkedin-mcp failed to connect").

**Since 2026-09-28** (`_reap_plan`, backup `launcher.py.bak-reaper-20260928`): on the live profile a starting
launcher kills only orphans (owner gone), whoever HOLDS the profile (a browser on it) unless the engine owns it, and
stray browsers. An engine-owned server (`run-commit.py`, `campaign.py`, `li_probe.py` as parent) is never killed; an
idle server of a live session is left alone. The poller family (`--user-data-dir`) is unchanged. Every decision is a
line in `~/.linkedin-mcp/reap.log`. Tests: `~/gtm-eng/agent/tests/test_reap_plan.py`.

**How to apply:** a LinkedIn failure = read `reap.log` first. A session opened before the fix keeps a dead server
until `/mcp` reconnect. Testing LinkedIn = `python ~/gtm-eng/agent/li_probe.py` (the engine's path, read-only), never
while a send runs. Login when the session itself expired stays his (CRM Repair button).

Related: [[reference-linkedin-mcp]], [[reference-system-agent]].

## LinkedIn "logged out" = restore first, his login last (2026-09-28)

His rule: "i want repair to AUTOMATICALLY go whenever down ... only then ping me if you DO NOT KNOW WHAT TO DO
ANYMORE." When the linkedin-mcp server decides the session is invalid it moves the whole logged-in profile, with
cookies.json and source-state.json, into `~/.linkedin-mcp/invalid-state-<time>/`. On 28 Sep that happened at the
first invite after the laptop woke (15:47, most likely no network yet); the session cookie inside was valid until
2027. `~/gtm-eng/agent/li_restore.py` copies the newest good quarantine back, runs `linkedin-mcp-server --status`,
rebuilds the poller clone (`clone-profile.ps1`), log `~/.linkedin-mcp/restore.log`. Exit 0 restored, 2 LinkedIn
really ended the session (only then he is asked), 3 a send is running. The system agent calls it by itself
(`li_repair`) and then releases the stopped LinkedIn channels. `campaign.py` skips a tick when there is no network.
The box cannot repair it: the session lives in the laptop's browser profile.
