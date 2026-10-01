---
name: feedback_commit_batch_is_the_yes
description: "A batch he COMMITS on a GTM board (or any commit gesture) is already the approval. Never post a hub card asking him to confirm a committed batch; the commit IS the yes and the send lane starts. Ruled 2026-09-16 after card #15 (\"estonia: 5 committed, waiting to be sent\") asked again with zero new information."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8b628b1a-a793-4289-b578-06e8098d767c
  modified: 2026-09-16T16:23:53.039Z
---

**Rule (his words, 2026-09-16 18:22, angry):** *"why are you asking me confirmation here????? i already committed the batch and you give me ZERO new info in this message. lets just setup that a commit batch is automatically a yes."*

**What happened:** he committed 5 messages on the Estonia GTM board (4 LinkedIn notes, 1 DM, Richard Jalakas leads). The system then posted hub card #15 "estonia: 5 committed, waiting to be sent. Nothing has gone out yet." asking for a yes. The card repeated what he had just done and added nothing: no new fact, no risk, no choice.

**Why it matters:** a confirmation card is only legitimate when it carries a decision he has not yet made (feedback_ping_cards_must_be_full: decision in `text`, artifact in `context`). Commit is a deliberate, keyboard-driven act on a page he reviewed line by line (feedback_review_pages_need_keyboard_shortcuts). Asking again is friction, not safety.

**How to apply:**
1. Commit on a board = approval. The send lane proceeds without a card. If the sender needs a human session to run (LinkedIn sends via a normal session), it runs it; it does not ask.
2. A card after a commit is allowed ONLY when something changed between commit and send that he could not have known: a recipient became unreachable, a message failed, a rate limit, a new reply from that person. Then the card states the new fact and the choice, never "are you sure".
3. Same principle for every commit-shaped gesture: `dsend`, "send it", `N yes`, a ticked checklist, an approved Inbox row. One yes is one yes.
4. Card #15 was resolved yes by the savior on his behalf the moment he complained; the producer of that card is to be changed so it no longer posts it (see bridge/GTM logs for where).

Related: [[feedback_approval_ping_once]], [[feedback_ping_cards_must_be_full]], [[feedback_message_send_protocol]], [[reference_gtm_boards]].
