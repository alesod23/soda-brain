---
name: feedback_review_page_design_system
description: "Every page he steps through with j/k or letter shortcuts (GTM boards, approval hub, CRM queues, candidate lists) follows ~/gtm-eng/DESIGN-SYSTEM.md: one item = one screen at 1568x773, same zones in the same places, explanations behind a ? hover, one draft per channel, screenshot before handover (ruled 2026-09-19)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-19T17:03:38.239Z
---

**Rule (his words, Quick Claude panel, 2026-09-19, relayed by another session):** "a very well-oiled design system ... apply it every time I ask you for a new go-to-market board, or even for an approval hub of some kind. I know it doesn't apply exactly the same because the items are different, but some rules must still apply."

The contract is `C:\Users\Alessandro\gtm-eng\DESIGN-SYSTEM.md` (read it before touching the hub, a board, the CRM Today queue or any review page). The reference implementation is `~/gtm-eng/board-page.html` (healthforce-it board): copy its `:root` tokens and the `.card / .chead / .body / .col / .help / .checks / .keys` blocks; never invent a second look.

The rules that transfer to every item-by-item page:
1. **One item = one screen at 100% zoom, 1568x773 CSS px.** j/k lands the item's top edge under the sticky header, the whole item visible, no scrolling inside a step: `scrollIntoView({block:"start", behavior:"auto"})` with `scroll-margin-top` = header + gap; never "center", never smooth. Item `max-height` = 100vh minus header, keys bar and gaps; long zones scroll inside themselves (at most two).
2. **Same zones, same places:** left = the context that explains, right = the thing he acts on, then the verdict buttons, then the amber "Check before sending" bullet list under the buttons on the right. Verdict buttons at the same spot on every item so a/s land blind.
3. **Explanations hide behind a small "?" hover** next to the badge (provenance, which pattern, where seen); a note under a field is one short line or nothing.
4. **One draft per channel:** the pill switches the text; edits stored per channel; never "email version if you switch: ..." pasted into a note.
5. **Screenshot at 1568x773 before handing a page over.**

**Why:** the healthforce-it board landed with cards running past the screen, one draft pretending to be four channels and a wall of provenance on the left; he reviews dozens of items in one sitting and wants his eyes and hands to know where everything is before the card arrives.

**How to apply:** any new or edited review surface, including the box's hub-review page (:4142) and the coattio Today view if it is ever reshaped into a stepper, starts from the template and is checked against the budget (header 56, gap 12, item <= 663, keys 30) with a screenshot. Pairs with [[feedback_review_pages_need_keyboard_shortcuts]] (a/s decide, j/k move, legend visible) and [[feedback_gtm_boards_open_via_script]].

**Addendum 2026-09-20 (CRM boards): s asks why.** On a CRM review board, pressing s opens a one-line box under the verdict: Enter alone = plain skip, text + Enter = skip with a reason, Esc = close without deciding. The reason rides in the commit line as `<id>: skip | perche': <text>` so the session executing the commit can put it in memory. His words: "avere comunque l'opzione di dare un commento sul perche' ho skippato, cosi' che ti possa andare in memoria." First page: [[reference_crm_catchup_board]]. Rule text lives in `~/gtm-eng/DESIGN-SYSTEM.md` §6.
