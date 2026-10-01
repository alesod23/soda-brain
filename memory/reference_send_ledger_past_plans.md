---
name: reference_send_ledger_past_plans
description: Send ledger counts a plan only until its day passes; us-campaign-100 daily.py carries failed days over (2026-09-29)
metadata:
  type: reference
---

`task-land/_system/outreach/ledger.py`: a `planned` entry whose day has passed and was never marked `sent` takes no room (`counts()`); `view` shows it as "planned, never sent". Before 2026-09-29 twenty invites booked for two days when LinkedIn was down kept the 7-day window full.

`gtm-eng/boards/us-campaign-100/daily.py carry_over()`: people of a past batch who never went out move to the first days with room (today included), booked through `ledger.py plan`; anybody the CRM says replied is left out; the old batch file keeps them under `moved`. `python daily.py --carry-dry` shows the moves without doing them. If the CRM cannot be read nobody is moved that run.

Related: [[reference_system_agent]], [[reference_daily_campaign]], [[reference_linkedin_launcher_reaper]].
