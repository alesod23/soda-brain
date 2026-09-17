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
