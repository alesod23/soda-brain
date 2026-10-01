---
name: feedback_no_headless_fuzzy_send
description: NEVER send a message headless/remotely to a fuzzy recipient; remote reply bots are draft-only; sends need triage-grade recipient verification
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 76c7578e-cb6d-4ecd-b540-c161a381259a
---

**A wrong-recipient send is the worst failure this system can produce. Never let it happen again.**

**What happened (2026-06-20):** the SODANOtif reply bot received "https://www.join-thebridge.com/ — DSend this to nick cdtm". It fuzzy-matched "nick" to **Nick Stracke (@stracken) on Slack cdtm** and sent immediately (DSend = send-now). Alessandro meant a DIFFERENT Nick (he has "Nick CDTM S26" as a WhatsApp contact) — wrong person AND wrong channel. He was (rightly) furious.

**Why it happened:** the headless bot called `slack.py send --confirmed` with a loose name. Slack's send auto-resolved the fuzzy name and fired, with NO ambiguity check and NO confirm-before-send. The on-computer WhatsApp send (`wa-daemon/send.js`) would have REFUSED it — it errors on ambiguous names ("Ambiguous: matches N contacts, pass a more specific name") — which is exactly the triage-grade safety the remote bot lacked.

**How to apply:**
- **Remote/headless reply bots (SODANOtif `bot.js`) are DRAFT-ONLY. They never send, on any channel, regardless of dsend/quotes/"send it".** `routing-prompt.md` enforces this. Sends happen on the computer via /triage.
- Any send path MUST: (1) resolve the recipient EXACTLY, (2) REFUSE ambiguous/fuzzy matches and list candidates (never silently pick one), (3) echo the exact resolved identity + channel + handle and confirm BEFORE sending.
- "nick", "nick cdtm" etc. are NOT recipients — `cdtm` is ambiguous (Slack workspace vs org vs a WA contact labelled CDTM). Disambiguate, never guess.
- **`slack.py send` has NO ambiguity guard** (unlike `wa-daemon/send.js`) — it auto-resolves fuzzy names. Treat it as unsafe for any non-explicit recipient until a guard is added.

See [[feedback_message_send_protocol]], [[reference_sodanotif]].
