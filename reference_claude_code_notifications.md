---
name: reference_claude_code_notifications
description: "Approval-only desktop notifications, and why the startup dialog opened on \"No\""
metadata: 
  node_type: memory
  type: reference
  originSessionId: a663f18a-252e-47b4-b092-035a97160645
  modified: 2026-08-29T23:09:49.957Z
---

**Approval-only pings.** Claude Code's `Notification` hook matches on the
notification type, so the matcher itself does the filtering. Wired in
`~/.claude/settings.json` to
`permission_prompt|worker_permission_prompt|elicitation_dialog|elicitation_url_dialog|agent_needs_input`
→ `~/.claude/hooks/notify-approval.ps1` (sound + NotifyIcon balloon, logs to
`~/.claude/notify-approval.log`). The excluded types are `idle_prompt`,
`agent_completed`, `auth_success`, `push_notification`, so end-of-turn and
background-agent events stay silent. The permission ping fires **6 s** after the
prompt appears and is cancelled if answered first, so answering promptly makes
no noise.

**The startup dialog that opened on "No".** That is the folder-trust /
settings-approval dialog ("Yes, I trust these settings" / "No, exit Claude
Code"). It renders cancel-first, with No focused and the digit shortcuts
hidden, whenever the settings being approved contain hooks, shell commands, or
env vars — which his always do. It kept reappearing because
`~/.claude.json` had `projects["C:/Users/Alessandro"].hasTrustDialogAccepted:
false`. Flipped to true (backup: `~/.claude.json.bak-trust`).

Related: [[reference_claude_design_permissions]].
