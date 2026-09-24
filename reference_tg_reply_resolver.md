---
name: reference_tg_reply_resolver
description: "Telethon user-session resolver for Telegram swipe-replies — how to see which message the user quoted (the plugin drops it); on-demand script, no daemon."
metadata: 
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-08-03T21:54:18.177Z
---

`C:\Users\Alessandro\.claude\tg-reply-resolver\` — built + authorized 2026-08-02. Solves the plugin limitation where swipe-replies arrive as bare text ([[feedback_telegram_ordinal_message_reference]] context): a **Telethon user-session** logged in AS Alessandro (+393459764713, no 2FA, api creds in `~/.env/tg-user-api.env`, app "monitor Claudio al tg 3") reads his dialog with `Claudio_al_TG_v3_bot` exactly as his app sees it.

**AUTOMATIC since 2026-08-02** — discretion was the bug (I answered a swipe-reply blind even though the tool existed, because the rule said "run it when it *smells* like one"). Now a **`UserPromptSubmit` hook** in `~/.claude/settings.json` (exec form, full python path, timeout 12) resolves it before I read anything. Two files, split on purpose:
- `~/.claude/hooks/tg-reply-context.py` — the gate. Imports **only `sys`**; every prompt of every session pays its parse cost.
- `~/.claude/hooks/tg_reply_context_impl.py` — the work. Imported only on Telegram turns, so it gets a cached `.pyc` instead of being re-parsed. Imports `resolve.py` for `BOT`/`SESSION`/`load_env`, so the bot name lives in exactly one place.

**Measured on this machine** (don't re-guess these): non-Telegram prompt ~350-380ms, which is essentially `python.exe` startup (bare `python -c pass` = 260ms). Telegram prompt ~1.6-1.8s internal: telethon import ~410ms + MTProto connect ~830ms + fetch ~180ms. Connect and import are the floor without a resident daemon. **`sh` (~385ms) and `node` (~300ms) were both benchmarked as gate runtimes and neither beats Python here** — don't retry that idea.

Three gotchas, each burned once:
- **The gate matches RAW stdin, where the payload is JSON-escaped** — it arrives as `source=\"plugin:telegram:telegram\"`. A marker containing `"` silently never matches and the hook no-ops with exit 0. Marker is quote-free (`plugin:telegram:telegram`) for that reason.
- `resolve.py` rebinds `sys.stdout` at import, closing any wrapper the caller made — the hook writes its JSON with `os.write(1, ...)`.
- An 8s internal `asyncio.wait_for` deadline sits under the 12s hook timeout, so a dead network degrades to "no quote" instead of stalling the turn. Verified by forcing `DEADLINE_S = 0.05`.

Log (has per-run timings, use it to spot drift): `~/.claude/hooks/tg-reply-context.log`.

**KNOWN HOLE (found 2026-08-03): mid-turn messages are NOT resolved.** `UserPromptSubmit` fires only
for the message that STARTS a turn. A Telegram message that arrives while I am already working shows
up as a system notification with no hook context, so its swipe-reply target is invisible. That is how
I missed that a bare "Yes" was approving approval-hub card #11 — he had to tell me. **When a message
arrives mid-turn and is bare/ambiguous ("Yes", "go", "no", an ordinal), run `resolve.py --last 15`
BY HAND before acting on it.** Fixing this properly needs a resolve step on mid-turn arrivals, which
the hook cannot currently express.

**Manual fallback** (hook disabled, or checking history): when a bare inbound smells like a swipe-reply, run
`C:\Users\Alessandro\AppData\Local\Programs\Python\Python312\python.exe C:\Users\Alessandro\.claude\tg-reply-resolver\resolve.py --last 15`
→ JSON with per-message `reply_to_msg_id` + `quoted_text` (also `--msg-id N`). Connect ~2s, no daemon, no watchdog, nothing to maintain.

**Gotchas (verified):**
- **ID spaces differ**: the plugin's `message_id` (bot-API, e.g. 1705) ≠ Telethon's ids (user MTProto view, e.g. 2876) for the SAME message. Correlate by text + timestamp, never by id.
- **Login codes die if pasted plainly in any chat** (Telegram anti-phishing) — during (re)login have him send the code SPLIT ("9 4 9 1 1"); strip non-digits. `login.py request --phone` / `confirm --code` are non-interactive for exactly this flow.
- Session = `user.session` file next to the scripts; revocable from Telegram Settings→Devices; portable to a future VPS (DA SYSTEM phase 2) like the WA auth folder.
- History is server-side → quotes resolve RETROACTIVELY after laptop-off gaps, better than the plugin's live-only view.

## Searching the WHOLE bot history (added 2026-09-24)

The resolver's session is also a full-text archive: use it when he asks "what was that thing I
sent you?" and the local corpus has nothing. On the box, 4,115 messages scan in about 40 seconds.

**Interpreter:** `/home/da/voice-lane/venv/bin/python`. **Telethon is NOT in the triage venv**, and
the bare `python` fails with `ModuleNotFoundError: telethon`. Run from `/home/da/tg-reply-resolver`
so the `user.session` file resolves.

```python
from telethon import TelegramClient
from pathlib import Path
env = {k.strip(): v.strip() for k, v in
       (l.split("=", 1) for l in (Path.home()/".env"/"tg-user-api.env").read_text().splitlines()
        if "=" in l and not l.strip().startswith("#"))}
c = TelegramClient('user', int(env["TG_API_ID"]), env["TG_API_HASH"])
# async for m in c.iter_messages('Claudio_al_TG_v3_bot', limit=6000): m.out is True when HE sent it
```

**What actually finds things:** he rarely uses the words you would search for. Searching
"personal assistant" over the whole history returned only his own question. What worked was
**listing every DOMAIN he ever sent**, excluding the noise (claude.ai, google, linkedin, t.me),
and reading the message around the one that looked like a product. That is how Kortyx was found.
Do the domain sweep first, the phrase search second.

Related: [[project_da_system]].
