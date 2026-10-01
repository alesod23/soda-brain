# HANDOFF 2026-09-27: to-do as an autonomous pipeline + hub review edits/outdated cards

Written by the 2026-09-25/26 session right before he compacts. The next session gets his prompt verbatim (he pastes it);
this file holds everything that session needs to build it well without re-reading two days of work. READ THIS FIRST,
then the memory files named at the bottom. Tone of his brief: "you always have to imagine what a very knowledgeable
system would do in front of a to-do like this".

## 1. His asks, in order (his words, 2026-09-27 00:30)
1. **To-do -> autonomous pipeline.** A to-do item is created -> in progress (picked up by AI) -> ready for review ->
   finished. Categories (`#tundra`, "personal") are noise ("everything is Tundra, I never read those categories"); do not
   bother with them now. "in progress" = being done by AI; "ready for review" = clickable, opens a summary of the AI's
   work. Example he gave: a to-do "own incubators" -> the system understands the goal (a Notion page with up-to-date
   deadlines for every top incubator), fills it, then gives him an easily reviewable list (yes/no per item, text
   shortcuts, "because it knows that's how I prefer to review"). Another: drafts for Tania on WhatsApp prepared and
   ready for review; drafts for legal already created.
2. **System rule: check existing drafts before creating one.** "I want to understand how you would find out that it was
   already created. You should start checking the drafts themselves when you build a draft to ensure it's not already
   there." (Gmail drafts across accounts + the lane's sidecars/queue.)
3. **Calls -> the CRM's Call page.** A to-do that is a call: find the number, put it in the CRM Call section ("that's where
   I would normally manage all the calls"). Ties to his handwritten notes (picture 3): in-person / call work recorded
   into the CRM workflow automatically.
4. **Ready-for-review items ARE hub cards**, and the Obsidian daily page links to that specific hub card.
5. **Edit-then-approve** (hub AND CRM review): "sometimes an email might be pretty much perfect but I'm missing a couple
   of things, not worth a prompt and a wait. I just wanna edit the text directly. You see the changes I made, and that
   gets approved. Then I can comment: 'I approve this version, I changed x, y', or I don't say it and you see it anyway."
6. **Hub keyboard design like the CRM review**: a shortcut to approve or skip that auto-opens a comment box. His example
   of what he'd type: "a) this thing actually went out, b) you didn't do what the CRM does: every new event should make
   you wonder whether the approval cards changed." **Outdated cards**: the moment he sent that message/email (an event),
   the system should have read it and noticed the hub card was outdated. "That's part of the reason why I never go in
   the hub: there's a bunch of outdated shit."
7. **hub-review page**: next to the manual Reload button, show the date/time of the last reload, and make refresh
   frequent/live.

## 2. What exists today (pointers; verified this session)
### The to-do system (task-land)
- Daily page engine: `task-land/_system/daily-lib.ps1` (Render-Bucket, Format-TaskLine, mirror lines: CRM count, hub
  open count, daily campaign), `daily-sync.ps1` (absorb: ticks, retitle=rename, replace-in-place, `((prompt))`
  directives, sub-checklists, done-stays-till-eod, junk guards). Task files `Tasks/{active,inbox,waiting,archive}/*.md`
  with frontmatter (`bucket, id, title, status, completed, created, due, surface_on, project, source, tags, pin`, plus
  `contact:`/`crm_url:` for CRM-born tasks, `migrated_to_crm`). **No status beyond open/done/cancelled exists**: the
  pipeline states (in_progress, ready_for_review) are new frontmatter + rendering + absorb rules. The whole contract of
  the page is in `task-land/CLAUDE.md` (read it: every guard there was paid for in data loss).
- A new mirror/status line needs THREE things (regex in `$script:MirrorLines`, `$script:MirrorHeld` in its `Format-*`,
  and a `continue` in `daily-sync.ps1 Parse-Section`); missing the third produced 104 junk tasks on 2026-09-25.
- Watcher: `DailySync-Watchdog` task every 5 min; `daily-sync.log` says why anything happened.
### The hub (approval cards) and hub-review
- Hub: `~/.claude/approval-hub/server.js` on :4180 (laptop), `POST /pending {text, context, notify}`, `/resolve`,
  `/close`, `GET /item/<id>`, `/unresolved-ids`; state.json; contract `task-land/_system/HUB-CARD-CONTRACT.md`;
  card kinds `email-draft`, `linkedin-draft`, `update`, decisions -> `_system/decisions.jsonl`.
- hub-review (his review page, keyboard, ONE commit): **on the box** `/home/da/hub-review/` (server.js :4142 tailnet
  ip, page.html, notify.py, queue.jsonl, last-commit.json, README.md); `POST /api/commit {decisions:[{id,seq,action,
  text?}], global?, dry_run?}`; change requests go to the savior's Telegram lane as a message sent AS him; the savior
  acts and marks `/api/queue/done`. The screenshot he sent shows this page: header "hub review · 61 open · 01:56",
  a "Reload" button top right, cards with SEND / NO / SKIP / CHANGE buttons and a `change: ...` box. **His ask 7 is
  there** (last-reload stamp next to Reload; live refresh). Editing the box's server means editing on the box (savior
  session "savior box (19-09)" via SendMessage, or ssh); the page is served from the box.
- Draft lane: every email = Gmail draft + sidecar `task-land/_system/drafts/r-*.md` + `register.py` -> hub card; the
  reconciler `reconcile.py` (box cron 5 min, safe on the laptop) already detects **his edits in Gmail**
  (`edited_in_gmail`, his text stored in the sidecar, pushed into the card) and **sent** (closes the card). That is the
  seed of "edit then approve": for an email card, his edit in Gmail + "N dsend" already works; what is missing is
  editing IN the card/page and approving that text (hub-review `text?` in decisions exists in the API; the page has
  no editable body), and the same on the CRM review board (that one DOES it already: the verdict carries the textarea
  text, commit sends his version; see below).
- Events -> outdated cards: nothing links a hub card to the event that would outdate it. The CRM monitor
  (`~/.medtech-crm/crm-app/monitor.js applyEvent`, `stepEffect`) already turns a sent message into "step done outside"
  for the CRM; the same signal (sent-log.jsonl, corpus, Gmail Sent via reconcile) can close/flag hub cards whose
  `context`/type names that person or draft. RULE-LOOP.md §1 "Observe" is the design home for it.
### The CRM review mode (built 2026-09-26; the design he wants copied to the hub)
- `~/.medtech-crm/review-api.js` + intake routes `/review/*` (:4137) + `crm-app/public/review.js` + styles `.rv-*`.
  Keys j/k a s r c e g o, ArrowLeft = WHY pane, Esc; the verdict box opens on a/s/r/c with pills sucks|like|change and
  message|timing; his sentence -> `addrule.py --contract email|crm` (or `--like`, or a change request in the workplan);
  every verdict -> `_system/decisions.jsonl` surface `crm-review`; **approve carries the edited textarea text and
  subject**, commit sends that text (`drawer-api.sendNext`) and closes the step: exactly his "edit then approve".
  Nightly `compare()` = proposed vs what he actually sent -> hypotheses. Workplan
  `~/.medtech-crm/WORKPLAN-20260926-today-review-mode.md`; memory `project_crm_review_loop_vision.md`.
- CRM Call page: `crm-app/public/app.js` `ACTION_PAGES.call` (people with a phone and no reach yet, or a call step due;
  log = call_attempt). A call to-do -> a CRM person with a phone + a `call` next step lands there by itself
  (`POST :4137/task-handoff {action:"step"}` or the drawer; the to-do bridge `_system/crm-bridge.ps1` already migrates
  `contact:` tasks into steps).
- The daily page's CRM line and hub line are count-only by his ruling (per-person lines were "too much clutter").
### Drafting rules that bear on ask 2
- `feedback_every_email_draft_goes_through_the_lane`, `feedback_email_todo_find_existing_thread` (reply in thread is the
  default; find the thread first). Existing-draft check = `gmail.py list-drafts --account <a>` (both cdtm and tundra)
  + the lane's `queue.jsonl` / sidecars by `to` + subject before `gmail.py draft`. Put it in the drafting skill's
  procedure via the ledger (`addrule.py --contract email`), and in code where drafts are made unattended (ask-api
  `draft` op, campaign.py, review-api).
### Gmail links (2026-09-26 evening, do not regress)
- A hex id in a Gmail URL hash is dead; links are `#drafts/<token>` from `gmail_draft_url()` (gmail.py, handoff.py,
  intake `gmailUrlToken`). Any "summary of the AI's work" link or card link to a draft must use it.

## 3. Standing constraints (still in force)
- Never send anything without his verdict (the daily campaign auto-fire is the one exception); "dsend" sends, "go" does
  not; a committed batch IS the yes, never a card asking to confirm a commit.
- Coattio servers :4124/:4137 are restarted with Stop-Process + `coattio-serve.ps1` (never run_in_background); the
  hub's :4180 by its watchdog; the box's hub-review by its supervise script.
- Boards open via `open-board.ps1`; Chrome extensions need HIS reload; AHK scripts need HIS reload.
- Bash heredocs with backslashes get mangled and the destructive-commands hook blocks some heredocs: write patch
  scripts with the Write tool and run them with the PowerShell tool.
- Ledgers append-only; a sentence of his is filed the same turn (`addrule.py`); "change this on the go" = a build item.
- Opus where something is decided or written; no Haiku.

## 4. Open from the previous session (unrelated, do not lose)
- Quick Claude: the J/K/D key-hint widget often does not show after Alt+Win+J; D on a GTM board tab ran
  `claude --resume "Board: parallel-news"` for a session that does not exist. An agent was asked for a root-cause report
  and never delivered; the AHK is `AutoHotkey\quick claude (alt win j).ahk`, registry `~/.claude/quick-claude/sessions.json`.
- `sodano23` Gmail token is dead (his reauth); DKIM on tundrahealth.ai is his action.
- Drafts Tabs 1.6 needs his one reload at chrome://extensions.

## 5. Memory files to read next session
`reference_rule_loop`, `reference_approval_hub`, `reference_hub_review_ui`, `reference_draft_review_lane`,
`project_crm_review_loop_vision`, `reference_daily_campaign`, `feedback_commit_batch_is_the_yes`,
`feedback_review_page_design_system`, `feedback_output_goes_into_the_owning_system`, `index_vault_daily_capture`.
