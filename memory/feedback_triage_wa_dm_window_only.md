---
name: feedback-triage-wa-dm-window-only
description: "WA DM snippets must show ALL messages within the effective cutoff window (since last_check, max 24h), not last-4-regardless-of-age. Never trust daemon's `text`/`lastIn.text` field — it collapses document/image/video + caption into one line. Always fetch via show-thread.js with --since-unix."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 42b41e83-f5e1-452a-a4d1-20388bf99778
---

For /triage WA DM display:

- **OLD (wrong):** show last 4 messages for the chat, prefixed `←`/`→`, regardless of age.
- **NEW (correct):** show ALL messages with timestamp >= `effective_cutoff_unix` (= `max(last_check_unix, now - 86400)`). Drop older context messages entirely — they're noise. If the window is empty (only outgoing before the cutoff), still surface the chat if it qualifies; otherwise don't.

**Why:** the user explicitly said the old context messages from days ago are noise. The signal is only what arrived in the relevant check timeframe. Surfacing day-old text alongside today's new message reads like clutter.

**How to apply:**

1. Always use `node show-thread.js --jid <chatJid> --since-unix <effective_cutoff_unix>` (the `--since-unix` flag was added 2026-05-21; see [[reference_wa_sender]]).
2. NEVER trust the daemon's `text` field or `lastIn.text` for display — it collapses multi-part bursts. Concretely: `[document: ...]`, `[image]`, `[video]`, `[voice note]` placeholders may have a caption that the daemon used to drop (fixed 2026-05-21 for document, was already correct for image/video). Even with the fix, two separate consecutive messages (doc + text typed right after) live as 2 store entries — only the burst fetch shows them both. **Bug case 2026-05-21:** Guido sent `[document: IDEA 19-200526.pdf]` and the caption "Pagina 32 e colonna viola a pagina 33"; daemon stored only the placeholder. /triage missed the caption entirely. Daemon fix in `daemon.js:40` now appends `documentMessage.caption` and handles `documentWithCaptionMessage`. Won't backfill retroactively — only new messages after daemon restart benefit.
3. WA groups: same rule — show all in-window messages, not just last N.

Related: [[reference_triage_operations]] (display format), [[reference_wa_sender]] (daemon stack).
