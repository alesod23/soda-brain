---
name: feedback_done_notifications
description: "Done-notifications rule (2026-09-07): PushNotification (Claude's own toast/phone push, clickable into the session) when a task longer than ~5 min finishes or a background job fails/blocks; never a Telegram card for \"done\"; no per-agent balloons"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-07T13:29:55.719Z
---

**Rule (user, 2026-09-07, decided via UI questions):** notify him when something FINISHES only in these two cases: (1) a task that ran longer than about five minutes (background agent, upload, transcription, deploy, box job) is complete, (2) a background job died or I am blocked on a decision only he can make. One line, what he would act on first, where to look.

**Channel = the PushNotification tool** (Claude Code's own notification: desktop toast, and the phone when Remote Control is attached to that session). He chose it because he can tap it and land in the right Claude Code session, and because Telegram "will be submerged" and must stay for approvals plus the sodanotif chat cards. So: **no Telegram / hub card for "done"**; hub cards stay for yes/no decisions. The tool suppresses itself when he is at the terminal, so calling it at the end of a long job costs nothing when he is watching.

**Not wanted:** an end-of-turn ping, and the `agent_completed` desktop balloon (one per background agent: five agents = five balloons). The Notification hook stays approval-only. Automatic lanes keep their existing behaviour: only the Notion meeting filer posts a hub card, and only when it actually moved a note (rare); nothing else pings on its own.

**How to apply:** when a background agent or job I started completes (task-notification) after a long wait, call PushNotification with the outcome before reporting; same on a failure. Do not push for quick tasks or while he is clearly still watching. See [[feedback_approvals_are_pings]], [[reference_claude_code_notifications]].
