---
name: project-langfuse-pains
description: "Langfuse user-pain corpus mined for ex-Langfuse-founder startup gaps. Engagement-weighted scoring, vendor-fix-committed items excluded. Dashboard rebuilds idempotently."
metadata: 
  node_type: memory
  type: project
  originSessionId: fb69d9f0-ecb2-4638-8cb0-03c6aba72187
---

Corpus path: `C:\Users\Alessandro\.claude\research-corpora\langfuse-pains\`
Dashboard: `C:\Users\Alessandro\OneDrive - HEC Paris\langfuse research\langfuse-pains-dashboard.html`

Sources mined: GitHub Discussions (52), GitHub Issues (305), Reddit r/LocalLLaMA + r/AI_Agents + r/LangChain (17), Hacker News (26). SDK repos explicitly excluded per user instruction.

Pipeline (all idempotent):
- `reports/stories-*.json` — raw per-platform extractions, one per subagent
- `merge.py` — dedupes by source_url, then (name, pain-prefix-80)
- `recalibrate.py` — classifies `lf_status` from `langfuse_response` text, excludes shipped/committed, recomputes score with engagement weighting (see `[[feedback-pain-corpus-scoring]]`)
- `render.py` — self-contained HTML dashboard with sort dropdown (score/engagement/upvotes/comments), status + tag + platform filters
- `rebuild.ps1` — runs all three; safe to re-run any time new reports/ files land

**Why:** Alessandro + Caleb are exploring an AI observability/improvement startup informed by ex-Langfuse-employee context. The pain corpus surfaces where Langfuse users are stuck AND Langfuse isn't fixing it. User's central hypothesis (2026-05-18): the gap is in *improving* AI workflows (right tool calls, agent trajectories, eval-driven iteration), not just monitoring them.

**How to apply:** when iterating with the user on this thesis: (1) add new sources by dropping `stories-<platform>.json` into `reports/`, then `rebuild.ps1`; (2) the dashboard is the source of truth, not the JSON — always re-render after data changes; (3) for related upstream startup-hypothesis work, see `[[project-lobbly]]` (different domain but same opinion-research methodology pattern); (4) scoring rules: `[[feedback-pain-corpus-scoring]]`.

**As of 2026-05-18, the 5 beyond-obs stories** (the gold subset; everything else is "improve Langfuse-as-observability" and is hidden by default in the dashboard):
1. *leothirdopinion* (score 75) — Skills repository: manage agent skills the way Langfuse manages prompts. `agentskills.io` standard. Beyond observability because it's about *capability management*, not tracing.
2. *nikothomas* (score 68) — Tool management interface: first-class tool registry, separate from prompts. Same theme: agent capability as a managed resource.
3. *Future_AGI* (score 66) — Trace-to-diagnosis gap: "every step visible, but during incidents we still ended up staring at a clean trace and guessing what actually caused it." Wants automated root-cause from observability data.
4. *FinanceSenior9771* (score 61) — Operational tooling for agents: canary, rollback, guardrail enforcement. Beyond dashboards.
5. *Educational-Bison786* (score 55) — End-to-end flow simulation + safe version testing. Pre-prod testing infra for agent workflows.

**Four distinct opportunity clusters in 5 stories:** capability management (1+2), automated diagnosis (3), production ops for agents (4), pre-prod simulation (5). Each is a defensible product category that Langfuse explicitly doesn't address.

**If the user asks for more beyond-obs stories:** the corpus is saturated at this width. Options: (a) mine adjacent sources — AI engineering blogs, vendor case studies of LangSmith / Braintrust / Maxim / Arize / Helicone competitors, Twitter/X, AI Engineer conference talks; (b) widen the beyond-obs patterns carefully (risk: false positives that re-introduce obs-feature noise — verify by hand-reading top 10).
