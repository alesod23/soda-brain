---
name: feedback_design_on_merit_not_his_offhand_numbers
description: "His off-hand numbers and words ('20 a day', 'waterfall', 'weekly') are not specs: design on merit, size from measured load, never cap arbitrarily, never use Haiku for judgement (Sonnet minimum, Opus for anything that decides). He wants a powerful system that may take time: smart, non-blocking, not sucky (2026-09-24)."
metadata:
  type: feedback
---

**What happened (2026-09-24):** I designed the CRM reading layer with a "20 Opus reads a day" cap, a Haiku triage tier and a three-tier waterfall, each lifted from something he had said in passing. His correction: *"Why are we capping it to 20 a day? It was a completely arbitrary, just random number that I put off the top of my head... Haiku is very bad... It seems like you took too much of what I want, what I said. Instead, want you to use your own common sense a bit more. I'm not afraid for it to be a powerful system that actually takes a lot of time. I want it to be smart. Don't want it to freeze anything, don't want it to block anything, but I don't want it to suck either."*

**Why:** he thinks out loud in numbers and metaphors; turning them into hard parameters produces a system shaped by his guesses instead of by the problem. He also expects me to actually look at a reference he names (Kortyx), not to infer its design from his one-line description.

**How to apply:** treat his numbers as the order of magnitude he can live with, then size from measured load and say what the measurement was. No arbitrary caps: bounded concurrency and a visible queue instead. Model choice by the job: Opus where something is decided or written, Sonnet at most for classification, Haiku nowhere in his systems. When he names a product or a person as a reference, fetch and read it before designing. Ask myself "is this smart, does it block, does it suck" before "is this what he said".

Related: [[feedback_iterative_means_on_the_go_flag]], [[reference_kortyx_design_reference]], [[feedback_verify_agent_capability_claims]].
