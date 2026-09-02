---
name: sodanotif-live-gmail-slack
description: "Gmail + Slack are LIVE SODANOtif sources since 2026-09-02: 60s pollers on the DA VPS write jsonl stores that daemon.js tails (same Telegram cards as WhatsApp); the 6h recap is no longer the first place he sees email/Slack"
metadata: 
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-02T17:19:41.496Z
---

**Built 2026-09-02.** Gmail and Slack reach the user as individual SODANOtif Telegram cards within ~1 min, laptop-independent. Before this they only surfaced via the 6h recap (laptop `SODANOtif-Recap`, left untouched). **The recap is no longer the first place he sees email/Slack** (recap contract in [[reference_sodanotif]] now holds for those two channels as well).

## Pipeline (all on the VPS, user `da`)
- `da-gmail-poll.timer` / `da-slack-poll.timer` (systemd, `OnUnitActiveSec=60s`, `OnBootSec=30s`, `AccuracySec=5s`) run `/home/da/sodanotif/pollers/gmail_poll.py` and `slack_poll.py` with `/home/da/triage/venv/bin/python`. Unit files also in the synced repo `~/task-land/_system/vps/` (+ `units.list`).
- Pollers append store lines (`id, ts, iso, timestamp, source, chatId, chatName, sender, text, url, fromMe:false, _group`) to `/home/da/sodanotif/stores/gmail-store.jsonl` / `slack-store.jsonl`.
- `daemon.js` tails them via `sources/gmail.js` / `sources/slack.js` (same offset-tail / start-gate / id-dedupe contract as `sources/linkedin.js`; env `SODANOTIF_GMAIL_STORE` / `SODANOTIF_SLACK_STORE` in `/etc/systemd/system/da-sodanotif.service`) -> 8s debounce -> Haiku classify with a per-source hint -> card. Dots: 🟢 WA, 🔵 LinkedIn, 🔴 Gmail, 🟣 Slack. Gmail cards show `<sender> /<account>`; Slack channel mentions show `<sender> /#channel`, DMs no group.
- Canonical source = laptop `~/.claude/sodanotif/` (pollers/, sources/, daemon.js); edit there, scp to the box, `chown da:da`. md5-identical on both sides as of build.

## Gmail poller facts
- `users.history.list(startHistoryId, historyTypes=messageAdded, labelId=INBOX)` per account, state `/home/da/sodanotif/state/gmail-state.json` (`accounts.<acct>.historyId`, `seen` 7d, `skipped` log-once reasons). Reuses `triage/gmail.py get_service()` (headless refresh; interactive auth hard-blocked there, so it can never pop an account chooser).
- Active mailboxes: **cdtm** + **tundra**. `lobbly` is SKIPPED as a duplicate of the cdtm mailbox (its token resolves to alessandro.sodano@cdtm.com). `sodano23` / `alesoda2002` tokens are dead on the box (AUTH REQUIRED) and skipped, logged once.
- Pre-filters (before the classifier): self-sent, noreply/notification/mailer/invitations/welcome/newsletter locals, `List-Unsubscribe`, `Precedence: bulk/list`, `Auto-Submitted`, calendar acks/receipts (`gmail._cal_type` reply/other; invite/update/cancel go to the classifier), `stale` > 12h by internalDate (code-level post-filter per [[reference_sodanotif_recap_stale_gmail_fix]]), not-INBOX / SENT / DRAFT.
- `text` = `Subject — <first 600 chars of the body>` (NOT Gmail's 200-char snippet: a warm-intro email was judged "FYI only" on the snippet because the ask sat past it; with the body preview it is kept with a draft). Classifier hint also states warm intros always need a reply.
- 404 on `messages.get` = draft autosave phantoms, counted as "vanished", ignored.
- historyId expiry (404 on history.list) -> reseed from `getProfile`, emits nothing.

## Slack poller facts
- ONE `client.counts` (POST, xoxc token + d cookie) per workspace per tick gives `latest` + kind for every conversation the user is in (`conversations.list` has NO `latest` and pages through every public channel: it tripped `ratelimited` on the first live test, do not use it per tick). `conversations.history oldest=<last-seen> limit=50` only for conversations whose `latest` moved, cap 12/tick (rest deferred). Names via lazy cached `conversations.info` (7d) and `users.info` (state cache + `slack/users-cache-<ws>.json`).
- State `/home/da/sodanotif/state/slack-state.json` (`workspaces.<ws>.last_seen{conv: ts}`, `convs`, `users`, `skipped`).
- Kept: all DM / group-DM messages; channel messages only with `<@U0AFHUWDUA0>` (own id from the token file). Dropped: own messages, bot/join subtypes, `slack/mute.json` channels, messages older than the user's own later message in the same conversation (2026-07-15 rule), ts <= last-seen ([[feedback_slack_cutoff_filter]] post-filter).
- Workspaces: **cdtm** live (34 conversations seeded). **xplore** token rotated (`invalid_auth`) and **horus** `admin_deactivated_account`: both skipped, logged once; re-run `slack.py auth-cookie` to revive xplore.
- Known gap: threaded replies inside a DM are not returned by `conversations.history` (only top-level + broadcasts).

## Ops
- Logs: `/home/da/sodanotif/logs/gmail-poll.log`, `slack-poll.log` (2MB rotate); each tick logs `tick: cdtm 0 new, tundra 0 new (1.1s)`. `journalctl -u da-gmail-poll -u da-slack-poll`. Daemon: `journalctl -u da-sodanotif | grep -E "Gmail in|Slack in|flush"`.
- **Re-seed** (emit nothing, restart from now): delete the account/workspace entry (or the whole file) in `state/gmail-state.json` / `state/slack-state.json`; next tick logs `seeded ...; emitted nothing`.
- **Replay test hook** (never sends anything outward): `gmail_poll.py --replay-latest cdtm` / `slack_poll.py --replay-latest cdtm[:CONV_ID]` (`--dry-run` to print only) re-emits the newest passing message re-stamped as now (id suffix `:replayNNN`, original time in `replay_of`) so the daemon's start-gate/dedupe let it through -> a real card lands on Telegram.
- flock per poller (`state/*.lock`): a manual run while the timer fires exits with "another ... is running".
- Rate math per minute: Gmail 2 accounts x 1 `history.list` (+1 `messages.get` per new mail) of a 250 units/s quota; Slack 1 `client.counts` + <=12 `history` + rare `info` calls against tier-3 ~50/min.
- Fixed on the way (2026-09-02): the daemon unit's `SODANOTIF_SKILL` pointed at `/home/da/.claude/commands/triage/SKILL.md` (does not exist; the skill is at `~/.claude/skills/triage/SKILL.md`), so the box classifier ran WITHOUT the /triage rules for every source. Corrected in the unit. The laptop `daemon.js` default still carries the old `commands\triage` path (only matters if the daemon runs on the laptop again).
