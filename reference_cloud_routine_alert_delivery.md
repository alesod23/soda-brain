---
name: reference_cloud_routine_alert_delivery
description: "How a cloud routine actually reaches Alessandro's phone with the laptop off — the claude.ai Gmail connector has NO send tool, so alerts go via a Google Calendar popup reminder."
metadata: 
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-08-04T04:47:29.301Z
---

**The claude.ai Gmail connector cannot send email.** Its whole surface is `create_draft`,
`update_draft`, `list_drafts`, `get_message`, `get_thread`, `search_threads`, the label tools, and
`apply_sensitive_message_label` (TRASH/SPAM). Any routine prompt that says "email me" silently
degrades into an **unsent draft**. Verified from live tool schemas 2026-08-03 after the DA SYSTEM
health routine produced 10 unsent drafts over ~18h while appearing to work.

**The working push channel is Google Calendar.** `create_event` supports
`overrideReminders: [{"method":"popup","minutes":N}]`, and a popup reminder is a real phone
notification that fires with the laptop off. Connector traffic bypasses the cloud session's network
allowlist entirely, so this needs **no secret and no environment configuration**. Pattern in use:
event starting ~6 min out, `availability: AVAILABILITY_FREE` so it does not block the day, reminders
`[{popup,5},{popup,0},{email,5}]` (two popups = two chances if the phone had not synced yet), the
alert text in `description`. Keep a Gmail draft alongside as a searchable record, never as delivery.

**Cloud routines CAN make arbitrary network calls** — per-environment network access is
None / Trusted (default) / Full / Custom-allowlist, configurable in the claude.ai UI. The common
claim that routines are hard-blocked is stale (issue #50146, closed). So a Telegram bot call is
viable, but the environment, allowlist entry and env var must be set up **by Alessandro in the UI**;
it cannot be done from a session. Anthropic explicitly says cloud environments have no secrets store
and should not hold credentials, so weigh that before putting a bot token there.

**How to apply:** When building any cloud routine that must reach him, make Calendar the primary
channel and say so explicitly in the prompt, including an instruction never to let a draft stand in
for a failed push. Test it by checking `list_events` for the event, not by trusting the run's green
status. Related: [[reference_floom_mcp]], [[project_da_system]], [[reference_sodanotif]].
