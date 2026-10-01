---
name: feedback_verify_agent_capability_claims
description: "A subagent's \"X is not possible / the platform has no trigger for that\" is a claim to verify, not a fact to relay; check the vendor changelog before designing around a limitation"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-02T21:50:38.334Z
---

On 2026-09-02 the Notion build agent reported "no Notion trigger fires when an AI Meeting Notes summary finishes", and I relayed it as fact and designed a daily 20:00 sweep around it. Alessandro asked "why would it not fire?"; a 30-second search showed Notion shipped the **"Meeting note summarized"** custom-agent trigger on 2026-07-31.

**Why:** an agent's negative capability claim ("cannot", "no trigger", "the API does not support") is usually reasoning from a mental model, not a test. Designing a workaround around a phantom limitation costs a real feature (here: live intake instead of a day-late sweep).

**How to apply:** before accepting any "not possible on platform X" from a subagent (or from myself), run one cheap discriminating check: vendor release notes / help page for the last 3 months, or a direct API probe. Report it as "unverified claim" if the check was not done. Related: [[feedback_diagnose_before_naming_root_cause]], [[reference_notion_tundra_system]].
