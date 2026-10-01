---
name: feedback_git_commit_message_file_on_powershell
description: "On PowerShell, write multi-line git commit messages to a file and use `git commit -F`, never `-m` with a here-string"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a05a078c-bda8-4aa3-8e63-a38b0d08b6a2
  modified: 2026-08-10T00:25:20.075Z
---

On this Windows/PowerShell 5.1 box, `git commit -m @'...'@` breaks whenever the message contains a double quote: PowerShell wraps the argument in double quotes, the embedded ones terminate it early, and git parses the remainder as pathspecs. The failure looks nothing like a quoting bug — it surfaces as `fatal: /: '/' is outside repository`.

**Why:** it cost two failed commits before the cause was obvious, and the error message points at the wrong thing entirely.

**How to apply:** write the message with the Write tool to a file in the scratchpad, then `git commit -F <path>`. Works for every message regardless of quotes, apostrophes, or arrows. Same fix applies to `gh pr create --body-file` over `--body`.

Related: [[project_tundrapage_repo]], [[feedback_ps1_ascii_only_no_unicode_dashes]].
