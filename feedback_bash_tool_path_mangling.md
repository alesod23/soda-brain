---
name: bash-tool-path-mangling
description: "Bash tool on Windows routes through Git Bash/MSYS, which mangles backslash Windows paths. Always use PowerShell tool for node/python/.cmd invocations on C:\\ paths."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d7cda427-75d2-40b5-93f1-2e4a03c2422b
---

**Never use the Bash tool to invoke a Windows executable with a `C:\...` backslash path.** Git Bash's MSYS layer rewrites the path, dropping the colon and merging segments:

```
node C:\Users\Alessandro\triage\fetch-all.js
# → node "C:\Users\Alessandro\UsersAlessandrotriagefetch-all.js"
# → Error: Cannot find module ...
```

**Why:** MSYS treats `\U` as an escape sequence in some contexts and strips it; the leading `C:\` segment gets duplicated/munged. The mangle is silent — the command runs, then node throws `MODULE_NOT_FOUND`. Verified 2026-05-22 in /triage: `node C:\Users\Alessandro\triage\fetch-all.js` failed via Bash, succeeded via PowerShell with the identical command string.

**How to apply:**
- Default to the PowerShell tool for any `node <C:\path>`, `python.exe <C:\path>`, `<C:\path>.cmd`, or similar Windows-path invocation.
- Bash tool is fine for shell-builtin operations (`date`, `echo`-like ops, POSIX scripts with forward-slash paths) but NOT for launching Windows executables with backslash paths.
- If you must use Bash for some reason, convert paths to forward slashes (`/c/Users/Alessandro/...`) — but PowerShell is cleaner.
- This applies across ALL skills, not just /triage. Anywhere the codebase or a SKILL.md says "run `node C:\...`", route via PowerShell.
- Affected skills already patched: /triage step 1+2 (2026-05-22).
