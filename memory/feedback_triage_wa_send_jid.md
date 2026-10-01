---
name: triage-wa-send-jid
description: "Inside /triage, send WA via --jid from the fetch-all bundle, never --to \"<name>\" — the JID is unique, names are not."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 08a010cc-3a1a-474f-995c-d20a76e7ae9c
---

When /triage's fetch-all bundle surfaces a WA chat, every item carries `jid` (e.g. `224953240682725@lid`, `393318062472@s.whatsapp.net`). That is the chat's unique identifier — the daemon dispatches by JID.

**Rule:** when sending a reply or suggested message INSIDE /triage, always pass `--jid "<chatJid>"` to `wa-daemon\send.js`. NEVER `--to "<name>"`.

**Why:** `--to <name>` triggers contact-name resolution against `contacts.json` + `aliases.json`. Many display labels are short ("Lara", "Marco") and match multiple contacts. The daemon's resolver correctly errors out:
> ERROR: Ambiguous: "Lara" matches 2 contacts:
>   - Klara UR #8576 -> +420770108576
>   - Lara CDTM -> +4915159416978

This forced a retry mid-round on 2026-05-23 even though the bundle had `jid: "224953240682725@lid"` in hand — the JID would have sent first try.

**How to apply:**
- Inside /triage: every send call uses `--jid "<chatJid>"`. Pull the value from the same item I'm acting on in the bundle.
- Outside /triage (e.g. /wa skill, ad-hoc "send Marco a msg" requests): `--to "<name>"` is still appropriate — that's where name resolution earns its keep.
- The display still shows the human label ("Lara", "Arianna Antonelli") — only the SEND CALL changes.

**Related:** [[reference_wa_sender]] — daemon send API spec; both `--to` and `--jid` are first-class. The choice is contextual, not a daemon limitation.
