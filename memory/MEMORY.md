# Memory Index

- 🧠🚪 [THE SODA BRAIN (2 Oct 2026): this repo, the system map in `system/`, the Postgres+pgvector door on the box (:4150, Funnel), the CRM mirrored, instinct as orchestrator](reference_soda_brain.md) — update `system/` in the same turn as any service, port, job, store or rule changes; tokens in `~/.env/soda.env`, never printed.

- 🪞📇 [Open hub draft cards are mirrored onto the CRM review item (latest revision); the CRM never drafts beside a card](reference_crm_mirrors_open_hub_draft_cards.md) — `review-artifact.js mirrorHubCards`, every 10 min + before generate (Vincent, 2026-10-04).
- 📇➡️ [The CRM is where every follow-up is decided and sent; the box becomes the CRM writer; the hub keeps non-person items (his decision 4 Oct 2026 04:00)](project_crm_is_the_followup_surface.md) — never a second writer of crm.json; a card about a person links to the CRM item; build order in THE PLAN item 10.
- 👁️🔁 [A visual deliverable gets a screenshot review LOOP before he sees it: no line through a node, no label on a shape, text centred, repeat until clean](feedback_visual_review_loop_before_handing_a_page.md) — "This is disgusting ... Continue until loop until you have all those minor details fixed" (2026-10-04).
- 🗺️ The visual map: `soda-brain/system/SODA-SYSTEM-MAP.html` (+ `.md` narrative), same rules as the system map; "loading cards" on hub-review with a healthy server = a client JS error, read the console first (2026-10-04).
- The simulation map: `soda-brain/system/SODA-SIMULATION-MAP.html` (+ `.md`), the harness drawn next to the system map: twins and fidelity, arms, guards, the eval, nights 1 to 3; changes in the same turn as `~/sim/harness` (2026-10-04).
- 💸🛑 [A cap he gives is the number to USE, never a line to stop a point before](feedback_cap_means_use_it.md) — "cap 92" and I stopped at 91: "No. No. Fuck." Check budget.py between steps, stop only at the cap (2026-10-03).
- 🔎🧩 [Edge first for every NEW task: look up a skill on getedge.cc (MCP `edge`, both machines) as the baseline; the simulation experiments with those skills](feedback_edge_first_for_new_tasks.md) — one `find_skill` call before building; prior: people-search lost to WebSearch on 18 Sep (2026-10-03).

## Rules that bite first
- 💬↩️ [A bare TG line after a SODANOtif card ("i got it") is his answer to that person: reply same turn, offer the send](feedback_bare_tg_line_after_notif_card_is_a_reply.md) — missed Caleb's hotel question while busy (2026-10-04).
- 🃏✍️ [A card proposing a new CRM row SHOWS THE DRAFT; the row yes never sends, the draft goes to the lane as its own card](feedback_propose_row_card_carries_the_draft.md) — hub #41 Vittoria + #40 Donarini, HUB H39 (partly supersedes H38 #42); instinct's own Gmail draft first, never a second; one-token addresses (dimarcoberardino@) matched inside (2026-10-04).
- 🚧 [The auto-mode classifier refuses remote shell writes on the box and `git rm --cached`: write those as HIS commands in the plan, never re-route them](reference_auto_mode_classifier_blocks.md) — a merge that untracks files deletes them from the working tree first (2026-10-04).
- 🛑 [Unattended run: NEVER end the turn waiting on agents](feedback_unattended_run_never_wait_on_agents.md) — do the work in the main thread, check agent liveness by transcript mtime after 10 min, keep a self-wake heartbeat; cost him 10 idle hours on the thesis (2026-09-27).
- 🧊 [Session frozen on "running PreToolUse hooks N/6" = a hook that never returned](reference_pretooluse_hook_hang_npx.md) — post-compaction-recall.sh ran `npx` on every tool call; fixed 2026-09-27, recipe inside.
- 🪟🚫 [NO console window ever in front of him: tasks through run-hidden.vbs, CREATE_NO_WINDOW, window_lint.py after every new task](reference_window_watch.md) — the recorder names who opened each window (2026-09-28).
- 📦✋ [Never scp/rm/edit a file inside a synced repo on the box by hand](feedback_never_touch_synced_repo_on_box_by_hand.md) — the box sync committed my deletion on both machines (2026-09-28).
- 📌 ["Make this a rule" = write NOW](feedback_rule_requests_are_binding.md)
- ✉️⚰️ [Un hard bounce e' definitivo: indirizzo morto, mai un altro invio](feedback_hard_bounce_is_final_never_resend.md) — 3 avvisi del Mail Delivery Subsystem = UN invio che Gmail ritenta per 48h; H96, e nessuno in gtm-eng legge ancora i bounce (2026-10-03).
- 🔄 [THE RULE LOOP: ledgers, compiled skills, observers, decisions.jsonl, system check](reference_rule_loop.md) — canonical `task-land/_system/RULE-LOOP.md`; his only inputs are five sentences; add rules with addrule.py the same turn (2026-09-24).
- 🧩🔁 RULE LOOPS EVERYWHERE (his ask 4 Oct 2026 18:45): every surface = six parts (ledger, skill loaded by the decider, input box, route, observer, brain), template in RULE-LOOP.md section 7, measured by `_system/rule_loop_check.py --md`; ONE classifier `drafts/ledger_verdict.py` (like/confirmation/rule/case/system/work); notifications built first; gaps in `handoffs/AUDIT-20261004-rule-loops.md`; brain `POST /brain/rules` / MCP `his_rules`.
- 🧠 [Design on merit, not his off-hand numbers](feedback_design_on_merit_not_his_offhand_numbers.md) — no arbitrary caps, Haiku never, Opus where it decides, read the reference he names (Kortyx) before designing; "smart, non-blocking, not sucky" (2026-09-24).
- 🔁 ["Iterative" = one sentence on the spot, never a review pass](feedback_iterative_means_on_the_go_flag.md) — backlogs are separate, optional cleanup; never call them the iterative part (2026-09-24). — file + index line, same turn.
- 🧹➡️ [Una regola vale anche sugli artefatti GIA' esistenti](feedback_standing_instruction_becomes_work_now.md) — "tutto da Tundra" (22 set) e tre draft sono rimasti in cdtm finche' non l'ha chiesto lui; e una domanda parcheggiata in una pagina non e' una domanda fatta (2026-09-23).
- 🏠 [L'output va DENTRO il sistema che possiede quel lavoro](feedback_output_goes_into_the_owning_system.md) — viaggi in trippy, persone nel CRM, board in gtm-eng, decisioni nella hub; mai l'ennesima pagina usa-e-getta. Nel dubbio chiediglielo su TG PRIMA di costruire (2026-09-20).
- ⌨️ [SHORTCUTS.md = master list](feedback_shortcuts_master_file.md) — update same turn for any hotkey/alias/skill.
- 🧩🔎 [Edge MCP + prompt nudge, box e laptop dal 2026-10-03](reference_edge_mcp.md) — prima di un NUOVO tipo di task chiedi a Edge se esiste una skill da usare come base, poi confrontala con le locali; wired in `/home/da/.mcp.json` perche' il savior non puo' lanciare la CLI claude; trovare un candidato e' gratis, adottarlo richiede ancora il test che nel 2026-09-18 la loro people-search ha perso.
- 🧩 [Skills on BOTH machines](feedback_skills_install_on_both_machines.md) — laptop + `/home/da/.claude/skills/`.
- 🖥️ [Startup opens NOTHING](feedback_laptop_startup_clean.md) · [power states](reference_laptop_power_states.md) · [16 GB, Windows sees 11.7](reference_laptop_memory_pressure.md).
- ↩️ ["nvm" cancels previous message](feedback_nvm_cancels_previous_message.md).
- 💾 [Tool mirrors = backups in task-land](reference_tool_mirrors.md) — `_system/laptop-tools/`, `_system/box-tools/` (git-sync step 0, secrets excluded); no new repos, never run from a mirror.
- 🔀 [Sync can park for DAYS unnoticed](reference_task_land_sync_parked_conflict.md) — `git status -sb` on all 4 repos when box and laptop disagree; merge, not rebase (2026-09-17).
- 🎟️ [Trippy: event trip = read the event schedule first; every ground step its own priced line](feedback_trippy_event_anchor_and_explicit_ground.md) (2026-09-25).
- 🎫 [Pagine evento: schede cliccabili, tema CHIARO, domande dentro la card di ogni persona](feedback_event_companion_pages.md) — forma da copiare `research-page/build_snitem_dm.py`; l'AIIC era scura, da lì in poi no (2026-09-28).
- 👥 [Trippy: a companion copies the user's whole chain until plans split](feedback_trippy_companion_mirrors_until_split.md) — Caleb = same Orlando/MD Expo/hotel/flight to SF, only his way home differs (2026-09-27).
- 🔀✅ [travel-search sync: the Sep 6-25 stall (box committed ":" filenames) and how it was unstuck](reference_travel_search_sync_colon_filenames.md) — resolved 2026-09-25, guard_winnames on the box; JSON conflicts = union by id.
- 🐍💥 [MAI un venv dentro un repo sincronizzato](reference_venv_in_synced_repo_wedges_push.md) — il cron committa gli 831 file e un binario da 120 MB blocca OGNI push finche' non resetti il commit fuori dalla history; venv sempre fuori dai repo (2026-09-25).
- ☠️🔀 [`--autostash` pop failure exits 0](reference_git_sync_autostash_pop_silent_corruption.md) — committed conflict markers into a draft sidecar and ate a queue.jsonl line (2026-09-22); guards live in `_system/vps/sync-guards.sh`.
- ✉️🔍 [EVERY email draft goes through the lane](feedback_every_email_draft_goes_through_the_lane.md) — gmail draft + sidecar + register.py, same turn; never stop at the draft · [lane details](reference_draft_review_lane.md) · ⚠️ [register.py from ~/task-land, check the card line](feedback_register_py_run_from_task_land_and_check_card_line.md) — draft → `_system/drafts/register.py` → hub card #N → `N dsend/no/change:`; Quick Claude Alt+Win+J then D; NEVER send. · 🛑 Drafts TAB GROUP retired 2026-09-30: open drafts from hub-review (m = Messages, o = open).
- 📱 [23:00 digest -> hub-review page, not "N yes" replies](feedback_hub_digest_replaced_by_review_page.md)
- 🧹 [22:12 pre-sweep deep check, close what he already answered](feedback_presweep_deep_check_before_23.md) — re-arm the session cron after a savior restart. · - ["Ping" = hub card](feedback_approvals_are_pings.md) — POST 127.0.0.1:4180/pending ONLY; never `tg-bridge/send-to-phone.js` · [Approval-hub](reference_approval_hub.md) — canonical y/n, card ≤58 lines.
- ✅ [A COMMITTED batch IS the yes](feedback_commit_batch_is_the_yes.md) — never a card asking to confirm a commit; a card after commit only if something NEW happened (2026-09-16, card #15 Estonia).
- 🔕 [Cards ping ONCE](feedback_approval_ping_once.md) · 🔌 [laptop+phone popups deactivated, TELEGRAM ONLY](feedback_laptop_ping_card_deactivated.md) · 🃏 [ping cards must be FULL](feedback_ping_cards_must_be_full.md) — decision in `text`, artifact in `context`.
- 🔔 [Done = PushNotification](feedback_done_notifications.md) — >5 min task or failure; never a TG card · [approval-only notifications](reference_claude_code_notifications.md).
- [Message-send protocol](feedback_message_send_protocol.md) — "dsend"=now; "quotes"=verbatim; else hub card · [dsend includes attachment](feedback_dsend_includes_attachment.md).
- Sending: [simple send = fast](feedback_simple_send_fast_no_diagnostics.md) · [check before nudging](feedback_pending_send_check_before_nudge.md) · [NEVER headless fuzzy send](feedback_no_headless_fuzzy_send.md).
- [Plan compute not API keys](feedback_no_api_keys.md) · 🧳 [Parked MCPs: cc-with, never global](feedback_mcp_per_session_not_global.md) · [Allowlist widening needs OK](reference_permission_allowlist_gaps.md).
- 📤 [Check SENT + calendar before saying "pending"](feedback_state_check_sent_and_calendar.md) — a hub card is a proposal, not state; 4/12 items were stale for this (2026-09-20). Review boards = visibility + proposal + a comment box, he decides.
- 🧪 [Verify "not possible" claims](feedback_verify_agent_capability_claims.md) · 🔎 [Diagnose before naming a cause](feedback_diagnose_before_naming_root_cause.md) · [never fabricate fetched](feedback_never_fabricate_fetched_content.md) · 📊 [Figures need sources](feedback_deliverable_figures_need_sources.md).
- [Track phased plans](feedback_track_phased_plans.md) — "later" = commitment · [Clipboard drafts: verify](feedback_clipboard_all_paste_drafts.md).

## Box (VPS), Telegram, savior
- 📂 [Sub-index: Box / Telegram / savior](index_box_telegram_savior.md) — TG lane reconnect, bridge fix log, hub on the box, hub-review UI, Telegram plugin rules, SODANOtif, voice lanes, DA SYSTEM, Kortyx, UTC/mktime trap, pgrep self-match; open it whenever the task touches these topics.
- 🚨 [Account migration PENDING](project_account_migration.md) — diff against `MIGRATION-account-switch.md`.

## coattio / CRM / GTM
- 📂 [Sub-index: coattio / CRM / GTM](index_coattio_crm_gtm.md) — every other pointer of this section (event loop, review mode, boards, servers, design system, outreach screens) lives there.
- 🤖📋 [TO-DO PIPELINE (2026-09-27): created / in progress / ready for review / finished, `pipeline.py`, the daily page links to the exact hub card, calls go to the CRM Call page, `/todo`](reference_todo_pipeline.md) — never write `stage:` by hand; the unattended worker is NOT built, his decision. Brief: `soda-brain/handoffs/HANDOFF-20260927-todo-agi-and-hub-review.md`, workplan `WORKPLAN-20260927-todo-pipeline-and-hub.md`.
- 🧾 [HANDOFF 2026-09-28 evening: open items of the system agent, the DKIM deal (he does DKIM, then I verify, raise the email cap with his number, release the queue)](../handoffs/HANDOFF-20260928b-system-agent-open-items.md) — read first. All handoffs live in `soda-brain/handoffs/` since 2026-10-02.
- 🛰️ [THE SYSTEM AGENT (task DA-SystemAgent, `task-land/_system/system-agent/`, 4 Oct 2026): maintainer of the whole system; its manual is the ledger `soda-brain/system/nodes.json`; registry broken.jsonl, fix sessions, STUCK cards, the ONE combined report; the GTM agent keeps only the campaigns](reference_system_agent.md) — judge it with `system_agent.py status|registry|incidents`.
- 🧭 THE SYSTEM AGENT, design 4 Oct (maintainer of the whole map, split from GTM, fix sessions 45 min / 1-2% week, STUCK card): `soda-brain/handoffs/DESIGN-20261004-system-agent.md`.
- 🔌 [LinkedIn "Connection closed" / sessions disconnected = launcher.py killed every other launcher; fixed, read `reap.log`](reference_linkedin_launcher_reaper.md) (2026-09-28).
- 🧺 [CRM review: a/s/c HELD until commit, digest sorts each sentence (person / confirms rule / new rule / system), never addrule a review sentence directly](reference_review_staged_commit.md) (2026-09-28).
- 🎪✅ [Event pages: the Confirmed button works the next steps (CRM, Gmail draft, plan back on the page)](reference_event_confirm.md) (2026-09-28).
- 🔎📇 [A step and no channel = a SEARCH (CRM H36): channel-search.js, found details shown on the review card, Approve confirms; review mode full screen (H35)](reference_channel_search.md) (2026-09-28).
- 📬🔁 [DAILY CAMPAIGN (US): 30 a day on `boards/daily-<date>`, first 10 fire at 16:55 via campaign.py](reference_daily_campaign.md) — `gtm-eng/daily-campaign/`, task DailyCampaign-Fire, subject fixed, people not offices, one provider sentence; replaced the GTM line on the daily page (2026-09-25).
- 🪟 [GTM boards open ONLY via open-board.ps1](feedback_gtm_boards_open_via_script.md) — never `navigate`.
- 🎨📦 [Un deck uscito in una mail E' lavoro finito e sta nel repo: leggilo da li', mai chiedergli uno zip](feedback_design_files_live_in_the_repo_not_in_his_export.md) — e una frase di capacita' in un doc ha una data: "Claude Design non e' leggibile" era vero il 30 ago, non il 1 ott (2026-10-01).
- 🔄🎨 [Claude Design <-> GitHub sync with Caleb: extension mirror, :4190 server, /design-sync, setup.py onboarding, the injection strip](reference_design_sync.md) (2026-09-30).

## Tundra / Notion / Granola / Drive
- 📂 [Sub-index: Tundra / Notion / Granola / Drive](index_tundra_notion_granola_drive.md) — all the pointers of this section live there; open it whenever the task touches these topics.

## Email / outreach voice
- 📂 [Sub-index: Email / outreach voice](index_email_outreach_voice.md) — Tundra signature, no signature block, reply in thread, thread leaks, styles, cold-email patterns, LinkedIn blind spot, MCP-first routing, HEC Outlook; open it before writing any email or outreach.

## Triage / WhatsApp / Slack
- 📂 [Sub-index: Triage / WhatsApp / Slack](index_triage_wa_slack.md) — all the pointers of this section live there; open it whenever the task touches these topics.

## Accounts / browser / fetching
- 📂 [Sub-index: Accounts / browser / fetching](index_accounts_browser_fetching.md) — all the pointers of this section live there; open it whenever the task touches these topics.

## Vault / daily / capture
- 📂 [Sub-index: Vault / daily / capture](index_vault_daily_capture.md) — all the pointers of this section live there; open it whenever the task touches these topics.

## Thesis / travel / misc projects
- 📂 [Sub-index: Thesis / travel / misc projects](index_thesis_travel_misc.md) — all the pointers of this section live there; open it whenever the task touches these topics.

## Machine / tools / gotchas
- 🧰 [Laptop tools, Windows/PS gotchas, 2026-09-08 sweep](index_laptop_and_misc.md) — sub-index (AHK, claude-bar, statusline, markless, tail -f locks, .ps1 ASCII, schtasks VBS, file:/// paths, lemlist, Lobbly KB).
- Agents: [long-running](feedback_agent_long_running.md) · ⏳ [output files are INTERIM](feedback_agent_output_file_is_interim.md) · [no polling bg tasks](feedback_no_polling_on_background_tasks.md).
- [User Background](user_background.md) · [User Life Context](context_user_life.md) — APPEND.

- 🕰️ [Get-Date before ANY written time; never carry a time forward from the thread](feedback_check_clock_before_timestamps.md) — told a peer "00:30" at 12:06 the next day (2026-10-01).
- 📂 [Sub-index: system rules 29 Sept to 1 Oct 2026](index_system_rules_2026_09_end.md) — meeting loop, feedback worker, owed to-dos, performance hints, LinkedIn ingest, simulation harness, Word batch edits, visual check, slot/calendar check, booked-call loop, Notion fetch-first, send ledger, the promised connectivity gate.
