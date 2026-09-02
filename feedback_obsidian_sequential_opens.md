---
name: feedback_obsidian_sequential_opens
description: "Opening multiple vault .md files in Obsidian — fire the obsidian:// URIs sequentially with a delay, never back-to-back, or only the first opens."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 243c6c95-af00-4d7d-9473-e22e4412d202
---

When a run produces **multiple** vault `.md` files to auto-open (e.g. `/audio-to-notes` with two recordings, a `/dump` that writes several notes), fire the `obsidian://open?vault=…&file=…` URIs **one at a time with a ~1.5s `Start-Sleep` between them** — never two `Start-Process` calls back-to-back.

**Why:** Obsidian is a single-instance app. Two (or more) `obsidian://open` URIs arriving with no gap get debounced — only the FIRST is processed, the rest are silently swallowed. Caught 2026-06-10: `/audio-to-notes` wrote two notes, fired both opens immediately, only part 1 opened.

**How to apply:** Loop the opens with a delay (the rare sanctioned blocking sleep — required for correctness):
```powershell
$names = @("06-10 note one.md", "06-10 note two.md")
foreach ($n in $names) {
  Start-Process "obsidian://open?vault=vault_kb&file=Raw/$([uri]::EscapeDataString($n))"
  Start-Sleep -Milliseconds 1500
}
```
Applies to ALL vaults and ALL skills/sessions that auto-open vault markdown ([[reference_kb_systems]], [[reference_vault]], [[reference_kb_vault]]). The `/audio-to-notes` SKILL.md step 5 already encodes this; replicate the pattern anywhere else that opens >1 note at once.
