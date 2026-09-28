---
name: reference-system-agent
description: "The system agent (task GTM-Agent, gtm-eng/agent/gtm_agent.py) - checks every 10 min that GTM is running, fixes from a whitelist, two hub updates a day, box fallback"
metadata:
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-28T12:25:14.238Z
---

Built 2026-09-28 on his ask: "a GTM agent, obsessed with ensuring a push in gtm is present everyday", then "what im
asking is a system agent more than a GTM. whose goal is for GTM to be running and running well".

- **Where:** `~/gtm-eng/agent/` (`gtm_agent.py`, `config.json`, `li_probe.py`, `README.md`, `tests/`). Task
  `GTM-Agent` every 10 min through `gtm-agent-hidden.vbs`. Workplan `~/gtm-eng/WORKPLAN-20260928-gtm-agent.md`.
- **Checks:** campaigns (stopped board or channel, steps due and not going, engine crash, no push by noon, daily
  board and fire), CRM Today, contacts to find ([[reference-channel-search]]), hub cards current and waiting
  (decision 24 h, draft 48 h), servers, scheduled tasks, Gmail, LinkedIn, sync, console windows
  ([[reference-window-watch]]).
- **Fixes alone (whitelist, capped):** release_channel (only after a dropped connection AND the tool tested working),
  start_task, start_servers, li_repair, hide_task. Anything else: Opus reads the evidence, ONE card, which closes by
  itself when the problem is gone. It never sends, never logs in.
- **Updates:** 09:00 and 18:15 Rome, hub cards kind update, head "GTM agent: pushing today, YES/NO". A report must
  carry no alert word (failed, down, error...) or `hub_outdated.py` never ages it: `calm()` rewrites them.
- **Box:** `task-land/_system/gtm-agent/box_watch.py`, cron */10, reads `~/.local/state/gtm-agent/heartbeat.json`
  pushed by the laptop over ssh. Laptop silent 60 min in business hours with sends due = one card a day.
- **After a wake** nothing is judged late for 30 min (`settle_min`): on the first day the agent nearly raised a false
  alarm for steps that were only waiting for the first tick after the lid opened.
- **Judge it:** `runs.jsonl`, `incidents.jsonl`, `python gtm_agent.py status|incidents|missed "..."`.

Related: [[reference-linkedin-launcher-reaper]], [[reference-daily-campaign]], [[reference-hub-lives-on-the-box]].

Brief it was built from: `task-land/_system/HANDOFF-20260928-gtm-agent.md`.

**System feedback (added 2026-09-28):** a sentence he types in a review field about the system ("why did you not see
it", "system problem", the "change the system" pill) used to be filed only as a rule of that surface (his Amos
comment became H80), which nobody builds from. `check_feedback` lifts it into
`task-land/_system/gtm-agent/system-feedback.jsonl` (status open) and every update lists the open ones. A session
that fixes one sets its line to `"status": "done"` with `"changed": "..."`. A card he commented on shows
"commented · waiting" and sorts last in the CRM review.
