---
name: feedback-ask-user-question-preference
description: "User prefers AskUserQuestion (CLI multi-select with auto Other freewriting) for preference/dimension/multi-pick prompts, not just mutually-exclusive single decisions"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c19162ff-56f0-4383-9e07-0dfdff7a81b1
---

User prefers the AskUserQuestion tool's UI (CLI option chips + auto "Other" for freewriting) whenever a response involves picking from a finite set of choices, even when the choices aren't strictly mutually exclusive. Use `multiSelect: true` when the dimensions allow more than one pick.

**Why:** Cleaner UX than markdown bullets requiring the user to type "D1 b, D2 c, D3 a+b+f"; the CLI tool lets them click and skip the syntax. Stated 2026-05-18 during the "what is actionable" triage review.

**How to apply:**
- Preference / dimension / opinion-gathering prompts → use AskUserQuestion with one question per dimension (max 4 questions per call).
- Multi-pick is fine — set `multiSelect: true` and don't force false mutual exclusivity.
- Every AskUserQuestion auto-provides "Other" for freewriting; don't manually add one.
- **/triage specifically (locked in 2026-05-18):** ALWAYS use AskUserQuestion right after the colored actionable-list display (don't replace the list — show both). One question per item (max 4 per call; batch+re-prompt if >4). Fixed option order per item: (1) Done (2) Todo (3) "Send my suggested reply" — with my pre-composed 1-2 sentence reply in the `description` field (for FYI items, this becomes "Acknowledge with: ..."); auto-Other for freeform. See /triage SKILL.md step 6.
- Overrides the CLAUDE.md default ("Reserve AskUserQuestion for mutually-exclusive single decisions") for this user.
