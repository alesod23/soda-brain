---
name: reference_draft_review_lane
description: "Email draft-review lane (built 2026-09-08): every outbound email = gmail draft -> register.py (separate critic, sidecar, queue, hub card #N -> Telegram expandable card) -> he answers 'N dsend / N no / N change:' or iterates in Quick Claude via Alt+Win+J then D. Where every piece lives, what needs him."
metadata: 
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-10T15:39:34.272Z
---

**Contract + workplan (READ FIRST for any email drafting):** `task-land/_system/WORKPLAN-20260908-draft-review-lane.md` (rulings, spec addendum, build log) and `task-land/_system/EMAIL-REVIEW-CONTRACT.md` (H1-H17 hard rules, soft register table, C1-C5 ruled).

**The spine, one call after `gmail.py draft`:**
`python task-land/_system/drafts/register.py <draft_id> --sidecar <id>.md [--origin box|laptop|quick-claude] [--replaces <old message_id>] [--no-apply] [--no-critic]`
= `critic.py` (deterministic checks + separate `claude -p --strict-mcp-config --tools ""` sonnet, ~75 s; pre-loop body kept verbatim in `<id>.critic.md`; rewrite APPLIED as a new Gmail draft by default) -> sidecar updated (ids, `## Revision log`, `## Body as registered`) -> `queue.jsonl` (laptop Drafts tab group) -> `send_card.py` -> approval hub `POST /pending` type `email-draft` / `linkedin-draft` (or `/revise` when the sidecar has `hub_card_id`: SAME #N, Telegram message edited in place + "revised" ping). `--origin quick-claude` = card registered `silent`, nothing to Telegram (channel affinity ruling). A revision is always a NEW draft + `--replaces` (closes the old Chrome tab).

**Verbs on a draft card:** `N dsend` / `N yes` = hub sends the draft itself (`gmail-send-draft` action, result reported as a one-line notice); `N no`; `N change: ...` = the savior revises and re-registers. `handoff.py list|<selector>` resolves "the draft I'm looking at" into Quick Claude's `HANDOFF.md`.

**Where it runs:** hub + `reconcile.py` cron (5 min: Sent detection -> `sent` + card closed via `POST /close`; his Gmail edits -> `edited_in_gmail`, his text becomes the base) on the box; the AHK D chord, the `drafts-tabs` Chrome extension (`~/browser-extensions/drafts-tabs`, polls intake `GET :4137/drafts/queue`) on the laptop. `gmail.py get-draft` exists on both machines since 2026-09-08. Hub backups `server.js.bak-20260908`, `push.js.bak-20260908`.

**Test state (2026-09-08):** UPMC draft = card #1 silent, MEDICON draft = card #2 in his chat, both HOLD, neither sent. The critic is a TEST (A/B open-ended, "I'll say when"): show him both versions every time. Needs him: load the extension (Load unpacked), restart the intake server once, press Alt+Win+J then D on a Gmail draft.

**GTM boards too (2026-09-08 evening):** `handoff.py board:<slug>` / a `127.0.0.1:4141/b/<slug>` URL renders the board + his `state.json` + commits + `gtm-eng/boards/<slug>/CONTEXT.md` (the brief: his ask, rules, per-person status; write one per board, same idea as a sidecar). The D chord handles a board tab. A Quick Claude changes messages via `POST /api/board/<slug>/state`; LinkedIn sends only via Commit + a normal session. Estonia's CONTEXT.md exists (Richard never named to Terje/Annika/Peeter; hacker house did not happen and is confidential; Tallinn hook being walked back).

**Is the Drafts tab group working? (2026-09-10):** do not guess from Chrome. `drafts-tabs` 1.2 posts a heartbeat after every 30 s poll; read `GET http://127.0.0.1:4137/drafts/tabs-status` (`groups`, `tabs_in_group`, `queue`, `opened_now`, `errors`, `stale_seconds`). `status:null` = the extension has not polled since the intake server started (not loaded, or needs a reload at chrome://extensions, which only he can click). A retest = register a draft to himself with `--origin quick-claude --no-critic`, then read that endpoint.

**Gotcha (2026-09-08):** `claude --mcp-config` is variadic (a list of paths). A positional prompt AFTER it is read as another config file ("MCP config file not found: ...\Read HANDOFF.md"). Put the prompt before `--strict-mcp-config --mcp-config`.

**How to apply:** never send; never call Telegram `getUpdates`; any `claude -p` gets `--strict-mcp-config`; keep the queue append-only per machine (git-synced file). See [[reference_approval_hub]], [[reference_quick_claude]], [[feedback_email_no_signature_block]], [[feedback_message_send_protocol]].


**drafts-tabs 1.5 (2026-09-26, his three asks):** ONE Drafts group in the whole browser (oldest wins, tabs move windows);
each tab's hover title is `Draft: <subject> -> <to> (<account>)` (scripting permission, pinned against Gmail's rewrites;
`to` in the queue entry, intake enriches old ones from the sidecar); a tab whose URL lost its `compose=` id closes on the
next poll (sent or binned inside the tab), no wait for the box reconciler. Reload at chrome://extensions after any
change (only he can). `reconcile.py` is safe on the laptop and was run there that day: the group had 20 genuinely
unsent drafts from 15-25 Sep, which is what it is for.
