---
name: reference-voice-lane
description: Voice fast lane — phone SodaOS recordings auto-routed instruction-vs-content; instructions pushed to Claudio TG for one-word execution
metadata: 
  node_type: memory
  type: reference
  originSessionId: b75b1302-8e9b-4e42-b796-f57031e2eebf
---

`C:\Users\Alessandro\.claude\voice-lane\` (built 2026-07-18). The phone's Voice Toggle macro uploads ALL recordings (quick to-dos AND long journals/meetings) to `G:\My Drive\From phone\SodaOS full view\` (.3gp, ~96kbps → ~12000 bytes/sec). Task **`Voice-Lane-Watch`** (every 1 min, hidden vbs) runs `watch-voice.ps1`:

- ≤75s → faster-whisper **small** transcribe → Haiku verdict `{instruction, confidence, kind: todo|send|other, green_light, todo_title, send_to, send_text, cleaned}` via `--system-prompt-file` (NEVER `--append-system-prompt` — that keeps the assistant persona and Haiku EXECUTES instead of classifying).
- **GREEN-LIGHT rules (user design 2026-07-18):** spoken "directly send"/"without review"/"dsend" + kind=send + recipient EXACT (case-insensitive) match in wa-daemon `aliases.json` → send.js executes immediately, 📤 receipt card; no exact alias → confirm card (wrong-recipient guard kept). kind=todo → ALWAYS auto-executes via `task-land\_system\capture.py --dest inbox`, ✅ receipt. Other instructions → 🎙️ confirm card (reply "go"/"dsend"; transcript+cleaned appended to sodanotif `notification-log.jsonl` for bare-reply resolution per [[feedback_resolve_reply_from_notiflog]]).
- 75–300s → same but only high-confidence instructions flag; else silent.
- >300s → untouched (content lane: journal/meeting → existing sodaOS flow).
- READ-ONLY on the folder (never moves files; content flow unaffected). State `state.json` (processed names, primed 55 files at build). DRY_RUN=1 for testing. Sets `TELEGRAM_STATE_DIR=telegram-null` before its `claude -p` ([[reference_telegram_channel_plugin]] 4th rule).
- Watches BOTH folders: `From phone\sodaos` (current — the phone macro re-targeted here Jul 14) AND `From phone\SodaOS full view` (older). Log = `lane.log` (voice-lane.log abandoned, locked by an orphaned debug tail). GOTCHA: never `tail -f` a live script's log on Windows — Git Bash tail blocks the writer's Add-Content. Willow Voice desktop CANNOT be used for transcription (no API/CLI; its own local fallback is a bundled whisper-server.exe).

**CONFIRM SCOPE (user rule 2026-07-20, "enable always"): phone popup fires ONLY for actions that reach/affect ANOTHER person** — sends, calendar events with other attendees. Solo or research-and-report-to-me tasks (lookups, "compile X and send it to ME", solo calendar blocks, todos) NEVER pop a confirmation; they just go to the session (card + notif-log) or auto-exec. Implemented via a classifier `involves_others` field; the webhook + "reply go" ask are gated on it. Trigger was an over-confirm popup for a pure Slack/WA research task. Green-light auto-send path unchanged. A misclassified real send is still safe (no popup → session card → message-send protocol still requires go/dsend).

**POPUP CONFIRM (built 2026-07-19 00:xx):** confirm-needed instructions also fire a MacroDroid webhook (`config.json#webhook_url` — EMPTY until the user sends their trigger.macrodroid.com URL from the imported "Claude Approve" macro) → phone shows YES/NO dialog with the action text → verdict returns as `claude-verdict-<id>-<yes|no>.txt` through the SAME sodaos Drive folder (chosen over Tailscale: phone's Tailscale is often offline; Drive sync is the always-on channel). Watcher Phase 1 executes/drops from `pending\<id>.json` and deletes the verdict file (verdict files are OURS — the never-touch rule covers only recordings). WA send commands are ALLOWLISTED in `~/.claude/settings.json` since 2026-07-19 (two PowerShell rules, user-approved "edit the rule") — Bash was already `Bash(*)`; every classifier block tonight was PowerShell-tool-only.

Related same-day phone-side pieces: MacroDroid macros authored from laptop and sent via TG as importable `.macro` files (schema learned from the user's Voice_Toggle export; OpenWebPageAction + ShortcutTrigger confirmed importing). "Claude Button" = floating-button → `tg://resolve?domain=Claudio_al_TG_v3_bot`. Auto-press-mic gesture (v2) FAILED on device — don't retry that path without a new approach.
