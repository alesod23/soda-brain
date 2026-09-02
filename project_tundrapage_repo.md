---
name: project_tundrapage_repo
description: "Tundra-Health/TundraPage (Caleb's Next 16 marketing site) — local clone, branch+PR workflow, and the two env gotchas that block every session"
metadata: 
  node_type: memory
  type: project
  originSessionId: a05a078c-bda8-4aa3-8e63-a38b0d08b6a2
  modified: 2026-08-10T00:25:10.961Z
---

`Tundra-Health/TundraPage` is the tundrahealth.ai marketing site (Next 16 + Turbopack, pnpm, single `app/page.tsx`). Caleb set it up; Alessandro and I change it via branch -> PR -> Caleb's automatic Claude PR review (haiku, posts inline comments on every push, not just the first). Always branch off a freshly pulled `master`, one change per PR.

Local clone: `C:\Users\Alessandro\TundraPage`.

**As of 2026-08-10 `alesod23` is an active org member but has `push: false` on this repo** (`gh api repos/Tundra-Health/TundraPage --jq .permissions`). Pushing dies with 403 "Write access to repository not granted". Caleb has to add alesod23 with Write. Re-check permissions before assuming a push will work.

Two environment gotchas, neither of them repo bugs:
- `pnpm lint` / `pnpm exec` / any `pnpm` script fails with `ERR_PNPM_IGNORED_BUILDS: unrs-resolver`, because pnpm 11 re-runs its deps check first. Set `$env:PNPM_CONFIG_STRICT_DEP_BUILDS="false"` in every PowerShell call. pnpm also keeps writing an `allowBuilds:` placeholder block into the tracked `pnpm-workspace.yaml` — `git checkout -- pnpm-workspace.yaml` before every commit or it lands in the PR.
- Verify UI changes against a real production build: `pnpm build`, then `node node_modules\next\dist\bin\next start -p 3210` via detached `Start-Process`, then Playwright screenshots at 1440 and 390 (script pattern in the session scratchpad, checks `scrollWidth == clientWidth` for overflow). `next start` serves the build it booted with, so restart it after a rebuild.

Related: [[feedback_git_commit_message_file_on_powershell]], [[reference_git_github_identity]].
