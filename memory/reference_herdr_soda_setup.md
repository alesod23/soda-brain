---
name: reference-herdr-soda-setup
description: "His herdr setup (10 Oct 2026): sessions in the sidebar, a \"soda\" status tab, a \"mind\" tab following the running headless agent, box saved as machine \"box\""
metadata:
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-10-10T20:17:43.998Z
---

He monitors SODA in herdr (v0.9.3, laptop, Claude integration active; sessions started inside herdr show working/done/blocked).
- Tab **soda**: `python ~/task-land/_system/herdr/soda_status.py` reports agent "soda" (blocked = needs him: hub cards, CRM items, LinkedIn down >2 h; idle = fine) every 60 s.
- Tab **mind**: `python ~/task-land/_system/herdr/soda_mind.py` follows the newest headless transcript (entrypoint `sdk-cli`) of the last 30 min: TASK / READ / RUN / GOT / SAYS lines. Private reasoning is not stored in transcripts, so not shown.
- A piece of his work gets its own tab + `herdr agent start <name> --kind claude --pane <id>` then `herdr agent prompt <name> "..."` (done for "speedrun").
- Box: saved machine `box` (SSH alias `box`, never the raw IP: the key is only on the alias). Nothing runs inside herdr on the box yet; the savior runs outside it.
- His ask was MINIMAL ("i can imagine it becoming huge.... cmon"): no per-agent panes, nothing that piles up.
- Before starting work on a to-do, check `_system/applications/runs/` and the to-do's `stage`: the headless to-do worker may already be on it (it picked the speedrun to-do at 16:14 before I started a session). See [[reference_todo_pipeline]].
