---
name: feedback_ping_cards_must_be_full
description: "PING CARD" is his word for an approval card on laptop AND phone; they must arrive FULL (decision + context), never as a bare decision line
metadata:
  node_type: memory
  type: feedback
---

**Terminology, his, 2026-08-10: a "ping card" is an approval-hub card on EITHER device — the laptop popup and the phone popup are both ping cards.** Use that word; he does.

**A ping card must be FULL.** *"The ping card you give me on laptop is very empty, nothing in it... even the Telegram messages are very empty. I need them to be full."*

**Why it was broken:** the hub composed the full body for the phone only. `GET /next` returned `"<id>\n<text>"` and `pushTelegram()` sent `item.text` — both the decision line alone. `context` never left the server, so the phone's "[cut] full text on the laptop popup" marker pointed at a place the text did not exist. Real cost: he rejected card #1 (Mila Ruiz, WA) with a bare no at 16:04 on 2026-08-10, minutes before reporting this — an unreadable card is a rejected card.

**Fixed 2026-08-10 in `approval-hub/`:**
- `GET /next` appends `\n\n---- CONTEXT ----\n\n` + context. Wire format is unchanged (`<id>\n<rest>`), because `popup.ahk` splits on the FIRST newline and renders everything after it.
- `popup.ahk` `Show()` switches to a read-only `VScroll` Edit when the body is >12 lines or >700 chars. A plain Text control with `AutoSize` would have grown past the bottom of the screen. Measured after: 366x517 px on a 1280x752 work area.
- `pushTelegram()` appends the context, capped at `TG_MAX = 3500` (Telegram's own limit is 4096), and now HTML-escapes both text and context via `htmlEsc()` — nothing escaped `item.text` before, so a `<` in a card could break or silently drop the whole ping.

**Surface roles — do not "fix" the phone by making it as long as the others.** Phone is where he DECIDES, laptop and Telegram are where he READS IN FULL. The phone body stays capped (`MD_MAX_LINES`, currently 58) because the MacroDroid dialog grows instead of scrolling and past some height the Yes/No buttons slide off and the card becomes unanswerable. He reported a phone scroll problem the same day; if it recurs the fix is LOWERING the cap toward the proven-safe 43, not raising it.

**Producer contract (unchanged, now load-bearing):** decision in `text`, the whole artifact in `context`. A producer that inlines an email into `text` gets clamped and looks broken on every surface.

See [[reference_approval_hub]], [[feedback_approvals_are_pings]], [[feedback_sodanotif_card_format]].
