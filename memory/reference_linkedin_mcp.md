---
name: reference_linkedin_mcp
description: "stickerdaniel linkedin-mcp-server — the ONLY LinkedIn surface (linkedin-pw and the Voyager helper both deleted). Covers search + profiles + companies + jobs + inbox + conversations + SEND + connect requests."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 40d275d4-a156-464d-8ca5-a5127c715e90
---

# linkedin-mcp (stickerdaniel/linkedin-mcp-server)

The primary LinkedIn surface. Installed 2026-05-20 after SAFE audit. Write tools (`send_message`, `connect_with_person`) enabled later that day after a live test on Caleb proved the path is structurally safer than the previous linkedin-pw send flow.

## Paths
- **Venv:** `C:\Users\Alessandro\.linkedin-mcp\venv\` (Python 3.12, isolated)
- **Launcher (shim):** `C:\Users\Alessandro\.linkedin-mcp\launcher.py` — `DENIED_TOOLS = set()` (empty). Kept as a single chokepoint so any future re-block is a 1-line edit.
- **LinkedIn session profile:** `C:\Users\Alessandro\.linkedin-mcp\profile\` (patchright persistent context)
- **Cookies export:** `C:\Users\Alessandro\.linkedin-mcp\cookies.json` (auto-written on server shutdown)
- **Patchright chromium:** `C:\Users\Alessandro\.linkedin-mcp\patchright-browsers\chromium-1217\chrome-win64\chrome.exe`

## Claude Code MCP wiring
- **Server name:** `linkedin-mcp` (scope: user — available in all projects)
- **Config file:** `C:\Users\Alessandro\.claude.json`
- **Command:** `…\venv\Scripts\python.exe …\launcher.py --tool-timeout 600`
- **Why 600:** default 180s isn't enough for patchright cold-start + LinkedIn nav + compose + type + send. First Caleb test timed out at 180; second succeeded with 600.
- **Env:** `HEADLESS=true`, `HOST=127.0.0.1`, `LOG_LEVEL=INFO`, `PYTHONIOENCODING=utf-8`
- **17 tools** (prefix `mcp__linkedin-mcp__`): close_session, **connect_with_person**, get_company_employees, get_company_posts, get_company_profile, get_conversation, get_feed, get_inbox, get_job_details, get_my_profile, get_person_profile, get_sidebar_profiles, search_companies, search_conversations, search_jobs, search_people, **send_message**

## Why this is the send path (not linkedin-pw send_dm.py)

Verified 2026-05-20 with a live Caleb test:

- **Mojibake (Carlo Cotrone incident) vector: GONE.** Message goes JSON-over-stdio in UTF-8 — no PowerShell pipe, no shell quoting layer.
- **Wrong-recipient (Nitya/Caleb incident) vector: STRUCTURALLY LOWER.** Driven by `linkedin_username` / `profile_urn` in the compose URL, not by clicking in the sidebar UI.
- **Read-back verification:** `get_conversation(linkedin_username=...)` immediately after `send_message` confirms exact bytes landed.

Residual risk: LLM defaulting to em dashes in content. Mitigated by global CLAUDE.md "NO em dashes" rule.

## Send protocol (when actually sending)

1. Draft the message. NO em dashes (use commas / periods).
2. Show user the verbatim text + resolved recipient (slug or URN) before sending.
3. On explicit "go" / "send" / "yes": call `send_message` with `confirm_send=True`.
4. Immediately call `get_conversation(linkedin_username=...)` to read back.
5. Report to user: latest message in thread (verbatim) + verified match.

For high-stakes recipients (advisors, professors, founders), prefer to draft with [[cold-outreach]] first.

## This is the ONLY LinkedIn surface (pw fully deleted 2026-05-27)

On 2026-05-27 the user demanded deleting Playwright for LinkedIn entirely. Both `~/.claude/skills/linkedin-pw/` and `~/.claude/linkedin-pw/` (lib.py, scrape.py, find_person.py, fetch_post.py, scrape_saved.py, the persistent `profile-chrome` session, `out/`) were removed. The Voyager helper `~/.claude/linkedin/` was already gone (deleted 2026-05-20). See [[feedback_mcp_over_pw]].

**Do NOT recreate any browser/Playwright LinkedIn path.** Capabilities that pw used to cover (enumerate accepted connections, list pending sent invitations, scrape a post + comments, saved posts, 1st-degree name search) are no longer available locally. If a task needs one of these and the MCP can't do it, tell the user it's not currently possible via MCP — do not spin up a scraper. The CRM (`outreach/crm/crm_li.py`) already drives this MCP only.

**If the MCP server drops mid-session** (its `mcp__linkedin-mcp__*` tools become unloadable via ToolSearch), there is NO fallback: the user must reconnect/restart the MCP.

## Operational notes
- Spawning the server takes ~12-15s (patchright cold-start). Each tool call lives in the same browser context (singleton driver) within a single MCP session.
- DO NOT run with `HEADLESS=false`, `HOST=0.0.0.0`, or `LOG_LEVEL=DEBUG` long-term — DEBUG logs cookies (audit finding).
- Re-login: `& "C:\Users\Alessandro\.linkedin-mcp\venv\Scripts\python.exe" "C:\Users\Alessandro\.linkedin-mcp\launcher.py" --login`
- Clear session: same command with `--logout`.
- Inbound-Allow firewall rules for the patchright chrome.exe were created during install and removed (low-risk Public-profile rules; MCP uses pipe IPC + outbound only).

## Failure mode: orphaned launcher processes = profile-lock war (fixed 2026-07-02)

**Symptom:** every `mcp__linkedin-mcp__*` call errors; `--status` reports "Session expired or invalid" **even immediately after a successful `--login` that saved a profile**; many `invalid-state-*` dirs accumulate in `~/.linkedin-mcp/`; `--logout` fails with "Failed to clear authentication state".

**Root cause:** `launcher.py` python processes **pile up** (each Claude session + each `claude mcp list` health-check spawns one and none are cleaned up — found **18** stale on 2026-07-02). They all contend for the single `~/.linkedin-mcp/profile/` persistent-context lock, so no external `--login`/`--logout`/`--status` can write a session that sticks. NOT a cookie/date-expiry issue (li_at was valid to 2027) and NOT headless detection (headed `--status` failed identically).

**Fix sequence:**
1. Kill all: `Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match 'launcher\.py' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }` → verify 0 remain. (Killing procs → ask user first.)
2. Clean clear: `printf 'y\n' | …\linkedin-mcp-server.exe --logout` (now succeeds → "✅ cleared").
3. Headed login: `HEADLESS=false PYTHONIOENCODING=utf-8 …\venv\Scripts\linkedin-mcp-server.exe --login` (run backgrounded; user signs in within the 5-min window; must fully reach the feed).
4. Verify: `HEADLESS=true … --status` → must print "✅ Session is valid".
5. **User restarts Claude Code** so exactly ONE fresh server spawns and reads the valid profile.

Console entrypoints live at `…\venv\Scripts\linkedin-mcp-server.exe` (also `--status`). The cp1252 `UnicodeEncodeError` when printing ✅/❌ is cosmetic (set `PYTHONIOENCODING=utf-8`). **Prevention TODO:** the launcher/health-check leaks a process per invocation — worth a cleanup/singleton guard so this doesn't re-accumulate.

## Re-block write tools (if ever needed)

Edit `launcher.py`: `DENIED_TOOLS = {"send_message", "connect_with_person"}`. That single line is the chokepoint — tools never reach `tools/list` when listed there.

## Due scheduler sullo stesso profilo = profilo in quarantena (2026-09-29)

**Sintomo:** la campagna US si ferma a meta' giro con `error: Session expired. A login browser
window has been opened` e il server mette il profilo in quarantena in `~/.linkedin-mcp`. Nei log:
`Browser warm-up failed`, `Page.goto: Timeout`. Successo due giorni di fila, **sempre alle 18:05**.

**Causa trovata dalla sessione laptop:** due task partivano su LinkedIn **nello stesso minuto**,
`Peer60-AcceptCheck-1800` e `US-Campaign-Daily`, entrambi alle 18:00, e le cartelle di quarantena
portano lo stesso timbro 18:05 in entrambi i giorni. Non era una sessione scaduta: era una
collisione fra due processi sullo stesso profilo browser, letta come logout. Fix: `US-Campaign-Daily`
spostato alle 18:15. **Prova attesa il 30 set: nessuna nuova cartella invalid-state dopo le 18:15.**

**La lezione che vale oltre LinkedIn:** un orario tondo in due scheduler diversi e' una collisione
in attesa. Quando un errore di sessione si ripete allo STESSO MINUTO in giorni diversi, la prima
ipotesi non e' la sessione, e' chi altro parte in quel minuto. (Io avevo proposto la pressione di
memoria, [[reference_laptop_memory_pressure]]: resta un secondo candidato, non era la causa.)

**Riparazione automatica, dal 2026-09-29:** `li_restore.py` ripara senza login in ~40 secondi;
exit 2 solo se LinkedIn rifiuta due volte, altrimenti exit 4 e si riprova. L'agente GTM e il
runner della campagna US chiamano ora lo stesso `li_restore.py`. Il box fa da rete di sicurezza
con `task-land/_system/gtm-agent/box_linkedin_watch.py` (cron 10 min): legge il blocco `linkedin`
di `~/.local/state/gtm-agent/heartbeat.json` e posta UNA card solo se `down_since` supera i 60
minuti mentre l'heartbeat e' fresco. Heartbeat vecchio = laptop spento = nessuna card.
Regola di fondo: NOTIF-CONTRACT.md H5, un'anomalia che una macchina puo' riparare non
diventa mai una card per lui.
