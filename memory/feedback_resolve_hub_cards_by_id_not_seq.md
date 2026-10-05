---
name: feedback_resolve_hub_cards_by_id_not_seq
description: "Hub cards are resolved by their id read from the card, never by #N; two numbering series coexist and the same seq names two cards"
metadata:
  node_type: memory
  type: feedback
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-10-05T10:04:29.984Z
---

A hub card is closed or resolved by its `id` (the string in /pending), matched to the card's text, never by its `#N` seq. On 5 Oct 2026 the hub carried two cards numbered #58 (an older series and the new one): the savior resolved the US campaign mission report (a25p85n5unc) when he meant the notary card (a35fgmt32c8). No harm (a report card, action null), but the wrong card left the list and the hub has no reopen route (only an idem-key re-post reopens).

The box's account of the same miss (5 Oct 2026 09:2xZ): he swipe-replied "already called the notary" to the notary card #58; the lookup "seq 58, unresolved" returned a25p85n5unc ("#58 · US CAMPAIGN · MISSION REPORT", older series) instead of a35fgmt32c8 (#58 of the new series).

**Why:** the seq restarted when the hub was rebuilt; the hub's daily #N handles reset and overlap, so a card from yesterday and one from today can both be #58. His words name cards by number, the API only by id.

**How to apply:** when he says "#N" or swipe-replies, GET /pending (or ?all=1), match the quoted text (or the card's tg_message_id) to the card's text, read its id, check the text matches, then act (POST /resolve) on that id; if two open cards share the #N, pick by text, never by number. When posting, write the id in the plan next to the seq. Same rule on the box (the savior saved it as its own memory). See [[reference_approval_hub]], [[feedback_telegram_ordinal_message_reference]].
