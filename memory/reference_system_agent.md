---
name: reference-system-agent
description: "THE SYSTEM AGENT (task DA-SystemAgent, task-land/_system/system-agent/system_agent.py, built 4 Oct 2026): maintainer of the whole SODA SYSTEM; the ledger nodes.json is its manual; registry broken.jsonl, fix sessions, STUCK cards; the GTM agent keeps only the campaigns"
metadata:
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-10-04T17:58:48.928Z
---

Split on 4 Oct 2026 (design `soda-brain/handoffs/DESIGN-20261004-system-agent.md`, his words: "a maintainer for the
whole SODA SYSTEM ... all the ones that are about maintenance get fixed"). Full description: `soda-brain/system/LOOPS.md`
section 7.

- **System Agent:** `task-land/_system/system-agent/` (`system_agent.py`, `registry.py`, `agentlib.py` the shared incident
  engine, `unstuck.py`, `fix_guard.py`, `config.json`, `tests/`). Task `DA-SystemAgent` every 10 min, `DA-Unstuck`
  every 1 min, both through run-hidden.vbs (`register-tasks.ps1`).
- **Its manual = THE LEDGER `soda-brain/system/nodes.json`** (his word 19:13): per node the checks (probe, healthy_when,
  if_fails, known_fixes, his_command, for_him), ports, tasks, paths. The map's NODES are RENDERED from it
  (`soda-brain/tools/build_map.py`): edit the ledger, never the HTML block. Drift (task missing, path missing, port up
  on a node marked off) = `stale-ledger` + a fix-session line.
- **Registry** `broken.jsonl` (newest line per id wins): maintenance / his_command / his_decision. Closes only when the
  check passes twice in its own ticks (or once after a fix session's own pass).
- **Fix session** = job kind `fix` (`jobs.add_fix`, `job_runner.run_fix`): Opus, 30 min soft, 45 hard, 1 week point,
  once to 2 after a reproduction, 3 a day, never at 5h >= 80%, kill switch `system-agent/OFF`. The box is READ-ONLY for
  it; a never-list cause = `stuck` at once. The guard hook fails OPEN if it crashes (Claude Code), hence the preflight.
- **STUCK card** only after a fix session said stuck, or for a check the ledger marks his_command. His yes runs through
  `unstuck.py`: auth (account pre-selected), terminal (pre-typed, `his-yes` in window-watch via expected.jsonl), run.
- **GTM agent** (`gtm-eng/agent/gtm_agent.py`, task GTM-Agent): campaigns only; non-campaign faults -> `inbox.jsonl`;
  reads `blockers.json`; `gtm_agent.py section --json` is its part of the ONE combined report (09:00, 18:15, posted by
  the System Agent, which also pushes the heartbeat `box_watch.py` reads).
- **Judge it:** `system_agent.py status | incidents | registry [--all] | brief <id> | check --only <key>`.

Gotchas learned building it: a quoted heredoc in the Bash tool still turns `\\n` / `\\b` inside python string
literals into real control characters: write code with the Write/Edit tools. A text-mode stdin to ssh on Windows sends
`\r\n` (bash reads `3\r`): send bytes.
