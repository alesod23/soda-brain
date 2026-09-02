---
name: feedback_diagnose_before_naming_root_cause
description: Never present a plausible guess as a diagnosis. Run the cheap check first; a wrong confident cause wastes his time and destroys trust.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f85a7d71-844e-4c73-90eb-29b50d9924f5
  modified: 2026-08-06T17:54:30.893Z
---

On 2026-08-06 a WhatsApp send failed while he was at MGH Boston. I told him the "most likely cause" was hospital WiFi throttling the websocket. He replied "this is BS. i am not on hospital wifi." He was right. A single `Test-NetConnection whatsapp:443` returned True and killed the theory in seconds. My second guess (modern-standby sleep cycling) was also wrong. The actual cause was a zeroed `auth/creds.json` from an unclean shutdown, findable in 30 seconds by reading the file's bytes and the Kernel-Power event log.

**Why:** a confident wrong root cause is worse than saying "I don't know yet." He acts on what I tell him, so a fake diagnosis sends him chasing his own network or rebooting things. It also burns the credibility that makes the real finding believable later. CLAUDE.md already bans speculation and "should"; this is the same rule applied to debugging.

**How to apply:**
- State a hypothesis as a hypothesis ("could be X, checking") and go run the check. Never write "most likely cause" before evidence exists.
- Prefer the cheapest discriminating test first: is the file valid, is the port reachable, did the process actually run, what does the log literally say.
- Read the artefact rather than reasoning about it. The log said `connected as` was never printed; that alone disproved every network theory.
- When two hypotheses die, stop guessing and go read the code/state. See [[feedback_windows_tail_locks_logfile]] for the related habit of verifying against the real system.
