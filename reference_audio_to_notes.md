---
name: reference_audio_to_notes
description: "/audio-to-notes skill — phone recording (mp4/m4a) → local faster-whisper transcript → AI summary into a KB vault's Raw/ → opens in Obsidian."
metadata: 
  node_type: memory
  type: reference
  originSessionId: c107453c-d700-4bae-a46c-4e78d87eb349
---

`/audio-to-notes` (skill at `~/.claude/commands/audio-to-notes/SKILL.md`) turns a phone-recorded chat into a KB Raw note.

- **Drop folder:** `G:\My Drive\From phone\` (Google Drive "From phone", synced by Drive for Desktop — canonical phone→desktop drop, per [[project_phone_to_desktop]]). Processed files + a `.transcript.txt` sidecar archive to `…\From phone\_processed\`. (Corrected 2026-07-13 — an older OneDrive "Audio Notes" path was stale.)
- **Transcriber:** `~/.claude/audio-notes/transcribe.py` — faster-whisper `small`, CPU/int8, decodes mp4/m4a/mp3/wav directly via PyAV (NO ffmpeg binary, NO API key). `--latest <folder>` picks newest unprocessed; or pass an explicit file. Prints JSON `{source,language,duration_sec,transcript}` to stdout, progress to stderr. faster-whisper 1.2.1 + av 17.0.1 + ct2 4.7.2 installed; `faster-whisper-small` cached. Verified 2026-06-06 (15s clip → accurate transcript in ~11s incl. model load).
- **Summary** is produced by the AGENT (plan compute, not API keys) — content is **summary-only** (raw transcript NOT in the KB note, only in the archived sidecar).
- **Target vault is now primarily content-driven (set 2026-07-13), not just invocation-driven.** Priority: (1) an explicit vault named when the skill was triggered wins outright; (2) else, if the TRANSCRIPT itself explicitly frames what it's about/a follow-up to, or clearly discusses entities that only exist in one vault (Tundra/hospital content → `medtech-brain`, Lobbly/patent → `vault_kb`, thesis → `thesis-kb`, personal/reflection → `self-reflection-wiki`) — proceed automatically, no need to ask; (3) else, if there's merely a topical signal without an explicit self-reference, **ask for confirmation** before writing rather than silently defaulting; (4) only with zero signal either way, default to `vault_kb`. Also auto-detects follow-up/continuation framing ("part 2", "continuing from...") and names the earlier related Raw file in the new note's header (never edits the earlier file — Raw is immutable). See [[reference_tundra_granola_folder]] for a worked example (the Cliniserve/Julian-call follow-up, 2026-07-13).
- **Drop-to-Raw only** — like [[reference_kb_systems]]/`/granola`, it NEVER ingests. User runs `/kb-ingest` or `/kb-maintain` later.
- **Auto-open:** runs `Start-Process "obsidian://open?vault=<vault>&file=Raw/<EscapeDataString name>"` directly on completion (user explicitly authorized opening, overriding the global never-open rule). Obsidian-registered vaults: `vault_kb`, `self-reflection-wiki`, `task-land`, `medtech-brain`. **`thesis-kb` is NOT registered in Obsidian** → write works, auto-open does not until user adds `~/thesis-kb` as a vault once.
