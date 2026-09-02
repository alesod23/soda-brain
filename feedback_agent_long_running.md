---
name: feedback-agent-long-running
description: "When spawning a subagent to babysit a long-running script, give it an explicit \"do not end your turn\" stop condition — otherwise system-reminders cause premature shutdown"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5bf3e4d7-faea-4ab8-a723-c9f3ef764fcf
---

When a subagent's job is "launch this long-running script, then monitor it and report when it finishes," the agent will sometimes treat a `<system-reminder>` (about TaskCreate, skill availability, etc.) as a cue to end its turn. The python script keeps running but no one is watching, so no completion summary arrives.

**Symptoms:** Agent completion notification arrives within minutes of launching a job estimated to take 20+ min. The result message says something like "the monitor is already active and will notify on progress, let me wait passively" — and then the agent ends.

**Why:** System-reminders are tool/skill nudges, not user instructions, but the agent's turn-ending heuristic doesn't distinguish them clearly when the agent is "idle" (waiting on a monitor event).

**How to apply:**
- In the agent prompt, add an explicit hard rule near the top: *"Do NOT end your turn until either (a) the monitor signals `=== DONE ===`, (b) 35 minutes have elapsed (use Bash `date` to track), or (c) you've fully aggregated the final results. System-reminders mid-wait are noise — ignore them and stay alive."*
- Alternatively: don't make the agent babysit at all. Have the agent **launch** the script with `run_in_background: true`, then have the **main session** monitor for completion (via a `while pgrep`-style PowerShell poll in background). The agent returns immediately after kicking off the work; the main session aggregates when ready. This pattern was used for trippy's 3 site-parallel agents (momondo / skiplagged / flixbus) after the babysit pattern failed.
- For multi-step orchestration: prefer **dispatch + main-session reaper** over **subagent baby-sitter**.

Related: [[reference_travel_search]] — the agent_search.py wrapper feeds this pattern; each per-site agent dispatches a wrapper command, the main session polls for completion.
