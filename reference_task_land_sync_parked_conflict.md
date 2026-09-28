---
name: reference_task_land_sync_parked_conflict
description: "task-land box<->laptop git sync silently parked on a rebase conflict for 7 days (10 to 17 Sept 2026): laptop never saw box tasks/sidecars, box never saw laptop sidecars, laptop dead-man's switch fired 'VPS DOWN' daily from the stale health-vps.json. Symptom list + the merge fix."
metadata:
  type: reference
---

**What happened:** 2026-09-10 17:21 the box's `git-sync.sh` hit a rebase conflict in `_system/drafts/r1384854480504427376.md` (both machines revised the same sidecar). By design it parks HEAD on `conflict-vps`, writes `GIT-SYNC-CONFLICT-VPS.md` and exits 1, every minute, forever. Nobody looked. Found 2026-09-17 19:40 only because the CDTM calendar carried "DA SYSTEM: VPS DOWN" events (laptop reads `_system/health-vps.json`, frozen at 10 Sept).

**Symptoms that mean "check the sync first":** laptop-made sidecars missing on the box (register.py says "no sidecar"); tasks made on the box never on the laptop's daily page; `GIT-SYNC-CONFLICT-*.md` at a repo root; `git status -sb` showing `ahead N, behind M` with both large; `systemctl is-failed da-sync.service` = failed; calendar "VPS DOWN" while the box is up.

**Fix used (not a rebase: 2750 local commits to replay):** hold the script's lock (`flock /tmp/da-git-sync.lock bash -c '...'`), `git merge --no-commit origin/main`, resolve only the overlapping files (append-only `queue.jsonl` = union sorted by ts; mirrored box tools = ours; sidecars = whichever machine is that draft's writer), delete the advisory, commit, push, delete `conflict-vps`. Next tick was clean.

**How to apply:** at the start of any long savior session, and whenever laptop and box disagree about a file, run `for r in task-land vault_kb medtech-brain claude-memory; do git -C ~/$r status -sb | head -1; done`. A detection hook is still missing (the health snapshot could report `da-sync.service` failed; it does not).

Related: [[reference_tool_mirrors]], [[reference_draft_review_lane]].

**Again, 2026-09-25 01:39 to 2026-09-27 15:50 (laptop side this time):** `git pull --rebase` hit conflicts in the two append-only logs both machines write (`_system/decisions.jsonl`, `_system/rule-hits.jsonl`); the laptop parked on `conflict-laptop` every minute for 2.5 days, 1347 commits ahead and 929 behind, and nobody saw it (found only because an scp looked odd). Fixed with `~/hubrev-work/merge_sync.ps1 -Mode apply` (holds the `Global\TaskLandGitSync` mutex, `git merge --no-commit origin/main`, jsonl = union by line ordered by ts, scripts = ours, sidecars by most advanced state; tag `pre-merge-20260927`). Both machines had numbered a new CRM rule H27: the box's became H32. STILL MISSING: a merge driver (`merge=union` in .gitattributes for the append-only logs) and an alarm when `ahead/behind` are both large.

**Third time, 2026-09-28 14:36 to 18:25 (box side), and the structural fix:** parked on `_system/rule-hits.jsonl` again,
right as the box registered the two Snitem drafts (Benoist, Costa): they never reached the laptop's Drafts tabs, and the
dead-man switch fired "VPS DOWN" (a true signal: health-vps.json could not sync). Fixed for good: `.gitattributes` has
`*.jsonl merge=union`, and BOTH sync scripts (`_system/git-sync.ps1`, `_system/vps/git-sync.sh`) now MERGE origin/main
instead of `pull --rebase --autostash`: a rebase replayed 100+ local commits and re-raised the already-resolved sidecar
conflicts on every replay, which is why hand fixes kept falling back to "parked". Manual merge recipe: hold the lock
(`flock /tmp/da-git-sync.lock`), make sure `.git/MERGE_HEAD` exists before committing (a sync tick between two steps
silently undid a merge once), sidecar conflicts = the side with the more advanced status. Backups `*.bak-20260928`.
Same evening: the merge itself then parked on draft SIDECARS both machines had written (Benoist's). Both sync scripts
now call `_system/drafts/resolve_sidecar_conflicts.py` after a failed merge: for `_system/drafts/*.md` only, the side
with the more advanced status wins (finished > edited > registered > stub), tie = longer file; anything else still
conflicting = abort + park as before. Verified live: "MERGED with sidecar auto-resolve" in git-sync.log 18:44.
Gotcha while editing git-sync.ps1 from a Python heredoc: `'\r'` in `drafts\resolve` became a carriage return and split
the line; use forward slashes in Join-Path strings.
