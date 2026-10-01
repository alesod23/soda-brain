---
name: feedback_sodanotif_card_format
description: "How SODANOtifications push cards must be formatted (bullets, bold sender, date+time, source shorthand)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 76c7578e-cb6d-4ecd-b540-c161a381259a
  modified: 2026-08-02T00:20:16.974Z
---

SODANOtifications push-card format, locked by Alessandro 2026-06-19. Implemented in `~/.claude/sodanotif/watch.ps1` (`Format-SourceLabel`/`Format-Item`/`Build-Card`) + `push.js` (sends `parse_mode=HTML` via `--file --html`).

**Why:** he reacts to these on his phone; he needs to know WHO/WHERE and WHEN at a glance, and the channel name already tells him the platform so a "(Slack ...)" tag is redundant noise.

**How to apply (every card):**
- **NO push-time in the card header (user rule 2026-08-01):** the header had the card's push time while item lines carry the message's SENT time; he flagged the duplication — "only the time underneath, when the message was sent, is important". Headers are now `SODANOtif · <source>` (daemon.js) / `SODANOtif · N new` (watch.ps1 Build-Card), timeless. The per-item `· MMM d, HH:mm` sent-time stays. Recap's header keeps its "as of" stamp (digest semantics, not a duplicate).
- **Channel color dot FIRST (user rule 2026-08-01, "always... that's a rule"):** every item line starts with its channel's color circle so the source is spottable at a glance — WhatsApp `🟢`, Gmail `🔴`, Slack `🟣`, anything else `⚪` (no logo emojis exist in Unicode). Implemented in `lib-format.ps1` (`$DOT_*` + `dot` field from `Format-SourceLabel`, rendered by `Format-Item` after the bullet) and mirrored in `daemon.js` `buildClassifiedCard` (WA-only → green, `\u{1F7E2}`). Order: `• 🟢 [!] <b>Sender</b> ...`.
- **Bullet + bold**: the **person/channel is bolded** (HTML `<b>`), urgent items prefixed `[!]`. **v2 rule (2026-06-19): a notification with a SINGLE message has NO bullet (one clean line); use bullets (`•`) ONLY when multiple messages are pooled** (the per-source 60s debounce batch).
- **Date + time**: show when the message arrived, `MMM d, HH:mm` (e.g. `Jun 18, 17:10`), after a middot. The classifier emits a `when` field (and a `kind` = group/channel/dm) per item — added via the SODANOtif prompt note in watch.ps1.
- **Source shorthand (the labels):**
  - Gmail cdtm -> ` (@cdtm)` (always parenthesised, like (WA))
  - Gmail lobbly -> ` (@lby)`
  - **Gmail "via" / mailing-list** (From header `Felix Doerpmund <x@cdtm.de> via cdtm.com`): render `<bold sender> via <list> (@account)`, e.g. **Felix Doerpmund** via cdtm (@cdtm). The `via <list>` (the path it came THROUGH) is kept SEPARATE from `(@account)` (which mailbox received it) — they can differ, e.g. **X** via substack (@cdtm). Classifier sets `from`=the human sender and `via`=the list domain shortened (cdtm.com -> cdtm), '' if direct.
  - WhatsApp -> NO tag since 2026-08-01 ("no need for (WA) anymore") — the green dot self-identifies the channel. Gmail KEEPS `(@cdtm)` because it names which mailbox, not the platform.
  - Slack channel / WhatsApp group -> `/<name>` and **NO** "(Slack ...)" tag — the channel/group name self-identifies the platform. Use `/` to mention any group/channel.
  - Slack DM -> just the bold person, no tag.
- Layout per item: `• [!] <b>Sender</b> @cdtm · Jun 18, 17:10` then the snippet indented on the next line.
- **RECAP card header/footer (user rule 2026-07-18, "always the same"):** title line = `🚨📬 <b>CATCH-UP</b> — N unread · MMM d, HH:mm` — the two emojis appear ONCE at the start, NO mirrored repeat at the end of the title; footer line = those SAME two emojis again `🚨📬` (was `🚨🚨`). Implemented in recap.ps1 `Build-RecapCard`.
- **PS 5.1 gotcha:** watch.ps1 source stays pure ASCII; the `•`/`·`/`—` glyphs are built from code points (`[char]0x2022` etc.) because PS 5.1 reads a BOM-less `.ps1` as ANSI and mojibakes literal Unicode. Cards go to Telegram via a UTF-8 temp file (`push.js --file`), not stdin, so glyphs survive.

See [[reference_sodanotif]].
