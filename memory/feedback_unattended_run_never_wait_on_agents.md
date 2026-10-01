---
name: feedback_unattended_run_never_wait_on_agents
description: "Unattended/overnight run: never end the turn waiting on background agents; check their liveness by transcript mtime; keep a self-wake heartbeat. Cost him 10 idle hours on 2026-09-27."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 6d6a4161-826b-4016-90da-5f2d7a0d8e7e
  modified: 2026-09-27T11:13:54.336Z
---

In an unattended run (he is asleep or away) NEVER end the turn to "wait for the agents to report". Do the owed work in the main thread, and treat background agents as optional accelerators.

**Why:** On 2026-09-27 (thesis final-review run, he wanted to finish the thesis that day) I launched 6 research agents at 01:50, kept working until 02:49, then ended my turn waiting for the last three. Those three had frozen between 01:50:41 and 01:54:53, each in the middle of a tool call with no result and no error in its transcript. Nothing wakes an idle session except a report or a user message, so the run sat idle for about 10 hours until he opened the lid at 12:30. The laptop had not slept (power log clean after 01:31). He was very upset: "10 hours of you running and not doing shit".

**Most likely cause of the freeze (evidence, not proof):** in all three agents the first call left without a result was a Bash command (`python --version; python -c ...; date`, `python "$TEMP/r6/inv.py" ...`, a python heredoc). That is the signature of a permission prompt nobody was there to answer; agents whose commands were already allowed finished. See [[reference_permission_allowlist_gaps]].

**How to apply:**
- Background agents in an unattended run get tasks they can do with Read, Grep and Glob; anything needing Bash or Python runs in the main thread, where a prompt is visible.
- Before ending any turn in an unattended run, ask: is work still owed that I can do myself? If yes, do it. Ending the turn is allowed only when the deliverable is finished or a real blocker needs him.
- Liveness check 10 minutes after launching agents: look at the modification time of `~/.claude/projects/<project>/<session>/subagents/agent-<id>.jsonl`. No write for 10 minutes while "running" = frozen: stop it and do that work in the main thread. `ListAgents` saying "running" proves nothing.
- Keep a heartbeat so the session wakes itself (a scheduled wake-up or cron every 20 to 30 minutes) whenever anything is running in the background.
- Give agents small, bounded tasks and tell them to write partial results to their file as they go, so a freeze loses minutes, not the whole task.
- Say in the first status message what would stall the run, so he can decide before leaving.

Related: [[feedback_agent_long_running]], [[feedback_agent_output_file_is_interim]], [[feedback_no_polling_on_background_tasks]], [[project_thesis_final_review_2026_09_27]].
