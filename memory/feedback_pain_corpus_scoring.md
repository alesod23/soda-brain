---
name: feedback-pain-corpus-scoring
description: "How to score practitioner pain corpora (e.g. /opinion-research) so the dashboard surfaces real startup gaps, not minor feature asks or actively-rejected ideas."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fb69d9f0-ecb2-4638-8cb0-03c6aba72187
---

When building a pain corpus to find startup-shaped gaps (worked example: `[[project-langfuse-pains]]`), score with these rules, not the SKILL.md defaults:

- **Exclude, do not boost, "vendor will fix"**: drop stories where the vendor said they shipped/will ship/are building (status shipped/committed). Don't keep them with a negative weight; just remove them.
- **`langfuse-wont-fix` / actively-declined is NOT a scoring bonus**: silence or "we'll consider" or "beyond our scope" is actually a *better* signal than active rejection. Active "we don't think it's useful" means the vendor has thought about it and chosen — that's a smaller surface to play in.
- **Deprioritized / stale-closed gets a small positive (+3)**: shows the vendor doesn't care enough to act, leaves room.
- **`no-known-fix` stays a strong positive (+15)**.
- **Engagement is the primary signal**: upvotes + comments + reactions, log-scaled, up to 40 points of the score. Add a sort-by-upvotes UI on top so the user can override the composite if wanted.
- **"Doing/improving the workflow" beats "monitoring the workflow"**: small bonus (+6) for tags like `agents`, `multi-step-agents`, `evals`, `prompt-mgmt` — the user's product hypothesis was about acting on AI workflows, not just observing them.
- **Minor feature asks self-sink** under engagement-weighted scoring (they get 0-2 upvotes) — no extra penalty needed.

**Why:** Initial Langfuse run had avg score 50.9, dominated by hundreds of `langfuse-wont-fix`-tagged items that were getting +15 each. User feedback 2026-05-18: "i dont think langfuse-wont-fix is a scoring, rather we should just exclude the ones they said they will implement. maybe signal still if deprioritized." After recalibration: avg 37.9, top 5 are all real high-engagement open questions where Langfuse is silent or said no.

**How to apply:** for any new `/opinion-research` run that produces a pain corpus from vendor-owned forums (GitHub Discussions/Issues, Discourse, vendor Slack archives), build a `recalibrate.py` stage between merge and render that: (1) classifies vendor response status from the captured maintainer text, (2) excludes shipped/committed, (3) recomputes score with engagement as the dominant term. Surface engagement prominently in the card UI; expose a sort dropdown. See `~/.claude/research-corpora/langfuse-pains/recalibrate.py` for the working reference implementation.

## Round 3 (2026-05-18, after second user feedback)

User clarified the *purpose* of the corpus: when the goal is "find untapped startup opportunities adjacent to an incumbent's product," the corpus must filter out feature-requests-for-the-incumbent's-product, even high-engagement ones. The user is not looking to build a better Langfuse — they're looking for the workflows Langfuse users want but Langfuse won't provide because it's outside Langfuse's product surface.

**The rule:** classify each story by `focus` along a binary, not a spectrum:
- **`obs-feature`** (or analogous "improve the incumbent's product"): user wants a fix/feature on the incumbent's existing surface (UI, SDK, infra, integrations, internal feature behavior, framework tracing support). These are *uninteresting* for startup hunting — building them = competing on the incumbent's home turf.
- **`beyond-obs`** (or analogous "go beyond the incumbent's product"): user wants a workflow the incumbent isn't built for: act on the data, improve the agent, evaluate decisions (not just track them), training-data pipelines, feedback loops, simulation, canary/rollback/guardrails, capability management (skills, tools, agents as first-class), trace-to-diagnosis.

**Default to obs-feature**, not neutral. Every pain mined from the incumbent's GitHub/Reddit IS about the incumbent unless explicitly otherwise. A `neutral` middle bucket sounds reasonable but in practice 100% of "neutral" stories were obs-feature mis-flagged. Binary is cleaner and forces honest classification.

**Patterns to lock in:**
- Beyond-obs is *text-pattern-driven only*, with HIGH precision. The patterns must be specific phrases like "manage tools the same way as prompts", "trace-to-diagnosis", "first-class tool registry", "feedback loop", "rollback the prompt", "canary", "guardrail enforcement", "simulate end-to-end flow". Generic words like "improve" alone are NOT enough.
- Apply -25 penalty to obs-feature, +15 to beyond-obs. Hide obs-feature in the dashboard by default; expose a toggle.
- Drop tag-based bonuses like `agents`/`evals` from the score — those tags are too ambiguous; rely on focus classification instead.

**Expected corpus shape:** in a 400-story corpus from a vendor's own forums, expect 1-3% beyond-obs (5-15 stories) and 97%+ obs-feature. That's the right ratio. If your beyond-obs count is >5%, your patterns are too permissive; if 0, too tight. Sanity-check by hand-reading the top 10 beyond-obs and the top 10 obs-feature to confirm classification.
