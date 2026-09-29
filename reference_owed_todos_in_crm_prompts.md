---
name: reference_owed_todos_in_crm_prompts
description: CRM reader + Today review generator read the open task-land to-dos that name a person (crm-app/owed.js), so a deliverable we owe is always named (email H87, 2026-09-29)
metadata:
  type: reference
---

`~/.medtech-crm/crm-app/owed.js` (`owedFor`, `owedBlock`): scans `task-land/Tasks/{inbox,active,waiting,today}` for open to-dos naming a CRM person: `contact:` = pid, the pid, the full name, or a surname / first name (>= 5 letters, not "alessandro"/"sodano") that no other CRM person carries. Both `review-api.js` buildPrompt and `crm-app/reader.js` buildPrompt print them as "HIS OPEN TO-DOS THAT NAME THIS PERSON"; the generator must name a deliverable we owe ("stiamo lavorando su X, se mi giri la sua email glielo mando").

**Why:** his comment on nevio-boscariol (28 Sep, again 29 Sep): the PoC document he asked for sat in `Tasks/inbox/documento-poc-per-nevio-aris.md` with no `contact:` line, and no prompt read task-land at all. Rule H87 existed but had nothing to act on.

**How to apply:** a new source of "what we owe" goes into owed.js, not into one prompt. Check a person with `node review-api.js prompt <pid>` (look for the block). Code reaches the laptop :4137 on its restart and the box via the coattio git sync.

Related: [[reference_review_staged_commit]], [[reference_feedback_loop_fix]], [[reference_meeting_loop]].
