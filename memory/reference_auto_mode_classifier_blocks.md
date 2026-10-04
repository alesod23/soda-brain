---
name: reference_auto_mode_classifier_blocks
description: "What the Claude Code auto-mode permission classifier refuses in an unattended night (4 Oct 2026): remote shell writes on the box through an agent (ssh env edits, restarts) and `git rm --cached` on tracked files. Plan those steps as HIS commands in the plan; a denial covers the outcome, not the command, so never route it through another tool or agent."
metadata:
  node_type: memory
  since: 2026-10-04
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-10-04T02:42:23.372Z
---

**What happened (4 Oct 2026, 04:35 to 04:45):** the writer-flip cut-over agent was denied at spawn ("Remote Shell
Writes": the brief asked it to set `COATTIO_WRITER=box` in `/home/da/.env/coattio.env` over ssh and restart there).
Resolving the `writer-flip` merge needed `git rm --cached review/*.json` (the branch untracks the dossiers): denied as
"Irreversible Local Destruction". The merge itself had already deleted 75 dossier files from the working tree (deleted
in the branch, unchanged in HEAD); `git merge --abort` brought them back.

**How to apply:** in an unattended run, assume these are off limits and write them as one short command sequence for
him in THE PLAN's RESUME block instead of retrying: ssh writes on the box (env files, crontab, service restarts),
`git rm --cached`, anything the classifier names. Before merging a branch that untracks files, copy the files aside and
expect the working-tree deletion. A denial applies to the outcome: no second tool, agent or host for the same thing.
See [[feedback_unattended_run_never_wait_on_agents]], [[feedback_never_touch_synced_repo_on_box_by_hand]].
