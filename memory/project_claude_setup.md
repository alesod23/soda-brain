---
name: Claude Setup Repo (moto)
description: buildingopen/moto cloned permanently at C:\Users\Alessandro\dev\moto; this is the Claude Code operating environment (hooks, skills, CLAUDE.md, memory). Old claude-setup is at dev\claude-setup (superseded).
type: project
originSessionId: 1c8ba62b-12c9-4589-8e2f-a3af84687160
---
The canonical Claude Code setup repo is **buildingopen/moto** (formerly claude-setup), permanently cloned at `C:\Users\Alessandro\dev\moto`.

To update: `cd C:\Users\Alessandro\dev\moto && git pull`, then re-run `./install.sh --copy` in Git Bash.

Old clone at `C:\Users\Alessandro\dev\claude-setup` is superseded — moto is the renamed continuation.

Volatile clone at `C:\Users\Alessandro\AppData\Local\Temp\claude-setup` can be ignored.

**Why:** User does not want to re-clone every session; `dev\moto` is the permanent home.

**How to apply:** If setup appears missing or broken, `cd C:\Users\Alessandro\dev\moto` and re-run `./install.sh --copy` in Git Bash without asking the user to explain anything.

**Windows-specific install notes (analyzed 2026-04-27):**
- Always use `./install.sh --copy` (not default symlinks — Windows symlinks need admin/dev mode)
- Run in Git Bash, not PowerShell
- After install, remove two Mac-only hooks from `~/.claude/settings.json`: `block-terminal-minimize.sh` and `rate-limit-auto-resume.sh`
- Comet browser (Chromium) works fine — no local Chrome paths in core `claude/` layer
- Skip `mac/` and `server/` directories entirely — Mac/Linux only
