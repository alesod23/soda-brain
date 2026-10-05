---
name: feedback_resolve_hub_cards_by_id_not_seq
description: Resolve a hub card by the id read from the card he replied to (swipe-reply quote, tg_message_id), never by its #N alone; two numbering series can carry the same #N at once
metadata:
  type: feedback
---

5 Oct 2026 09:2xZ: he swipe-replied "already called the notary" to the notary card #58. I looked up "seq 58, unresolved" and
resolved a25p85n5unc, which was "#58 · US CAMPAIGN · MISSION REPORT" from the older numbering series. The real notary card
was a35fgmt32c8 (#58 of the new series). The wrong one was an update card with no action, so nothing ran, and the hub has
no reopen route.

**Why:** the hub's daily #N handles reset and overlap; a card from yesterday and one from today can both be #58.

**How to apply:** match the quoted text of his swipe-reply (or the card's tg_message_id) to the card's text, read its id,
check the text matches, then POST /resolve with that id. If two open cards share the #N, pick by text, never by number.
Related: [[reference_approval_hub]], [[feedback_telegram_ordinal_message_reference]].
