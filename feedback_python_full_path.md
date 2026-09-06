---
name: feedback-python-full-path
description: "RESOLVED 2026-09-07: bare `python` now resolves to the real Python 3.12 in bash, PowerShell and cmd (user PATH puts Python312 before WindowsApps); the enforce-python-fullpath hook was removed. Full path still fine in scripts; never suggest installing Python."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7528a222-3515-4a7e-95d0-39ba429ccc6d
  modified: 2026-09-06T23:56:53.712Z
---

**History.** Until 2026-09 bare `python.exe` / `python3.exe` on this laptop hit the Windows App Execution Alias (Microsoft Store stub), so the Store opened instead of running anything. That produced the rule "always use the full path `C:\Users\Alessandro\AppData\Local\Programs\Python\Python312\python.exe`" and a PreToolUse hook `~/.claude/hooks/enforce-python-fullpath.sh` that blocked the bare word in every Bash/PowerShell command.

**2026-09-07, verified and closed.** The user PATH now lists `...\Python312\Scripts\` and `...\Python312\` FIRST (before `...\Microsoft\WindowsApps`), and `python --version` prints `Python 3.12.10` from `AppData\Local\Programs\Python\Python312\python.exe` in Git Bash, PowerShell 5.1 and cmd. The hook entry was removed from `~/.claude/settings.json` (backup `settings.json.bak-pyhook-*`); the script file stays on disk unused. User asked for this ("so you stop thinking I don't have it").

**How to apply now:** bare `python` / `pip` are fine. Scripts that already carry the full path keep working, no need to rewrite them. Python is installed: never suggest downloading it. If the Store page ever opens again, the user PATH order changed; fix the order, do not reinstate the hook without asking.
