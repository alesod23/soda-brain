---
name: feedback_register_py_run_from_task_land_and_check_card_line
description: "Lane gotcha (bit three times 2026-09-17/18): register.py invoked with a relative path after `cd _system/drafts` silently does nothing (no 'card #N' line), so the hub card keeps pointing at the OLD, already-deleted draft; a later `N dsend`/resolve then sends nothing. Always run `cd ~/task-land && python _system/drafts/register.py ...` and require the 'card #N created/revised' line before resolving."
metadata:
  type: feedback
---

**What happened:** on the Andellini mail (18 Sept) the draft was recreated (rev 3), the sidecar moved, but `register.py` was called from `_system/drafts/` with the path `_system/drafts/register.py` (relative to task-land), so the command failed quietly inside a `grep`-filtered pipeline. Card #3 still carried the deleted draft id; `POST /resolve yes` therefore sent nothing (0 mails in Sent). Caught by checking Sent before re-sending. Same slip happened twice the day before (Roussel, Ramana), caught by re-running.

**How to apply:**
1. Every register call: `cd /home/da/task-land && /home/da/triage/venv/bin/python _system/drafts/register.py <draft_id> --sidecar _system/drafts/<draft_id>.md ...`. Never after a `cd` into the drafts dir.
2. Read the output for `card #N created` / `card #N revised (hub id ..., revision R)`. No line = not registered. Then confirm `state.json` `pending[<hub id>].meta.draft_id` equals the NEW draft before any resolve/dsend.
3. After any hub send, verify `gmail.py search --query 'to:<addr> in:sent newer_than:1d'` returns 1 before telling him "sent".

Related: [[reference_draft_review_lane]], [[feedback_verify_state_not_queue]].
