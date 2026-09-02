---
name: feedback_open_wa_web_in_comet
description: "To OPEN WhatsApp for the user, ALWAYS open web.whatsapp.com in the default browser (= CHROME since 2026-09-02, Comet abandoned) — NEVER launch the WhatsApp desktop app."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6ae8a5d1-8ed7-4951-926a-c95e51082ad5
  modified: 2026-09-01T22:34:13.777Z
---

**2026-09-02: Comet ABANDONED — the default browser is CHROME now ([[feedback-browser-chrome-default]]). Everything below reads "Chrome" wherever it said "Comet"; WA Web needs a fresh QR scan in Chrome on first open.**

When the user asks me to **open WhatsApp** (to view/open a chat, e.g. "open the WA BMW chat"), ALWAYS open **`https://web.whatsapp.com/`** so it lands in his daily-driver browser via the OS default handler — `Start-Process "https://web.whatsapp.com/"`.

**NEVER** launch the WhatsApp **desktop app** (`whatsapp://` / the Store app). He finds WA Web on Comet much simpler/lighter and does not want the desktop client opened.

**Why:** On 2026-07-02 I opened the WhatsApp desktop app (I'd wrongly inferred "desktop" from an earlier offhand "I'm also connected on WA desktop app" — that was situational info, NOT a preference for how to OPEN chats). He corrected it firmly and wants this to hold across all sessions.

**How to apply:**
- "open WhatsApp" / "open the WA <X> chat" → `Start-Process "https://web.whatsapp.com/"` (opens Comet). Note WA has no deep link to a specific group by internal jid, so it lands on the chat list and he taps the group.
- Do NOT `Start-Process "whatsapp://"` or launch the Store/desktop app.
- This is the user opening his own daily browser to a URL (NOT browser automation), so the Chrome-for-automation rule does not apply — Comet is correct here. Consistent with [[feedback_output_delivery_rules]] (HTML deliverables auto-open in Comet). Related: [[feedback_browser_chrome_default]], [[reference_wa_sender]].
