---
name: reference_laptop_ipv6_google_flaky
description: "Home Wi-Fi (Fastweb 2001:b07::/32): ~1 in 3 TCP connects to Google's IPv6 addresses time out, IPv4 is clean. httplib2 (google-api-python-client) tries v6 first and waits 21 s per dead address, so gmail.py/gcal.py/drive.py fail or take 23 s. Fix: triage/_prefer_ipv4.py (getaddrinfo sorted v4 first), imported by every laptop triage Google script (2026-09-22)."
metadata: 
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-22T14:32:27.656Z
---

**Symptom (2026-09-22 16:23):** Quick Claude D handoff failed: `list-drafts tundra failed (1): Traceback ... gmail.py line 755 cmds[args.cmd](args)`, then "could not tell which draft in tundra you are typing". Same command worked from a shell minutes later. Not a token problem: tokens/tundra.json was valid.

**Measured cause:** `socket.connect` to each resolved address of www/gmail/oauth2.googleapis.com, 6 s timeout, 3 tries: IPv6 addresses failed 11 of 39 tries (e.g. 2001:4860:4845:400:: 2/3 fails), IPv4 0 of 27. httplib2 walks getaddrinfo in order (v6 first) and a dead v6 costs the Windows SYN timeout (21 s); 6 concurrent list-drafts took 23 s with 3 failures, and even 1 of 3 sequential runs failed. The laptop has global v6 from the router (2001:b07:ac9:3471:...) plus Tailscale's fd7a:.

**Fix in code (done):** `~/triage/_prefer_ipv4.py` wraps `socket.getaddrinfo` to put AF_INET first (IPv6 not disabled). Imported by gmail.py, gcal.py, drive.py, contacts_sync.py, gdoc_agenda.py. After: 6 concurrent list-drafts all ok in 3.8 s, 5 sequential ~2 s each. `_system/drafts/common.py` now prints the TAIL of a failing gmail.py stderr (the exception), not the first 200 chars.

**Not done (his call, system setting):** a machine-wide `netsh interface ipv6 set prefixpolicy` to prefer IPv4 would also cover Chrome/Node/curl. Any other Python that hits Google from the laptop and shows 21 s stalls or WinError 10060: import the shim.

Related: [[index_laptop_and_misc]], [[reference_draft_review_lane]], [[reference_quick_claude]].
