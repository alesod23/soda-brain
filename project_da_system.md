---
name: project_da_system
description: "DA SYSTEM — Alessandro's umbrella project for cloud-resident Claude, an approve/reject decision loop, a self-maintaining personal brain, and a labelled y/n preference corpus."
metadata: 
  node_type: memory
  type: project
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-08-21T13:12:02.720Z
---

**DA SYSTEM** is the name Alessandro gave (2026-07-29, from San Francisco) to one large multi-phase system project. Four parts, ordered by his stated urgency:

**1. Laptop-off Claude (URGENT, do first).** He wants to run a session like a normal Claude Code session with the laptop completely powered off, and to move his files to Google Drive to support that. Native-Claude options preferred; Telegram channels considered but the current `tg-bridge` long-poller runs on his machine, so it dies with the laptop. Confirmed 2026-07-29: the claude.ai **remote-trigger API is enabled on his account** (`RemoteTrigger action:list` → HTTP 200, empty) — Anthropic-hosted scheduled cloud sessions are available to him.

**2. Approve/reject decision loop.** A working approve/disapprove button so Claude-built agents can watch his messages and activity live, infer what to add / what he finished, and ask permission before mutating his to-dos. Requires a to-do system the machine can read and write — possibly the existing Obsidian one, but it must be (a) cloud-resident and editable while the laptop is down, and (b) wired to a good context window. See [[reference_approval_hub]] (existing hub on :4180) and [[reference_vault]] (task-land).

**3a. Self-maintaining brain.** Apply self-updating / self-pruning LLM memory to his personal brain ([[reference_kb_vault]], `vault_kb`). Not fully autonomous: **his approval is required for all big changes** — retiring outdated memories, and any time something contradicts.

**3b. Preference corpus (year-long).** Record ALL y/n decisions from the push-notification loop, each labelled with a self-forming category (e.g. `messaging`, with subcategories like `whatsapp messaging` where warranted) plus a short free-text description so mislabels can be repaired later. He will never curate it by hand — categories must self-maintain. Design for ~20 decisions/day for a year. Eventual goal: use the corpus to fine-tune / improve the assistant. Near-term, Claude decides how to test viability: run a query/retrieval-based predictor in the background against accumulated decisions and ping him only once hit-rate looks real.

**Why it exists (his words):** the push-notification system is being built *so that Claude involves him often*, because he wants Claude doing much more work in the background from now on. He is explicitly unsure push notifications are the right mechanism and asked for a researched recommendation (he floated "hermes" as an alternative).

**Phase-2 chassis candidates (2026-07-31):** YC open-sourced **QM** (`github.com/yc-software/qm`, MIT) — their internal multi-agent harness: cloud-first, Slack + web UI native, triggers (crons/webhooks), shared memory/files, connectors, multiplayer, three approval postures, can drive Claude Code as its engine. Deploys to own Fly.io/AWS + Postgres, needs API keys (conflicts with [[feedback_no_api_keys]] — real token spend). YC calls it early/buggy. It is close to a DA SYSTEM skeleton: evaluate ADOPT vs build before writing phase-2 code. Also seen: **AutoGTM by Explee** (hosted full-autopilot outbound, $30 free credits, $0.03/email) — user wants the tactic mimicked for Tundra GTM; agreed sketch = auto sourcing/enrichment/sequencing, human y/n only on reply-sends via the approval loop. Awaiting his pick: benchmark AutoGTM / build in-house / both.

**CANONICAL STATUS DOC — read it FIRST, before anything else DA-SYSTEM:**
`C:\Users\Alessandro\task-land\_system\WORKPLAN-20260730-da-system-phase1.md`
(auto-syncs to GitHub `alesod23/task-land` within ~10s, so it is readable from the phone, a cloud session, or another machine). It carries the settled architecture, what is BUILT vs NOT, the broken items needing the user, and the open loops. Keep it updated in place — do not start a second status file.

**One-line state (2026-08-04):** FULL IMPLEMENTATION HANDED TO CLAUDE ("I trust you, Fable, to figure it out... implement the system in one go... ping me when everything is nice and ready"). VPS greenlit at ~€8/mo Hetzner CX32, with the explicit portability requirement: everything must later move to any always-on computer (mini-PC, Caleb's laptop) by re-running the kit. **Waiting on him: create the Hetzner box and paste the IPv4** (his steps + the SSH pubkey are in `task-land/_system/vps/VPS-SETUP.md`; automation keypair at `~/.ssh/da-vps_ed25519`). The provisioning kit (`bootstrap.sh`, `git-sync.sh` bash port, `health-vps.sh`, systemd units) is written, bash -n-checked, LF-clean, in `task-land/_system/vps/`. Phase 1 sync layer was adversarially audited 2026-08-04 (15 findings) and the critical ones are FIXED AND TESTED: commit-first ordering, conflict → work parked on GitHub branch `conflict-laptop` + fault raised (proven with a real engineered conflict, including automatic recovery), watcher heartbeat replacing pid-liveness (Modern Standby froze the watcher 5h48m while health reported green), wake-aware staleness. `supervisor.ps1` (auto-repair → escalate-as-decision via approval hub) is built and repair-tested but NOT yet scheduled. Alerts: claude.ai Gmail connector CANNOT send (drafts only) — cloud alert channel = Calendar popup (see [[reference_cloud_routine_alert_delivery]]); user's standing rule: alerts/emails to him are a last resort, the system must SELF-REPAIR and only ping a yes/no decision through the approval hub. Phase 2 spine proven; phase 3a/3b not started.

**The Tundra-facing branch of phase 2 (2026-08-10, settled after two revisions):** anything
Tundra-relevant the watcher finds is classified LOCALLY (plan-included compute, not Notion credits),
then pushed as an ordinary row into the shared `📥 Inbox` database via the Notion MCP — the same
doorway Caleb fills by hand, see [[project_notion_signals]]. From there Notion's own `Inbox filer`
agent does propose → approve → file, identically for both producers. Machine plumbing (dedupe keys,
sources, confidence) stays in CC local state, never as Inbox columns. The team side works with zero
DA SYSTEM dependency; the CC producer gets built later, starting from DA SYSTEM. Non-Tundra findings
keep going to task-land / vault_kb unchanged.

**Phase 2 v2 spec (2026-08-19, user-dictated):** two waiting flavors (`surface_on:` 🌊 vs new `trigger:` ⚙️, both in Waiting, marker on the first sub-bullet); new **In progress** section above Today on the daily page (`status: doing`); NO Notion done-UI (page is the edit surface, engine infers completions). Kortyx-style engine (kortyx.co) on the VPS: persistent TG-facing Claude, event queue (WA store/Gmail/Calendar/git), hot-set context (context.md + active tasks, never a mega window) + deep lookups into task-land/vault_kb, infers new/done/conflict, ONE TG approval card per proposal, follows the thread, always asks before mutating, verdicts feed corpus 3b. Full spec in the workplan.

**Goal-ended tasks (2026-08-21, user-dictated):** goals ("get into Founders Inc", "close hospital X") are durable objects ABOVE tasks; steps attach to them and completing a step spawns a monitor, never closes the goal; dead paths close the task chain but the goal stays on the radar awaiting a new path; the engine treats open goals as standing intent and proposes new paths. Sketch: `goal:` frontmatter → `Goals/<slug>.md`. First live instance: founders-inc (repick task in Tasks/waiting, surface 2026-08-28).

**How to apply:** treat DA SYSTEM as the standing name for this work. Research first, then ask everything needed in ONE multiple-choice round per phase, then fan out agents. Phase 1 is scoped and asked separately from 2/3 because of the urgency.
