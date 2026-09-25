---
name: reference-venv-in-synced-repo-wedges-push
description: "Never create a venv (or any >100 MB file) inside a git-synced repo: the 5-min sync cron commits it and GitHub's 100 MB pre-receive limit then blocks EVERY push until the commit is reset out of local history"
metadata:
  type: reference
---

2026-09-25, travel-search. I made a playwright venv at `travel-search/.venv-pw` to price a multi-city
flight. The `repo-sync.sh` cron runs every 5 minutes with a blind `git add -A`, so it committed all
**831** files of the venv (`b511426`) within minutes.

The damage is not the clutter. `.venv-pw/lib/python3.12/site-packages/playwright/driver/node` is
**120.73 MB** and GitHub refuses any file over 100 MB at the pre-receive hook:

    remote: error: File .venv-pw/.../playwright/driver/node is 120.73 MB; this exceeds GitHub's
    remote: error: file size limit of 100.00 MB
    ! [remote rejected] master -> master (pre-receive hook declined)

So the branch was **wedged, not merely dirty**: deleting the files and committing the removal does not
help, because the offending blob is still in the commit being pushed. Every later push fails too, and
the repo silently stops syncing — the same class of failure as
[[reference_travel_search_sync_colon_filenames]], reached a different way.

**Fix, when the bad commit has not been pushed:** check what is local-only first
(`git log --oneline origin/master..HEAD` + `git diff --name-only origin/master..HEAD`), confirm the net
change is small, then `git reset --mixed origin/master`, re-commit only what belongs, push. Here both
local commits netted out to one `.gitignore` line. Nothing had reached the remote, so the laptop was
never affected.

**Prevention:** venvs live OUTSIDE every synced repo. The playwright one is now `~/.venv-playwright`
(see [[reference_gflights_engine]] for how `gflights_mc.py` uses it). `travel-search/.gitignore` now
carries `.venv*/` and `venv/`, but the gitignore is the second line of defence, not the first — the
first is not putting it there.

**How to apply:** before creating a venv, a model cache, or anything with a large binary, check whether
the cwd is inside `task-land`, `vault_kb`, `medtech-brain`, `claude-memory` or `travel-search`. Those
five all have a commit-everything cron; there is no review step that would catch it.
