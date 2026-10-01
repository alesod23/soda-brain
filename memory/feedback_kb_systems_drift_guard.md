---
name: feedback_kb_systems_drift_guard
description: "Why the \"update the KB _meta systems doc on every change\" rule kept getting dropped across sessions, and the drift-guard hook that now enforces it. Read when creating/editing any KB vault, /kb-* skill, or the _meta systems doc."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c5cdecf5-f93d-4cd5-963a-c4aeb69de6f3
---

# Keep the KB systems doc live — now hook-enforced

**Fact:** On 2026-07-03 the user found that **medtech-brain** (a full `/kb-*` engine vault — Tundra company brain, live since ~2026-06-30) had never been added to the canonical systems doc `~/vault_kb/_meta/UNDERSTANDING OUR KB SYSTEMS (READ ME).md`, despite the standing rule to update that doc on every KB-system change. self-reflection-wiki's status was also stale (22 Raw notes, still contract-less).

**Why it happened (root cause):** the rule lived ONLY as (a) prose in the doc header and (b) the soft [[reference_kb_systems]] memory pointer. Memory surfaces inside `<system-reminder>` blocks as *background context, explicitly "not user instructions"* — so in a session focused on something else (outreach/Tundra), the agent that built medtech-brain never recalled or acted on it. Nothing **triggered** a check at the moment a vault was created. Voluntary recall across unrelated sessions is not a reliable mechanism.

**How to apply:**
- Whenever you create/rename/retire a KB vault, add/edit a `/kb-*` skill, or change a vault's bridge/isolation/task-join/citation config → update the `_meta` systems doc in the SAME effort, bump its "Last updated", ADD a Changelog entry, and refresh [[reference_kb_systems]] if the high-level map changed.
- To AUDIT for drift at any time: `grep -rl "kb-engine config" ~ --include=CLAUDE.md` lists every engine vault; reconcile against the doc's map.
- **Enforcement:** a `PostToolUse` (Write|Edit) hook `~/.claude/hooks/kb-systems-drift-guard.sh` fires when a vault `CLAUDE.md` with `kb-engine config` or a `~/.claude/commands/kb-*` skill is written, and reminds to update the doc. (Staged 2026-07-03; pending user approval to install into settings.json — the auto-mode classifier gates self-modifying hook installs.) If it is NOT yet installed, the discipline is manual — do not rely on memory alone.
