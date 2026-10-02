---
name: reference_hub_review_ui
description: "hub-review (box, http://100.85.52.84:4142/, Tailscale only): phone-first page to decide every open approval-hub card (yes/no/skip/change + system feedback), keyboard-driven, ONE commit. Change requests arrive on the savior's lane as a Telegram message sent AS him via Telethon; the savior acts on them and marks queue entries done."
metadata:
  node_type: memory
  type: reference
  originSessionId: 8b628b1a-a793-4289-b578-06e8098d767c
  modified: 2026-09-18T22:44:05.679Z
---

**What it is (built 2026-09-19):** `/home/da/hub-review/` (server.js port 4142 bound to the tailnet ip, page.html, notify.py, queue.jsonl, last-commit.json, README.md). Replaces answering the 23:00 digest card by card on Telegram. The digest card now ends with "Review on your phone: http://100.85.52.84:4142/ (Tailscale)". Kept alive by `~/.local/bin/hub-review-supervise.sh` (cron @reboot + */5, socket check on :4142, never pgrep -f). Reads the hub's state.json read-only; every mutation goes through the hub's HTTP routes.

**Page:** cards grouped Contacts / Drafts / Other, newest first, one per row, four 46 px verbs (YES = SEND on drafts, NO, SKIP, CHANGE with a text box), a "System-wide feedback / rules" box at the top, sticky bar with "3/19 decided" + COMMIT, legend always visible. Keys: `j/k` move, `a` yes, `s` no, `x` skip, `c` change, `e` expand body/context, `g` global box, `Enter` save, `Esc` cancel, `Ctrl+Enter` commit, `?` compact legend. Staged in localStorage per local day; nothing hits the hub until COMMIT. `?dry` in the URL = plan only.

**Commit = the yes (feedback_commit_batch_is_the_yes).** `POST /api/commit {decisions:[{id,seq,action,text?}], global?, dry_run?}`: yes/no -> hub `/resolve` (a draft yes = "N dsend", the hub sends the Gmail draft and reports); skip -> nothing (hidden for the day); change -> NOT resolved, appended to `queue.jsonl` `{qid, ts, kind:"change", id, seq, type, head, request, status:"open"}`; global text -> `{kind:"system", ...}`. Then, if anything was queued, ONE Telegram message to the bot chat sent AS HIM by `notify.py` (Telethon, `/home/da/tg-reply-resolver/user.session`, api creds `~/.env/tg-user-api.env`, python `/home/da/voice-lane/venv/bin/python`). Format: `hub-review commit <local ts>: n yes, n no, n skip, n change. CHANGES:\n#<seq> <type> <head> · id <hub id>: <text>\n...\nSYSTEM: <global>` (sections omitted when empty). Notify failure never fails the commit: `notified:false`, the page warns "changes queued, notify failed", the queue is the record.

**What the savior does when that message arrives (it reads as his own instruction):** for each CHANGES line act on the request using the hub id (a draft = revise + re-register per [[reference_draft_review_lane]], `N change:` semantics; other cards = do what he wrote, then `/resolve` the card), and `POST 127.0.0.1:4142/api/queue/done {id:<hub id or qid>}`. SYSTEM lines are rules: save them (memory or the producer) and mark done. `GET 127.0.0.1:4142/api/queue` shows what is still open. Never re-ask him about a committed decision.

**Gotchas:** seq resets daily, so the page shows "#4 · 16 Sept" for older cards and the message carries the hub id; a bare NO still triggers the hub's own one-line "Disapproved #N" notice per card (switch to `/close notify:false` in server.js if that becomes noise); bound to 100.85.52.84 only, loopback refuses by design. Test only with `dry_run` or skip-only commits: a real yes executes the card's action.

Related: [[reference_approval_hub]], [[feedback_review_pages_need_keyboard_shortcuts]], [[feedback_commit_batch_is_the_yes]], [[reference_draft_review_lane]], [[feedback_pgrep_self_match_use_script_files]].

**2026-09-27 rebuild (his asks of that day, all live on the box):** the card's text is EDITABLE (draft body + subject, or the single message of a Slack/WhatsApp card; `e` focuses it) and a yes on an edited card sends HIS version: the server runs `task-land/_system/drafts/hubedit.py` first (Gmail draft rewritten in place with `gmail.py update-draft`, sidecar `edited_in_hub`, hub `/revise`, before/after in `_system/hub-edits.jsonl`), then `/resolve`; if the edit fails nothing is sent. a/s/x/d open a one-line verdict box (Enter = verdict, sentence + Enter = verdict with comment, Esc = nothing). New verdict `done` (`d`) = hub `/close`, nothing executed. Comments travel in the commit message under `COMMENTS:` and are queued `kind: comment`. Header: "last reload HH:MM:SS" + "live, checked N s ago"; the page polls `/api/cards` every 10 s and redraws only on a new `rev`, never while a field has focus. Cards with `meta.outdated` come first with the evidence. One card by link: `/#c<id>`. The type chip used to carry the class `card` (35 chips styled as cards): now `t-<type>`. Backups `*.bak-20260927`.

**2026-09-30: Messages filter + open the message (replaces the Drafts tab group):** cards carry `channel` + `open_url`;
`All | Messages` filter (`m`), chip colour per channel (email blue, LinkedIn violet, WhatsApp green, Slack plum; chip
only), Open button + clickable subject (`o`). `GET /open/<hub id>` -> 302 to `#drafts/<token(threadId)>` with
authuser (thread id ALWAYS: the message id opened a blank pane). Tally and commit use `ALLC` (all cards), never the
filtered `CARDS`. Next: open_url for LinkedIn / WhatsApp cards. README section "2026-09-30".
Same day, his correction ("more visual ... same colors we use on tg chat ... a nice logo"): channel = SOLID badge with
the real brand mark (Simple Icons paths in `CHANNEL_LOGO`), colours of the Telegram dots (Gmail red #d93025, LinkedIn
blue #0a66c2, WhatsApp green #128c4a, Slack purple #611f69), plus one outlined filter button per channel present.
Lesson: for channels he wants logo + the TG colour everywhere, never a pale text chip. Filed as a hub rule (addrule).

**2026-10-02: one card = one screen + the brief (hub H22).** His words: "not able to see fully the card when I click j or
k ... fix forever" and "approvals that arrive pre-chewed: what, who, why, my recommendation". Every card is a flex column
capped at `100dvh - --head-h - --bar-h - 20px` (`.chead` fixed / `.cmid` scrolls / `.cfoot` = verdict buttons + boxes,
fixed); verified on all 38 cards at a 701 px window. `briefOf()` in server.js gives every card `brief {what, who, why,
rec}`: a producer's `meta.brief` wins, otherwise derived (sidecar "Chi e'" / instruction sections, critic suggestion,
"Who:" / "Suggested:" lines). New producers SHOULD send meta.brief. Test gotcha: Claude-in-Chrome tabs are `document.hidden`,
so smooth scrollIntoView never runs; measure with behavior:'auto' instead of trusting screenshots.

**2026-10-02: every message card is editable (his "why can i not edit the text there before sending???").** Root cause:
`gtm-eng/agent/inbound_asks.py chat_card` attached the `wa-send` action only when the draft had no questions for him,
and built the jid as `<key>@s.whatsapp.net` although these chats are `<lid>@lid` (a send would have gone nowhere).
Now: `chat_jid(key)` reads the real chatJid from the WA store and every WhatsApp reply carries its send; the 9 open
wa-drafts were backfilled via hub `/revise` (action with the @lid jid). hub-review `editableOf` falls back to meta.body
for wa-draft/slack-draft, and `hubedit.py` writes his text into meta.body when a card has no action. Verified: all 17
open message cards editable. Not verified: a live WhatsApp send to an @lid jid through the hub (daemon send.js accepts @lid).
