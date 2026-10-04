---
name: feedback_propose_row_card_carries_the_draft
description: "A hub card proposing a new CRM row SHOWS the draft (instinct's unsent Gmail draft, else ours from the last exchange + why); the row yes never sends, the draft goes to the lane as its own card (hub #41 Vittoria + #40 Donarini, HUB H39, 4 Oct 2026; partly supersedes H38 / #42 Roussel)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c187d271-3593-4bb6-8043-3c5ba319d8a1
  modified: 2026-10-04T02:32:07.789Z
---

A card that proposes opening a CRM row for someone the system means to write to SHOWS THE DRAFT, already written, so he
judges it on the spot. The draft is the person's unsent Gmail draft when one exists (instinct saves its own, never write
a second), else one written from the last mail exchange with a "Why this text" line. His yes opens the row and puts the
draft into the lane as its OWN email card (register.py), where his yes is the send. His words on the row card become a
note on the row and rewrite our draft.

His words (hub #41, Vittoria Di Marco Berardino, 4 Oct 2026): "Why did you not already draft? In general, why are you not
already drafting these emails ... You can draft and go back to me. I can actually tell you whether I like a certain
draft". Same commit, #40 Donarini: "You should have drafted it already, so that I could also check the draft."

**Why:** the three cards #41/#42/#43 were answered in ONE commit (3 Oct 23:20). The earlier session read #42 Roussel
("the yes is referred to creating a row, not to draft ... I don't see you having thought about what to put in the
draft") as "no draft at all" (H38). Read together they say: draft first, show the thinking, keep the send a separate yes.
Also: instinct HAD saved a draft to Vittoria on 2 Oct, but `draft_already` searched `to:Berardino` and her address
`vittoria.dimarcoberardino@` is one token, so it was missed.

**How to apply:** `gtm-eng/agent/instinct_inbox.py`: `propose_row_card` -> `draft_for_row_card` (existing draft or
`WRITE_NEW` from `person_thread`); `apply_decisions` yes -> `open_row` + `note_on_row` + `lane_on_yes` (instinct's draft:
`register_existing`, register.py `--no-apply`, never replaced or deleted; ours: `REVISE` with his words, then
`handle_proposal(pid=...)` through the lane). With a row, an unsent instinct draft with no sidecar is registered, not
skipped. Name matching: `is_person` (surname inside the squashed address). Tests: `python
gtm-eng/agent/tests/test_instinct_inbox.py` cases [5], [8], [9].
Row EXISTS and instinct gave no text (hub #39, Andellini, 4 Oct: "You should have drafted the message too."): `write_text`
drafts it (H34), the old `ask_text_card` is deleted; `scheduled_already` first skips when a message to the person already
sits in Gmail's Scheduled folder (Martina's follow-up was scheduled for 5 Oct 06:00Z, so nothing was drafted). Hints in `_system/hints/instinct-inbox.md`. Rule: HUB H39.
See [[reference_approval_hub]], [[reference_soda_brain]], [[feedback_every_email_draft_goes_through_the_lane]].
