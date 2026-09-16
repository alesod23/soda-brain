---
name: reference_voice_longform_lane
description: The long-form voice lane — long phone recordings are transcribed out-of-band and PING him; they used to be silently dropped
metadata: 
  node_type: memory
  type: reference
  originSessionId: 8fb3a61a-b367-4d96-bd49-39a3cdbbb356
  modified: 2026-09-16T14:40:52.603Z
---

**⚠️ MOVED TO THE VPS 2026-08-30 — the laptop lane below is RETIRED.** Long-form now runs on da-box:
`task-land/_system/vps/voice-longform-vps.py` via `da-voice.timer` (5 min, systemd, in units.list),
watching the rclone-mounted drop folder `/home/da/gdrive/From phone/sodaos/` for >300s recordings,
laptop-off capable. Laptop schtask **`Voice-Longform` is DISABLED** (do not re-enable — double
processing); the laptop FAST lane `Voice-Lane-Watch` still runs for short clips. Box lane adds:
ffmpeg→WAV pre-convert before faster-whisper (raw long AMR-NB used to transcribe EMPTY — the silent
killer of every long recording), size-based duration fallback (phone .3gp often has NO ffprobe
duration; ~1700 B/s), and the **safe-word protocol** (`_system/vps/safeword-prompt.md`): he marks
spoken instructions inside a recording with OPEN "a butterfly flaps its wings" / CLOSE "ghost cat",
order interchangeable, closer optional, fuzzy + Italian variants; instruction routes/names the note
and is stripped from content. Routes: vault Raw note / Tasks/inbox file / archive-only + ALWAYS a
Telegram report. Transcripts at box `voice-lane/transcripts/`. Whisper hallucinates dots on pure
noise — a near-empty transcript of a pocket recording is legitimate, and the TG report says so.

**The 240-min guard is not enough (2026-09-16).** He forgot to stop a recording: 3.7 h (13,345 s, AMR-NB, 24 MB), landed on the box at 16:31, and only the first 30 min mattered. At 222 min it sat UNDER `MAX_DURATION_MIN = 240`, so the lane would have transcribed all of it (hours of CPU, useless text). Caught by hand: appended the filename to `state["processed"]` in `/home/da/voice-lane/state.json` before the 5-min timer fired, then ran a 30-min job (`ffmpeg -t 1800`, `+6 dB`, faster-whisper `small`, `vad_filter=False`, **`language=None`** to auto-detect) with an out-of-harness notifier posting the txt via Bot API. Open design question for him: for any file over ~45 min, transcribe the first N minutes and ask, instead of all-or-nothing. Same family as the unanswered short-recording A/B/C.

**NEVER force `language=` on a recording you have not sampled (2026-09-15).** Nocco's MEDICON talk
was transcribed with `language='it'` because the event was in Italy and he is Italian: the talk was
in ENGLISH, and faster-whisper `small` dutifully produced 5,000 words of fluent Italian nonsense
("le muuture caratteristiche", "spada di effetti") that read like a bad transcript rather than a
wrong-language one. Cost: a whole summary and a Telegram pitch built on invented content, then a
re-run. Re-run with `language='en'` gave 8,034 words and the real argument, including his actual
bottleneck (data entry + standardisation) which the Italian pass had lost entirely. Rule: let
whisper auto-detect (it reports `info.language` + probability), or transcribe the first 60 s first
and read it before committing to a language. Only force a language when a sample confirms it.
Conference talks in Italy are routinely in English; the audience language is not the speaker's.
Same run also confirmed: `vad_filter=False` + `+6 dB` is right for noisy halls (see INBIT), and an
out-of-harness `nohup` notifier posting via Bot API `sendDocument` survives harness watcher pruning.

--- retired laptop lane, kept for reference ---

**`C:\Users\Alessandro\.claude\voice-lane\longform.ps1`**, scheduled task **`Voice-Longform`**
(every 5 min + at logon, hidden via `longform-hidden.vbs`). Handles exactly the recordings the fast
lane refuses.

**The bug it fixes (2026-08-05).** `watch-voice.ps1` dropped anything over `$MaxLaneSec` on the
floor: logged `content lane (long recording), untouched`, marked it processed, and never transcribed,
classified, or mentioned it again. His 39.8-minute SSM Health discovery recording from 2026-08-04
sat unseen until he chased it by hand — *"the problem with the recording is that I shouldn't nudge
you. That system should work in such a way where I get physically pinged if I recorded something
that has some type of next steps or some value to it."*

**Flow:** `watch-voice.ps1` now writes `longform\queue\<name>.job` (containing the audio path) instead
of dropping — enqueue only, because transcribing a 40-min file inside that 1-minute tick would stall
it. `longform.ps1` takes ONE job per tick, transcribes via `audio-notes\transcribe.py`
(faster-whisper `small`, CPU, local, no API key), writes `longform\transcripts\<name>.{json,txt}`,
then classifies with `claude -p` into
`{worth_filing, has_next_steps, title, summary, next_steps[], people[], org}`.
- `has_next_steps` + non-empty steps -> **approval-hub card, `notify:true`** (phone + laptop popup).
- else `worth_filing` -> quiet Telegram note via `sodanotif\push.js`.
- else -> log only.

**It never auto-executes anything.** Long recordings are meetings and calls where a misread costs a
real message to a real person; the card proposes, he approves. The classifier prompt is explicitly
conservative ("a missed step he adds himself is cheaper than a fabricated one").

**`-DryRun`** runs transcribe + classify for real but logs the ping instead of firing it. Use it to
test without buzzing his phone. Verified 2026-08-05 on a real 3.7-min recording: transcribed in 93s,
classified `worth_filing=false`, no ping, job moved to `done`, lock released.

**The lock is stale-tolerant on purpose (90 min).** A hung `watch-voice` once held its mutex for FIVE
DAYS and every tick exited silently — never ship a lock here that cannot expire. See
[[feedback_windows_tail_locks_logfile]] for the related "don't touch a live log" rule.

**Corrupt recordings are a real failure mode.** `2026-08-04_09-59-08.3gp` (18.5 MB) is undecodable —
`moov atom not found`, i.e. the 3gp was never finalised, the recorder was still running when Drive
synced it. `ffprobe` reports the error immediately; check that before assuming a transcript is
missing for some subtler reason.

Related: [[reference_voice_lane]] (the fast lane), [[reference_approval_hub]], [[project_sodaos]].

**2026-09-14 incident + guard.** His phone recorded **12.6 h** overnight (`sodaos/2026-09-13_22-21-28.3gp`, 82 MB, recorder left on). `voice-longform-vps.py` tried it at 11:05 and 11:13, whisper `small` ballooned to ~5.9 GB RSS on the 8 GB box, both attempts were OOM-killed (they also killed two of the savior's background shells), and because nothing was written to `state.json` the timer crashlooped every tick. Fixed the same morning: the file was marked `processed` by hand, and the runner got a **`MAX_DURATION_MIN = 240` guard** (skip + log line + mark processed; file untouched on Drive), backup `voice-longform-vps.py.bak-20260914`. If he wants the first minutes of such a file, transcribe a trimmed copy separately. Watch for: `lane.log` showing the same file "processing" twice with no "done" = this failure mode.
