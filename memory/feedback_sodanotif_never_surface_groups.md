---
name: feedback_sodanotif_never_surface_groups
description: "Standing never-notify list for SODANOtif - CDTM Engineering and Servus & See You are never actionable; the enforcement point is muted-jids.json, not judgement"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bcf4ed36-d8ed-4e48-817b-146c5998e5ca
  modified: 2026-08-10T13:32:59.106Z
---

Some chats are **never** worth a SODANOtif card or a recap line, no matter what they contain. Do not re-evaluate them message by message.

- **CDTM Engineering** `120363071370133642@g.us` — user rule 2026-08-10: *"cdtm engineering is never actionable/worthy of sodanotif."* It is a peer tech-chat (tool recommendations, links); nothing in it is ever a to-do for him.
- **Servus & See You - Adil & Lucas** `120363410693408849@g.us` — user rule 2026-08-10: *"in it for the vibes, wont be present."* Event-coordination group for something he will not attend, so every logistics message is noise.

**Why:** these were generating cards that cost attention and returned nothing. He does not want a smarter classifier for them, he wants them gone.

**How to apply:** add the JID to `~/.claude/sodanotif/muted-jids.json` (`muted` array **plus** a `_comments` entry saying what it is and which rule created it). Read by `sodanotif/sources/wa.js` and `sodanotif/recap.ps1`, so one edit covers both daemon cards and recap catch-ups. **Interactive `/triage` is deliberately NOT affected** — muting hides a chat from push, it does not hide it when he goes looking.

To resolve a group's JID from a name, grep `sodanotif/notification-log.jsonl` for `"group":"<name>","jid":"..."` — the first match often has an empty jid, so take the one that is populated.

Joins the existing absolute mutes: Fosdinovesi, Car Sharing Torino-Milano-Monaco, HEC Paris 23 | Car Sharing. See [[reference_sodanotif]], [[feedback_sodanotif_card_format]], [[feedback_noreply_never_in_notifications]], [[feedback_triage_actionable_definition]].
