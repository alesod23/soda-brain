---
name: feedback-triage-actionable-definition
description: "Canonical definition of \"actionable\" for /triage — priorities, time window, always-skip categories, and the burst-tail exception"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c19162ff-56f0-4383-9e07-0dfdff7a81b1
---

Set 2026-05-18 by user via the 4-dimension AskUserQuestion review. Supersedes prior actionable definition in /triage SKILL.md step 3.

**Actionable = ANY of:**
1. Would affect what Alessandro does next (changes plans, requires action, surfaces info for a real upcoming commitment), even if not directly addressed to him.
2. Mentions a deadline that regards him.
3. Project update for a priority project.

**Priority projects (always-flag — surface every new msg regardless of latest-line content):**
- BMW / MPD BMW
- Lobbly
- CDTM Onboarding TF (RETIRES the prior late-August deprioritization rule)
- xplore
- Thesis

**Time window:** any real commitment, however far out. The 7-day cap is REMOVED for surfacing. (The 24h fetch ceiling in [[feedback_triage_24h_cap]] still governs what we LOOK AT, not what we surface within it.)

**Always-skip categories:** reactions / closures / emojis / "ok", newsletters / digests / calendar acks, community-broad asks, banter / moot / self-sent.

**Burst-tail exception (load-bearing):** before skipping a chat because its LATEST msg is a reaction/closure/banter, check the earlier msgs in the burst via `show-thread.js`. If there's an earlier actionable msg unacted-on, surface THAT one. Don't classify on the daemon's `text` field alone — it only exposes the latest line. Pairs with the group-burst-fetch rule in [[feedback_triage_24h_cap]].

**Why:** Stated by user during the actionable-definition review on 2026-05-18 — "ensure you check if behind these reactions/banter, etc. there is something that was sent before in that chat that is actionable."

**How to apply:** Encoded in `~/.claude/skills/triage/SKILL.md` step 3.1 (Gmail) + 3.2 (WA) + 3.3 (Slack). The priority-projects list lives in `[[context_user_life]]` under "Priority projects" and is read at classification time. The CDTM-onboarding-skip rule has been deleted from context_user_life since it's now a priority.
