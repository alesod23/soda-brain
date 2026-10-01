---
name: reference_lby_dead
description: The lobbly (@lby) Gmail account is DEAD as of 2026-07-02 — removed from triage + SODANOtif; those tools are now cdtm-only for Gmail.
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6ae8a5d1-8ed7-4951-926a-c95e51082ad5
  modified: 2026-08-02T22:20:43.913Z
---

The **lobbly Gmail account (`@lby`) is dead** — Alessandro no longer has access to that mailbox (told me 2026-07-02). It has been **removed from the fetch/label paths** of both inbox tools:
- SODANOtif: `recap.ps1`, `watch.ps1` (fetch calls + blob fields), `lib-format.ps1` (the `@lby` source-label mapping), `bot.js` (help text).
- /triage: `triage/fetch-all.js` (was `["cdtm","lobbly"]` in 5 spots → now `["cdtm"]`).

So **Gmail = cdtm only** now for triage/SODANOtif. Any older memory that says "Gmail cdtm+lobbly" or "@lby" (e.g. [[reference_sodanotif]], [[reference_triage_gmail]], [[reference_triage_operations]], [[feedback_sodanotif_card_format]]) is **superseded on the lobbly point** — do NOT re-add lobbly. `gmail.py` itself is account-agnostic (still takes `--account`); only the account LISTS were changed, and the lobbly OAuth token file was left in place (harmless once unreferenced).

**Correction (verified live 2026-08-02): token filenames ≠ mailbox.** Ran `gmail.py whoami --account <x>` on every token in `triage/tokens/`:
- `cdtm.json` → **alessandrosodano23@gmail.com** (personal, NOT the cdtm.com mailbox)
- `sodano23.json` → alessandrosodano23@gmail.com (same mailbox as `cdtm` — duplicate)
- `lobbly.json` → **alessandro.sodano@cdtm.com** (re-authed 2026-07-31; no longer the dead @lby box)
- `tundra.json` → alessandro@tundrahealth.ai · `alesoda2002.json` → alesoda2002@gmail.com

So the `--account` label is a filename, not a promise. **Always `whoami` before any send** — sending "as cdtm" actually sends from a personal Gmail. All five refresh silently (no interactive login).

NOT removed: `daemon.js` still lists "Lobbly" as a WhatsApp *project-relevance* keyword — that's the Lobbly PROJECT (see [[project_lobbly]]), not the email account. Only revisit if the project itself is confirmed dead.
