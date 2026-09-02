---
name: project_sodaos
description: "sodaOS — phone-first journaling + self-tracking life OS for emotional awareness, food, and experiment→insight"
metadata: 
  node_type: memory
  type: project
  originSessionId: acf18dca-884b-41b6-9f8b-3aaf150ca57f
---

# sodaOS — life assistant / journaling OS

A phone-first **journaling + self-tracking system** Alessandro is designing (named 2026-06-16). Lives on the phone now; later portable to a physical recorder (Plaud-Pocket-style) or self-built hardware.

## Vision / pillars
1. **Powerful journaling** — emotional awareness, not just data ABOUT emotions. Capturing the felt experience, not only mood scores.
2. **Self-data gathering** — food intake, hunger/water/downtime "needs" events, energy slumps, and later biometrics.
3. **Experiment → insight loop** — inspired by **Rhise AI** (blocks apps + runs experiments on how you feel). Run small n-of-1 experiments, surface patterns. (e.g. observed pattern: low-protein late breakfast + caffeine on empty stomach + heavy fried lunch → afternoon crash.)
4. **Food coaching** — log meals via same quick-capture channel; nutrition insights surface alongside hunger/energy.

## Hard design constraints (locked 2026-06-14)
- **System for LIFE**: must be durable over YEARS, super easy to maintain, no babysitting.
- **Open, human-readable storage** — flat JSON/CSV/markdown log. NOT locked inside any one LLM's context or a specific model.
- **Deterministic plumbing** decoupled from the LLM — capture + dashboard logic must survive swapping/upgrading the model wired in. LLM is the insight layer only.
- Time/context must be well filled in on every log entry.

## Capture mechanics (current plan, phone = Pixel 9a)
- **No physical device yet.** Zero-hardware path: ping the Telegram bridge ("food", "water", "down") → timestamped → flat log → laptop dashboard.
- **Voice-log shortcut idea**: double-press Vol-Down → start recording "how I feel"; re-press → stop → share to Telegram as audio (or write a gdrive .mp4 Claude can access) → signal a Telegram chatbot a new log exists → pipeline analogous to existing **/audio-to-notes** transcribes + summarizes → new log in the system.
- New **dedicated Telegram chatbot** (separate from tg-bridge) to chat with + accept quick captures, surfaced via a phone widget.
- Hardware later: device with real button/screen (Pixel Watch) or a **Flic 2 button** → webhook → our timestamped log. (Fitbit Air rejected — screenless, no input surface, all logging on phone.)
- **Google Fitbit Air** (screenless, $99.99, AI coach, ~7d battery): purely passive sensor band, logging is phone-side. When Alessandro gets it, integrate its API (Google Health / Health Connect) for biometric data.

## OSS research findings (2026-06-16, 3 parallel agents)

**Emotion / journaling layer:**
- **Emotional granularity is the differentiator** (every app stores a mood *score*; sodaOS captures the felt word). Reference: **How We Feel** (Yale RULER) — 2-axis Mood Meter (pleasantness × energy) → drill to ~144 precise words. Use **Plutchik's wheel** as the stored emotion *schema*.
- **Vinaya-Journal** (MIT, GitHub) = closest architecture: flat files canonical, LLM reads a RAG/ChromaDB index built OVER them via Ollama. Proves model-swappable.
- **dartungar/obsidian-mood-tracker** (MIT) = storage blueprint: granular emotions in plain JSON, stats rendered as a view over data.
- **Rosebud** = reflection loop to copy: dialogic follow-up questions + weekly cross-entry retrospectives. **Mindsera** = detect cognitive distortion → offer reframe.
- Voice pipeline (record → on-device Whisper → reflect) validated; reuse existing faster-whisper /audio-to-notes.

**Experiment→insight engine (the moat):**
- Space splits 3 layers; almost nobody closes the loop = sodaOS's opening.
- **v1 = "Exist.io in ~150 lines":** flat daily JSONL events → collapse to ONE wide row per day (qs_ledger move) → for every (input,outcome) pair compute same-day AND lag-1 Spearman correlation, n≥~14 → surface as honest sentence. LLM only narrates rows, never does the math (= the swappable boundary).
- **Differentiator = QuantifyMe** (MIT Media Lab, the only real OSS n-of-1 loop): baseline → manipulate variable in phases → ADHERENCE GATE (comply ≥5 days + stable) → then score effect. = "run an experiment on how you feel" (Rhise idea).
- **v2 = Tigramite/PCMCI** lagged causal discovery (controls confounders). **Storage upgrade path** = SQLite + Datasette (Dogsheep) / HPI typed file-backed modules.
- Rhise AI has NO public footprint — treated as north star; reproducible = one-sec instrumented interception + QuantifyMe phasing + Exist lagged reporting.
- **Build order: correlation engine → n-of-1 loop → causal discovery.**

**Capture + health (Pixel 9a):**
- **No native double-Vol-Down mapping exists.** Route around it: best gesture = **Tap,Tap back-gesture → Tasker → Hi-Q `TOGGLE_RECORD` → AutoShare to Telegram**, or MacroDroid QS-tile/widget. Power double-press locked to camera/wallet.
- **Spine = Telegram bot as universal capture bus** (reuses tg-bridge, zero phone background process, OS-Doze-proof). Voice = .oga/Opus, whisper reads directly, 20MB cap fine. Long-polling getUpdates beats webhooks on a home laptop.
- **Health: do NOT build on Google Fit (sunsets end-2026); legacy Fitbit Web API dies Sept 2026.** Durable = **Health Connect** (Android 14+, Pixel 9a OK) built-in **Scheduled Export** → Drive zip (SQLite) → Python unpack → flat CSV/JSON. Google Health API only for headless cloud pulls.

**MVP (ships in an afternoon):** extend `~/.claude/tg-bridge/bot.js` → on `message.voice`, getFile → download .oga into `G:\My Drive\From phone\` (or voice\ drop) → reply "captured" → point existing faster-whisper /audio-to-notes at the drop. Phone: pin bot chat to home screen, hold mic to record. Tap,Tap+Hi-Q = phase 2; Health Connect = phase 3.

Key OSS to copy: How We Feel/Plutchik (schema), Vinaya-Journal (RAG-over-flat-files), QuantifyMe (n-of-1), qs_ledger (wide-daily-table + corr explorer), HPI (storage access), one-sec (instrumented intervention, PNAS-validated).

## DECISIONS
- **Storage = JSONL canonical** (decided 2026-06-16). Append-only flat JSONL is the single source of truth (machine-first, feeds the Exist-style correlation engine directly). Chose JSONL over Obsidian-vault and over hybrid. BUT must integrate easily with the existing /audio-to-notes voice pipeline: voice → faster-whisper transcript → structured event/entry appended into the JSONL. Capture spine = Telegram bot bus (reuses tg-bridge) + /audio-to-notes + Drive watcher.
- Three-layer architecture confirmed: CAPTURE (plumbing) → STORAGE (flat JSONL, model-agnostic) → INSIGHT (swappable LLM + deterministic correlation engine, reads OVER the files, never owns them). Emotion stored as structured record `{valence, arousal, label, note}` (Plutchik/How-We-Feel), NOT a 1-5 scalar.

## BUILT — capture MVP (2026-06-16, tested working)
Module at `~/.claude/sodaos/`; data at `~/sodaos/` (data/ raw/ _processed/). Components:
- `schema.md` — event contract. `structure-prompt.md` — LLM→JSONL prompt. `ingest.js` (zero-dep Node) — audio/text → transcribe.py → `claude -p` structuring → append `~/sodaos/data/events-YYYY-MM.jsonl`; always saves raw transcript + fail-safe journal fallback. `watch.ps1` — polls Drive drop folder.
- Patched `~/.claude/audio-notes/transcribe.py` to accept `.oga/.opus` (Telegram/Opus voice).
- Drop folder = `G:\My Drive\From phone\sodaos\` (SEPARATE from /audio-to-notes' `From phone\` root to avoid file contention).
- Structuring uses `claude -p` CLI (plan compute, model-swappable), NOT API keys. Tested: diario seed → 8 clean events, relative times resolved, emotion structured (valence/arousal/label), Italian preserved.
- Run: `node ~/.claude/sodaos/ingest.js --text "..."` or `--file "x.oga"` or `--latest <folder>`.

## PHONE SHORTCUT findings (research 2026-06-16)
- **Double Vol-Down screen-off is NOT reliable no-root on stock Pixel 9a** — volume keys only reach 3rd-party apps screen-ON without root; screen-off volume detection (Key Mapper / MacroDroid) is ROOT-only.
- Vol-Down double-press screen-ON works no-root via **Key Mapper** (FOSS, F-Droid; double-press native; needs WRITE_SECURE_SETTINGS via Shizuku/ADB) → Send Intent Hi-Q `TOGGLE_RECORD`.
- **Reliable no-root pocket gesture = Quick Tap (double-tap back)** — native, works locked/screen-off, improved Dec 2025. Can "Open app/shortcut" but not broadcast directly → point at MacroDroid shortcut.
- Recorder = **Hi-Q MP3** broadcast `yuku.mp3recorder.action.TOGGLE_RECORD` (pkg `com.hiqrecorder.free`), one toggle start/stop; `%last_recording_filename` for upload.
- Transport: (a) **Telegram bot HTTP** `sendDocument` multipart (skip flaky ACTION_SEND); (b) **FolderSync/Autosync → Drive `From phone\sodaos`** = lowest-maintenance, watch.ps1 already reads it. Battery=Unrestricted is #1 reliability fix.
- Recommended stack: **Quick Tap → MacroDroid → Hi-Q TOGGLE_RECORD → FolderSync→Drive (or Telegram HTTP)**.

## BUILT round 2 (2026-06-16)
- **Telegram voice ingestion LIVE**: `bot.js` (@Soda2402_bot, chat 5362797891) now downloads voice/audio msgs → ingest.js → JSONL → replies `🥤 logged: …`. Restarted, verified up. Hold-mic in the bot chat = instant capture, zero phone setup.
- **KEY ARCH FACT**: a Telegram BOT cannot ingest its own `sendDocument` (that's bot→user, not an incoming update). So fully-automatic gesture capture CANNOT route through the bot via Bot API. Resolution: **transport ≠ surface** — Drive carries the gesture file (reliable, durable), Telegram is the interactive surface + manual capture + confirmations. watch.ps1 DMs the summary to the bot after ingesting a Drive drop.
- **DECISIONS**: gesture = **Quick Tap (back double-tap)** (Vol-Down can't screen-off w/o root); transport = Drive for auto-gesture + Telegram as surface. Quick Tap fires one action → toggle (1st tap rec, 2nd stop+save) logic lives in MacroDroid (state var soda_rec); FolderSync mirrors Hi-Q folder → `From phone/sodaos`.
- **insights.py BUILT + tested** (pure Python stdlib, NO LLM, NO deps): JSONL → wide daily table → same-day + lag-1 **Spearman** for each controllable-INPUT→wellbeing-OUTCOME pair → plain-English sentences with caveat. Inputs=food tags/caffeine/drinks/sleep/activity; outcomes=energy/mood valence+arousal/symptoms. Synthetic 14-day test nailed planted pattern (fried→lower energy r=-0.70). Real data correctly says "not enough history" (need ~14 days). Run: `python ~/.claude/sodaos/insights.py [--min-days N --min-r X --json]`.

## BUILT round 3 (2026-06-16) — config-mutable engine + DEDICATED bot
- **Correlation engine now config-driven**: structure (outcomes, thresholds, lags, tag_groups, inputs_extra/exclude, labels) lives in `~/.claude/sodaos/insights.config.json`; insights.py reads it, code stays fixed/deterministic. Added `--recap` (quick structure print). User wanted ability to change the "too deterministic" structure ON THE GO, governed by approval + a recap each time, lean.
- **`/tune` governance flow** (in the bot): user describes change in plain words → `claude -p` (tune-prompt.md) proposes {recap, change_summary, new_config} → bot shows recap+diff → `/yes` applies (backs up old to config.history/, bumps version, appends changelog), `/no` discards. VERIFIED via Node path: "group fried+greasy as high_fat, require 10 days" → correct new_config v2. (PowerShell arg-passing mangles multiline; bot uses spawn args array = clean.)
- **DEDICATED sodaos-bot** (`~/.claude/sodaos/bot.js`, own chat, SEPARATE from tg-bridge per user req): voice/audio → ingest; plain text → ingest --text; `/insights` `/recap` `/tune` `/yes` `/no` `/id` `/help`. Zero-dep. start.ps1/stop.ps1, env at `~/.env/sodaos-bot.env` (NEEDS NEW BOTFATHER TOKEN from user). 
- **DECOUPLED tg-bridge**: reverted the voice-handling I'd added to tg-bridge bot.js; @Soda2402_bot is back to general assistant only. sodaOS capture now lives ONLY in the dedicated bot.
- watch.ps1 Drive path still valid as the gesture transport (DMs summary to whichever bot token is in tg-bridge env — NOTE: may want to repoint watch.ps1's notify to sodaos-bot token once created).

## BUILT round 4 (2026-06-16) — traceability + (next) self-auditor
- **TRACEABILITY (built+tested)**: every capture now replies with the full PARSED BREAKDOWN (summary + one bullet per event showing tags/values), so the user sees HOW a note was recorded (e.g. "fried greasy lunch [fried, high-fat, heavy]"). `/last [n]` re-shows the last n captures as RAW transcript -> PARSED events. New files: `format.js` (shared ASCII-safe formatter, no em-dash/•/… to survive all pipes), `review.js` (powers /last). ingest.js now prints breakdown via format.js; bot sends full output; watch.ps1 DMs full breakdown.
- **DESIGN PIVOT on structure-tuning (user feedback)**: user does NOT want to manually drive /tune or hold the structure in their head. Instead sodaOS should SELF-AUDIT how they log + the data and PROACTIVELY OFFER concrete, evidence-backed structure changes (synonym tags to group, sparse features to drop, sub-threshold correlations, journal-only dimensions like "stress" not yet tracked). User approves via compact batch reply (1 yes, 3 no). Cadence chosen = BOTH (weekly push + appended to /insights), plus /audit on demand. /tune stays as manual escape hatch. ENGINE math stays fixed/deterministic; only structure config changes, on approval.
- **CAPTURE I/O model (clarified w/ user)**: the OUTPUT they want = the chatbot's response = the parsed breakdown. Two input paths, both reply with breakdown in-chat: (1) MANUAL = hold mic in the bot chat (file goes straight to bot, bot replies) — purest input->response, works once bot live; (2) GESTURE = Quick Tap records -> file to Drive -> watcher ingests -> bot DMs the breakdown (no "check Drive" ping needed; watcher detects the file by polling). Do NOT send a text saying "check Drive"; unnecessary.

## TODO NEXT (immediate)
Build the SELF-AUDITOR: `audit.py` (deterministic signals: tag freq/synonyms, sparse features, sub-threshold corrs, journal vocab) -> `claude -p` (audit-prompt.md) -> short batch of proposals -> bot `/audit` + append-to-/insights + weekly self-push (bot tracks last_push timestamp in a file, no scheduler) -> batch-approve applies via tune machinery (backup+version+changelog). Then (a) n-of-1 experiment runner.

## PHONE SETUP — option 2 gesture (verified recipe 2026-06-16, IN PROGRESS w/ user)
Stack (no root): **MacroDroid** (record toggle) + **Autosync for Google Drive** (instant upload) + **Tap,Tap** FOSS (back-tap → macro, since Quick Tap can only "Open app" not a specific macro).
- MacroDroid: action **Record Microphone → "record until cancelled"**; stop via **Cancel Recording**. Saves to `/sdcard/MacroDroid/Recordings` (.wav, no path var returned). Toggle macro: trigger **Shortcut Launched**; Set Variable boolean `recording` INVERT; If true→Record until cancelled, Else→Cancel Recording + Wait 2s.
- No native Drive upload in MacroDroid (confirmed). **Autosync** (MetaCtrl, v7.2.8+): folder pair Local=`MacroDroid/Recordings` Remote=Drive `From phone/sodaos`, **Upload only + Instant upload** on that pair. MUST auth to the **cdtm Google account** (the one Drive Desktop syncs to `G:\My Drive\` on laptop), NOT necessarily the phone's primary account — #1 likely failure point.
- Quick Tap: Settings>System>Gestures>Quick Tap = "Open app" only. For true back-tap→macro use **Tap,Tap** targeting the macro's home-screen shortcut. Quick Tap reliability improved Android 16 QPR2 / Dec 2025.
- Fallback if native recorder flaky: **Hi-Q MP3** broadcast `yuku.mp3recorder.action.TOGGLE_RECORD` pkg `com.hiqrecorder.free` (one Send Intent Broadcast, no var/If needed); point Autosync at Hi-Q's folder.
- Gotchas: Battery=**Unrestricted** for MacroDroid+Autosync(+Hi-Q); Mic permission Allow; Android14+ ok because gesture brings macro to foreground (FGS mic allowed from user action). Screen-off recording works once started from the gesture.

## PHONE SETUP PROGRESS (2026-06-18/19)
- Recorder DECIDED = **MacroDroid NATIVE Record Microphone** (NOT Hi-Q). Hi-Q via TOGGLE_RECORD intent FAILED because swiping Hi-Q from recents → Android "stopped state" → broadcast not delivered. MacroDroid is always-alive (runs the gesture) so native recording has no closed-app failure. Records **`.3gp`** (compressed, tiny) to `/storage/emulated/0/MacroDroid/Recordings`.
- **MacroDroid has NO "Else"** (user confirmed twice). Toggle macro uses TWO If blocks, no Else: `Set var recording=INVERT` → `If recording=true → Record Microphone (until cancelled)` / `If recording=false → Cancel Recording`. WORKS + toggles.
- Added `.3gp/.3gpp/.amr` to MEDIA exts in transcribe.py, ingest.js, watch.ps1, bot.js (2026-06-18). Still need to VERIFY a real .3gp transcribes via faster-whisper/ffmpeg when first file lands.
- Sync app = **Autosync for Google Drive / "DriveSync"** (com.ttxapps.drivesync, MetaCtrl). Folder pair: local `MacroDroid/Recordings` → remote `From phone/sodaos`, Upload only. Battery=Unrestricted set.
- **Near-live sync FACTS (verified 2026-06-19)**: real-time = **"Instant upload"** toggle that lives INSIDE the folder-pair config (NOT the global "Autosync schedule" which is just a 15min-min fallback timer). Instant upload is FREE (event-driven FileObserver), but "best-effort" and MetaCtrl docs say it's flaky for NON-photo files (our .3gp audio) → may fall back to the 15-min sweep. Free tier = 1 folder pair, files ≤10MB (3gp fine). Pro one-time ~$6-8 (more pairs/bigger files, NOT needed). **If audio instant-upload proves laggy → switch to Syncthing-Fork phone→laptop direct (true real-time, skips Drive, watcher reads it directly).**
- Phone is **minimalist launcher** (Olauncher-style, no home-screen widgets). Gesture (Rung C) = Tap,Tap back-tap OR MacroDroid Quick Settings tile (both launcher-independent). NOT YET DONE.

## ARCHIVE / OFFLINE-RESILIENT FLOW (built + verified 2026-06-19)
User's design: MacroDroid macro on stop = Cancel Recording + **Move All Files (Documents -> sodaos)**; the **"Delete All Files" step is REMOVED** because the LAPTOP drains the folder. Laptop side (watch.ps1 + ingest.js):
- Watcher polls Drive `From phone/sodaos`, ingests each file, then **moves the ORIGINAL audio to `From phone/SodaOS full view`** (permanent Drive archive of ALL recordings; user has space). This drains `sodaos` (so no Delete-All needed) AND keeps history.
- `ingest.js --archive <dir>` (or SODAOS_ARCHIVE env) = archive destination; cross-device-safe (EXDEV copy+unlink) + collision-safe naming. watch.ps1 passes `--archive 'G:\My Drive\From phone\SodaOS full view'`.
- **Recording time comes from the FILENAME** (`parseTsFromName`), NOT mtime — Drive sync rewrites mtime to sync-time. MacroDroid names files `YYYY-MM-DD_HH-MM-SS.3gp`. Verified: "Yoo-hoo!" .3gp logged with ts=13:26:28 (filename) vs ingested_at=13:36 (processing).
- **Offline-resilient**: recordings pile up in `sodaos` while laptop asleep; when laptop wakes + Drive syncs them down, watcher drains+transcribes+archives ex-post.
- watch.ps1 modes: default = always-on loop (15s poll); **`-Once`** = drain all pending then exit (matches "whenever I fire up Flood" model). VERIFIED both.
- `.3gp` transcription via faster-whisper CONFIRMED working (no codec issue). Empty/silent clips handled (skipped for logging, still archived).
- **ALWAYS-ON watcher LIVE (2026-06-19)**: `watch-start.ps1`/`watch-stop.ps1` (PID file `watch.pid`, log `watch.log`) run watch.ps1 backgrounded. Started + verified catching new recordings in real-time (caught "Hey" .3gp live → logged → drained → archived). Reboot persistence: `register-watch-task.ps1` (logon task 'sodaOS-Watcher') — STAGED FOR USER to run (classifier gates Claude from registering tasks); command put on clipboard 2026-06-19.
- watch.ps1 notify now reads `~/.env/sodaos-bot.env` (NOT tg-bridge) so drain summaries go to the sodaOS bot once it exists; until then tg-notify=False (silent), drain+log+archive still work.
- **Watcher now EVENT-DRIVEN (2026-06-19)**: watch.ps1 rewritten to use a .NET FileSystemWatcher (Created+Changed) + Wait-Event, with a 30s fallback poll. VERIFIED FSW fires on the Drive G: virtual drive (test clip processed in <12s, well under fallback). Latency now ~seconds vs old 15s poll. Size-settled gate (2s) kept for Drive placeholder streaming. `Invoke-DrainPass` refactored, reused by -Once. Restart watcher after editing sodaos-bot.env so it loads the token for DM confirmations.
- Scaffolded empty `~/.env/sodaos-bot.env` (token blank) 2026-06-19 — user just pastes BotFather token.
- **Test log WIPED 2026-06-19** (events-2026-06.jsonl + raw/*.txt cleared) for clean slate; user chose always-on (decision 1) + wipe (decision 2). Macro's Delete-All step REMOVED by user. Only entry now = "Hey" test (harmless).

## MIC / AIRPODS (verified 2026-06-19)
MacroDroid Record Microphone CANNOT use AirPods/Bluetooth mic — records phone built-in mic only. MacroDroid has no Set-Audio-Mode/SCO/input-route action; Android needs explicit SCO/communication-mode (which MacroDroid never requests); AirPods-over-HFP on Pixel is mono ~8kHz + buggy (A2DP-offload distortion). Verdict: don't chase AirPods. Pocket = muffled if deep trouser pocket → use chest/shirt pocket mic-out or phone in hand (Whisper handles normal phone-mic fine). For true close-mic hands-free later: non-Apple buds/wired mic + a recorder app with a "Bluetooth mic" toggle (SCO), launched by MacroDroid. NOTE: chosen trigger = Volume Button Long Press (Vol-Down + "don't change volume"), but volume triggers are SCREEN-ON only no-root — so "deep pocket + screen off + AirPods" works on zero axes; realistic capture = phone in hand/chest pocket, screen on.

## VERIFICATION LADDER (do in order, test each before next)
- A1 transport: Autosync a manually-placed test file → confirm it lands at `G:\My Drive\From phone\sodaos\` (proves account+sync). [Claude verifies laptop side.]
- A2 record: MacroDroid macro run (manual) → .wav lands in Drive → laptop. 
- B ingest: run `watch.ps1` → confirm breakdown in its console.
- C gesture: Tap,Tap back-tap → full chain.
- D output: create sodaos-bot → repoint watch.ps1 notify to sodaos-bot token → DM breakdown.

## LOG DELETE/MODIFY shipped (2026-06-20)
Bot can now fix wrongly-recorded logs. `review.js --json N` outputs an index->capture map; bot `/last [n]` shows numbered captures (raw->parsed) AND stores `last-shown.json`; `/del <n>` (or /delete) maps the number to its capture's `raw` and calls `delete.js --raw <raw>`. **`delete.js`** = tombstone soft-delete: removes matching events from `events-*.jsonl`, moves them (with `deleted_at`) to `~/sodaos/data/_deleted.jsonl` (recoverable; invisible to insights/review/audit which only read events-*). Tested in temp dir: delete by raw removes the capture, keeps others, tombstones the removed. Bot restarted to load it. (Edit-a-field not built yet — for now "delete + re-log" covers the wrongly-recorded case.)

## BOT TOKEN MAP (canonical, 2026-06-20) — 3 distinct bots, no conflicts
- **@SodaOS_bot** (token `8666136391:…`) = sodaos LIFE-LOG bot (`~/.claude/sodaos/`, sodaos-bot.env). chat 5362797891.
- **@sodanotif_bot** (token `8827899111:…`) = notifications (`~/.claude/sodanotif/`, sodanotif.env).
- **@Soda2402_bot "Claudio Codice"** (token `8996229117:…`) = tg-bridge Claude-on-phone (`~/.claude/tg-bridge/`, tg-bridge.env). RESTORED to its own token 2026-06-20 after the collision.
- (stray dup `@TG_CC_Sodabot` token `8994310734:…` = abandoned, ignore.)
THE 409 was tg-bridge.env wrongly holding the @SodaOS_bot token. FIX = put tg-bridge back on @Soda2402_bot's own token. To find a bot's token later: getMe per token; tokens recoverable from session transcripts via grep `[0-9]{9,10}:AA...`.

## 409 (2026-06-20) — tg-bridge had been mis-tokened, NOW REVIVED on its own token
Three layers kept tg-bridge resurrecting on the @SodaOS_bot token: (1) `TG-Bridge-Autostart` scheduled task, (2) `tg-bridge/keep-awake.ps1` watcher that re-runs start.ps1 (spawns bot + a NEW keep-awake = self-perpetuating, defeats PID-killing), (3) tg-bridge.env held the @SodaOS_bot token. DEFINITIVE FIX applied: (a) disabled TG-Bridge-Autostart task, (b) **renamed keep-awake.ps1 → keep-awake.ps1.retired** so the respawn loop can't recreate itself, (c) **blanked TELEGRAM_BOT_TOKEN in tg-bridge.env** (commented, with revive note), (d) killed all tg-bridge procs. tg-bridge is now permanently down + can't conflict even if launched. To REVIVE tg-bridge later: rename keep-awake back, set tg-bridge.env token to @Soda2402_bot's own token (from BotFather, NOT the SodaOS one), re-enable task. @SodaOS_bot = life-log's bot (unchanged, correct).

## 409 ROOT CAUSE (earlier diagnosis 2026-06-20)
The persistent getUpdates 409 on @SodaOS_bot was NOT sodanotif (that's a separate notifications bot @sodanotif_bot on token 88278991, no conflict — earlier blame was WRONG). Real cause: **`tg-bridge.env` had been re-pointed to the @SodaOS_bot token (86661363) — SAME as `sodaos-bot.env`** — so the old "Claude Code" phone bot (tg-bridge) and the sodaOS life-log bot were both long-polling the same token, terminating each other (continuous 409 when sodaos ran; token mostly free when it didn't). Verified via getMe: BOTH tg-bridge.env and sodaos-bot.env resolve to @SodaOS_bot. FIX: stopped tg-bridge (PID killed) → sodaos bot polls clean. **CAVEAT: `TG-Bridge-Autostart` scheduled task (State Ready) will relaunch tg-bridge at next logon → 409 returns** unless retired OR tg-bridge given its own token. User called tg-bridge "the very first bot, not working anymore" (defunct). DECISION PENDING: retire tg-bridge (disable TG-Bridge-Autostart) vs give it its own token (note: user recently added image→Screenshots forwarding to tg-bridge/bot.js). Debug method for future: `getMe` per env token maps token→bot; sample telegram conns with IP filter 149.154.* AND 91.108.* (149-only missed bots).

## SODAOS BOT LIVE (2026-06-19)
- **@SodaOS_bot** created + running (PID via start.ps1), token in `~/.env/sodaos-bot.env`, `ALLOWED_CHAT_ID=5362797891` (same chat_id as tg-bridge — same Telegram user, ids are per-user not per-bot, so no bootstrap needed). Sent a test ping (API ok=True).
- Watcher restarted → **tg-notify: True**: after every drain it DMs the parsed breakdown to the SodaOS chat (= user's "confirm what's logged"). Bot also does in-chat capture (voice/text) + /last /insights /recap /tune /yes /no /help.
- **Persistence STAGED**: `register-tasks.ps1` registers BOTH 'sodaOS-Bot' + 'sodaOS-Watcher' at logon; command on clipboard for USER to run once (Claude gated from task registration). Supersedes register-watch-task.ps1.
- NEXT BUILD: the **auditor** (/audit + proactive structure suggestions, both cadence). Then optional one-tap **gesture** (Tap,Tap/QS tile) so user doesn't open MacroDroid to fire the macro.

## PENDING USER STEP
Create the new bot: @BotFather /newbot ("sodaOS", username ...bot) → paste token into `~/.env/sodaos-bot.env` → run `~/.claude/sodaos/start.ps1` → message it → paste chat_id into ALLOWED_CHAT_ID → restart. Then test voice + /insights + /recap + /tune.

## Status
Capture + config-mutable correlation engine + governed /tune + dedicated bot ALL BUILT & tested (2026-06-16). NEXT (user chose): **(a) n-of-1 experiment runner** (QuantifyMe: baseline→manipulate→adherence gate→score). (b) emotional-awareness reflection layer = nice-to-have, my discretion later. Phone gesture = user sets up (Quick Tap→MacroDroid→Hi-Q→FolderSync→Drive).

## BUILT round 5 (2026-07-13) — content-based ROUTER (the same phone shortcut now fans out beyond sodaOS)
User wanted the EXISTING gesture/bot capture pipeline (not a manually-invoked skill) to also
recognize when a recording isn't a personal wellbeing log, and route it elsewhere automatically.
- **New routing step in `ingest.js`**, runs BEFORE sodaOS structuring: `classifyDestination()`
  calls `claude -p` with a new `route-prompt.md` on the raw transcript, returns
  `{destination, confidence, reason, title, flag_notion_lead}`.
- **Destinations:** `sodaos` (default — food/mood/energy/journal, unchanged pipeline) ·
  `vault_kb` (personal note/idea, not wellbeing, not Tundra) · `medtech-brain` (Tundra business —
  discussing with Caleb, hospital/competitor/customer mentions, strategy/fundraising).
  `flag_notion_lead` (bool, only under medtech-brain) marks a potential-client mention.
- **Confidence gates whether it asks first:** `"explicit"` (speaker states what it's for, or
  content is unambiguous) → writes directly to `<vault>/Raw/` with NO confirmation.
  `"inferred"` (topical guess only) → writes NOTHING yet; saves
  `~/sodaos/_pending/route-pending.json` and prints a `CONFIRM: ...` line instead. Genuinely
  unsure → the prompt is instructed to default to `sodaos` rather than force a guess.
- **Confirmation surfaces in the sodaOS Telegram bot** (both paths): `watch.ps1`'s
  `Send-TgSummary` detects the `CONFIRM:` prefix and formats it as a question (❓) instead of the
  normal 🥤 log-confirmation; `bot.js`'s `captureMedia`/`captureText` do the same for in-chat
  captures. The user's reply (yes/no, or "tundra"/"personal"/"sodaos" to pick directly) is caught
  by `bot.js`'s `matchRouteReply()`/`resolvePendingRoute()` — checked BEFORE audit-selection and
  the command switch in `handleUpdate` — which calls `node ingest.js --finalize-route <dest>` to
  either append the sodaOS journal entry (the "no" / safe-default path) or write the vault Raw
  note (the "yes"/correction path), then deletes the pending file. Single pending slot (a second
  ambiguous capture before the first is resolved overwrites it) — acceptable v1 limitation.
- **Vault Raw notes** get a light header (`Audio note (via sodaOS)` + raw txt filename + why it
  was routed there) and, when `flag_notion_lead`, a `⚠️ NOTION-FLAG` callout — the actual Notion
  write is explicitly NOT automated (the headless bot/ingest process has no MCP/Notion access,
  `claude -p` calls here run with `--strict-mcp-config`); it's left for the next live Claude Code
  session to review and add, per [[feedback_notion_write_needs_approval]].
- **Gotcha hit + fixed:** `watch.ps1`'s Telegram formatting used `[char]0x1F964` for 🥤 — that
  code point is outside the BMP (needs a UTF-16 surrogate pair), so `[char]` silently fails
  ("Cannot convert value ... to type System.Char"). Fixed with
  `[System.Char]::ConvertFromUtf32(0x1F964)`. Caught via a live queued recording that logged
  correctly (JSONL append succeeded) but failed to DM — data was never lost, only the
  notification; verified the fix against the real Telegram API afterward.
- **Tested end-to-end** (2026-07-13): explicit sodaos / explicit medtech-brain / explicit
  vault_kb all write correctly and skip the wrong pipeline; the pending-file + `--finalize-route`
  mechanism verified for both the sodaos-fallback and vault-write resolution paths; one real
  queued phone recording correctly auto-classified as sodaos (personal/emotional content) and
  logged 5 mood events + a journal line. Both `sodaos-bot` and `sodaos-watch` restarted via their
  existing `start.ps1`/`watch-start.ps1` to load the new code (their PIDs were already stale at
  restart time, unrelated to this change).
- Every destination/use-case above is meant to be **speakable** — the user steers routing by
  what they say in the recording itself (e.g. "this is about Tundra", "note to self", "this is a
  follow-up to my call with Caleb about X"), not by invoking a separate skill.

Related: [[reference_audio_to_notes]], [[reference_tg_bridge]], [[project_phone_to_desktop]], [[reference_kb_vault]]
