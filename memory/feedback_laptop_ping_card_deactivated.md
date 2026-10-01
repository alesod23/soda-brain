---
name: feedback_laptop_ping_card_deactivated
description: POWERFUL RULE - laptop ping card is DEACTIVATED (not deleted). Phone keeps its popup; Telegram ALWAYS gets a complete approve card that recurs across sessions and chats
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bcf4ed36-d8ed-4e48-817b-146c5998e5ca
  modified: 2026-08-12T23:18:24.668Z
---

His words, 2026-08-10, twice in caps: *"IT NEEDS TO BECOME A POWERFUL RULE THAT SURVIVES EVERYWHERE EVERYTIME."*

**Why:** *"i always receive the ping card AND the tg notification at the same time anyway."* Two surfaces for one decision is noise. Telegram won because it reaches him anywhere.

## The rule
1. **Laptop ping card: OFF.** *"dont delete the ping card on laptop setup, but i want it deactivated."* Deactivated, **not deleted** — the code stays.
2. ~~**Phone: keep the popup.**~~ **SUPERSEDED 2026-08-12 — the phone is OFF too.** *"I've decided to cut the MacroDroid push from now on, at least until I change my mind. I think we should use Telegram as the one and only approved channel. Rule from now on."* Same treatment as the laptop: deactivated, not deleted.
3. **Telegram: ALWAYS, and COMPLETE.** Every card, decision line plus full context ([[feedback_ping_cards_must_be_full]]). **As of 2026-08-12 it is the ONLY surface**, so a Telegram failure is now a total failure — there is no second channel to catch it.
4. **It must recur, across different sessions and chats.** Not tied to whatever session created it.

## How it is implemented (`approval-hub/server.js`)
- **`const LAPTOP_POPUP_ENABLED = false`** — the single switch. `GET /next` returns empty when false, so `popup.ahk` keeps polling harmlessly and never draws a window. `popup.ahk`, `/resolve`, the dismissed-set persistence and the whole laptop lane are untouched and still work; **flip the flag to `true` and the old behaviour is back with no other edit.** `Push-Lane-Watchdog`'s LAPTOP_POPUP check still sees a live idle process, so nothing starts alarming.
- **`pushTelegram()` now fires for EVERY card, not just `notify:true` ones.** The laptop popup used to be the catch-all that displayed every pending item regardless of `notify`; with it stood down, a `notify:false` card would have reached nobody. Telegram is the guaranteed surface now.
- **The re-notify loop pushes Telegram as well as the phone** (every 5 min, up to 6 times). That loop lives in the hub, which runs under `Push-Lane-Watchdog`, which is exactly why the card keeps coming back with no chat open and after the originating session is gone. Never move this into a session.

- **`const PHONE_POPUP_ENABLED = false`** (added 2026-08-12) — the single switch for the MacroDroid phone lane, mirroring the laptop one. It gates the only two `fireMacroDroid()` call sites in `server.js`: the one in `POST /pending` and the one in the re-notify loop. `fireMacroDroid()`, `macroDroidBody()` and the whole `MD_MAX_LINES` / `MD_CHARS_PER_LINE` budget stay intact and correct; flip the flag to `true` and the phone lane is back with no other edit. Verified 2026-08-12: `node --check` clean, hub restarted (PID 4472), 5 pending cards survived. The approval-hub is the **only** live MacroDroid caller on the machine, so this one flag is the whole cut.

**Do not "fix" a missing approval by re-enabling the laptop or phone popup.** If a card is not reaching him, the fault is in the Telegram leg; diagnose that (see the runbook in [[reference_approval_hub]]).

Related: [[reference_approval_hub]], [[feedback_approvals_are_pings]], [[feedback_ping_cards_must_be_full]], [[feedback_ping_card_active_vs_passive]] (superseded, do not implement).
