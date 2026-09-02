---
name: feedback-lemlist-badge-detection
description: "The LinkedIn lemlist badge \"Not added to lemlist\" contains \"added to lemlist\" — always test the negative first when detecting campaign channel."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6c32b433-096b-4c00-9d06-03e5f167f558
---

When detecting whether a LinkedIn contact came via a **lemlist** campaign vs a **coattio** DIY one, the page badge (injected by the lemlist extension) reads either **"Added to lemlist"** or **"Not added to lemlist"**.

**BUG to never reintroduce:** the string "Not added to lemlist" *contains* "added to lemlist" (a space is a `\b` word boundary), so a regex like `/added to lemlist/i` (or `/\bAdded to lemlist\b/i`) matches the NOT-added case and misflags a DIY lead as lemlist.

**Why:** caught 2026-07-02 — Zakaria Baid showed "campagne lemlist" in the coattio widget while LinkedIn said "Not added to lemlist".

**How to apply:** ALWAYS test the negative first and return, then the positive:
```js
if (/not\s+added\s+to\s+lemlist/i.test(text)) via = "coattio";
else if (/added\s+to\s+lemlist/i.test(text)) via = "lemlist";
```
Lives in `medtech-capture-extension/background.js` (Alt+Shift+M widget) → `outreach_via` field. See [[reference_outreach_system]].
