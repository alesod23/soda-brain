---
name: reference_floom_mcp
description: Floom hosted-MCP setup — how the Floom worker platform is connected and how to reconnect it
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4e67827e-2d29-4818-b145-58f24f4caa03
  modified: 2026-08-03T02:10:06.551Z
---

## ✅ STATUS 2026-09-02: endpoint is BACK UP — and there are TWO Floom accounts, not one

- **The 404 is GONE.** `tools/list`, `workspace.info`, `connections.list`, `workers.list` all return
  HTTP 200 against `https://workeros-api.floom.dev/mcp/ws_9b31dcfd40154f` with the stored bearer
  from `~/.env/floom.env`. The 2026-08-02 outage below was transient. The MCP entry can be restored
  with the `claude mcp add` line further down whenever it's wanted.
- **Alessandro has TWO separate Floom accounts, each signed in with a DIFFERENT personal Google
  account.** Floom names a workspace after the email local-part, so `workspace_name` identifies the
  login. `workspace.info` returns `email: null`, so the login email comes from `workspace_name` plus
  the CLI credential files at `~/.config/floom/`:

  | Floom account | Google login | workspace_id | authed | Connections | Workers |
  |---|---|---|---|---|---|
  | `a99a1a49-626f-4529-9f38-b55bea822302` | **alesoda2002@gmail.com** | `ws_9b31dcfd40154f` | 2026-07-02 | gmail → `alessandro.sodano@cdtm.com` (active/healthy) | text-normalizer, gmail-summary-agent, tundra-followup-brief |
  | `e5a45167-ebb3-4205-b090-c4eb522c410d` | **alessandrosodano23@gmail.com** | `ws_d8b676b8295748` | 2026-07-19 | linkedin → `alessandrosodano23@gmail.com` (active/healthy) | none (empty workspace) |

- **`~/.config/floom/active` currently points at `e5a45167-…` = alessandrosodano23@gmail.com**, i.e. the
  EMPTY workspace. The `floom` CLI therefore talks to the wrong workspace by default. All the real
  workers live under alesoda2002@gmail.com. Switch the active account before any `floom` CLI work.
- **`~/.env/floom.env` holds the alesoda2002 token** (`floom_lC…`, matches
  `~/.config/floom/credentials/a99a1a49-….json`). The alessandrosodano23 token (`floom_ZX7F…`) is in
  `~/.config/floom/credentials.json`. Both are valid.
- **Do NOT answer "which account is Floom on?" with a work address.** `alessandro.sodano@cdtm.com`
  is only the Gmail DATA CONNECTION inside workspace #1, never the login.
  `alessandro@tundrahealth.ai` has no Floom relationship at all.
- Mail check 2026-09-02: zero Floom messages in cdtm, tundra, or lobbly mailboxes — consistent with
  both signups living in the two personal Gmails (whose `triage/tokens/` are revoked, so those
  mailboxes can't be searched programmatically right now).

---

## ⚠️ STATUS 2026-08-02: endpoint 404s, token relocated, entry removed from settings.json

- **The workspace endpoint is DEAD.** `POST tools/list` to
  `https://workeros-api.floom.dev/mcp/ws_9b31dcfd40154f` with the stored bearer returns **404**
  (host root also 404s; `floom.dev` itself returns 200). Cause unknown: expired free-tier workspace,
  rotated token, or changed API path. **Unrelated to the Anthropic account migration** — the Floom
  credential is a static header token Anthropic never touched.
- **The token now lives at `C:\Users\Alessandro\.env\floom.env`** (`FLOOM_MCP_URL`, `FLOOM_TOKEN`),
  matching the `~/.env/<service>.env` convention. It was previously plaintext inside
  `~/.claude/settings.json`. **It was never in git** (`~/.claude` is not a repo and no repo tracks
  it), so **no rotation was needed**. Backup of the old config:
  `~/.claude/settings.json.bak-pre-floom-token-move`.
- **The `mcpServers.floom` block was REMOVED from settings.json.** It never worked anyway: Claude
  Code does not load MCP servers from `settings.json`, which is why floom never appeared in
  `claude mcp list` and no `mcp__floom__*` tool ever loaded.
- **To restore when Floom is back**, add it at user scope so it actually loads:
  `claude mcp add --transport http floom <FLOOM_MCP_URL> --header "Authorization: Bearer <FLOOM_TOKEN>"`
  then restart Claude Code. Verify with `claude mcp list` (it should now appear, unlike before).
- **⚠️ Floom CANNOT do LinkedIn** — see the 2026-07-06 entry below. Cloud reaches Gmail only;
  LinkedIn and personal WhatsApp have no cloud API and stay local (`linkedin-mcp`, `wa-daemon`).
  Do not set Floom up expecting LinkedIn coverage.

---

Floom (hosted cloud AI-worker platform) is connected as an HTTP MCP. Installed 2026-07-03 via `npx -y @floomhq/floom mcp install --target claude` (package `@floomhq/floom`, ships a `floom` CLI). The installer wrote the server into `~/.claude/settings.json` under `mcpServers.floom` (type `http`, url `https://workeros-api.floom.dev/mcp/ws_9b31dcfd40154f`, `Authorization: Bearer <token>`). Workspace id = `ws_9b31dcfd40154f`.

- Tools land as `mcp__floom__*` (worker names use dots: `workers.list`, `workers.create`, `workers.run`, `runs.get`, `runs.watch`, `runs.logs`, `runs.approve`, `secrets.*`, `connections.*`, `contexts.*`). New session required to load them (MCP loads at startup).
- GOTCHA: it lives in `settings.json#mcpServers`, so `claude mcp list` does NOT show it (that command reads project-scoped `.mcp.json` / `~/.claude.json`, not settings.json). To verify it's live, POST a `tools/list` JSON-RPC to the url with the bearer token, or use `/mcp` in-session.
- Model: hosted, runs on `workeros-api.floom.dev` — no self-hosting, no local server, no `.env`. Drive it via the `/floom` skill.
- First-worker playbook (from the skill): smallest read-only manual worker → `workers.run` → watch `runs.*` → show output → only then offer to schedule.
- PIPELINE PROVEN 2026-07-03 via a curl bridge (no session restart needed): created `text-normalizer` (scaffolded by `floom init`, pure-script/`e2b`/python311, `network.egress:false`, no connections) and ran it → run `run_19d991df2791` status `completed`, real output. So create→run→completed→output all work over raw HTTP.
- CURL BRIDGE (use when `mcp__floom__*` not loaded this session): POST JSON-RPC `tools/call` to the mcp url with the bearer token; body `{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"<tool>","arguments":{...}}}`. Response is plain JSON (sometimes SSE `data: ` prefixed — strip it). Result payload at `.result.structuredContent`. `runs.get` keys: status(`completed`/`running`/`failed`), outputs, output, logs, transcript, duration_ms. Helper script was at scratchpad `floom-rpc.sh`.
- WorkerContract (worker.yml) shape: `schema_version "0.3"`, name/title/description/version, `entrypoint`, `trigger.type: manual`, `exec:{mode: pure-script|…, entry, runtime: python311, runner: e2b, command, inputs[], outputs[]}`, `capabilities:{network:{egress}, secrets:[], connections:[]}`. `run.py` reads `inputs.json`, writes `result.json` = `{status, outputs, artifacts, error}`.
- Connections are Floom-workspace-scoped via COMPOSIO (separate from Claude Code's own MCP connections). Add with `floom connections add <slug> --open` (slugs: gmail, github, googlecalendar). GOTCHA: the authorize link is under `floom.dev/app/...` and needs an authenticated floom.dev web session first, else it stalls at status `initializing` (updated_at frozen, empty scopes) and never completes.
- DONE (2026-07-03): Gmail connected & LIVE. Connection `cc6f2fe7-…` status `active`, account `alessandro.sodano@cdtm.com`, full mail scope. (First attempt stalled at `initializing`; completing it via the floom.dev/app dashboard in Comet worked.) `whoami`: account a99a1a49-…, workspace `alesoda2002`.
- WORKERS live: (1) `text-normalizer` (proof, manual). (2) `gmail-summary-agent` = "Gmail Intake Brief" — agent-mode, read-only (only `GMAIL_FETCH_EMAILS`), scaffolded from template `gmail-summary-agent` (`floom workers templates list`), SKILL.md customized to a triage brief (🔴 needs action / 🟡 FYI / ⚪ noise). SCHEDULED: cron `57 7 * * 1-5` Europe/Berlin, input `query=newer_than:1d`. First real run `run_7dc0a7084cbb` completed, produced an accurate brief.
- AGENT-WORKER create GOTCHA: `workers.create` 422s "run_py is required when files are not supplied" if you pass only worker_yml+skill_md. Fix: ALSO pass `files:[{path,content}...]` for worker.yml + SKILL.md. And post the request as a FILE via `curl --data-binary @body.json` (build with `jq --rawfile`) — inline `-d` with emoji/multiline mangles UTF-8 → server -32700 Parse error.
- Agent worker.yml: top-level `connections:[{app:gmail, allowed_tools:[GMAIL_FETCH_EMAILS]}]`, `exec.mode: agent`, `entry: SKILL.md`, outputs a file (`out/summary.md`), `capabilities.network.egress: true`. To change cadence/undo: `workers.update` with `trigger_type: manual|cron`, `cron_expr`, `cron_timezone`, `input_values`.
- NEXT (offered, not built): deliver the scheduled brief somewhere (email-to-self / notify) so it's useful without opening the Floom dashboard; add more workers (Slack digest, follow-up drafter).
- TUNDRA follow-up monitor (2026-07-06): user wants Floom to monitor LinkedIn+WA+email for Tundra-Health follow-ups. REALITY: Floom cloud reaches EMAIL only (Gmail); LinkedIn + personal WhatsApp have no cloud API → must stay LOCAL (linkedin-mcp scraper, wa-daemon). And coattio ALREADY has an email checker (CRM `~/.medtech-crm/crm-app/server.js` dailyTick every 30min → `gmail.py contact-status` → advances stages; + lemlist-sync every 15min) watching `alessandro.sodano@cdtm.com` — do NOT double-write it. Floom's clean slice = the follow-up REMINDER layer (read-only) which today doesn't exist. Recognition context pack saved at scratchpad `TUNDRA-RECOGNITION-CONTEXT.md` (real entities: French hospital domains chru-nancy.fr/chu-lyon.fr/etc + German champions Flüthmann/Hoffmann@Matthias-Stiftung; trilingual DE/EN/FR; EXCLUDE "Tundra Talents" decoy). Built worker `tundra-followup-brief` (agent, read-only Gmail, report-only). Delivery to local task-land needs a cloud→local bridge (Floom can't write local files). PENDING user answers: Floom role (reminders-only vs replace CRM checker) + reminder destination.
- DA SYSTEM research verdict (2026-07-30, deep web-verified): Floom is the best available HOSTED substitute for the Gmail+Slack half of triage — background workers with cron/webhook triggers, a real declared human-approval gate ("Sensitive actions wait for your yes"), 1,047+ Composio integrations, Cloud currently $0 "free during launch" (paid later with notice). Its WhatsApp integration is BUSINESS-accounts-only, explicitly not personal — so it can never cover the wa-daemon half. "WorkerOS" in the API hostname is Floom Cloud's internal backend name, not a separate product. Competitive field same date: Relay.app shutting down Aug/Sep 2026; Claude Cowork Gmail connector is draft-only (cannot send); Lindy $49.99-199.99/mo with multi-inbox Gmail but WA page 404'd; OpenAI Workspace Agents strongest approval UX but needs 2-seat Business plan. No vendor anywhere ships personal-WhatsApp triage: Meta ToS bans unofficial bridges (ban risk) AND now bars AI-assistant providers from the Business API. The Baileys wa-daemon is the one irreplaceable local component.
- OUTAGE GOTCHA (2026-07-06 ~15:00): ALL agent(LLM)-mode workers fail workspace-wide with error "The platform AI model is not fully configured. Set the required provider credentials and retry." + secondary "Tool <x> not found in agent" / `llm_model_not_configured`. Gmail fetch succeeds first, dies at model step. Pure-script workers unaffected. `floom doctor` stays GREEN (doesn't test model provider). Known-good gmail-summary-agent that completed at 11:58 failed at 14:56 → Floom-side regression, not the worker. Fix is Floom's (or wait); re-run when restored. `floom support`/`floom feedback` file a ticket (feedback attaches session transcript — get user consent, Tundra business context).
