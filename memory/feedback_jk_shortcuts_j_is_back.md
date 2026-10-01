---
name: feedback_jk_shortcuts_j_is_back
description: "Standing rule 2026-09-19: in EVERY keyboard-driven review page of his (hub-review 4142, GTM boards 4141, trippy 4126, anything new), j = BACK and k = FORWARD, the opposite of the vim default. Arrow keys keep their natural meaning (Down = forward, Up = back). Legends must say 'j back / k fwd'."
metadata:
  type: feedback
---

**His words (2026-09-19 01:08):** *"to change for everytime we have this text shortcuts (even in gtm boards if needed: j is back and k is fwd, not other way around)"*

**Why:** he reads j as "jump back" and k as "keep going"; the vim convention (j down, k up) works against his muscle memory, and a wrong direction key on a 20-card review costs a mis-decision.

**How to apply:**
1. Every new review surface binds `k` (and ArrowDown) to next, `j` (and ArrowUp) to previous. The first keystroke on a fresh page selects the top card, as before.
2. The always-visible legend spells it out: "j back / k fwd" (never "j/k move").
3. Done 2026-09-19 in `/home/da/hub-review/page.html` and `/home/da/gtm-eng/board-page.html` (box copies). The LAPTOP is the writer of gtm-eng (hourly tar push), so the same swap must be applied in `C:\Users\Alessandro\gtm-eng\board-page.html` or the next push reverts it: handoff `task-land/_system/HANDOFF-20260919-jk-shortcut-swap.md`.
4. Trippy boards (4126) have no j/k yet; when they get one, use this rule.

Related: [[feedback_review_pages_need_keyboard_shortcuts]], [[feedback_never_collapse_what_he_must_read]], [[reference_gtm_boards]], [[reference_hub_review_ui]].
