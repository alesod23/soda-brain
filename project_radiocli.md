---
name: project_radiocli
description: RadioCLI — terminal internet-radio player Alessandro asked to build (Node + mpv + radio-browser)
metadata: 
  node_type: memory
  type: project
  originSessionId: 8f531da2-e002-4e2f-9912-14df531d5939
---

RadioCLI: terminal internet-radio player at `C:\Users\Alessandro\radiocli` (Node ESM, one dep `@inquirer/prompts` pinned 8.5.2). Built 2026-07-01 from RadioCLI docs he liked.

Architecture: `src/api.js` (radio-browser.info mirror-resolve + search/top/bycountry), `src/player.js` (finds mpv, runs it with `--input-ipc-server` named pipe `\\.\pipe\radiocli-mpv`, drives pause/volume/stop over IPC), `src/store.js` (favorites in `~/.radiocli/radiocli.json`, `RADIOCLI_HOME` overrides), `src/cli.js` (command mode + interactive menu). Global command via `npm link` (on PATH at `C:\nvm4w\nodejs`).

Playback backend: **mpv** installed via `winget install shinchiro.mpv -h` (silent+interactive; `--disable-interactivity` cancels it) → landed at `C:\Program Files\MPV Player\mpv.exe`. No 7-Zip/scoop on machine; portable-mpv .7z route failed (SF returns HTML, tar can't read 7z).

MVP DONE + verified (doctor, search, silent E2E playback+IPC test all PASS). NOT yet verified: interactive TTY keypress loop (needs real terminal). Roadmap (v2, committed per [[feedback_track_phased_plans]]): tabbed TUI, playlist import/export (.m3u/.pls/.xspf), sleep timer, resume-last, media keys, ffplay/VLC fallback. Workplan: `radiocli\WORKPLAN-20260701-radiocli.md`.
