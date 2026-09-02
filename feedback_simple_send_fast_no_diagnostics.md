---
name: feedback-simple-send-fast-no-diagnostics
description: A routine send (dsend/WA/Slack) is ONE fast action — never run a multi-step daemon diagnostic or shell retry-loop for it; the send tools now self-heal transient flaps
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b75b1302-8e9b-4e42-b796-f57031e2eebf
---

2026-07-23: a "dsend this LinkedIn URL to Caleb" took **8 minutes**. Cause was two things, both avoidable:
1. The WA daemon had a transient flap (Baileys reconnect, code 428, recovers in ~5s) so the first send failed.
2. Instead of riding through it, I ran a full diagnostic (process check, port check, heartbeat, /health, log tail) AND deliberated between every step, then hand-rolled a `sleep 6` shell retry loop.

**Why it matters:** the user's whole point is low-friction. An 8-minute round trip for a one-line send destroys that and reads as the system being broken.

**How to apply (every session/chat):**
- A routine send is ONE action: resolve recipient → call the send tool ONCE → confirm. That's it.
- `wa-daemon\send.js` now **auto-waits up to 35s through a flap** (`waitForConnection`) before deciding, and sends exactly once. So just call it — do NOT wrap it in a shell health-poll / `sleep` retry loop, and do NOT pre-check the daemon yourself.
- Do NOT investigate daemon internals (process/port/heartbeat/log) for a routine send. Only escalate to diagnostics if `send.js` still fails AFTER its own 35s wait (then it's a real outage — check [[reference_wa_daemon_repair]] / [[reference_wa_daemon_health]]).
- Same principle for any tool that self-heals: trust the tool's own retry, don't reimplement it slower in the shell.

Related: [[reference_wa_sender]] (send.js now flap-tolerant), [[reference_approval_hub]].
