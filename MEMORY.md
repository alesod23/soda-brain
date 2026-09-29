# Memory Index

## Rules that bite first
- 🛑 [Unattended run: NEVER end the turn waiting on agents](feedback_unattended_run_never_wait_on_agents.md) — do the work in the main thread, check agent liveness by transcript mtime after 10 min, keep a self-wake heartbeat; cost him 10 idle hours on the thesis (2026-09-27).
- 🧊 [Session frozen on "running PreToolUse hooks N/6" = a hook that never returned](reference_pretooluse_hook_hang_npx.md) — post-compaction-recall.sh ran `npx` on every tool call; fixed 2026-09-27, recipe inside.
- 🪟🚫 [NO console window ever in front of him: tasks through run-hidden.vbs, CREATE_NO_WINDOW, window_lint.py after every new task](reference_window_watch.md) — the recorder names who opened each window (2026-09-28).
- 📦✋ [Never scp/rm/edit a file inside a synced repo on the box by hand](feedback_never_touch_synced_repo_on_box_by_hand.md) — the box sync committed my deletion on both machines (2026-09-28).
- 📌 ["Make this a rule" = write NOW](feedback_rule_requests_are_binding.md)
- 🔄 [THE RULE LOOP: ledgers, compiled skills, observers, decisions.jsonl, system check](reference_rule_loop.md) — canonical `task-land/_system/RULE-LOOP.md`; his only inputs are five sentences; add rules with addrule.py the same turn (2026-09-24).
- 🧠 [Design on merit, not his off-hand numbers](feedback_design_on_merit_not_his_offhand_numbers.md) — no arbitrary caps, Haiku never, Opus where it decides, read the reference he names (Kortyx) before designing; "smart, non-blocking, not sucky" (2026-09-24).
- 🔁 ["Iterative" = one sentence on the spot, never a review pass](feedback_iterative_means_on_the_go_flag.md) — backlogs are separate, optional cleanup; never call them the iterative part (2026-09-24). — file + index line, same turn.
- 🧹➡️ [Una regola vale anche sugli artefatti GIA' esistenti](feedback_standing_instruction_becomes_work_now.md) — "tutto da Tundra" (22 set) e tre draft sono rimasti in cdtm finche' non l'ha chiesto lui; e una domanda parcheggiata in una pagina non e' una domanda fatta (2026-09-23).
- 🏠 [L'output va DENTRO il sistema che possiede quel lavoro](feedback_output_goes_into_the_owning_system.md) — viaggi in trippy, persone nel CRM, board in gtm-eng, decisioni nella hub; mai l'ennesima pagina usa-e-getta. Nel dubbio chiediglielo su TG PRIMA di costruire (2026-09-20).
- ⌨️ [SHORTCUTS.md = master list](feedback_shortcuts_master_file.md) — update same turn for any hotkey/alias/skill.
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
- ✉️🔍 [EVERY email draft goes through the lane](feedback_every_email_draft_goes_through_the_lane.md) — gmail draft + sidecar + register.py, same turn; never stop at the draft · [lane details](reference_draft_review_lane.md) · ⚠️ [register.py from ~/task-land, check the card line](feedback_register_py_run_from_task_land_and_check_card_line.md) — draft → `_system/drafts/register.py` → hub card #N → `N dsend/no/change:`; Quick Claude Alt+Win+J then D; NEVER send.
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
- 🔁 [One-way TG lane → HE types `/mcp reconnect plugin:telegram:telegram`](feedback_telegram_one_way_lane_mcp_reconnect.md) — no restart, context intact, queue drains; savior answers via Bot API curl meanwhile.
- 🩹 [Telegram bridge FIX LOG](../../task-land/_system/TELEGRAM-BRIDGE-LOG.md) — read before touching TG, append after every fix.
- 💀🔌 [Le 4 morti della lane erano COATTIO](reference_coattio_spawns_claude_kills_telegram.md) — i suoi server giravano senza TELEGRAM_STATE_DIR, ogni claude figlio rubava il poller; fix in `coattio/start-box.sh`, prova in `/proc/<pid>/environ` (2026-09-24).
- ☠️ [NEVER run the `claude` CLI from the savior](feedback_never_run_claude_cli_from_savior.md) — `claude mcp list` alone killed the lane (2026-09-19); check health with `pgrep -a bun` + plugin logs.
- 📦 [The live hub is ON THE BOX (`/home/da/approval-hub`, systemd da-hub); the laptop copy is dead, laptop :4180 is a TCP forward](reference_hub_lives_on_the_box.md) — edit hub code over ssh only (2026-09-27).
- 📋 [hub-review UI](reference_hub_review_ui.md) — http://100.85.52.84:4142/ (Tailscale): decide every open hub card on the phone, j/k a/s/x/c, ONE commit = the yes; a "hub-review commit ..." Telegram message from him = the savior executes the CHANGES lines and marks `/api/queue/done`.
- [Telegram plugin](reference_telegram_channel_plugin.md) — @Claudio_al_TG_v3_bot; BOX owns the savior lane; `claude -p` without `--strict-mcp-config` kills the poller · [tg-bridge](reference_tg_bridge.md) · [NEVER respawn savior](feedback_never_respawn_savior_session.md) — `restore-savior` / `vpsc`.
- Telegram: [reply tool every turn](feedback_telegram_reply_tool_every_turn.md) · [reply_to inbound id](feedback_telegram_reply_to_threading.md) · [bare N = Nth-newest card](feedback_telegram_ordinal_message_reference.md) · [swipe-reply resolver](reference_tg_reply_resolver.md) · [channel msgs separate](feedback_channel_sequential_handling.md) · [React 👀 FIRST](feedback_react_eyes_before_working.md).
- 💬🚫 [Su Telegram NIENTE markdown](feedback_telegram_no_markdown_asterisks.md) — il tool manda testo grezzo se non passi `format`, quindi `**grassetto**` arriva con gli asterischi in chiaro; struttura le frasi invece (2026-09-28).
- [DA SYSTEM](project_da_system.md) — laptop-off Claude, approve/reject loop · 🚨 [Account migration PENDING](project_account_migration.md) — diff against `MIGRATION-account-switch.md`.
- 🧭 [Kortyx = il riferimento di design di DA SYSTEM](reference_kortyx_design_reference.md) — kortyx.co, mandato il 2026-08-14: monitora, memoria organizzata, task proattivi, approvazione su TG. E' lui che ha scritto la specifica della ping hub.
- Voice: [long-form on VPS](reference_voice_longform_lane.md) · [fast lane](reference_voice_lane.md) · [Quick Claude](reference_quick_claude.md) — Alt+Win+J then J/K/D.
- 🔴🟣 [Gmail + Slack LIVE on VPS](reference_sodanotif_live_gmail_slack.md) · [lby DEAD](reference_lby_dead.md) · SODANOtif: [core](reference_sodanotif.md) · [card format](feedback_sodanotif_card_format.md) · [battery](feedback_sodanotif_battery_power_task_setting.md) · [stale-Gmail filter](reference_sodanotif_recap_stale_gmail_fix.md) · [noreply never](feedback_noreply_never_in_notifications.md) · 🎓🚫 [CDTM group mail never on TG unless an event](feedback_no_cdtm_community_mail_on_telegram.md) · 🔇 [never-surface groups](feedback_sodanotif_never_surface_groups.md).
- [Cloud routine alerts → Calendar popup](reference_cloud_routine_alert_delivery.md) · [Bare replies → notif-log](feedback_resolve_reply_from_notiflog.md).

## coattio / CRM / GTM
- 📂 [Sub-index: coattio / CRM / GTM](index_coattio_crm_gtm.md) — every other pointer of this section (event loop, review mode, boards, servers, design system, outreach screens) lives there.
- 🤖📋 [TO-DO PIPELINE (2026-09-27): created / in progress / ready for review / finished, `pipeline.py`, the daily page links to the exact hub card, calls go to the CRM Call page, `/todo`](reference_todo_pipeline.md) — never write `stage:` by hand; the unattended worker is NOT built, his decision. Brief: `task-land/_system/HANDOFF-20260927-todo-agi-and-hub-review.md`, workplan `WORKPLAN-20260927-todo-pipeline-and-hub.md`.
- 🧾 [HANDOFF 2026-09-28 evening: open items of the system agent, the DKIM deal (he does DKIM, then I verify, raise the email cap with his number, release the queue)](../../task-land/_system/HANDOFF-20260928b-system-agent-open-items.md) — read first.
- 🛰️ [THE SYSTEM AGENT (task GTM-Agent, `gtm-eng/agent/`): every 10 min, whitelist of fixes, 2 updates a day, box fallback](reference_system_agent.md) — built 2026-09-28; judge it with `gtm_agent.py status|incidents|missed`.
- 🔌 [LinkedIn "Connection closed" / sessions disconnected = launcher.py killed every other launcher; fixed, read `reap.log`](reference_linkedin_launcher_reaper.md) (2026-09-28).
- 🧺 [CRM review: a/s/c HELD until commit, digest sorts each sentence (person / confirms rule / new rule / system), never addrule a review sentence directly](reference_review_staged_commit.md) (2026-09-28).
- 🎪✅ [Event pages: the Confirmed button works the next steps (CRM, Gmail draft, plan back on the page)](reference_event_confirm.md) (2026-09-28).
- 🔎📇 [A step and no channel = a SEARCH (CRM H36): channel-search.js, found details shown on the review card, Approve confirms; review mode full screen (H35)](reference_channel_search.md) (2026-09-28).
- 📬🔁 [DAILY CAMPAIGN (US): 30 a day on `boards/daily-<date>`, first 10 fire at 16:55 via campaign.py](reference_daily_campaign.md) — `gtm-eng/daily-campaign/`, task DailyCampaign-Fire, subject fixed, people not offices, one provider sentence; replaced the GTM line on the daily page (2026-09-25).
- 🪟 [GTM boards open ONLY via open-board.ps1](feedback_gtm_boards_open_via_script.md) — never `navigate`.

## Tundra / Notion / Granola / Drive
- 📂 [Sub-index: Tundra / Notion / Granola / Drive](index_tundra_notion_granola_drive.md) — all the pointers of this section live there; open it whenever the task touches these topics.

## Email / outreach voice
- 🖋️ [TUNDRA mail ALWAYS carries the Tundra signature: gmail.py adds it by itself, never a connector draft](feedback_tundra_signature_always.md) (2026-09-28).
- ✍️ [NO signature block, end 'Alessandro'](feedback_email_no_signature_block.md) — ask-first is DEFAULT · ✉️ [Remind, don't re-confirm](feedback_remind_dont_reconfirm.md).
- Email ops: [REPLY IN THREAD IS THE DEFAULT; to-do = find existing thread](feedback_email_todo_find_existing_thread.md) · [catch-up](feedback_email_catchup_consistency.md) · [not-findable](feedback_email_not_findable_tracking.md) · [shared inbox cutoff](feedback_shared_inbox_cutoff.md) · [draft = real Gmail draft](feedback_email_draft_must_be_real_not_clipboard.md).
- ⚠️ [Mixed threads leak internal comms](feedback_thread_reply_leaks_internal_comms.md) · [Read source thread first](feedback_read_source_thread_before_acting.md) · [Follow links not labels](feedback_follow_links_not_link_labels.md).
- Style: [professor](feedback_professor_email_style.md) · [warm-intro](feedback_warm_intro_phrasing.md) · [Italian tu/Lei](feedback_italian_practitioner_followup_style.md) · [HTML multipart](feedback_gmail_html_rendering.md).
- 🗣️ ["I understand it's X guidance to…" NOT "the website says"](feedback_cite_knowledge_not_the_website.md) — naming the source reads as AI.
- 🚫 [No "You are listed as…" role recall, no "xx rather than yy"](feedback_email_no_role_recall_no_rather_than.md) — fold the role into the ask; say the one thing (CMIA drafts, 2026-09-17).
- ✉️ [Cold email to operator = ask to learn](feedback_cold_email_operator_ask_for_advice.md) · 🎯 [Outreach: ASK FIRST, peer voice](feedback_outreach_ask_first_peer_voice.md) · [Lovable pattern](feedback_cold_email_lovable_pattern.md) · [template mining](feedback_outreach_template_mining.md) · [ONE cible/tpl](feedback_template_cible_single_persona.md) · [OUTREACH-SYSTEM.md read+UPDATE](reference_outreach_system.md).
- 🕵️ [LinkedIn people search = mio punto cieco](feedback_linkedin_people_search_is_a_blind_spot.md) — WebSearch non vede l'indice membri: di' "non ci arrivo, provala tu loggato", mai "non esiste" (San Raffaele, 2026-09-21).
- 🔎 [getedge people-search: removed](reference_getedge_people_search_skill.md) — found nothing a plain search did not (2026-09-18); the recipe that works: procurement PDFs, AIIC programmes, native-language queries, stale-name check.
- [MCP-first routing](feedback_mcp_over_pw.md) · [linkedin-mcp](reference_linkedin_mcp.md) · 🔎 ["Connections of" works](reference_linkedin_connections_of_filter.md) · 🔵 [LinkedIn poll lane](reference_linkedin_poll.md).
- HEC Outlook: [setup](project_hec_outlook_setup.md) · [COM, Classic only](reference_hec_outlook.md) · [Gmail Snippets ext](project_gmail_snippets_extension.md).

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

- 🪤 [pgrep -f matches its own shell](feedback_pgrep_self_match_use_script_files.md) — background jobs from script files + pidfiles; wait with kill -0, never pkill -f a pattern.
- 🧷 [Notion update_content: fetch first](feedback_notion_update_content_fetch_first.md) — anchors must match Notion's re-render (`_x_`→`*x*`); one bad anchor rejects the whole call.
- 📒 [Send ledger: a past plan never sent takes no room; US daily.py carries failed days over](reference_send_ledger_past_plans.md) (2026-09-29).
- 📞 [MEETING LOOP: a finished call (Notion notes) = CRM event + one hub card with the next step within 15 min, task DA-MeetingLoop](reference_meeting_loop.md) (CRM H41, 2026-09-29).
