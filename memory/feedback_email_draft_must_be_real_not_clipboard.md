---
name: ""
metadata: 
  node_type: memory
  originSessionId: 2128ab65-69ab-46de-9e4c-680c11ed4fc3
---

> **2026-09-02: COMET ABANDONED — every "Comet" below now means CHROME (the default browser). See [[feedback-browser-chrome-default]].**

When asked to "draft an email" (to anyone, for any purpose), the deliverable is a REAL
platform draft — `mcp__claude_ai_Gmail__create_draft` — auto-opened in Comet via
`Start-Process "https://mail.google.com/mail/?authuser=<account>#drafts/<id>"`. This is TIER 0
in [[feedback_output_delivery_rules]] and was already documented before this miss — the failure
was not missing a rule, it was defaulting to the generic "pasteable draft" path (write a .txt,
`Set-Clipboard`, done) instead.

**Why:** On 2026-07-12 I drafted a Chris email as a scratchpad .txt file copied to the clipboard
instead of a real Gmail draft. The user caught it: "why didn't you open the draft email? you are
supposed to always — how come?" No email client ever opened because no real draft was ever
created. Root cause: when a recipient isn't trivially known (search needed first), it's tempting
to fall back to "just give them text to paste" — that fallback is wrong. Resolve the recipient
first (Gmail `search_threads` by name/context), THEN create the real draft. Only skip the real
draft if no Gmail account plausibly applies (e.g., a platform with no API access, like a
LinkedIn DM) — in that case clipboard+text is correct, per the normal message-send gate.

**How to apply:** Any time the task is "draft/write an email" — regardless of channel context
(Telegram, terminal, mid-conversation aside) — treat it as TIER 0 email-draft behavior, not
generic clipboard-draft behavior. Checklist before calling anything "done":
1. Recipient resolved (search Gmail threads/CRM if not given directly — never guess/fabricate).
2. `create_draft` actually called this turn (real draft ID returned).
3. `Start-Process` opened the draft's Gmail URL this turn.
4. Only THEN say "drafted" — the word is a lie if steps 2–3 didn't run.

This applies across sessions/chats, not just this one.
