---
name: reference-env-files
description: "Canonical location for per-service env/secret files on Alessandro's machine; PS profile auto-loader convention"
metadata: 
  node_type: memory
  type: reference
  originSessionId: ad932466-d0d9-428b-80e8-6ced6f6fb688
---

All secrets/env vars for external services live in **`C:\Users\Alessandro\.env\`** (NOT in OneDrive, so they don't sync). One file per service:

- `langfuse.env` — Langfuse Cloud (LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_BASE_URL, TRACE_TO_LANGFUSE)
- (add new services as their own `.env` file: `openai.env`, `anthropic.env`, etc.)

Every new PowerShell session auto-loads all `*.env` files via:
`C:\Users\Alessandro\OneDrive - HEC Paris\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`

The profile iterates `~/.env/*.env`, parses `KEY=value` lines (`#` comments + quoted values supported), and `Set-Item Env:KEY`. So any CLI that reads env vars (`langfuse`, `openai`, `vercel`, etc.) just works in any fresh terminal.

For scripts that run OUTSIDE a shell (e.g. Claude Code hooks invoked directly by the harness), the script itself must load `~/.env/<service>.env` — don't assume env inheritance. See `~/.claude/hooks/langfuse_hook.py` for the 9-line pattern (read file, partition on `=`, `os.environ.setdefault`).

**Why this matters:** before this convention (2026-05-17), secrets were scattered across `.claude\settings.json#env`, `Downloads\codex_coding_session.txt`, and inline configs — no single place to find/rotate/audit a key. Now: one folder, one file per service.

**When suggesting a new env var:** propose adding it to (or creating) the appropriate `~/.env/<service>.env` file. Never embed secrets in `settings.json#env` or in tracked source.

Related: [[reference_onedrive_path]] (why `.env\` lives outside OneDrive).
