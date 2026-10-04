---
name: feedback_propose_row_card_carries_the_draft
description: A hub card proposing a new CRM row asks for the ROW ONLY; no draft on it, his yes carries no message (hub #42 Roussel, 4 Oct 2026, HUB H38; supersedes hub #43 Severi / H37)
metadata:
  type: feedback
---

A card that proposes opening a CRM row for someone asks ONE thing: "yes = open the row only (no message)". Nothing is
drafted for it, his yes never carries a text, and his words on the card become a `note` activity on the new row. A
message to that person comes later as its own card that shows what it says and why.

His words (hub #42, Sandrine Roussel, 4 Oct 2026): "The yes is referred to creating a role in the CRM, but not to actually
draft a message ... I don't see you having thought about what to put in the draft."

**Why:** the earlier rule (hub #43, Severi, same day, H37) put a written draft on the row card so he judged both at once.
The drafts were written from instinct's one-line reason ("pilot unanswered for 17 days") with no thought about content,
and bundling made his yes to the row look like a yes to a message. H37 is marked SUPERSEDED in HUB-CARD-CONTRACT.md.

**How to apply:** `gtm-eng/agent/instinct_inbox.py` `propose_row_card` writes no text (instinct's own text, if any, is
shown "for information, NOT carried by this yes"); `apply_decisions` on his yes calls only `A.open_row` + `note_on_row`
(his feedback), never `handle_proposal`. Test: `python gtm-eng/agent/tests/test_instinct_inbox.py` case [5]. Any new
script that proposes a row follows the same shape. Hints line in `_system/hints/instinct-inbox.md`. See
[[reference_approval_hub]], [[reference_soda_brain]].
