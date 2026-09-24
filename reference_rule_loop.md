---
name: reference_rule_loop
description: "The rule loop (2026-09-24): one design for drafting, Ping hub and CRM. Ledgers = task-land/_system/*-CONTRACT.md via addrule.py --contract; compiled skills; observers append rule-hits.jsonl; his verdicts go to decisions.jsonl; system-check.py (Task RuleLoop-SystemCheck 09:10) writes system-check-<n>.md, the box's sweep posts it. His only inputs: 'this sucks because', 'I like this', 'this again', a change request, 'slower/faster'."
metadata:
  type: reference
---

**Canonical:** `task-land/_system/RULE-LOOP.md` (v3). Build plan and status: `_system/WORKPLAN-20260924-loop-build.md`. CRM detail: `~/.medtech-crm/WORKPLAN-20260924-crm-cleanup-and-monitor.md`.

**Files (all git-synced in task-land unless noted):**
- Ledgers: `EMAIL-REVIEW-CONTRACT.md`, `HUB-CARD-CONTRACT.md`, `CRM-CONTRACT.md`; add with `python ~/task-land/_system/drafts/addrule.py --contract email|hub|crm --rule "..." --quote "his words" [--soft] [--like] [--item <id>] [--suppress "<regex>" (hub only, also files a downgrade pattern)]`. Never hand-edit the tables.
- Compiled skills: `~/.claude/skills/drafting/SKILL.md` (from `drafts/compile_skill.py`), hub and CRM skills to follow; frontmatter `skill_v`, `rules_in_front`, `rules_in_ledger`.
- Observers: `drafts/critic.py` (email; hit lines via `common.hit()`, path from `DRAFT_ORIGIN`), `approval-hub/server.js` guard on the box (`hub-rules.json` downgrade/drop patterns; downgrade = `kind:"update"`, never refuses a card), `crm-app/observer.js` (CRM). All append `_system/rule-hits.jsonl` `{ts,surface,rule,action,item,model,skill_v,path,by,note}`; `action:"ok"` lines are the denominator.
- Decisions ledger: `_system/decisions.jsonl` `{ts,surface,seq,item,verdict,by,type,kind,guard,text,created_at,feedback}`: hub (both resolve paths; state.json prunes resolved cards after 24 h so never count from it), boards (`board-server.js logDecision`), CRM (observer). Lines whose `by` contains "test" are ignored by the counter.
- Config/state: `_system/rule-loop-state.json` (window 60 decisions / 14 days, CRM at least 7; skill cap 15; retire after 50 applicable; repeat 2; compile after 5 entries / 14 days; reader concurrency 2; coalesce 10 min; cadence 2 days; model opus).
- System check: `_system/system-check.py` (laptop, Task Scheduler `RuleLoop-SystemCheck` daily 09:10 via `system-check-hidden.vbs`, log `system-check.log`); fires when the window is full; writes `system-check-<n>.md` with a `posted:` header line the box's eod sweep fills after posting it as a hub `kind:"update"`. `--dry-run`, `--force`.

**Rules of the loop:** design on merit, no arbitrary caps ([[feedback_design_on_merit_not_his_offhand_numbers]]); "iterative" = his one sentence on the spot ([[feedback_iterative_means_on_the_go_flag]]); Opus wherever something decides or writes, Haiku nowhere; a verdict is never blind ([[feedback_review_page_design_system]]). Kortyx is the reference shape ([[reference_kortyx_design_reference]]).
