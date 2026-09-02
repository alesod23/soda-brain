---
name: reference_mpd_granola_folder
description: "The shared \"MPD\" Granola folder Alessandro uploads calls to, how to read it, the URL-suffix gotcha, and the MPD-specific /granola rules (no Notion, no auto-to-do). Use when processing MPD/BMW/AllUnderground/Aura call notes or when asked to check/poll the MPD Granola folder."
metadata: 
  node_type: memory
  type: reference
  originSessionId: c5cdecf5-f93d-4cd5-963a-c4aeb69de6f3
---

# MPD Granola folder + processing rules

**The folder:** Alessandro's shared Granola folder **"MPD"** ("anything related to mpd, our pilot allunderground, or bmw partners") — he uploads relevant MPD/BMW/AllUnderground calls here.
Folder link (updated 2026-07-11, supersedes the old one below): `https://notes.granola.ai/t/40c4939a-c971-46ed-b78d-34a41e47dc1d`
Old link (may be stale/rotated — verify before use): `https://notes.granola.ai/t/a9bebcb3-8769-4729-8098-882bc8725b62`

**How to read it (interim, until a paid Granola MCP):** fetch with web-fetch-pw — `node ~/.claude/web-fetch-pw/fetch.js "<url>" 9000`. The folder link renders a **list of notes** (title + author + date) client-side; a single note renders its full enhanced-note text.

**URL GOTCHA (important):** a single note's real URL needs the **trailing suffix after the UUID**, e.g. `/t/<uuid>-00c40a7t`. The **bare UUID** (`/t/<uuid>` with no suffix) returns Granola's generic marketing/demo page, NOT the note. Always use the full link Alessandro pastes.

**MPD-specific /granola rules (per Alessandro, 2026-07-06; DESTINATION CHANGED 2026-07-11):**
- **Drop-to-Raw only** — as of 2026-07-11 this goes into **`C:\Users\Alessandro\mpd-kb\Raw\`** (`MM-DD <Title>.md`), NOT `~/vault_kb/Raw/` anymore. MPD content was split out of vault_kb into its own standalone vault `mpd-kb` (see [[reference_kb_systems]]) because the course ends ~2026-07-18 and its ~90-interview corpus was polluting the personal wiki. `mpd-kb` is Raw-only/contract-pending as of the split — check whether Alessandro has activated it (a `CLAUDE.md` with `kb-engine config` present) before assuming `/kb-ingest` can run there.
- **NO Notion page** for MPD calls (Notion is only the Lobbly customer-discovery flow).
- **NO auto-generated to-dos/reminders** by default — he tracks MPD next-actions himself in task-land `project: mpd`. (Still transcribe the call's "Next steps" as text in the Raw note.)

**MPD used to be mapped inside vault_kb; as of 2026-07-11 the full detail lives in `mpd-kb`.** vault_kb keeps only a thin `Projects/mpd.md` pointer + `MPD:STATE` block (bridged from mpd-kb's own future `/kb-maintain`) — `Orgs/allunderground.md`, `People/leander.md`, `Projects/{mpd-report-outline,marc-bmw-asks}.md`, and the ~16 MPD Sources all moved to `mpd-kb/Raw/` (flat, pending re-ingest there). `Orgs/bmw.md` was split: the Lobbly-relevant half (BMW IP team, Aumovio demo) stayed in vault_kb, the MPD-relevant half moved to `mpd-kb/Raw/bmw-mpd-context.md`. `Projects/aura.md` and the Topics it fed (`industrial-data-as-product`, `tacit-knowledge`, `go-to-market`, `becoming-technical`) stayed in vault_kb since Lobbly still needs them.

**Auto-poll:** feasible to build a watcher that fetches the folder link, extracts new note URLs, and auto-drops each to Raw in MPD-mode — but needs an href-extractor (the text render strips per-note links) + a processed-state file + a scheduled task. Not built yet (pending Alessandro's go). Caveat: it only sees notes actually shared into the "MPD" folder.
