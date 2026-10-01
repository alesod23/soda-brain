---
name: feedback_kb_split_needs_bridge
description: "When splitting content out of a vault into its own standalone KB, don't default to full isolation — ask/design for a query-time bridge back unless the user explicitly wants the content to go dark. Use when spinning off a new vault from an existing one."
metadata:
  node_type: memory
  type: feedback
  originSessionId: unknown
---

# Splitting a vault out ≠ isolating it — build the bridge back by default

**What happened:** Alessandro asked to split MPD course-project content out of `vault_kb` into a new standalone vault (`mpd-kb`) because it was polluting his personal wiki with ~90 transient discovery-call notes from a course ending in about a week. The first design declared `isolation: true` / `bridge: disabled` for the new vault — a reasonable-looking default given the precedent (self-reflection-wiki and 07-thesis-kb are both fully isolated spin-offs). Alessandro pushed back: *"I wanted my vault to have this knowledge... I need to be able to query my personal wiki... and through it query the MPD LLM wiki as well."*

**Why it happened:** I conflated two different reasons a vault gets split out — (a) genuinely private/sensitive content that must never leak sideways (self-reflection-wiki), and (b) content that's just too large/domain-specific/short-lived to live in the main wiki but is still information the user wants reachable. Only (a) calls for full isolation. I defaulted to the isolated pattern because it was the most recent precedent in the codebase, without checking which reason actually applied here.

**How to apply:** When spinning a new vault out of an existing one, default to a **bridge back** (a `MPD:STATE`-style tracker block written by the new vault's `/kb-maintain`) plus a **read-only query-time join** (so `/kb-query` on the origin vault can reach into the new vault when its own coverage is thin) — UNLESS the content is private/sensitive in a way that demands true isolation. Ask, or infer from context, which case it is before defaulting to `isolation: true`. This led to building a new generalizable capability: `related_vaults` on `/kb-query` (distinct from `bridge`, which is write-time, and `task_join`, which is task-land-only) — see [[reference_kb_systems]]. Full design + rationale logged in the KB systems doc's v14 changelog entry.
