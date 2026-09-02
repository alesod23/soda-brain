---
name: reference_claude_design_permissions
description: "Why Claude Design pushes always ask for approval, and the only thing that suppresses it"
metadata: 
  node_type: memory
  type: reference
  originSessionId: a663f18a-252e-47b4-b092-035a97160645
  modified: 2026-08-29T23:09:38.096Z
---

In Claude Code 2.1.251 the `DesignSync` tool's own `checkPermissions` hardcodes
`behavior:"ask"` with `classifierApprovable:false` for **`finalize_plan`** and
**`create_project`**. Every other method (`write_files`, `delete_files`,
`register_assets`, reads) returns `{behavior:"allow"}` and never prompts.

Consequences:
- One approval per push, always on `finalize_plan` (its prompt renders as
  "Design: Upload design system (N to upload)"). `write_files` right after it
  is silent.
- `"DesignSync"` / `"DesignSync(*)"` allow-rules in settings do **not** clear it,
  and neither does auto mode. `classifierApprovable:false` bars the classifier.
- The only supported bypass is a `PreToolUse` hook with matcher `DesignSync`
  returning `hookSpecificOutput.permissionDecision:"allow"`. One is configured
  in `~/.claude/settings.json`.
- Hook config is read at process start: a settings edit needs `/hooks` or a
  restart before it takes effect.

A newer `ClaudeDesign` tool exists in the same build with **durable per-project
write grants** (approve once per project, revocable at claude.ai/design settings)
but it sits behind the server-side gate `tengu_omelette_fouet`, off for this
account. Nothing local turns it on. See [[reference_claude_code_notifications]].
