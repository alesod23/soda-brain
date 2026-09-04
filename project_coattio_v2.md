---
name: project_coattio_v2
description: coattio v2 (2026-09-04) — contract in ~/.medtech-crm/WORKPLAN-20260904-coattio-v2.md; channel facts + derived warmth replace stages; one owner per person (CRM vs task-land); daily-page CRM line; lemlist API locked
metadata: 
  node_type: memory
  type: project
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-04T11:22:18.253Z
---

**coattio v2** is the 2026-09-04 rebuild of Alessandro's local outreach CRM (`~/.medtech-crm`, UI :4124, intake :4137). The contract is `~/.medtech-crm/WORKPLAN-20260904-coattio-v2.md` (11 sections + a log per phase, with Playwright screenshots in `verify-shots/`). Read it before any coattio change.

**Model:** no French stage ladder. Per person: `facts` (li_request_sent, li_connected, li_dm_sent, email_sent, call_attempts, call_done, wa_sent, replied{channel}), last step + days since, **warmth 1-5 derived** (1 replied/call done · 2 DM'd/emailed · 3 connected · 4 request sent · 5 nothing) with `warmth_override`, `state` active/waiting/dead, `kind` outreach/ecosystem, `next_step`, `campaign_plan` (planned linkedin/email, auto-assigned; `campaign_opt_out`), `enrich` checklist (Claude deep · lemlist · other), `owned_by_task`. Legacy fields (`stage`, `touch*`, `*_date`) are kept coherent by `model.js` / `logStep` / `monitor.js applyEvent` because ingest-intake, lemlist-sync, notion-sync still read them.

**Boundary with task-land (user-dictated):** CRM obtains conversations, task-land pursues them. A task file with `contact:` freezes the CRM row (`owned_by_task`, set by `task-land/_system/crm-bridge.ps1` from daily-sync). Warm leads that never came from outreach never enter the CRM. Daily page has ONE mirror line "Today's items in the CRM (n)" (today only, auto-checked when empty; the parser skips it). "Make it a task" button + (phase 7) a hub card after a detected meeting hand a person over.

**Views:** Today (due / coming up / replies to answer / campaign alerts, nothing else), People, Companies, Campaigns, action pages LinkedIn DM / Email / Call, Templates. Drawer: timeline (corpus + LinkedIn store + WA store), Draft next step from his own sent corpus via headless claude, Send via LinkedIn MCP / gmail.py / wa send.js with confirm (Claude-in-Chrome fallback). Monitoring ticks in `crm-app/server.js` + `monitor.js` (corpus/WA/LinkedIn store, Gmail, calendar); Playwright LinkedIn path RETIRED.

**lemlist:** the API is 402-locked on the current plan (every route, since 2026-07-03); Start is plan-gated, manual `cam_…` recording works. User decision pending: Multichannel plan ($87/mo) or manual campaigns.

**How to apply:** treat the contract file as the spec; new features go in as a numbered phase with a log; keep the single-writer rule (all writes through `GET/PUT :4124/api/data`, never direct `crm.json` writes from a second process); English labels only; HubSpot-like density rules (section 10). See [[reference_coattio_servers]], [[project_da_system]], [[feedback_agent_long_running]].
