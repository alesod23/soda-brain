---
name: feedback_rule_requests_are_binding
description: "When he says \"this is a rule\" / \"make this a rule to remember\", write the memory THAT TURN and confirm it back by name — do not treat it as conversational context."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 26333c6f-5f43-43b7-badf-07594a1db485
  modified: 2026-08-05T20:28:15.983Z
---

**Standing meta-rule (set 2026-08-05, on Telegram):** when Alessandro says any of *"this is a
rule"*, *"make this a rule"*, *"make this a rule to remember"*, *"remember this"*, *"always/never
do X from now on"* — that is a **binding instruction to write a memory file in the same turn**, not
a preference expressed in passing. Then say back, in the reply, which memory it landed in.

**Why:** he has repeatedly stated rules and then watched them not exist. His words: *"sometimes I
tell you 'this is a rule' on TG and I don't see it becoming one … I want you to take it more
seriously."* From his side a rule that was acknowledged but not written is indistinguishable from
one that was ignored — worse, he stops trusting that stating a rule does anything, so he has to
re-state it, which is exactly the cost the memory system exists to remove. The failure is never
disagreement; it is the rule getting handled as chat and dying with the context window.

**How to apply:**
1. **Write it before finishing the turn.** Not "later", not "if it comes up again" — the standing
   guidance to check for duplicates first still holds, but the default is write, not defer.
2. **New file, or edit the existing one** if a memory already covers that area (e.g. a Telegram
   rule goes into the Telegram memory). Add the `**Why:**` — a rule without its reason decays into
   something I feel free to reinterpret.
3. **Add the MEMORY.md index line** in the same turn. A memory that is not indexed is not recalled.
4. **Confirm by name in the reply**: "saved as `feedback_x`" — that is his receipt that it stuck.
5. **If the rule is mechanical and I keep decaying on it, move it out of memory into the harness**
   (a hook, a config file, a script default). This is the proven fix: the 👀-reaction rule decayed
   across three sessions as a memory instruction and only became reliable once it was a
   `UserPromptSubmit` hook — see [[feedback_react_eyes_before_working]]. Ask whether a rule can be
   made structural rather than remembered; prefer structural every time.

Related: [[feedback_output_delivery_rules]], [[feedback_message_send_protocol]],
[[feedback_laptop_startup_clean]].
