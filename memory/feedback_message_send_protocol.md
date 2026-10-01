---
name: feedback_message_send_protocol
description: "How to send messages for the user — \"dsend\"/\"d send\"/\"d-send\" = draft my way + send immediately; quoted text = send verbatim; otherwise draft + clipboard + WAIT for confirmation before sending. \"Draft\" = a REAL draft in the platform's drafts folder (Gmail/Outlook), not just clipboard."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 275dd959-6416-4d79-9d30-55c651bd453e
  modified: 2026-08-03T02:11:48.258Z
---

Protocol for sending any outbound message on Alessandro's behalf (WhatsApp, email, Slack, LinkedIn, any channel):

- **"dsend" / "d send" / "d-send"** (direct send) appears in the request → draft the message myself (my wording, channel-appropriate, honoring any instructions in the request) and **SEND immediately**. No prior review, no waiting.
- **Content in quotes `"..."`** → that quoted text is the EXACT message. Use/send it **verbatim**, do not rephrase. Combined: `dsend "exact text"` → send that exact text immediately.
- **Neither of the above (DEFAULT)** → draft the message, show it in chat, AND copy it to the clipboard via `Set-Clipboard`. Then **STOP and wait**. Only send after an explicit go-ahead ("go", "send", "go send", or similar). Do not send on my own initiative in this case.

**"Draft" means a REAL draft in the platform's drafts folder whenever a draft mechanism exists — NOT just clipboard text.** When the user says "draft an email / message", create the actual draft via the platform helper so it shows up in their drafts:
- Email (lobbly / cdtm) → `gmail.py draft --account <lobbly|cdtm> --to … --subject … --body-file …` (use `--body-file` for multi-line; call `python.exe` directly, not the .cmd shim, to avoid mangling). See [[reference_triage_operations]] / [[reference_triage_v2_reply]].
- HEC Outlook → `outlook.py draft` (see [[reference_hec_outlook]]).
- WhatsApp/Slack/LinkedIn have no draft folder → clipboard-only is the correct "draft" there.
Clipboard copy is ADDITIVE, never a substitute for a real draft when the platform supports one. Caught 2026-06-02: said "draft" for a lobbly email but only clipboarded it; user expected it in Gmail drafts.

**Why:** Established 2026-06-01. Alessandro often knows he wants something sent without checking my exact wording (→ dsend), but also wants the option to review/edit when he hasn't decided the wording. The clipboard copy in the default case is so he can grab the draft himself — copy-paste, tweak it, paste it back or send from the app directly — instead of round-tripping every edit through me.

**"GO" PROTOCOL (added 2026-08-02, Telegram lane):** when Alessandro swipe-replies **"Go"** to a message that contains a suggested response (a 💬 draft on a notification card, a draft I posted in chat), that suggested text is SENT immediately, verbatim, to that message's person/channel — same force as dsend. Resolve WHICH message via the Telethon resolver ([[reference_tg_reply_resolver]]). **"Go" + comments** = do ONE revision incorporating the comments, then push it as a numbered approval-hub card (notify) for his tap — never send directly in that case. If a direct send is classifier-blocked, route it as an approval-hub `wa-send` card (proven ~30s round trip); never bypass. The auto-mode classifier judges per-command and can block sends to first-time recipients — the standing fix is a user-added allowlist line (see task-land `_system/ALLOW-RULE-FOR-GO-SENDS.md`); I must never edit permission rules myself.

**THE DEFAULT'S SURFACE IS THE APPROVAL-HUB, NOT A CHAT DRAFT (corrected 2026-08-03).** When the default (draft + wait) applies and the ask is a real person-affecting send, `POST /pending` to the hub with `notify:true` and the `wa-send`/`slack-send` action — that is what produces the numbered `#N` card, the 🟣❓ TG ping AND the MacroDroid phone popup, so he can tap yes/no from any device. Posting the draft as Telegram text only is NOT fulfilling the default: he gets no phone request and no numbered handle. Burned 2026-08-03 — asked "send a message to Caleb", I posted a chat draft, he asked "how come I didn't receive a MacroDroid request?" The hub was up the whole time and its queue was empty. Clipboard copy stays additive. See [[reference_approval_hub]].

**How to apply:** Applies to ALL outbound message channels. `dsend` = skip review + send now. Quotes = verbatim content. Default = draft + clipboard + await confirmation; the confirmation gate overrides the global "no confirmations" preference for sends specifically. This replaces the deleted WA close-style clipboard rule. Distinct from [[feedback_clipboard_all_paste_drafts]], which covers pasteable drafts generally (essays, form fields, builder prompts) — this one is specifically the send-a-message confirmation gate.
