---
name: reference_phone_recordings_on_box
description: Where his phone recordings and their transcripts actually are on the VPS, and the three traps that made the 2026-09-14 "find the clinical-engineer recording" hunt take 4 minutes of agent time
metadata:
  node_type: memory
  type: reference
---

Learned 2026-09-14 hunting the Augusto Pavan (ing. clinico, Ospedale Cardinale Massaia, Asti)
recording for the MEDICON briefing.

**Where audio lives on the box**
- `/home/da/gdrive/From phone/` (CDTM My Drive, rclone FUSE): phone voice recordings as `.m4a`
  / MP4-audio, e.g. `Jul 1 at 4-55 PM.m4a`, `Audio from Alessandro S`. Processed ones move to
  `_processed/` with a sibling `*.transcript.txt`.
- `/home/da/gdrive/From phone/sodaos/*.3gp`: voice-lane recordings; transcripts in
  `/home/da/voice-lane/transcripts/`, state `/home/da/voice-lane/state.json`. The lane started
  2026-08-21: anything older there was never transcribed.
- `/home/da/gdrive/From phone/Phone calls/<date>/*.mp4`: call recordings, but the 2026-09-01
  ones are 0 bytes on Drive too (failed uploads).
- Telegram voice notes: `/home/da/.claude/channels/telegram/inbox/*.oga`.

**Traps**
1. **Name collisions are invisible on the FUSE mount.** Several files are literally named
   `Audio from Alessandro S`; `ls` shows one. Use `rclone lsl "cdtm:From phone"` to see all of
   them with sizes and dates (2026-08-11 has two, IDs `1uvY6VIEeB0mucHorH8xLQnf2_L1yyVSN`,
   `12rJm-o-4j8gPFOJ6Ip_ppIUZua6oT_cP`).
2. **The WhatsApp store starts 2026-08-23** (`/home/da/wa-daemon/message-store.jsonl`). Any
   conversation before that is not there; do not conclude "no meeting happened".
3. **No transcript = not in any vault.** `grep -ril pavan` across vault_kb and medtech-brain hit
   only `_system/DECK-SOURCES.md`. Deck of 2026-07-22 cites the Pavan conversation as a source,
   so it happened before 07-06 (relance task) and was never captured.

**How to transcribe here:** `/home/da/voice-lane/venv/bin/python` + `faster_whisper`
`WhisperModel('small', device='cpu', compute_type='int8')` (the only cached model); ~1.4x
real time on this CPU (68 s audio = 98 s). Run long ones detached with nohup and watch a log;
never foreground.

Related: [[reference_audio_to_notes]], [[reference_voice_longform_lane]], [[reference_wa_web_scrape]].
