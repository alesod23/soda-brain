---
name: feedback_propose_row_card_carries_the_draft
description: A hub card proposing "open a CRM row and draft" must already show the draft; his yes carries that exact text into the lane (hub #43 Severi, 4 Oct 2026, HUB H37)
metadata:
  type: feedback
---

When a card proposes opening a CRM row AND writing to the person, the draft is written before the card goes out and is
shown on it, so he judges both at once. His words (hub #43, Severi): "did you not also draft the email so that I could
judge that too?"

**Why:** a "yes = open the row and draft" card with no text made him say yes blind, then judge a second card later.

**How to apply:** `gtm-eng/agent/instinct_inbox.py` `propose_row_card` calls `write_text` when instinct gave no text and
stores the text in the remembered proposal; after his yes, `handle_proposal(..., pid=)` finds the new row by pid (never a
name + org re-match, which once posted a duplicate card). Any new script that proposes row + message follows the same
shape. Rule filed as HUB-CARD-CONTRACT H37; hints line in `_system/hints/instinct-inbox.md`. See [[reference_approval_hub]],
[[reference_soda_brain]].
