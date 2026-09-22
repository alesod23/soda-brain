---
name: reference_git_sync_autostash_pop_silent_corruption
description: "git pull --rebase --autostash EXITS 0 when the autostash pop conflicts. On 2026-09-22 the box's git-sync.sh therefore logged 'PULLED 1 commit(s)' and the next run's blind `git add -A` committed <<<<<<< markers into a draft sidecar and dropped a queue.jsonl line. Guards now in _system/vps/sync-guards.sh."
metadata:
  type: reference
---

**The trap:** `git pull --rebase --autostash` returns **exit 0** when the rebase
succeeds but re-applying the autostash afterwards conflicts. Git only prints
`Applying autostash resulted in conflicts. / Your changes are safe in the stash.`
So any script that checks the exit code sees success, carries on, and leaves
`<<<<<<< Updated upstream` markers sitting in the working tree. Reproduced
deterministically: remote edits a line, local has an uncommitted edit to the same
line, pull.

**What it cost (2026-09-22, task-land):** commit `2b43ad044 "vps sync 18:31"`
committed markers into `_system/drafts/r4308580185910502606.md` front matter, and
`_system/drafts/queue.jsonl` silently LOST the `r-6836536035100572677` line. The
laptop's own work parked on `origin/conflict-laptop` (5 commits). Resolved by
merging the laptop side for both files - verified against the live tundra mailbox:
`r-7746030380654745040` was the draft that actually existed, so the box's
`draft_gone_unsent` was its reconciler chasing a draft_id the laptop had replaced.

**The guards (`~/task-land/_system/vps/sync-guards.sh`, sourced by both
`git-sync.sh` and `repo-sync.sh`):**
- `guard_autostash "$out"` - greps the pull output for the message. Order matters:
  `git reset -- :/` FIRST (a failed pop leaves UNMERGED index entries and
  `git checkout --` refuses those), then `git checkout -- :/`. The stash entry is
  never dropped, so the work stays recoverable with `git stash list`.
- `guard_markers` - run with everything staged, BEFORE the commit: refuses to
  commit any staged text file carrying the full `<<<<<<<` / `=======` / `>>>>>>>`
  triad. Escape hatch for a file that legitimately contains them:
  `touch <repo>/.git/allow-conflict-markers`.
- Both write the advisory and fire ONE SODANOTIF Telegram ping
  (`~/.local/state/sync-alert-<repo>.flag`), because the previous failure mode was
  silence for days.

**How to apply:** never add `--autostash` to a sync script without `guard_autostash`
behind it, and never trust a git exit code for a command that does two things.
If a sync stops, read `_system/git-sync-vps.log` / `~/.local/state/repo-sync-*.log`
and the `GIT-SYNC-CONFLICT*.md` at the repo root.

Related: [[reference_task_land_sync_parked_conflict]], [[reference_draft_review_lane]].
