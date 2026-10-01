---
name: feedback_wa_recipient_resolution
description: "When a WhatsApp recipient isn't in contacts.json, DON'T give up — grep the daemon message-store for their name/pushName (they may have messaged), try spelling variants, and know contacts.json goes stale when the Google sync token expires."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6ae8a5d1-8ed7-4951-926a-c95e51082ad5
---

Before ever telling the user "contact X not found on WhatsApp," exhaust these — a "not found" that's actually findable reads as sloppy (caught 2026-07-02: failed to find "Alessandro Zannis EF" because I searched "Zanis" not "Zannis", and never checked the store):

1. **Try spelling variants of the name** (single/double letters, with/without suffix). Transform what the user says into plausible saved forms; don't only try the literal string.
2. **Grep the daemon message store** `C:\Users\Alessandro\.claude\wa-daemon\message-store.jsonl` (case-insensitive) for the name — if they've messaged, you'll get their `chatJid` and `pushName` even when they're NOT in contacts.json. WA's `pushName` is the person's OWN profile name (often just a first name), which differs from the contact name the user saved.
3. **contacts.json is Google-synced and goes STALE** when the OAuth token expires (`sync-contacts.js sync` → `invalid_grant`). A recently-saved contact won't be there until a re-auth: `node ~/.claude/wa-daemon/sync-contacts.js auth` (interactive Google login — trigger it directly per [[feedback_open_auth_directly]]). If the user says "I definitely saved this contact," suspect a stale/broken sync, not a missing contact.
4. **Always append the discovered name↔jid to `wa-daemon/aliases.json`** (standing rule in [[reference_wa_sender]]) so the next send is one-step.

Only after (1)-(3) come up empty should you ask the user for the number. Related: [[reference_wa_daemon_repair]].
