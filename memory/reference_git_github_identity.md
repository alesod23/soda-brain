---
name: reference-git-github-identity
description: "Alessandro's GitHub username + the email to use on public git commits, and how to commit without a global git identity set"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 675a9107-fc6c-4ecc-98c1-d9a341d0d439
  modified: 2026-08-12T18:57:01.299Z
---

For any `git`/`gh` work on this machine:

- **GitHub username:** `alesod23` (repos live at `github.com/alesod23/<name>`).
- **Public commit email:** `alesoda2002@gmail.com`. NOT `primocaleb@gmail.com` (that's the Claude/login email, wrong for git authorship — used it once on 2026-05-25 and Alessandro corrected it). NOT a work email unless he says so for a specific repo.
- **Author name:** `Alessandro Sodano`.
- **NO `Co-Authored-By: Claude` trailer on his commits — ON HIS OWN PERSONAL REPOS.** Overrides the CLAUDE.md default — Alessandro doesn't want commits attributed to "and claude" on GitHub (confirmed 2026-05-25 on terminal-inbox; he saw it in the GitHub UI and asked to remove it). Omit the trailer when committing for him.
  - **EXCEPTION, `Tundra-Health/*` repos: the trailer is REQUIRED there** (Caleb's convention, relayed 2026-08-12). Do not strip it. See [[feedback_tundra_commits_need_claude_trailer]].

**Git has NO global identity configured** (`git config --global user.name/email` are empty), and CLAUDE.md forbids touching global git config. So set identity per-commit via env vars instead:
```powershell
$env:GIT_AUTHOR_NAME="Alessandro Sodano"; $env:GIT_AUTHOR_EMAIL="alesoda2002@gmail.com"
$env:GIT_COMMITTER_NAME="Alessandro Sodano"; $env:GIT_COMMITTER_EMAIL="alesoda2002@gmail.com"
git commit -m "..."
```

**gh CLI:** installed 2026-05-25 at `C:\Program Files\GitHub CLI\gh.exe` (v2.92), authed to `alesod23`. It's NOT on the Git Bash PATH and `gh auth login` is interactive — run auth in a real PowerShell window, and call gh by full path from tools. PowerShell wraps git/gh stderr progress lines as `NativeCommandError` even on success — check `$LASTEXITCODE`/`exit: 0`, not the red text.

First repo created this way: [[project_terminal_inbox]] (public, the /triage package shared with Raphael Schaad at YC).
