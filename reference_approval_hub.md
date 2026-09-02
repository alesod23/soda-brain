---
name: reference-approval-hub
description: "The approval-hub (port 4180) is the canonical cross-device approve/reject system — how to queue an action for confirmation, and the behavior guarantees not to regress"
metadata: 
  node_type: memory
  type: reference
  originSessionId: b75b1302-8e9b-4e42-b796-f57031e2eebf
  modified: 2026-08-31T14:48:07.353Z
---

**`C:\Users\Alessandro\.claude\approval-hub\`** — always-on Node service (port 4180, `Approval-Hub-Watchdog` keeps it alive) that gates person-affecting actions behind a yes/no confirm across laptop + phone. `popup.ahk` (AutoHotkey, bottom-right laptop popup) polls it; phone reaches it over Tailscale at `https://desktop-1bojsrg.taile93f00.ts.net/approvals` (path prefix is stripped → hub root).

**To queue an action for confirmation:** `POST /pending` with `{text, context, notify, action}`.
- `notify:true` → fires a distinctive `🟣❓ APPROVA?` Telegram ping (emoji deliberately unlike the usual 🚨📬🎙️ SODANOtif cards) via `push.js` **and** the MacroDroid webhook (phone popup). The laptop popup shows every pending regardless of `notify`.
- `action` executes ONLY on approve: `{type:'wa-send', jid, messages:[...]}` (each message = its own WA message), `{type:'slack-send', workspace, to, text}` (via `slack.py send --confirmed`), or `{type:'gmail-send-draft', account:'cdtm', drafts:['r123','r456']}` (via `gmail.py send-draft --confirmed`, serial with a 700ms gap). Put the EXACT text (emojis, multi-message) in `text` so the popup preview is truthful.
- **ALWAYS attach `gmail-send-draft` to an email card (added 2026-08-05, his explicit instruction).** Email cards used to carry no action, so a YES tap resolved the card and sent NOTHING — it waited for a session to read the verdict back and send by hand. He approved the 3 photo-nudge emails from his phone at 05:10 and they sat unsent until he chased it 10 minutes later: *"by replying go an email will automatically go... so install it."* Verified end-to-end 2026-08-05 with a self-addressed draft: card queued -> resolved yes -> hub sent it with no session involved. It takes **draft IDs only** and never composes an email, so nothing can be sent that he did not already preview on the card — the no-fuzzy-send rule stays intact. **Do not attach it when the recipient address is unverified**; draft to himself instead and ask for the address on the card.
- First device to resolve wins (idempotent); the others dismiss (cross-device dedup).

**Behavior guarantees (do NOT regress — each cost a real incident 2026-07-23):**
- **Esc suppresses on the laptop for good.** `popup.ahk` keeps a `dismissed` Map; Esc/X adds the id so it is never re-shown on that laptop (the item stays pending for other devices/TG). Without this, a phone-confirm that hasn't reached the hub left the laptop popup re-popping forever.
- **Reject-with-feedback is never lost.** On `verdict:no` with typed feedback + an action, the hub fires a `🟣⚠️ Correzione ricevuta` TG ping with the feedback and writes `last-rejected.json`. The voice-lane links the user's next audio correction to that rejected suggestion (see [[reference_voice_lane]]). NOTE: a fully-automatic no-session re-draft (headless agent on reject) is intentionally NOT wired — the auto-mode safety classifier blocks auto-running a skip-permissions agent on the hub; the re-draft happens when a session processes the voice/TG follow-up.
- **"soda machine"** is the spoken GO password → the voice classifier treats it as absolute green-light (execute directly).

**Phone (MacroDroid) approval macro — correct wiring (verified 2026-07-23):** do NOT ship a hand-authored `.macro` file — the notification-buttons + HTTP-POST-body field schema is undocumented and MacroDroid imports a bad file broken/silently. Build steps instead (then the user can Export a real file): (1) pre-create two GLOBAL STRING variables `id` and `text` — webhook query params do NOT auto-become magic text, the webhook writes into pre-existing variables; (2) Trigger → Webhook (URL), identifier `claude-approve`; (3) Display Notification (High priority), text `[v=text]`, two buttons "✅ Sì" / "❌ No, vedi dopo", each → Run macro; (4) helper macro Claude-Yes → HTTP Request POST `https://desktop-1bojsrg.taile93f00.ts.net/approvals/resolve`, header `Content-Type: application/json`, body `{"id":"[v=id]","verdict":"yes","device":"phone"}`; (5) Claude-No identical with `"no"`. Magic-text syntax is `[v=name]` (NOT `{id}`/`[wh_param_id]`).

**THE PHONE MACRO AS IT ACTUALLY IS (seen in a screenshot 2026-08-03 — supersedes the build-steps above where they conflict):** the live "Claude Approve" macro uses **LOCAL** variables with `{lv=name}` syntax (NOT global `[v=name]`), and it is the **Write-to-File** variant: `Set Local Variable (Boolean) approve: [User Prompt]` → `If approve = True` → write `claude-verdict-{lv=id}-yes.txt`, else the `-no.txt`. The Tailscale `POST /approvals/resolve` wiring in the build steps above is a DIFFERENT design that his phone does not use — a file built from those steps would replace a working verdict path with the wrong architecture. (Superseded 2026-08-04 on the "never hand him a `.macro`" point: shipping a file is fine and he asks for it — but only ever by patching his own export, see below.)

**THE INVASIVE POPUP IS THE POINT — do NOT talk him out of it (2026-08-04).** On 08-03 I diagnosed `[User Prompt]` as the bug (a blocking dialog cannot draw over the lock screen without overlay permission) and pushed him to notification-only "Claude Ping". He hated it: *"the MacroDroid thing really just does notification… it was actually creating a pop-up, like an invasive pop-up window."* The dialog is a deliberate design choice, not a defect. **The real fix is the Android permission** — MacroDroid → *Display over other apps* — not removing the dialog. Rebuilt as `Claude Approve v2` (10 actions): sticky NotificationAction as a lock-screen fallback, `approve=false` reset, then the original User Prompt dialog and all the original if/else + verdict-file + Drive-move actions untouched.

**`approve` is a Boolean that keeps its previous value.** Cancelling the prompt does not clear it, so a cancelled card could be resolved with the STALE answer (suspected cause of card #13, the Tom Mannmeusel mentor email, being silently rejected). Fixed in v2 by an explicit `approve = False` SetVariableAction before the prompt.

**MacroDroid .macro files: build them by PATCHING his own exports, never hand-author.** Two hand-written files failed in one night (invented `m_identifier`, wrong nesting; then `m_text` instead of `m_notificationText` → blank card). His MacroDroid-authored exports live in `C:\Users\Alessandro\.claude\channels\telegram-v3\inbox\`:
- `1785807287929-AgADuhoAApAniVM.macro` — **"Claude Approve", the complex/original one** (WebHookTrigger → SetVariable userPrompt → If/WriteToFile ×2 → FileOperationV21 move to Drive `sodaos`). This is the canonical source to rebuild from.
- `1785817752417-AgADwhoAApAniVM.macro` — "Claude Ping", the only MacroDroid-authored `NotificationAction` schema available.
Build script: `scratchpad/build_claude_approve_v2.py` — asserts key-sets match MacroDroid's own output and that no SIGUID collides. **Still missing:** the schema for a Clear-Notification action and for `notificationActionButtons` entries — both are empty/absent in his exports, so remote dismissal of an already-shown phone card is NOT possible yet. Ask him to add one in the UI and export it back rather than guessing.

**Webhook identifier drifted to `claude-ping`** (`voice-lane/config.json`) on 2026-08-04 when the notify-only macro was introduced. `Claude Approve v2` keeps `claude-ping` so no hub edit is needed — name and identifier deliberately disagree.

**Diagnostic that settles "is it delivering?" in one shot:** `curl` the webhook directly — `https://trigger.macrodroid.com/4c4ead84-90a5-4ce1-912f-e4ef2993d2b0/claude-approve?id=X&text=Y`. It returned 200 OK for both a short and a 3,100-char payload, proving length is not a limit and the hub→cloud leg is healthy. Then ask him to open MacroDroid and read the `id`/`text` local variables: if they hold the latest card, delivery works and the problem is rendering, not transport.

**THE PHONE CARD IS TOP-DOWN, AND IT HAS A HARD HEIGHT CEILING (2026-08-04).** He wants the phone
popup to be the FULL artifact: decision line first, then the whole email/event/reasoning underneath,
so he can approve without opening the laptop. Before this the hub sent only `text` to the phone and
`context` never left the laptop, which is why the popup felt empty. `macroDroidBody()` in `server.js`
now composes `text` + `---- CONTEXT ----` + `context` for the phone only — the TG ping and the AHK
popup deliberately keep the short `text`.
Two ceilings, both measured, both real:
- **Transport:** `trigger.macrodroid.com` returns 200 up to ~4000 encoded query chars, 400 at 5000, 414 at 10000+.
- **Rendering (the binding one):** the User Prompt dialog GROWS to fit its text instead of scrolling in a fixed frame, and past a certain height **the Yes/No buttons disappear entirely** — the card becomes unanswerable. Calibrated live: 43 lines of real prose came back with a tapped verdict (`claude-verdict-CALIBC-no.txt`); 73 lines had no buttons. `MD_CHARS_PER_LINE = 28` (measured off his screenshot).
**RE-CALIBRATED 2026-08-05 21:36 → `MD_MAX_LINES = 58` (applied 2026-08-06).** A 58-line prose card (id `CALIB58`, 1662 encoded chars) fired straight at the webhook came back **tapped yes** (`claude-verdict-CALIB58-yes.txt`); he confirmed he could scroll to the final line with the buttons reachable. The session that ran the test never applied the result — the cap sat at 43 for a day while cards were being truncated for no reason. **Unknown territory is 59..73; push further only with another CALIB card he actually taps.** Scrolling was never the constraint (a 3000-char body already scrolled with buttons); *button visibility* is.
**The cut marker used to LIE.** It said "full text on the laptop popup", but `GET /next` returns only `"<id>\n<text>"` and `popup.ahk` renders exactly that — `context` has never reached the laptop, so the trimmed remainder existed nowhere readable. Marker now reads `[cut - reply "rest" and I paste the remainder]`. **Still open:** teach the popup to fetch context (needs a new `/context/<id>` endpoint + a `popup.ahk` change, i.e. a change to the guarded laptop lane — propose it, do not slip it in).
Height, not byte count, is what matters: a newline costs 3 encoded chars but a whole display line, so
a long run of one unbroken token is cheap and normal prose is expensive. Only `context` is trimmed,
never the decision line; overflow gets `[cut here - full text on the laptop popup]`. **Producers must
keep `text` to the decision and put the artifact in `context`** — card #12 inlined a whole email into
`text` (3132 chars, 113 lines) and was unanswerable on the phone; `macroDroidBody` now clamps the head
too as a backstop.

**THE LAPTOP POPUP LANE — how it works and how to fix it (2026-08-04). READ THIS BEFORE TOUCHING IT.**
`popup.ahk` (AutoHotkey v2, `#SingleInstance Force`) polls `GET /next` every 1.5s and shows a
bottom-right GUI titled **`Claude asks`**. Enter = approve, type text + Enter = reject with feedback,
Esc/X = dismiss on this laptop only. It POSTs `/resolve` with `device:"laptop"`, and auto-closes when
`GET /resolved/<id>` returns `1` (that is the cross-device dedup).

**The bug that made him say "the ping on my laptop doesn't work" — head-of-line blocking.** `/next`
returned only the **single oldest** unresolved card, and popup.ahk filtered its local `dismissed` set
**client-side**. So one Esc'd card at the head of the queue hid **every** newer card, permanently.
Card #8 was dismissed and cards #9, #10, #12, #14 were invisible on the laptop for ~24h while
`popup.ahk` sat there apparently healthy (it had been up 8 days). Fixed on both sides:
- `GET /next?skip=id1,id2` filters **server-side**, so the queue advances past dismissed ids. There is
  also `GET /unresolved-ids` -> `"id1,id2,..."` for health checks.
- popup.ahk sends its dismissed set as `skip` (capped at 60 ids) and **persists** it to
  `approval-hub\popup-dismissed.txt`, one id per line. Before this the set was memory-only, so every
  restart resurrected cards he had already killed — the exact re-pop loop the Esc rule exists to stop.
- Per-card dismissal is still permanent. That guarantee was never the problem.

**DIAGNOSTIC RUNBOOK — "the laptop popup isn't showing anything":** a running process proves nothing,
so never stop at `Get-Process`. In order:
1. `curl -s http://127.0.0.1:4180/unresolved-ids` — if empty, there is genuinely nothing to show.
2. `Get-Content approval-hub\popup-dismissed.txt` — ids here are hidden on this laptop **by design**.
3. Showable = (1) minus (2). If showable is non-empty there MUST be a window within ~2s.
4. Window check: `Get-Process AutoHotkey64 | Where-Object { $_.MainWindowTitle -eq 'Claude asks' }`.
   **`MainWindowTitle` is the reliable detector; the Win32 `FindWindow(null,"Claude asks")` returns 0**
   for this GUI (it is `+ToolWindow`), so do not use FindWindow.
5. Showable non-empty + no window = wedged. Repair = kill the popup process and run `start-hub.ps1`
   (`start-hub.ps1` only starts what is ABSENT, so a wedged popup must be killed first or the repair
   is a silent no-op). `Push-Lane-Watchdog` now does exactly this automatically.

**`Push-Lane-Watchdog` — both lanes alive at all times (2026-08-04, his standing order).**
`approval-hub\push-watchdog.ps1`, every 5 min + at logon via `push-watchdog-hidden.vbs`. `start-hub.ps1`
only checked that PROCESSES EXIST (a hung node passes) and knew nothing about the phone. This
health-CHECKS five legs — `HUB_HTTP` (hub actually answers on 4180), `LAPTOP_POPUP` (**functional**:
a card is showable but no `Claude asks` window is on screen, re-checked 5s later to avoid the
resolve-race, then kill + restart — a process-existence check is what let the head-of-line bug hide
for 24h),
`PHONE_CFG` (webhook URL in voice-lane config), `PHONE_CLOUD` (TCP 443 to trigger.macrodroid.com —
deliberately NOT a GET on the trigger URL, that would fire a real popup every 5 min), `PHONE_RETURN`
(Voice-Lane-Watch healthy) — repairs what it can (kills a hung node, runs start-hub, re-enables the
task), then pings Telegram only if a leg is still down. Alert dedup by failure-set key with a 60-min
re-nag; a blip repaired inside one run is not announced. Verified by controlled failure: killed the
hub → repaired; renamed `start-hub.ps1` away → `PUSH LANE DOWN` ping; restored → `RECOVERED` ping.
**PS 5.1 trap hit while building it:** an empty `@()` serializes to `{}` and `@($obj)` re-wraps it
into a 1-element array, so "nothing failed" read back as "something failed" and fired a bogus recovery
ping. State now persists `failed_key` as a joined STRING. See [[feedback_ps51_convertfrom_json_no_unroll]].

**2026-08-02 upgrades (all live, all user-requested):**
- **Daily #N numbering**: every POST /pending stamps `seq` (resets per local day) and prepends `#N · ` to `text` — so popup, TG ping, and later references ("proposal 11") share one handle. No MacroDroid change was needed (number rides in the text the macro already shows).
- **Re-notify loop**: unresolved `notify` items re-fire the phone webhook every 5 min, max 6 tries/30 min (MacroDroid popups evaporate ~5 min if unanswered — user confirmed live). `notify` is now persisted on the item. **TG REPEAT DISABLED 2026-08-31** (`TG_RENOTIFY_ENABLED = false` in server.js): cards ping Telegram exactly ONCE, at creation — see [[feedback_approval_ping_once]]; the loop still ticks for the (deactivated) phone lane only.
- **Instant disapprove ping**: bare NO (no typed feedback, i.e. phone) fires `❌ Disapproved — #N …` to TG immediately so the user can swipe-reply instructions to it. Typed-feedback NOs keep the Correzione ping only (no double ping).
- **Verdict-file bridge**: the CURRENT phone macro ("Claude Approve") does NOT POST /resolve over Tailscale — it writes `claude-verdict-<id>-<yes|no>.txt` to Drive `From phone/sodaos`; `watch-voice.ps1` (1-min task) forwards unknown-id verdicts to hub `/resolve` (device `phone-macrodroid`). Before 2026-08-02 those files were logged and DELETED — hub verdicts from phone never landed. Round trip proven ~30s (card #1 Tanya wa-send).
- **Numbering caveat**: resolving 'yes' EXECUTES the action — never "test-resolve" a card with a real action; superseding a card = resolve 'no' WITH feedback text (bare no now pings the user).

Related: [[reference_voice_lane]] (voice fast-lane + correction linking), [[feedback_message_send_protocol]], [[feedback_no_headless_fuzzy_send]], [[reference_pixel_call_recording]].
