---
name: feedback-python-full-path
description: "On Windows, always invoke Python via the full path `C:\\Users\\Alessandro\\AppData\\Local\\Programs\\Python\\Python312\\python.exe` (or via the existing `.cmd` shims). Never bare `python.exe` / `python3.exe`."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7528a222-3515-4a7e-95d0-39ba429ccc6d
---

On this machine, bare `python.exe` and `python3.exe` are intercepted by the Windows App Execution Alias for the Microsoft Store. If a script depends on bare `python.exe`, the Store opens instead of running the script — a recurring annoyance the user has flagged multiple times (WA daemon setup, LinkedIn auth debug).

**Rule:** for any Python invocation NOT going through a known `.cmd` shim (gmail.cmd, slack.cmd, linkedin.cmd, etc.), use the full path:

```
C:\Users\Alessandro\AppData\Local\Programs\Python\Python312\python.exe
```

Applies to:
- One-off diagnostics (`python -c "..."`)
- `pip` calls if PATH is uncertain (`python.exe -m pip ...`)
- Scripts the user runs manually that I'm generating

**Why:** Avoids opening the Microsoft Store mid-task and breaking flow. User has explicitly called this out as a recurring miss.

**How to apply:** when about to type `python` or `python.exe` in a Bash/PowerShell command, swap in the full path. Same rule lives implicitly in the `.cmd` shims under `~/.claude/{linkedin,slack,triage}/` and in `gmail.cmd` — those are safe.

**ENFORCED (2026-05-29):** this is no longer advice-only. A `PreToolUse` hook on Bash|PowerShell — `~/.claude/hooks/enforce-python-fullpath.sh`, wired as the first entry in `settings.json` PreToolUse — BLOCKS (exit 2) any bare `python`/`python3`/`pip`/`pip3` command and tells the caller to use the full path. Root cause the user flagged: bare `python` triggers the Windows App Execution Alias → opens the Microsoft Store "Get Python" page, which reads as "trying to reinstall Python" (it installs nothing). Memory alone kept getting missed under momentum across sessions, so it was promoted to a deterministic hook. The hook allows: the full path, `.cmd` shims, `pipenv`, and paths that merely contain "python".

**Known latent bug (NOT fixed — user chose hook-only on 2026-05-29):** `settings.json` Stop hook still runs `python C:/Users/Alessandro/.claude/hooks/langfuse_hook.py` with bare `python`. Same Store-alias risk; left as-is per user.

**User-side parallel fix:** the user can also disable the App Execution Aliases for `python.exe` + `python3.exe` in `Settings → Apps → Advanced app settings → App execution aliases`. After that, bare `python.exe` resolves cleanly. Either fix alone is sufficient; both together is belt-and-suspenders.

Related: [[reference_triage_gmail]], [[reference_wa_sender]].
