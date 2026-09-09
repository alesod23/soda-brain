---
name: feedback_review_pages_need_keyboard_shortcuts
description: "Any page where he steps through a batch of cards must be keyboard-drivable - a/s to decide, j/k to move, e to edit, esc to leave the box"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 67360653-a4fa-4a49-9fe9-75fbdcbb9319
  modified: 2026-09-09T21:56:59.923Z
---

Every review surface I build for him (GTM boards, approval pages, any list he goes through card by
card) ships with keyboard shortcuts and a visible legend. Not as an extra; as part of the first
version. He asked for this on 2026-09-09, naming the old peer-60 approvals page as the thing he
liked: "we had ways to click 'a' to move to the next card etc. (like shortcuts to make me go
through it all faster)".

The canonical set, now in `~/gtm-eng/board-page.html` (the shared template, so every board gets it):

- `j` / `Down` next card, `k` / `Up` previous
- `a` mark ready and advance, `s` (or `x`) skip and advance. Pressing the same verdict twice clears
  it, so a mistyped key is one keystroke to undo, and advancing only happens when a verdict is SET.
- `e` focus that card's message box, `Esc` leave it. While a field has focus the letters are just
  text, never shortcuts.
- `o` open the profile, `c` copy the message, `1-4` pick the channel, `?` hide the legend.
- A fixed legend bar at the bottom, because a shortcut nobody can see does not exist.
- Clicking a card makes it current, so mouse and keyboard never disagree about where "here" is.

**Why:** on a 60-person board a mouse trip per card is the entire cost of the review, and that cost
is what makes him stop halfway. It is also an accuracy problem, not only a speed one: on ache-sd he
edited Sean Ring's message, never marked the card ready, and the commit silently shipped seven of
eight people. Only `ready` is committed. So the same change added a permanent header warning
("Edited but not marked ready, will NOT commit: <name>"), which is the guard against exactly that.

**How to apply:** build it into the template, never per board. If a new review UI is not
keyboard-drivable it is not finished. Implementation notes worth keeping: drive a CURRENT card
rather than DOM focus (there is no per-card focusable control, and stealing focus fights the
textarea), and guard `e.target.closest` since a synthetic event dispatched on `document` has no
`closest` and one TypeError there silently kills every shortcut.

Related: [[reference_gtm_boards]], [[feedback_gtm_boards_open_via_script]].
