---
name: project_phone_to_desktop
description: "Phone→desktop capture + interactive Claude-on-phone — Happy is a dead end; canonical drop folder = Google Drive \"From phone\" (cdtm acct, via Drive MCP); audio-to-notes repoint pending"
metadata: 
  node_type: memory
  type: project
  originSessionId: 668acb3f-a008-4138-ab8f-33f25fe5852a
---

Goal (from 2026-06-04): let Alessandro (a) dump thoughts / view today's tasks / ask Claude from his phone on the go, and (b) capture files/photos/audio/notes from the phone for Claude to process.

## Status & decisions (as of 2026-06-07)
- **Happy Coder = DEAD END.** Spent a long session wiring it (npm `happy`/`happy-coder`, runs the real `claude` binary, subscription OAuth, hosted relay, scoped-allowlist perms chosen). Pairing fails: tapping **Accept Connection** → **"Failed to connect terminal"** on BOTH the mobile app AND the desktop web client (app.happy.engineering, logged in). It's a server/account-side bug in Happy's connect-terminal RPC (matches open issues #1120, #987, #982), unfixable from our machine. Credentials never persist (catch-22: phone connect-terminal needs the desktop daemon; `happy daemon` won't start without creds; creds only save on a successful connect). Revisit only if Happy ships a fix. **Fully uninstalled 2026-06-07 per user** (`npm uninstall -g happy happy-coder`, `~/.happy` removed, workplan deleted) — going with the Telegram bridge instead. Side-fix kept: stripped a UTF-8 BOM from `~/.claude/settings.json` (was breaking Happy's settings read; Node tolerated it).
- **Custom Telegram bridge EXISTS + verified** at `~/.claude/tg-bridge/` (see [[reference_tg_bridge]]) — the working fallback for INTERACTIVE dump/ask/view-tasks from phone. Tradeoff: Telegram not E2E. **LIVE 2026-06-07** as @Soda2402_bot, locked to chat 5362797891 — solves need (a). Token in `~/.env/tg-bridge.env`; autostart task pending manual user registration.

## CANONICAL SOURCE (decided 2026-06-07): Google Drive "From phone" — LOCAL via Drive Desktop
The phone→desktop **drop folder** is the Google Drive folder **"From phone"** in **alessandro.sodano@cdtm.com** (folder id `1rZwdy0SZeBM78xE4P0xI8mDklX84kCtU`). This REPLACES the never-created OneDrive `(from phone)\` plan. Single drop zone for everything from the phone (photos, files, notes, audio).
- **Access = LOCAL PATH `G:\My Drive\From phone\`.** User installed **Google Drive for Desktop** 2026-06-07, so the folder syncs to disk and behaves like any local folder — read/move with normal file tools, NO MCP needed. (Earlier "MCP-only" assumption is obsolete — Drive Desktop wasn't installed at first, now it is.) The Drive MCP still works as a fallback to list/pull (`search_files parentId=…` + `download_file_content`), but MCP downloads of large binaries (e.g. a 14.7 MB m4a) are unreliable: session expired twice on 2026-06-07, and base64-inline is huge. Prefer the local `G:` path.
- Moves within the folder (e.g. to `_processed\`) sync back to the cloud.

## DONE / remaining
- **DONE 2026-06-07:** `/audio-to-notes` repointed from `Audio Notes\` to `G:\My Drive\From phone\` (drop + archive `…\From phone\_processed\`); skill at `~/.claude/commands/audio-to-notes/SKILL.md`. First real run transcribed `Jun 7 at 7-00 PM.m4a` (a Lobbly demo-call rehearsal) → guide in `vault_kb/Raw/`.
- **Remaining:** old `Audio Notes\` folder still exists with its own `_processed\`; not deleted (had prior content — migrate/confirm before removing). [[feedback_wa_web_for_media]] updated: "From phone" (local `G:`) is now PRIMARY for phone media; WA-Web scrape is last-resort.
5. **Langfuse diagnosis** of why this session was so slow: the Langfuse MCP was NOT loaded this session (only the `langfuse_hook.py` Stop-hook posts traces); needs a Claude Code restart to expose MCP tools. User wants the inefficiency diagnosed.

## WA media note
The wa-daemon store keeps only `text:"[image]"`, no media bytes/keys — can't download media via the daemon. Today's screenshots were retrieved via `~/.claude/wa-web-scrape/grab-me-images.js` (open Me chat in the logged-in WA Web Playwright profile, real click on the title, scroll, fetch blob <img> → base64 → disk). Slow (~3 min). The Google Drive "From phone" folder (via Drive MCP) will replace this.
