# Memory Index

## Rules that bite first
- 📌 ["Make this a rule" = write NOW](feedback_rule_requests_are_binding.md) — file + index line, same turn.
- ⌨️ [SHORTCUTS.md = master list](feedback_shortcuts_master_file.md) — update same turn for any hotkey/alias/skill.
- 🧩 [Skills on BOTH machines](feedback_skills_install_on_both_machines.md) — laptop + `/home/da/.claude/skills/`.
- 🖥️ [Startup opens NOTHING](feedback_laptop_startup_clean.md) · [power states](reference_laptop_power_states.md) · [16 GB, Windows sees 11.7](reference_laptop_memory_pressure.md).
- ↩️ ["nvm" cancels previous message](feedback_nvm_cancels_previous_message.md).
- 💾 [Tool mirrors = backups in task-land](reference_tool_mirrors.md) — `_system/laptop-tools/`, `_system/box-tools/` (git-sync step 0, secrets excluded); no new repos, never run from a mirror.
- 🔀 [Sync can park for DAYS unnoticed](reference_task_land_sync_parked_conflict.md) — `git status -sb` on all 4 repos when box and laptop disagree; merge, not rebase (2026-09-17).
- ✉️🔍 [EVERY email draft goes through the lane](feedback_every_email_draft_goes_through_the_lane.md) — gmail draft + sidecar + register.py, same turn; never stop at the draft · [lane details](reference_draft_review_lane.md) · ⚠️ [register.py from ~/task-land, check the card line](feedback_register_py_run_from_task_land_and_check_card_line.md) — draft → `_system/drafts/register.py` → hub card #N → `N dsend/no/change:`; Quick Claude Alt+Win+J then D; NEVER send.
- 📱 [23:00 digest -> hub-review page, not "N yes" replies](feedback_hub_digest_replaced_by_review_page.md)
- 🧹 [22:12 pre-sweep deep check, close what he already answered](feedback_presweep_deep_check_before_23.md) — re-arm the session cron after a savior restart. · - ["Ping" = hub card](feedback_approvals_are_pings.md) — POST 127.0.0.1:4180/pending ONLY; never `tg-bridge/send-to-phone.js` · [Approval-hub](reference_approval_hub.md) — canonical y/n, card ≤58 lines.
- ✅ [A COMMITTED batch IS the yes](feedback_commit_batch_is_the_yes.md) — never a card asking to confirm a commit; a card after commit only if something NEW happened (2026-09-16, card #15 Estonia).
- 🔕 [Cards ping ONCE](feedback_approval_ping_once.md) · 🔌 [laptop+phone popups deactivated, TELEGRAM ONLY](feedback_laptop_ping_card_deactivated.md) · 🃏 [ping cards must be FULL](feedback_ping_cards_must_be_full.md) — decision in `text`, artifact in `context`.
- 🔔 [Done = PushNotification](feedback_done_notifications.md) — >5 min task or failure; never a TG card · [approval-only notifications](reference_claude_code_notifications.md).
- [Message-send protocol](feedback_message_send_protocol.md) — "dsend"=now; "quotes"=verbatim; else hub card · [dsend includes attachment](feedback_dsend_includes_attachment.md).
- Sending: [simple send = fast](feedback_simple_send_fast_no_diagnostics.md) · [check before nudging](feedback_pending_send_check_before_nudge.md) · [NEVER headless fuzzy send](feedback_no_headless_fuzzy_send.md).
- [Plan compute not API keys](feedback_no_api_keys.md) · 🧳 [Parked MCPs: cc-with, never global](feedback_mcp_per_session_not_global.md) · [Allowlist widening needs OK](reference_permission_allowlist_gaps.md).
- 🧪 [Verify "not possible" claims](feedback_verify_agent_capability_claims.md) · 🔎 [Diagnose before naming a cause](feedback_diagnose_before_naming_root_cause.md) · [never fabricate fetched](feedback_never_fabricate_fetched_content.md) · 📊 [Figures need sources](feedback_deliverable_figures_need_sources.md).
- [Track phased plans](feedback_track_phased_plans.md) — "later" = commitment · [Clipboard drafts: verify](feedback_clipboard_all_paste_drafts.md).

## Box (VPS), Telegram, savior
- 🔁 [One-way TG lane → HE types `/mcp reconnect plugin:telegram:telegram`](feedback_telegram_one_way_lane_mcp_reconnect.md) — no restart, context intact, queue drains; savior answers via Bot API curl meanwhile.
- 🩹 [Telegram bridge FIX LOG](../../task-land/_system/TELEGRAM-BRIDGE-LOG.md) — read before touching TG, append after every fix.
- 📋 [hub-review UI](reference_hub_review_ui.md) — http://100.85.52.84:4142/ (Tailscale): decide every open hub card on the phone, j/k a/s/x/c, ONE commit = the yes; a "hub-review commit ..." Telegram message from him = the savior executes the CHANGES lines and marks `/api/queue/done`.
- [Telegram plugin](reference_telegram_channel_plugin.md) — @Claudio_al_TG_v3_bot; BOX owns the savior lane; `claude -p` without `--strict-mcp-config` kills the poller · [tg-bridge](reference_tg_bridge.md) · [NEVER respawn savior](feedback_never_respawn_savior_session.md) — `restore-savior` / `vpsc`.
- Telegram: [reply tool every turn](feedback_telegram_reply_tool_every_turn.md) · [reply_to inbound id](feedback_telegram_reply_to_threading.md) · [bare N = Nth-newest card](feedback_telegram_ordinal_message_reference.md) · [swipe-reply resolver](reference_tg_reply_resolver.md) · [channel msgs separate](feedback_channel_sequential_handling.md) · [React 👀 FIRST](feedback_react_eyes_before_working.md).
- [DA SYSTEM](project_da_system.md) — laptop-off Claude, approve/reject loop · 🚨 [Account migration PENDING](project_account_migration.md) — diff against `MIGRATION-account-switch.md`.
- Voice: [long-form on VPS](reference_voice_longform_lane.md) · [fast lane](reference_voice_lane.md) · [Quick Claude](reference_quick_claude.md) — Alt+Win+J then J/K/D.
- 🔴🟣 [Gmail + Slack LIVE on VPS](reference_sodanotif_live_gmail_slack.md) · [lby DEAD](reference_lby_dead.md) · SODANOtif: [core](reference_sodanotif.md) · [card format](feedback_sodanotif_card_format.md) · [battery](feedback_sodanotif_battery_power_task_setting.md) · [stale-Gmail filter](reference_sodanotif_recap_stale_gmail_fix.md) · [noreply never](feedback_noreply_never_in_notifications.md) · 🎓🚫 [CDTM group mail never on TG unless an event](feedback_no_cdtm_community_mail_on_telegram.md) · 🔇 [never-surface groups](feedback_sodanotif_never_surface_groups.md).
- [Cloud routine alerts → Calendar popup](reference_cloud_routine_alert_delivery.md) · [Bare replies → notif-log](feedback_resolve_reply_from_notiflog.md).

## coattio / CRM / GTM
- 🎪 [Event contact workflow](project_event_contact_workflow.md) — capture -> one card -> coattio + Notion + 48 h task; `POST :4137/intake` exists since 2026-09-15 (it was the missing link).
- 🧭 [coattio v2](project_coattio_v2.md) — contract `~/.medtech-crm/WORKPLAN-20260904-coattio-v2.md`; CRM OWNS every person follow-up (reversed 2026-09-19), daily page = COUNT LINE ONLY (per-person lines reversed 2026-09-19 evening, clutter).
- 📱 [coattio on the box](reference_coattio_box_hosting.md) — phone http://100.85.52.84:4124 · [servers 4124+4137, NEVER run_in_background](reference_coattio_servers.md) · [Tailscale](reference_coattio_tailscale.md) · ⌥⇧M [Alt+Shift+M draft](reference_alt_shift_m_ai_draft.md) · [local server start = detached](feedback_local_server_start_pattern.md).
- 📇 [/overnight email-find](reference_overnight_email_find.md) · [harness: args JSON string](reference_overnight_harness.md).
- [GTM v3 stack](project_gtm_v3_stack.md) · 🗂️ [GTM boards (4141)](reference_gtm_boards.md) · 🪟 [Boards open ONLY via open-board.ps1](feedback_gtm_boards_open_via_script.md) — never `navigate`; tab groups are extension-only · ⌨️ [Review pages MUST be keyboard-drivable](feedback_review_pages_need_keyboard_shortcuts.md) · 🎛️ [Review-page DESIGN SYSTEM](feedback_review_page_design_system.md) — `gtm-eng/DESIGN-SYSTEM.md`: one item = one screen at 1568x773, same zones, ? hovers, one draft per channel, screenshot first (2026-09-19) · 👁️ [never collapse what he must read](feedback_never_collapse_what_he_must_read.md) · ⌨️ [j = back, k = forward, everywhere](feedback_jk_shortcuts_j_is_back.md) — a/s decide, j/k move, legend visible · [message-builder corpus](reference_message_builder_corpus.md) · [Outreach CRM :4123](project_outreach_crm.md).
- [Tundra CRM taxonomy](reference_tundra_crm_taxonomy.md) · [NPD vs Tundra separate](feedback_npd_vs_tundra_separate.md) · [Lobbly](project_lobbly.md) · [Unclear-disclosure corpus](project_unclear_disclosure_corpus.md) · [Practitioner research](feedback_practitioner_research_methodology.md).

## Tundra / Notion / Granola / Drive
- [Tundra stack](../../medtech-brain/_system/TUNDRA-STACK.md) — READ ALWAYS for Tundra · [deliverables → gsheet](feedback_tundra_deliverables_gdrive.md) · 💰 [Investor leads CDTM](reference_investor_leads_cdtm.md) · 📝 [Tundra Weekly doc](reference_tundra_weekly_meeting_doc.md).
- 📥 [Notion Inbox](project_notion_signals.md) · 🧬 [Notion deliverables NATIVE](feedback_notion_deliverables_must_be_native.md) · [Tundra system](reference_notion_tundra_system.md) · [MCP scoped](reference_notion_mcp_access.md) · [writes need approval](feedback_notion_write_needs_approval.md) · [coattio→Notion sync](reference_coattio_notion_sync.md) · 📱➡️📅 [Notion meeting filer](reference_notion_meeting_filer.md).
- Granola: [MPD folder](reference_mpd_granola_folder.md) · [granola-auto](reference_granola_auto.md) · [reminder timing](feedback_granola_reminder_next_day.md) · [Tundra Granola folder](reference_tundra_granola_folder.md) · [Tundra call-prep](reference_tundra_call_prep_flow.md) · [ICO prospect Renou](project_tundra_ico_renou.md).
- Decks: [Deck→PDF print snapshot](feedback_deck_pdf_needs_print_snapshot.md) · [Design source only](feedback_tundra_deck_workflow.md) · [bridged EN pinned](reference_tundra_bridged_deck_source.md) · [pull-before-write](feedback_designsync_pull_before_write.md) · [fingerprint+fitz](feedback_deck_source_fingerprint_and_render.md) · 🎨 [Claude Design asks every push](reference_claude_design_permissions.md) · [/design-lib](reference_design_lib.md).
- 👥 [Meeting doc with Caleb = share caleb@tundrahealth.ai AT CREATION](feedback_meeting_docs_always_share_caleb.md) — never leave the other participant off the access list (2026-09-19).
- 📝 [Edit a tundra Google Doc from the box](reference_google_doc_edit_path_from_box.md) — MCP creates, Docs API via drive-cdtm token edits after share; tundra tokens dead (2026-09-18).
- Drive: [public share](reference_gdrive_public_share.md) · 🗂️ [VPS gdrive mounts](reference_vps_gdrive_mounts.md) · 📁 [drive.py CLI](reference_drive_cli.md).
- 🔁 [TundraPage PR review loop](feedback_tundrapage_pr_review_loop.md) — after a PR, read the bot review threads: fix commit or resolve, never leave them (Caleb, 2026-09-18).
- 🌐 [TundraPage repo](project_tundrapage_repo.md) — alesod23 read-only, PR to Caleb · [Git identity](reference_git_github_identity.md) · 🏔️ [Tundra commits NEED Claude trailer](feedback_tundra_commits_need_claude_trailer.md).
- [Tundra Talents](project_tundra_talents.md) · [Langfuse pains](project_langfuse_pains.md) · [scoring](feedback_pain_corpus_scoring.md) · [CDTM kickoff TF](project_cdtm_kickoff_tf.md).

## Email / outreach voice
- ✍️ [NO signature block, end 'Alessandro'](feedback_email_no_signature_block.md) — ask-first is DEFAULT · ✉️ [Remind, don't re-confirm](feedback_remind_dont_reconfirm.md).
- Email ops: [REPLY IN THREAD IS THE DEFAULT; to-do = find existing thread](feedback_email_todo_find_existing_thread.md) · [catch-up](feedback_email_catchup_consistency.md) · [not-findable](feedback_email_not_findable_tracking.md) · [shared inbox cutoff](feedback_shared_inbox_cutoff.md) · [draft = real Gmail draft](feedback_email_draft_must_be_real_not_clipboard.md).
- ⚠️ [Mixed threads leak internal comms](feedback_thread_reply_leaks_internal_comms.md) · [Read source thread first](feedback_read_source_thread_before_acting.md) · [Follow links not labels](feedback_follow_links_not_link_labels.md).
- Style: [professor](feedback_professor_email_style.md) · [warm-intro](feedback_warm_intro_phrasing.md) · [Italian tu/Lei](feedback_italian_practitioner_followup_style.md) · [HTML multipart](feedback_gmail_html_rendering.md).
- 🗣️ ["I understand it's X guidance to…" NOT "the website says"](feedback_cite_knowledge_not_the_website.md) — naming the source reads as AI.
- 🚫 [No "You are listed as…" role recall, no "xx rather than yy"](feedback_email_no_role_recall_no_rather_than.md) — fold the role into the ask; say the one thing (CMIA drafts, 2026-09-17).
- ✉️ [Cold email to operator = ask to learn](feedback_cold_email_operator_ask_for_advice.md) · 🎯 [Outreach: ASK FIRST, peer voice](feedback_outreach_ask_first_peer_voice.md) · [Lovable pattern](feedback_cold_email_lovable_pattern.md) · [template mining](feedback_outreach_template_mining.md) · [ONE cible/tpl](feedback_template_cible_single_persona.md) · [OUTREACH-SYSTEM.md read+UPDATE](reference_outreach_system.md).
- 🔎 [getedge people-search: removed](reference_getedge_people_search_skill.md) — found nothing a plain search did not (2026-09-18); the recipe that works: procurement PDFs, AIIC programmes, native-language queries, stale-name check.
- [MCP-first routing](feedback_mcp_over_pw.md) · [linkedin-mcp](reference_linkedin_mcp.md) · 🔎 ["Connections of" works](reference_linkedin_connections_of_filter.md) · 🔵 [LinkedIn poll lane](reference_linkedin_poll.md).
- HEC Outlook: [setup](project_hec_outlook_setup.md) · [COM, Classic only](reference_hec_outlook.md) · [Gmail Snippets ext](project_gmail_snippets_extension.md).

## Triage / WhatsApp / Slack
- 📇 [Google contacts → CRM sync](reference_contacts_sync.md) — `triage/contacts_sync.py`, cron on the box; NEVER auto-files: each batch = ONE hub card (yes=all · no+"1 3"=those · no+none=skip), approved → coattio, Notion row is a session step (`review` → `mark-filed`); consent done 2026-09-14.
- 📲🔑 [Re-auth Gmail from the PHONE](reference_gmail_phone_oauth.md) — `triage/phone_auth.py url` then `exchange`; personal mailbox = alessandrosodano23@gmail.com (token `sodano23`).
- [Triage Gmail helper](reference_triage_gmail.md) · [Slack helper](reference_slack_helper.md) · [slack.cmd eats newlines](feedback_slack_cmd_newline_truncation.md) · plumbing: [v2 reply](reference_triage_v2_reply.md) · [operations](reference_triage_operations.md) · [v3 aliases](reference_triage_aliases_and_state.md).
- Triage rules: [chips+24h](feedback_triage_askquestion_and_24h.md) · [24h cap](feedback_triage_24h_cap.md) · [actionable def](feedback_triage_actionable_definition.md) · [WA window-only](feedback_triage_wa_dm_window_only.md) · [--jid only](feedback_triage_wa_send_jid.md) · [unread-tail](feedback_triage_unread_tail_slicing.md) · [Slack cutoff](feedback_slack_cutoff_filter.md).
- [WA Stack](reference_wa_sender.md) · [creds zeroed](reference_wa_daemon_creds_corruption.md) · [RE-LINK = QR ONLY](reference_wa_daemon_repair.md) · [health](reference_wa_daemon_health.md) · [flap lies](feedback_wa_daemon_flap_and_outgoing_gap.md) · [Web scrape](reference_wa_web_scrape.md) · [UTC-guard](reference_wa_scheduled_sends.md) · [recipient variants](feedback_wa_recipient_resolution.md) · [WA Web in default browser](feedback_open_wa_web_in_comet.md).

## Accounts / browser / fetching
- 🚫 [NEVER bare account chooser](feedback_never_trigger_bare_account_chooser.md) · [resolve account BEFORE linking](feedback_resolve_account_before_linking.md) · [OAuth login_hint + verify](feedback_oauth_login_hint_and_verify.md) · 🔑 [open URLs with correct account](feedback_open_urls_with_correct_account.md).
- 🚫🪐 [COMET ABANDONED, Chrome ONLY](feedback_browser_chrome_default.md) · [Output delivery CANONICAL](feedback_output_delivery_rules.md) — file:/// links; HTML auto-open; vault .md → Obsidian+clipboard.
- Fetching: [YouTube transcripts](feedback_yt_transcripts.md) · [web-fetch-pw](reference_web_fetch_pw.md) · [Floom MCP](reference_floom_mcp.md) · [Calendar availability](reference_calendar_availability_link.md).

## Vault / daily / capture
- [Vault task system](reference_vault.md) · /daily: [11-step](reference_daily_briefing.md) · [dedup](feedback_daily_dedup_today_page.md) · [full-section](feedback_daily_full_section_contract.md) · [deletion→Waiting](feedback_daily_deletion_parks_to_waiting.md) · [no rollover](feedback_daily_waiting_and_no_rollover.md) · [page = only edit surface](feedback_daily_is_interface_folders_are_plumbing.md) · [tag CSS](reference_daily_tag_css_split_fix.md).
- Task fields: [surface_on vs due](feedback_future_due_to_inbox.md) · [/dump dated → inbox](feedback_dump_dated_followups_to_inbox.md) · [AskUserQuestion for prefs](feedback_ask_user_question_preference.md) · [Curriculum tracker](feedback_curriculum_tracker.md) · [weekly learnings](reference_weekly_learnings.md).
- KB: [split needs bridge](feedback_kb_split_needs_bridge.md) · [drift guard](feedback_kb_systems_drift_guard.md) · [systems doc READ-FIRST](reference_kb_systems.md) · [KB vault](reference_kb_vault.md).
- Obsidian: [sequential opens](feedback_obsidian_sequential_opens.md) · [obsidian:// preferred](reference_obsidian_app_path.md) · Capture: [paper notes → Raw](feedback_paper_notes_standalone_raw.md) · [Raw filename MM-DD](feedback_raw_note_filename_month_day.md) · [/audio-to-notes](reference_audio_to_notes.md) · 🎙️ [Call recording](reference_pixel_call_recording.md).
- 🎙️📁 [Phone recordings on the box](reference_phone_recordings_on_box.md) — `gdrive/From phone/`; FUSE hides same-name files (use `rclone lsl`); WA store starts 2026-08-23; transcribe with voice-lane venv faster-whisper `small`.
- [Transcript artifact format](feedback_transcript_artifact_format.md) · [sodaOS](project_sodaos.md) · [Phone→desktop](project_phone_to_desktop.md) · [WA Web media](feedback_wa_web_for_media.md) · [BIG MOVE backup](reference_big_move_backup.md).

## Thesis / travel / misc projects
- 🎓 [THESIS CHECKPOINT 2026-09-04](project_thesis_checkpoint_2026_09.md) · [Seeling + cumulative ch8](feedback_thesis_seeling_and_cumulative_conclusion.md) · [Thesis system](project_thesis_system.md) · [Artifacts → Raw/](feedback_thesis_artifacts_to_vault.md).
- 🚄 [Rail-price lane box->laptop LIVE](reference_trippy_rail_lane.md) — Drive request/result JSON, DB BahnCard by URL token, Italo via booking XHR, task Trippy-RailLane every 2 min (2026-09-19).
- 🚫🚄 [Box cannot price SNCF/Italo/DB; cards need the laptop](reference_trippy_box_rail_price_limits.md) — 403 map + gflights throughput (2026-09-18).
- 🧭 [Trippy box sources](reference_trippy_box_sources.md) — LeFrecce + gflights + FlixBus live from the VPS; Italo unpriceable; headless Chrome render check.
- 🚄 [Trainline GraphQL from the box](reference_trainline_graphql_box.md) — `travel-search/trainline_render.py`: /graphql persisted query works (REST + rendered page are DataDome-403); Carte Avantage via discountCards URN; Kombo fallback.
- Travel: ✈️ [gflights engine](reference_gflights_engine.md) · [travel-search](reference_travel_search.md) · 📱 [Trippy on the BOX](reference_trippy_on_box.md) · 🧭 [Trippy naming](reference_trippy_naming.md) · [core](project_trippy_v2.md) · [metro](feedback_trippy_metro_airport_normalization.md) · [headless](feedback_trippy_headless_parallel.md) · [links](feedback_trippy_durable_links.md) · [two-pass](feedback_trippy_deep_dive.md) · [airline-direct](feedback_airline_direct_for_known_carrier.md) · [Italy travel](context_travel_patterns.md).
- [RadioCLI](project_radiocli.md) · [Restore-CC](reference_restore_cc.md) · [Claude Setup Repo](project_claude_setup.md) · [Dynamic-HTML](reference_dynamic_html.md) · [static DEFAULT](feedback_dynamic_html_default.md).

## Machine / tools / gotchas
- 🧰 [Laptop tools, Windows/PS gotchas, 2026-09-08 sweep](index_laptop_and_misc.md) — sub-index (AHK, claude-bar, statusline, markless, tail -f locks, .ps1 ASCII, schtasks VBS, file:/// paths, lemlist, Lobbly KB).
- Agents: [long-running](feedback_agent_long_running.md) · ⏳ [output files are INTERIM](feedback_agent_output_file_is_interim.md) · [no polling bg tasks](feedback_no_polling_on_background_tasks.md).
- [User Background](user_background.md) · [User Life Context](context_user_life.md) — APPEND.

- 🪤 [pgrep -f matches its own shell](feedback_pgrep_self_match_use_script_files.md) — background jobs from script files + pidfiles; wait with kill -0, never pkill -f a pattern.
- 🧷 [Notion update_content: fetch first](feedback_notion_update_content_fetch_first.md) — anchors must match Notion's re-render (`_x_`→`*x*`); one bad anchor rejects the whole call.
